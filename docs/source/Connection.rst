
Connecting to notebooks from outside UCL
========================================

.. container::

   You can find more information about accessing the Lab computers in
   this webpage.

Jupyter notebooks are accessed through the browser, and it is possible
to run the jupyter notebook on the computers in the UCL Geography lab,
but still access the browser remotely (either from a laptop while on
UCL, or from anywhere else).

It is also possible to access the UNIX shell remotely, and doing this is
a requirement for accessing the Jupyter notebooks remotely. Let’s first
look at accessing the UNIX shell remotely first.

Remote access to your UCL shell
-------------------------------

The UNIX lab computers can be accessed using the ``ssh`` command. This
command is encrypted and allows one to connect to a remote computer
through the Internet. On **Linux** and **MacOSX**, ``ssh`` is installed
by default. On **Windows**, it has to be installed. A good option for
this is `MobaXterm <https://mobaxterm.mobatek.net/>`__, although there
is also `Kitty <http://www.9bis.net/kitty/>`__ if you like more
bare-bones systems (and a less restrictive license).

We will assume that you want to access your home directory. You can do
this by “ssh-ing” to one of the bastion computers that are open to the
outside internet:

-  ``arch.geog.ucl.ac.uk``
-  ``round.geog.ucl.ac.uk``
-  ``square.geog.ucl.ac.uk``
-  ``triangle.geog.ucl.ac.uk``

In Linux or MacOSX, you can simply do this using the command

::

   ssh -YXC username@triangle.geog.ucl.ac.uk

where ``username`` needs to be substituted by your Geography Linux
username. The system will prompt you for a password (note that if you
start typing, it will not print anything back, this is normal), and as
finish typing the password and pressing “Return”, you’ll be logged into
your home space.

This isn’t very exciting: the bastion computers have little software
installed, and they’re a *gateway* to the other computers in the lab.
However, they work fine for transferring files to and from your own
computer and Geography’s Linux system.

Accessing a lab computer
~~~~~~~~~~~~~~~~~~~~~~~~

Once you’ve logged into to one of the bastion hosts, you can use ``ssh``
again to log into a lag machine, e.g. \ ``ankara``:

::

   ssh -YXC username@ankara.geog.ucl.ac.uk

This is equivalent as being sitting down in front of the terminal in the
lab.

Actually accessing the Jupyter notebooks remotely
-------------------------------------------------

Once you have access, you can launch the Jupyter notebook

jupyter notebook –no-browser –ip=\* –port=8889

You will see some text scroll down the screen. This is what I get if I
run this command, your result will be slightly different:

::

   [W 16:17:05.852 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
   [I 16:17:05.878 NotebookApp] [jupyter_nbextensions_configurator] enabled 0.2.7
   [I 16:17:05.883 NotebookApp] Serving notebooks from local directory: /home/ucfajlg
   [I 16:17:05.883 NotebookApp] 0 active kernels
   [I 16:17:05.883 NotebookApp] The Jupyter Notebook is running at:
   [I 16:17:05.883 NotebookApp] http://[all ip addresses on your system]:8889/?token=0b856e664152b8fa3a4b6e688945f3e59e490cf5fd0c2f05
   [I 16:17:05.884 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
   [C 16:17:05.884 NotebookApp] 

       Copy/paste this URL into your browser when you connect for the first time,
   to login with a token:
       http://localhost:8889/?token=0b856e664152b8fa3a4b6e688945f3e59e490cf5fd0c2f05

We note that we can connect to the notebook by using port number 8889,
and using this complicated token. For the time being, **just note down
the port number**, 8889. Sometimes, you might get a different port as
this one is already in use. Note the number, and modify the commands
below accordingly.

In order to connect, you can use the following command in your local
remote machine (open a new shall, and it is all in one line, the ``\``
is just a line continuator)

::

   ssh -L 8889:localhost:8889 username@triangle.geog.ucl.ac.uk \
        ssh -L 8889:localhost:8889 -N username@ankara.geog.ucl.ac.uk
        

This should just hang on the shell without much going on. Open your
browser, and visit the URL that we had above, and you should see the
notebook in all its glory!
