======
quorra
======

A python wrapper around `quorra.js <https://github.com/bprinty/quorra>`_, for creating reusable visualizations.


Installation
============

Currently, the best way to install this repository is directly from the source:

.. code-block:: bash

    git clone http://github.com/bprinty/quorra-python.git
    cd quorra-python
    python setup.py install



Usage
=====

Coming soon ...

In the meantime, here's a snippit of how to generate a toy plot:

.. code-block:: python
    
    >>> import quorra
    >>> import pandas
    >>> import random
    >>> data = pandas.DataFrame({ 
    >>>     'x': [i for i in range(0, 10)],
    >>>     'y': [round(random.gauss(100, 10), 2) for i in range(0, 10)],
    >>>     'group': ['data']*10
    >>> })
    >>> plt = quorra.line().data(
    >>>     data,
    >>>     x='x',
    >>>     y='y',
    >>>     group='group'
    >>> ).xlabel('Index').ylabel('Random Value')
    >>> quorra.render(plt)



Questions/Feedback
==================

File an issue in the `GitHub issue tracker <https://github.com/bprinty/quorra/issues>`_.
