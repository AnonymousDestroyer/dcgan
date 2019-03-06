#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer
# from tensorlayer.layers.core import LayersConfig

from tensorlayer import logging

from tensorlayer.decorators import deprecated_alias

__all__ = [
    'Dropout',
]


class Dropout(Layer):
    """
    The :class:`Dropout` class is a noise layer which randomly set some
    activations to zero according to a keeping probability.

    Parameters
    ----------
    keep : float
        The keeping probability.
        The lower the probability it is, the more activations are set to zero.
    seed : int or None
        The seed for random dropout.
    name : None or str
        A unique layer name.

    """

    def __init__(self, keep, seed=None, name=None):  #"dropout"):
        super(Dropout, self).__init__(name)
        self.keep = keep
        self.seed = seed

        self.build()
        self._built = True

        logging.info("Dropout %s: keep: %f " % (self.name, self.keep))

    '''
    def build(self, inputs):
        pass

    def forward(self, inputs, is_train):
        if is_train:
            outputs = tf.nn.dropout(inputs, keep=self.keep, seed=self.seed, name=self.name)
        else:
            outputs = inputs
        return outputs
    '''

    def build(self, inputs_shape=None):
        # return inputs_shape
        pass

    def forward(self, inputs):
        # print(self.is_train)
        if self.is_train:
            outputs = tf.nn.dropout(inputs, rate=1 - (self.keep), seed=self.seed, name=self.name)
        else:
            outputs = inputs
        return outputs
