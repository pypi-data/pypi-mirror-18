bonfy	-	leetcode-dl
=======================

*leetcode-dl* is a Command-line program to download solutions from leetcode.com


Installation
^^^^^^^^^^^^

=====================
Installing from PyPI
=====================

Once you have `pip3`, execute:

.. code-block:: shell

    $ pip3 install leetcode-dl

=======================
Installing source code
=======================


First you need to clone `python-openflow` repository:

.. code-block:: shell

   $ git clone https://github.com/bonfy/leetcode-dl.git


After cloning, the installation process is done by `setuptools` in the usual
way:

.. code-block:: shell

   $ cd leetcode-dl
   $ python3 setup.py install


Usage
^^^^^

.. code-block:: shell

    $ leetcode-dl
    $ leetcode-dl -h|help     help page
    $ leetcode-dl -set        set config
    $ leetcode-dl -show       show config
    $ leetcode-dl -readme     generate|update readme
    $ leetcode-dl -q qid      download by qid(like 1 2 16)


