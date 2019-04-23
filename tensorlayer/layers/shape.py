#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer
from tensorlayer.layers.utils import flatten_reshape

from tensorlayer import logging

from tensorlayer.decorators import deprecated_alias

__all__ = [
    'Flatten',
    'Reshape',
    'Transpose',
]


class Flatten(Layer):
    """A layer that reshapes high-dimension input into a vector.

    Then we often apply Dense, RNN, Concat and etc on the top of a flatten layer.
    [batch_size, mask_row, mask_col, n_mask] ---> [batch_size, mask_row * mask_col * n_mask]

    Parameters
    ----------
    name : None or str
        A unique layer name.

    Examples
    --------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> x = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
    >>> net = tl.layers.Input(x, name='input')
    >>> net = tl.layers.Flatten(net, name='flatten')
    [?, 784]

    """

    def __init__(self, name=None):  #'flatten'):
        # super(Flatten, self).__init__(prev_layer=prev_layer, name=name)
        super().__init__(name)

        self.build()
        self._built = True

        logging.info("Flatten %s:" % (self.name))

    def __repr__(self):
        s = '{classname}('
        if self.name is not None:
            s += 'name=\'{name}\''
        s += ')'
        return s.format(classname=self.__class__.__name__, **self.__dict__)

    def build(self, inputs_shape=None):
        pass

    def forward(self, inputs):
        outputs = flatten_reshape(inputs, name=self.name)
        return outputs


class Reshape(Layer):
    """A layer that reshapes a given tensor.

    Parameters
    ----------
    shape : tuple of int
        The output shape, see ``tf.reshape``.
    name : str
        A unique layer name.

    Examples
    --------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> x = tf.placeholder(tf.float32, shape=(None, 784))
    >>> net = tl.layers.Input(x, name='input')
    >>> net = tl.layers.Reshape(net, [-1, 28, 28, 1], name='reshape')
    >>> print(net.outputs)
    (?, 28, 28, 1)

    """

    def __init__(self, shape, name=None):  #'reshape'):
        # super(Reshape, self).__init__(prev_layer=prev_layer, name=name)
        super().__init__(name)
        self.shape = shape
        logging.info("Reshape %s" % (self.name))
        if not self.shape:
            raise ValueError("Shape list can not be empty")

        self.build()
        self._built = True

    def build(self, inputs_shape=None):
        pass

    def forward(self, inputs):
        outputs = tf.reshape(inputs, shape=self.shape, name=self.name)
        return outputs


class Transpose(Layer):
    """A layer that transposes the dimension of a tensor.

    See `tf.transpose() <https://www.tensorflow.org/api_docs/python/tf/transpose>`__ .

    Parameters
    ----------
    perm: list of int
        The permutation of the dimensions, similar with ``numpy.transpose``.
    name : str
        A unique layer name.

    Examples
    ----------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> x = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
    >>> net = tl.layers.Input(x, name='input')
    >>> net = tl.layers.Transpose(net, perm=[0, 1, 3, 2], name='trans')
    [None, 28, 1, 28]

    """

    def __init__(self, perm, name=None):  #'transpose'):
        # super(Transpose, self).__init__(prev_layer=prev_layer, name=name)
        super().__init__(name)
        self.perm = perm

        logging.info("Transpose  %s: perm: %s" % (self.name, self.perm))
        if self.perm is None:
            raise AssertionError("The `perm` argument cannot be None")

        self.build()
        self._built = None

    def build(self, inputs_shape=None):
        pass

    def forward(self, inputs):
        outputs = tf.transpose(a=inputs, perm=self.perm, name=self.name)
        return outputs
