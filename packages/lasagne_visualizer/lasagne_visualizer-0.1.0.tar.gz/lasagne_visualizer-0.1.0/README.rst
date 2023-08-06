===============================
lasagne_visualizer
===============================


.. image:: https://img.shields.io/pypi/v/lasagne_visualizer.svg
        :target: https://pypi.python.org/pypi/lasagne_visualizer

.. image:: https://img.shields.io/travis/SimonKohl/lasagne_visualizer.svg
        :target: https://travis-ci.org/SimonKohl/lasagne_visualizer

.. image:: https://readthedocs.org/projects/lasagne-visualizer/badge/?version=latest
        :target: https://lasagne-visualizer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/SimonKohl/lasagne_visualizer/shield.svg
     :target: https://pyup.io/repos/github/SimonKohl/lasagne_visualizer/
     :alt: Updates


A small python package that lets you have a glimpse at the inner workings of your deep lasagne architectures.
-----------------------------------------------------------------------

Using ipython notebook you can now live-monitor the weight learning of your models, or just save the generated visualizations when running command line python scripts.

Obviously, having a rough idea of how the weights of your model progress, can guide you in how to tweak your architecture and its parameters.
Other frameworks such as Tensorflow have had such visualizations from the start and lasagne_visualizer tries to provide a similar, though much more leight-weight, tool.

The image below gives a flavor of how your output might come out to look:

.. image:: https://github.com/SimonKohl/lasagne_visualizer/blob/develop/examples/example.png
    :target: https://github.com/SimonKohl/lasagne_visualizer/blob/develop/examples/

Example
-----
For an example on how to use lasagne_visualizer in an IPython Notebook, see `Finetuning for Image Classification <https://github.com/SimonKohl/lasagne_visualizer/blob/develop/examples/Finetuning%20for%20Image%20Classification.ipynb>`_, which borrows the underlying example from  `ebenolson <https://github.com/ebenolson>`_.


Further Information
-----

* Free software: MIT license
* Documentation: https://lasagne-visualizer.readthedocs.io.


Features
--------

* plot the mean/extremal values/1 sigma error band of the weights of lasagne layers as a function of the training epochs
* use modes to either auto-select all trainable/the currently trainable/user-specified layers for plotting
* adjust the range of the weights in the plots
* TODO: enable the plotting of bias weights

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

