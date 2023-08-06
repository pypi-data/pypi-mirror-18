nose2-spark
===========

Nose2 plugin to run the tests with support of pyspark (`Apache Spark`_).

Features:

1. Make "pyspark" importable in you code executed by nose2.
2. Add a list of `py-files`_ dependencies of your pyspark application.


Install
-------

.. code-block:: shell

    $ pip install nose2-spark

Usage
-----

Load "nose2-spark" plugin into nose2 by creating ``nose2.cfg`` in your project
directory::

    [unittest]
    plugins = nose2_spark

Run tests with nose2-spark activated (pyspark and friends are added to
pythonpath)::

    $ nose2 --pyspark

nose2-spark will try to import pyspark by looking into:

1. SPARK_HOME environment variable
2. Some common Spark locations.

You can set it manually in case if all of mentioned methods are failing
to find Spark. Add section "nose2-spark" to ``nose2.cfg``::

    [nose2-spark]
    spark_home = /opt/spark

You can add a list of required `py-files`_ to run your code::

    [nose2-spark]
    pyfiles = package1.zip
              package2.zip


Example
-------

Example of ``nose2.cfg`` with spark_home defined, one `py-files`_ dependency and
auto activating nose2-spark plugin::

    [unittest]
    plugins = nose2_spark

    [nose2-spark]
    always-on = True
    spark_home = /opt/spark
    pyfiles = package1.zip

This will allow to run tests by single command::

    $ nose2


.. _Apache Spark: https://spark.apache.org/
.. _py-files: http://spark.apache.org/docs/latest/submitting-applications.html#bundling-your-applications-dependencies
