Time Till Done (ttd)
-------------------

.. image:: https://travis-ci.org/JarrodCTaylor/ttd.svg?branch=master
    :target: https://travis-ci.org/JarrodCTaylor/ttd

Time Till Done ``ttd`` for short is a simple progress bar to help give you some
feedback for your long running Python scripts.

Installation
============

``pip install ttd``

Demo Gif
========
.. image:: https://cloud.githubusercontent.com/assets/4416952/3593813/177b9caa-0c8e-11e4-9e6d-87340fe43bd1.gif

Usage
=====

The easiest way to use the module is in a for loop as demonstrated in the demo
gif above and the code snippet below.

.. code:: python

    import time
    from ttd import ttd

    for i in ttd(range(99)):
        time.sleep(.05)

You may also update the progress bar manually by calling ``print_ttd(index, total)``
throughout your script as demonstrated below.

.. code:: python

    import time
    from ttd import print_ttd

    print_ttd(0, 5)
    time.sleep(.5)

    print_ttd(1, 5)
    time.sleep(.04)

    print_ttd(2, 5)
    time.sleep(.5)

    print_ttd(3, 5)
    time.sleep(.5)

    print_ttd(4, 5)
    time.sleep(.5)

    print_ttd(5, 5)
    print("\ndone")
