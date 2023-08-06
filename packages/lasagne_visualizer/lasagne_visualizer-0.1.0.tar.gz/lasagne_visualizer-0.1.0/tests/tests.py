#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lasagne_visualizer
----------------------------------

Tests for `lasagne_visualizer` module.
"""

import unittest

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from lasagne_visualizer import lasagne_visualizer
from lasagne.layers import InputLayer, ReshapeLayer, Conv2DLayer, DenseLayer
from lasagne.nonlinearities import softmax
from lasagne.init import Constant
import collections


class TestLasagne_visualizer(unittest.TestCase):
    net = collections.OrderedDict()
    net['l_in'] = InputLayer((None, 784))
    net['l_shape'] = ReshapeLayer(net['l_in'], (-1, 1, 28, 28))
    net['l_conv'] = Conv2DLayer(net['l_shape'], num_filters=3, filter_size=3, pad=1)
    net['l_out'] = DenseLayer(net['l_conv'], num_units=10, nonlinearity=softmax)

    def test_weight_ranges_initialization(self):

        net = self.net
        no_epochs = 5

        ws = lasagne_visualizer.weight_supervisor(net, no_epochs, mode='all_trainable')

        self.assertEquals(ws.weight_ranges.values(), [[-1.,1.]]*2)
        self.assertItemsEqual(ws.layer_names, net.keys()[-2:])
        self.assertItemsEqual(ws.max_weights.keys(), net.keys()[-2:])
        self.assertItemsEqual(ws.min_weights.keys(), net.keys()[-2:])
        self.assertItemsEqual(ws.mean_weights.keys(), net.keys()[-2:])
        self.assertItemsEqual(ws.err_band_lo_weights.keys(), net.keys()[-2:])
        self.assertItemsEqual(ws.err_band_hi_weights.keys(), net.keys()[-2:])

    def test_custom_weight_ranges_initialization(self):

        net = self.net
        no_epochs = 5

        custom_weight_range = {'l_out':[-5.,5.]}
        ws = lasagne_visualizer.weight_supervisor(net, no_epochs, mode='all_trainable', custom_weight_ranges=custom_weight_range)

        self.assertEquals(ws.weight_ranges['l_conv'], [-1.,1.])
        self.assertEquals(ws.weight_ranges['l_out'], [-5.,5.])

    def test_init_mode_currently_trainable(self):

        net = self.net
        no_epochs = 5

        net['l_conv'].params[net['l_conv'].W].remove('trainable')
        net['l_out'].params[net['l_out'].W].add('trainable')

        ws = lasagne_visualizer.weight_supervisor(net, no_epochs, mode='currently_trainable')

        self.assertItemsEqual(ws.layer_names, ['l_out'])
        self.assertItemsEqual(ws.max_weights.keys(), ['l_out'])
        self.assertItemsEqual(ws.min_weights.keys(), ['l_out'])
        self.assertItemsEqual(ws.mean_weights.keys(), ['l_out'])
        self.assertItemsEqual(ws.err_band_lo_weights.keys(), ['l_out'])
        self.assertItemsEqual(ws.err_band_hi_weights.keys(), ['l_out'])

    def test_init_mode_custom(self):

        net = self.net
        no_epochs = 5

        ws = lasagne_visualizer.weight_supervisor(net, no_epochs, mode='custom', layer_names=['l_conv'])

        self.assertItemsEqual(ws.layer_names, ['l_conv'])
        self.assertItemsEqual(ws.max_weights.keys(), ['l_conv'])
        self.assertItemsEqual(ws.min_weights.keys(), ['l_conv'])
        self.assertItemsEqual(ws.mean_weights.keys(), ['l_conv'])
        self.assertItemsEqual(ws.err_band_lo_weights.keys(), ['l_conv'])
        self.assertItemsEqual(ws.err_band_hi_weights.keys(), ['l_conv'])

    def test_init_custom_exception(self):

        net = self.net
        no_epochs = 5

        self.assertRaises(Exception, lasagne_visualizer.weight_supervisor(net, no_epochs, mode='custom'))

    def test_custom_weight_range_aspect_ratio_exception(self):

        net = self.net
        no_epochs = 5

        custom_weight_range = {'l_out':[1.,-1.]}
        ws = lasagne_visualizer.weight_supervisor(net, no_epochs, mode='all_trainable', custom_weight_ranges=custom_weight_range)

        self.assertRaises(Exception, ws.initialize_grid)

    def test_simple_stats(self):
        net = collections.OrderedDict()
        net['l_in'] = InputLayer((None, 784))
        net['l_shape'] = ReshapeLayer(net['l_in'], (-1, 1, 28, 28))
        net['l_conv'] = Conv2DLayer(net['l_shape'], num_filters=3, filter_size=3, W=Constant(1.), pad=1)
        net['l_out'] = DenseLayer(net['l_conv'], num_units=10, W=Constant(1.), nonlinearity=softmax)

        no_epochs = 5
        ws = lasagne_visualizer.weight_supervisor(net, no_epochs, mode='all_trainable')
        ws.initialize_grid()
        ws.accumulate_weight_stats()

        self.assertEquals(ws.max_weights.values(), [[1.]]*2)
        self.assertEquals(ws.min_weights.values(), [[1.]]*2)
        self.assertItemsEqual(ws.mean_weights.values(), [[1.]]*2)
        self.assertItemsEqual(ws.err_band_lo_weights.values(), [[1.]]*2)
        self.assertItemsEqual(ws.err_band_hi_weights.values(), [[1.]]*2)

    def test_number_of_matplotlib_objects(self):

        net = self.net
        no_epochs = 5

        ws = lasagne_visualizer.weight_supervisor(net, no_epochs, mode='custom', layer_names = ['l_conv'])
        ws.initialize_grid()
        ws.accumulate_weight_stats()
        ws.live_plot()

        self.assertEquals(len(ws.axis[0].lines), 1)
        self.assertEquals(len(ws.axis[0].collections), 3)
        self.assertEquals(len(ws.axis[0].texts), 1)


if __name__ == '__main__':
    unittest.main()
