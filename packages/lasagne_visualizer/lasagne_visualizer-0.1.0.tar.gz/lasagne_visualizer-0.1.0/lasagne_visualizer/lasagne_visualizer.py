# -*- coding: utf-8 -*-
# import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from copy import deepcopy


def get_currently_trainable_layers(net):

    layers = [l for l in net.keys() if hasattr(net[l], 'W') if 'trainable' in list(net[l].params[net[l].W])]
    return layers

def get_all_trainable_layers(net):

    layers = [l for l in net.keys() if hasattr(net[l], 'W')]
    return layers

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

class weight_supervisor():
    """
    Class that lets you live-monitor the weights of an arbitrary number of layers.
    Example: PLOT ALL CURRENTLY TRAINABLE WEIGHTS IN LASAGNE NETWORK
        ...import <libraries>
        ...%matplotlib notebook
        ...define net
        ...define no_epochs

        f = plt.figure()

        weight_supervisor = lasagne_visualizer.weight_supervisor(net, mode='currently_trainable', no_epochs, custom_weight_ranges = {'conv1_2':[-2., 2.]})
        weight_supervisor.initialize_grid()
        for epoch in range(no_epochs):
            ...train
            ...evaluate
            weight_supervisor.accumulate_weight_stats()
            weight_supervisor.live_plot()
            f.canvas.draw()
    """

    def __init__(self, net, no_epochs, mode='currently_trainable', layer_names=[], custom_weight_ranges={}):
        """
        Initialize the weight_supervisor class.
        :param net: dictionary with layer names as keys and lasagne layers as values.
        :param no_epochs: integer number of epochs to supervise for.
        :param mode: one in 'currently_trainable', 'all_trainable', 'custom'; if 'custom', @param layer_names needs to be given
        :param layer_names: list of names of layers to supervise, used only if @param mode equals 'custom'
        :param custom_weight_ranges: a dictionary with layer names as keys and lists specifying the custom max/min values of the layers' weights as values.

        """
        if mode == 'currently_trainable':
            self.layer_names = get_currently_trainable_layers(net)
        elif mode == 'all_trainable':
            self.layer_names = get_all_trainable_layers(net)
        elif mode == 'custom':
            self.layer_names = layer_names
        else:
            raise Exception("Give a @param mode in ['currently_trainable', 'all_trainable', 'custom']!")

        self.net = net
        self.no_epochs = no_epochs

        self.weight_ranges = {l:[-1.,1.] if l not in custom_weight_ranges.keys() else custom_weight_ranges[l] for l in self.layer_names}
        init_dict = {l: [] for l in self.layer_names}
        self.max_weights, self.min_weights, self.mean_weights, self.err_band_lo_weights, self.err_band_hi_weights = \
            deepcopy(init_dict), deepcopy(init_dict), deepcopy(init_dict), deepcopy(init_dict), deepcopy(init_dict)
        self.epochs = []
        self.curr_epoch = 1

    def initialize_grid(self):

        no_layers = len(self.layer_names)
        gs = gridspec.GridSpec(no_layers, 1)
        self.axis = []

        for l in range(no_layers):
            self.axis.append(plt.subplot(gs[l, 0]))

            y_min = self.weight_ranges[self.layer_names[l]][0]
            y_max = self.weight_ranges[self.layer_names[l]][1]

            self.axis[l].set_xlim(1, self.no_epochs)
            self.axis[l].set_ylim(y_min, y_max)

            aspect_ratio = self.no_epochs // 5 /(y_max-y_min)

            try:
                assert aspect_ratio > 0.
            except AssertionError:
                raise Exception("aspect ratio must be > 0., was found {}".format(aspect_ratio))

            self.axis[l].set_aspect(aspect_ratio)
            self.axis[l].locator_params(axis='y', nbins=5)
            self.axis[l].locator_params(axis='x', nbins=5)

        self.axis[-1].set_xlabel('epochs')

    def accumulate_weight_stats(self):

        for l in self.layer_names:

            weights = self.net[l].W.get_value()[0]
            total_weights = 1
            for w in weights.shape:
                total_weights *= w

            weights = weights.reshape(total_weights)
            weights = [weights[i] for i in range(len(weights))]

            self.max_weights[l].append(max(weights))
            self.min_weights[l].append(min(weights))
            self.mean_weights[l].append(mean(weights))
            self.err_band_lo_weights[l].append(mean(weights) - pstdev(weights) / 2.)
            self.err_band_hi_weights[l].append(mean(weights) + pstdev(weights) / 2.)

        self.epochs.append(self.curr_epoch)
        self.curr_epoch += 1

    def live_plot(self):

        fs = 12

        for l_ix, l in enumerate(self.layer_names):

            if self.axis[l_ix].lines:
                self.axis[l_ix].lines[0].set_xdata(self.epochs)
                self.axis[l_ix].lines[0].set_ydata(self.mean_weights[l])
            else:
               self.axis[l_ix].plot(self.epochs, self.mean_weights[l], 'r', label='mean')

            ### remove collection objects to avoid stacked redrawing
            self.axis[l_ix].collections[:] = []

            self.axis[l_ix].fill_between(self.epochs, self.min_weights[l], self.err_band_lo_weights[l], facecolor='green', edgecolor='green',alpha=0.5, label='extremata')
            self.axis[l_ix].fill_between(self.epochs, self.max_weights[l], self.err_band_hi_weights[l] , facecolor='green', edgecolor='green', alpha=0.5)
            self.axis[l_ix].fill_between(self.epochs, self.err_band_lo_weights[l] , self.err_band_hi_weights[l], facecolor='blue', edgecolor='blue',alpha=0.5, label='std. dev.')

            ### remove previous text objects to avoid stacked redrawing
            self.axis[l_ix].texts[:] = []

            y_max = self.weight_ranges[l][1]

            self.axis[l_ix].text(1., y_max, l, color='black', fontsize=fs, bbox=dict(facecolor='white', alpha=1))

        handles, labels = self.axis[0].get_legend_handles_labels()
        leg = self.axis[0].legend(handles, labels, ncol=3, loc=1, fontsize=fs)
        leg.get_frame().set_alpha(0.5)







