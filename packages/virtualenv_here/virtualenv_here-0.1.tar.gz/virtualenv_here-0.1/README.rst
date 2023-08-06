=================
 virtualenv-here
=================

Manage a virtualenv based on a project's path.

Example
=======

.. code:: bash

    $ cd /tmp/

    $ git clone https://github.com/pypa/sampleproject
    Cloning into 'sampleproject'...
    remote: Counting objects: 220, done.
    remote: Total 220 (delta 0), reused 0 (delta 0), pack-reused 220
    Receiving objects: 100% (220/220), 37.26 KiB | 0 bytes/s, done.
    Resolving deltas: 100% (103/103), done.
    Checking connectivity... done.

    $ cd sampleproject/

    $ virtualenv-here
    virtualenv-here: Initializing virtualenv for project: '.'
    Using real prefix '/usr'
    New python executable in /home/user/.virtualenv-here/venvs/tmp.sampleproject/bin/python2
    Also creating executable in /home/user/.virtualenv-here/venvs/tmp.sampleproject/bin/python
    Installing setuptools, pip, wheel...done.
    virtualenv-here: Launching subshell for project: '.'

    user@myhost:/tmp/sampleproject $ export PS1="\n\$ "

    $ echo $VIRTUAL_ENV
    /home/user/.virtualenv-here/venvs/tmp.sampleproject/

    $ pwd
    /tmp/sampleproject

    $ pip install .
    Processing /tmp/sampleproject
    Collecting peppercorn (from sample==1.2.0)
      Downloading peppercorn-0.5.tar.gz
    Building wheels for collected packages: peppercorn
      Running setup.py bdist_wheel for peppercorn ... done
      Stored in directory: /home/user/.cache/pip/wheels/d3/86/5f/8a590bb8d2c95024b7dd0c01d348549818324f37b523589f70
    Successfully built peppercorn
    Installing collected packages: peppercorn, sample
      Running setup.py install for sample ... done
    Successfully installed peppercorn-0.5 sample-1.2.0

    $ python
    Python 2.7.12+ (default, Sep  1 2016, 20:27:38)
    [GCC 6.2.0 20160822] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import peppercorn
    >>> peppercorn
    <module 'peppercorn' from '/home/user/.virtualenv-here/venvs/tmp.sampleproject/local/lib/python2.7/site-packages/peppercorn/__init__.pyc'>
    >>> ^D

    $ exit
    virtualenv-here: Exiting subshell (status 0) for project: '.'

    $ python -c 'import peppercorn'
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named peppercorn
