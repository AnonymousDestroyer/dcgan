#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer
# from tensorlayer.layers.core import LayersConfig

from tensorlayer.layers.utils import compute_alpha
from tensorlayer.layers.utils import ternary_operation

from tensorlayer import logging

from tensorlayer.decorators import deprecated_alias

__all__ = ['TernaryConv2d']


class TernaryConv2d(Layer):
    """
    The :class:`TernaryConv2d` class is a 2D binary CNN layer, which weights are either -1 or 1 or 0 while inference.

    Note that, the bias vector would not be tenarized.

    Parameters
    ----------
    n_filter : int
        The number of filters.
    filter_size : tuple of int
        The filter size (height, width).
    strides : tuple of int
        The sliding window strides of corresponding input dimensions.
        It must be in the same order as the ``shape`` parameter.
    act : activation function
        The activation function of this layer.
    padding : str
        The padding algorithm type: "SAME" or "VALID".
    data_format : str
        "NHWC" or "NCHW", default is "NHWC".
    use_gemm : boolean
        If True, use gemm instead of ``tf.matmul`` for inference. (TODO).
    W_init : initializer
        The initializer for the the weight matrix.
    b_init : initializer or None
        The initializer for the the bias vector. If None, skip biases.
    W_init_args : dictionary
        The arguments for the weight matrix initializer.
    b_init_args : dictionary
        The arguments for the bias vector initializer.
    use_cudnn_on_gpu : bool
        Default is False.
    name : None or str
        A unique layer name.

    Examples
    ---------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> x = tf.placeholder(tf.float32, [None, 256, 256, 3])
    >>> net = tl.layers.Input(x, name='input')
    >>> net = tl.layers.TernaryConv2d(net, 32, (5, 5), (1, 1), padding='SAME', name='bcnn1')
    >>> net = tl.layers.MaxPool2d(net, (2, 2), (2, 2), padding='SAME', name='pool1')
    >>> net = tl.layers.BatchNorm(net, act=tl.act.htanh, is_train=True, name='bn1')
    ...
    >>> net = tl.layers.Sign(net)
    >>> net = tl.layers.TernaryConv2d(net, 64, (5, 5), (1, 1), padding='SAME', name='bcnn2')
    >>> net = tl.layers.MaxPool2d(net, (2, 2), (2, 2), padding='SAME', name='pool2')
    >>> net = tl.layers.BatchNorm(net, act=tl.act.htanh, is_train=True, name='bn2')

    """

    def __init__(
            self,
            n_filter=32,
            filter_size=(3, 3),
            strides=(1, 1),
            act=None,
            padding='SAME',
            data_format=None,
            use_gemm=False,
            W_init=tf.compat.v1.initializers.truncated_normal(stddev=0.02),
            b_init=tf.compat.v1.initializers.constant(value=0.0),
            W_init_args=None,
            b_init_args=None,
            use_cudnn_on_gpu=None,
            name=None,  #'ternary_cnn2d',
    ):
        # super(TernaryConv2d, self
        #      ).__init__(prev_layer=prev_layer, act=act, W_init_args=W_init_args, b_init_args=b_init_args, name=name)
        super().__init__(name)
        self.n_filter = n_filter
        self.filter_size = filter_size
        self.strides = strides
        self.act = act
        self.padding = padding
        self.data_format = data_format
        self.use_gemm = use_gemm
        self.W_init = W_init
        self.b_init = b_init
        self.W_init_args = W_init_args
        self.b_init_args = b_init_args
        self.use_cudnn_on_gpu = use_cudnn_on_gpu

        logging.info(
            "TernaryConv2d %s: n_filter: %d filter_size: %s strides: %s pad: %s act: %s" % (
                self.name, n_filter, str(filter_size), str(strides), padding,
                self.act.__name__ if self.act is not None else 'No Activation'
            )
        )

    def build(self, inputs):
        if len(self.strides) != 2:
            raise ValueError("len(strides) should be 2.")

        if self.use_gemm:
            raise Exception("TODO. The current version use tf.matmul for inferencing.")

        try:
            self.pre_channel = int(inputs.get_shape()[-1])
        except Exception:  # if pre_channel is ?, it happens when using Spatial Transformer Net
            sefl.pre_channel = 1
            logging.warning("unknow input channels, set to 1")

        self.shape = (self.filter_size[0], self.filter_size[1], self.pre_channel, self.n_filter)
        self.strides = (1, self.strides[0], self.strides[1], 1)

        # self.W = tf.compat.v1.get_variable(
        #     name=self.name + '\kernel', shape=self.shape, initializer=self.W_init, dtype=LayersConfig.tf_dtype,
        #     **self.W_init_args
        # )
        self.W = self._get_weights("filters", shape=self.shape, init=self.W_init, init_args=self.W_init_args)
        if self.b_init:
            self.b = self._get_weights("biases", shape=(self.shape[-1]), init=self.b_init, init_args=self.b_init_args)
        # if self.b_init:
        #     self.b = tf.compat.v1.get_variable(
        #         name=self.name + '\bias', shape=(self.shape[-1]), initializer=self.b_init, dtype=LayersConfig.tf_dtype,
        #         **self.b_init_args
        #     )
        #     self.add_weights([self.W, self.b])
        # else:
        #     self.add_weights(self.W)

    def forward(self, inputs):

        alpha = compute_alpha(self.W)

        W_ = ternary_operation(self.W)
        W_ = tf.multiply(alpha, W_)

        outputs = tf.nn.conv2d(
            inputs, W_, strides=self.strides, padding=self.padding, use_cudnn_on_gpu=self.use_cudnn_on_gpu,
            data_format=self.data_format
        )

        if self.b_init:
            outputs = tf.nn.bias_add(outputs, self.b, name='bias_add')

        if self.act:
            outputs = self.act(outputs)

        return outputs
