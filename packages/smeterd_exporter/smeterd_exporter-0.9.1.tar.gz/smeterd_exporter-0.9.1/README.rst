smeterd_exporter
================

.. image:: https://travis-ci.org/nrocco/smeterd_exporter.svg?branch=master
    :target: https://travis-ci.org/nrocco/smeterd_exporter

A prometheus exporter for your smart meter.



installation
------------

`smeterd_exporter` is fully python 2.7 and python 3.4 compatible.

It is highly recommended to use virtual environemnts for this::

    $ pyvenv my_virtual_env
    $ cd my_virtual_env
    $ . bin/activate


After having your virtual environment installed and activated run the following command to install
the `smeterd` package directly from pypi (using pip)::

    $ pip install smeterd_exporter


Alternatively you can manually clone `smeterd_exporter` and run setupttools `setup.py`::

    $ git clone https://github.com/nrocco/smeterd_exporter.git
    $ cd smeterd_exporter
    $ python setup.py install


This will install the needed python libraries which are needed to start reading
P1 packets.

If you don't want to install `smeterd_exporter` as a package you can run it
directly from the root directory of the git repository using the following
command but you are responsible for manually installing dependencies::

    $ python -m smeterd_exporter


To install the required dependencies manually see `requirements.txt`
or simply run::

    $ pip install -r requirements.txt



usage
-----

TODO



contribute
----------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Make sure that tests pass (`make test`)
5. Push to the branch (`git push origin my-new-feature`)
6. Create new Pull Request
