#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import logging
import numpy
import theano
import theano.tensor as tensor
from theanolm.matrixfunctions import random_weight, orthogonal_weight

class BasicLayer(object):
    """Superclass for Neural Network Layers
    """

    def __init__(self, layer_options, network, profile=False):
        """Saves some attributes that are common to all layers.

        :type layer_options: dict
        :param layer_options: dictionary of layer options

        :type network: Network
        :param network: the network object creating this layer

        :type profile: bool
        :param profile: if set to True, creates a Theano profile object
        """

        self.name = layer_options['name']
        self.input_layers = layer_options['input_layers']

        if 'size' in layer_options:
            self.output_size = layer_options['size']
        else:
            self.output_size = \
                sum([ x.output_size for x in self.input_layers ])

        logging.debug("- %s name=%s inputs=[%s] size=%d",
            self.__class__.__name__,
            self.name,
            ', '.join([x.name for x in self.input_layers]),
            self.output_size)

        self.network = network
        self._profile = profile
        self.param_init_values = OrderedDict()

    def set_params(self, params):
        """Sets the dictionary that can be used to access Theano shared
        variables.

        :type params: dict
        :param params: a dictionary of Theano shared variables indexed by
                       parameter name
        """

        self._params = params

    def _param_path(self, param_name):
        """Returns the HDF5 path used to address a parameter.

        :type param_name: str
        :param param_name: name of a parameter within this layer

        :rtype: str
        :returns: full path of the parameter in a HDF5 file.
        """

        return 'layers/' + self.name + '/' + param_name

    def _get_param(self, param_name):
        """Returns a Theano tensor variable by parameter name.

        :type param_name: str
        :param param_name: name of a parameter within the layer

        :rtype: TensorVariable
        :returns: the corresponding tensor variable
        """

        return self._params[self._param_path(param_name)]

    def _init_random_weight(self, param_name, shape, scale=None, count=1):
        """Generates a weight matrix from “standard normal” distribution.

        :type shape: tuple of ints
        :param shape: size of each dimension (typically there are two
                      dimensions, input and output)

        :type scale: float
        :param scale: if other than None, the random numbers will be scaled by
                      this factor

        :rtype: numpy.ndarray
        :returns: the generated weight matrix
        """

        self.param_init_values[self._param_path(param_name)] = \
            numpy.concatenate([random_weight(shape, scale=scale)
                               for _ in range(count)],
                              axis=1)

    def _init_orthogonal_weight(self, param_name, input_size, output_size, scale=None, count=1):
        """Generates a weight matrix from “standard normal” distribution. If
        in_size matches out_size, generates an orthogonal matrix.

        :type input_size: int
        :param input_size: size of the input dimension of the weight

        :type output_size: int
        :param output_size: size of the output dimension of the weight

        :type scale: float
        :param scale: if other than None, the matrix will be scaled by this factor,
                      unless an orthogonal matrix is created
        """

        self.param_init_values[self._param_path(param_name)] = \
            numpy.concatenate([orthogonal_weight(input_size, output_size, scale=0.01)
                               for _ in range(count)],
                              axis=1)

    def _init_bias(self, param_name, shape, value=None):
        """Initializes a bias vector with given value.

        If ``value`` is not given, initializes the vector with zero value. If
        ``value`` is a list, creates a concatenation of as many vectors as there
        are elements in the list.

        :type param_name: str
        :param param_name: name for the parameter within the layer

        :type shape: int or tuple of ints
        :param shape: size of the vector, or a tuple of the sizes of each
                      dimension (in case ``value`` is a list, each part will
                      have this size)

        :type value: float or list of floats
        :param value: the value to initialize the elements to, or a list of
                      values to create a concatenation of vectors
        """

        values = value if isinstance(value, list) else [value]
        parts = []
        for part_value in values:
            if part_value is None:
                part = numpy.zeros(shape).astype(theano.config.floatX)
            else:
                part = numpy.empty(shape).astype(theano.config.floatX)
                part.fill(part_value)
            parts.append(part)
        self.param_init_values[self._param_path(param_name)] = \
            numpy.concatenate(parts)

    def _tensor_preact(self, input_matrix, param_name):
        """Helper function that creates a pre-activation of ``input_matrix`` by
        multiplying it by a weight matrix and adding a bias.

        ``input_matrix`` and the result normally have the shape of a mini-batch:
        the first dimension is the time step and the second dimension is the
        sequence. The last dimension is always the data vector. The size of the
        input data vector should equal to the first dimension of the weight
        vector, and the second dimension of the weight vector defines the size
        of the output data vector.

        :type input_matrix: TensorVariable
        :param input_matrix: the preactivations will be computed by multiplying
                             the data vectors (the last dimension of this
                             matrix) by the weight matrix, and adding bias

        :type param_name: str
        :param param_name: name of a parameter group that contains a weight
                           matrix and a bias vector

        :rtype: TensorVariable
        :returns: a matrix tha has the same number of dimensions as
                  ``input_matrix``, but the data vectors (the last dimension of
                  this matrix) are the preactivations
        """

        weight = self._params[self._param_path(param_name) + '/W']
        bias = self._params[self._param_path(param_name) + '/b']
        return tensor.dot(input_matrix, weight) + bias
