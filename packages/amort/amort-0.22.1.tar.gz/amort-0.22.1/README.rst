.. image:: amort/images/title.png

|travis| |coverage| |pyversions| |version| |status| |format| |license|

Amortization is a command line interface that outputs an amortization schedule
based on the user's input of the borrowed amount, interest rate, loan duration, and
number of payments made annually. For reading on amortization schedules please
visit: https://en.wikipedia.org/wiki/Amortization_schedule

*************
Installation
*************

Amortization requires the pandas library in order for the command line application to work correctly. Pandas should be pre-installed in the environment where amortization is installed. For pandas install instructions, please visit: http://pandas.pydata.org/

To install the Amortization package simply open a command line prompt and run::
    
    pip install amort

If you would rather install from source, run the following commands::

    git clone https://github.com/mandeep/Amortization.git
    cd Amortization
    python setup.py install 

******
Usage
******

Once Amortization is installed, the command line application can be invoked with the following command and mandatory arguments::

    amortization BORROWED INTEREST LENGTH PERIODS [NAME]

    Example:

    amortization 70000000 3 30 12 "Gulfstream G650 Loan"

Output of the command line application appears below:

.. image:: amort/images/amort.png

.. |version| image:: https://img.shields.io/pypi/v/amort.svg
    :target: https://pypi.python.org/pypi/amort
.. |travis| image:: https://travis-ci.org/mandeep/Amortization.svg?branch=master
    :target: https://travis-ci.org/mandeep/Amortization
.. |coverage| image:: https://coveralls.io/repos/github/mandeep/Amortization/badge.svg?branch=master
    :target: https://coveralls.io/github/mandeep/Amortization?branch=master
.. |license| image:: https://img.shields.io/pypi/l/amort.svg
    :target: https://pypi.python.org/pypi/amort
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/amort.svg
    :target: https://pypi.python.org/pypi/amort
.. |status| image:: https://img.shields.io/pypi/status/amort.svg
    :target: https://pypi.python.org/pypi/amort
.. |format| image:: https://img.shields.io/pypi/format/amort.svg
    :target: https://pypi.python.org/pypi/amort