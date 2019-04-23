#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer
# from tensorlayer.layers.core import LayersConfig

from tensorlayer.layers.utils import compute_alpha
from tensorlayer.layers.utils import ternary_operation

from tensorlayer import logging

from tensorlayer.decorators import deprecated_alias

__all__ = [
    'TernaryDense',
]


class TernaryDense(Layer):
    """The :class:`TernaryDense` class is a ternary fully connected layer, which weights are either -1 or 1 or 0 while inference.

    Note that, the bias vector would not be tenaried.

    Parameters
    ----------
    n_units : int
        The number of units of this layer.
    act : activation function
        The activation function of this layer, usually set to ``tf.act.sign`` or apply :class:`SignLayer` after :class:`BatchNormLayer`.
    use_gemm : boolean
        If True, use gemm instead of ``tf.matmul`` for inference. (TODO).
    W_init : initializer
        The initializer for the weight matrix.
    b_init : initializer or None
        The initializer for the bias vector. If None, skip biases.
    W_init_args : dictionary
        The arguments for the weight matrix initializer.
    b_init_args : dictionary
        The arguments for the bias vector initializer.
    name : None or str
        A unique layer name.

    """

    def __init__(
            self,
            n_units=100,
            act=None,
            use_gemm=False,
            W_init=tf.compat.v1.initializers.truncated_normal(stddev=0.1),
            b_init=tf.compat.v1.initializers.constant(value=0.0),
            W_init_args=None,
            b_init_args=None,
            name=None,  #'ternary_dense',
    ):
        # super(TernaryDense, self
        #      ).__init__(prev_layer=prev_layer, act=act, W_init_args=W_init_args, b_init_args=b_init_args, name=name)
        super().__init__(name)
        self.n_units = n_units
        self.act = act
        self.use_gemm = use_gemm
        self.W_init = W_init
        self.b_init = b_init
        self.W_init_args = W_init_args
        self.b_init_args = b_init_args
        logging.info(
            "TernaryDense  %s: %d %s" %
            (self.name, n_units, self.act.__name__ if self.act is not None else 'No Activation')
        )

    def build(self, inputs_shape):
        # if inputs.get_shape().ndims != 2:
        if len(inputs_shape) != 2:
            raise Exception("The input dimension must be rank 2, please reshape or flatten it")

        if self.use_gemm:
            raise Exception("TODO. The current version use tf.matmul for inferencing.")

        n_in = inputs_shape[-1]

        # self.W = tf.compat.v1.get_variable(
        #     name=self.name + '\W', shape=(n_in, self.n_units), initializer=self.W_init, dtype=LayersConfig.tf_dtype,
        #     **self.W_init_args
        # )
        self.W = self._get_weights(
            scope_name=self.name, var_name="weights", shape=(n_in, self.n_units), init=self.W_init,
            init_args=self.W_init_args
        )
        if self.b_init is not None:
            self.b = self._get_weights(
                scope_name=self.name, var_name="biases", shape=(self.n_units), init=self.b_init,
                init_args=self.b_init_args
            )
        #     try:
        #         self.b = tf.compat.v1.get_variable(
        #             name=self.name + '\b', shape=(self.n_units), initializer=self.b_init, dtype=LayersConfig.tf_dtype,
        #             **self.b_init_args
        #         )
        #     except Exception:  # If initializer is a constant, do not specify shape.
        #         self.b = tf.compat.v1.get_variable(
        #             name=self.name + '\b', initializer=self.b_init, dtype=LayersConfig.tf_dtype, **self.b_init_args
        #         )
        #     self.get_weights([self.W, self.b])
        # else:
        #     self.get_weights(self.W)

    def forward(self, inputs):
        # W = tl.act.sign(W)    # dont update ...
        alpha = compute_alpha(self.W)
        W_ = ternary_operation(self.W)
        W_ = tf.multiply(alpha, W_)
        # W = tf.Variable(W)

        outputs = tf.matmul(inputs, W_)
        # self.outputs = xnor_gemm(self.inputs, W) # TODO

        if self.b_init is not None:
            outputs = tf.nn.bias_add(outputs, self.b, name='bias_add')
        if self.act:
            outputs = self.act(outputs)
        return outputs
