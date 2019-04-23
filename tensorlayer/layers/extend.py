#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer

from tensorlayer import logging

from tensorlayer.decorators import deprecated_alias

__all__ = [
    'ExpandDims',
    'Tile',
]


class ExpandDims(Layer):
    """
    The :class:`ExpandDims` class inserts a dimension of 1 into a tensor's shape,
    see `tf.expand_dims() <https://www.tensorflow.org/api_docs/python/tf/expand_dims>`__ .

    Parameters
    ----------
    axis : int
        The dimension index at which to expand the shape of input.
    name : str
        A unique layer name.

    Examples
    --------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> x = tf.placeholder(tf.float32, (None, 100))
    >>> n = tl.layers.Input(x, name='in')
    >>> n = tl.layers.ExpandDims(n, 2)
    [None, 100, 1]
    """

    @deprecated_alias(layer='prev_layer', end_support_version=1.9)  # TODO remove this line for the 1.9 release
    def __init__(
            self,
            prev_layer,
            axis,
            name='expand_dims',
    ):
        # super(ExpandDims, self).__init__(prev_layer=prev_layer, name=name)
        super().__init__(name)
        self.axis = axis
        logging.info("ExpandDims  %s: axis: %d" % (self.name, self.axis))

    def build(self, inputs_shape):
        pass

    def forward(self, inputs):
        outputs = tf.expand_dims(inputs, axis=self.axis, name=self.name)
        return outputs


class Tile(Layer):
    """
    The :class:`Tile` class constructs a tensor by tiling a given tensor,
    see `tf.tile() <https://www.tensorflow.org/api_docs/python/tf/tile>`__ .

    Parameters
    ----------
    multiples: tensor
        Must be one of the following types: int32, int64.
        1-D Length must be the same as the number of dimensions in input.
    name : None or str
        A unique layer name.

    Examples
    --------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> x = tf.placeholder(tf.float32, (None, 100))
    >>> n = tl.layers.Input(x, name='in')
    >>> n = tl.layers.ExpandDims(n, 2)
    >>> n = tl.layers.Tile(n, [-1, 1, 3])
    [None, 100, 3]
    """

    def __init__(self, multiples=None, name=None):  #'tile'):

        # super(Tile, self).__init__(prev_layer=prev_layer, name=name)
        super().__init__(name)
        self.multiples = multiples

        logging.info("Tile  %s: multiples: %s" % (self.name, self.multiples))

    def build(self, inputs_shape):
        pass

    def forward(self, inputs):
        outputs = tf.tile(inputs, multiples=self.multiples, name=self.name)
        return outputs
