KernelUpgrader
==============

A Python tool for upgrade your kernel safely from https://kernel.org

.. image :: https://img.shields.io/badge/v1.18.4%20-PyPi-green.svg
         :target: https://pypi.org/project/KernelUpgrader/
         :alt: PyPi
.. image :: https://img.shields.io/badge/Package%20-Zip-green.svg
         :target: https://github.com/Javinator9889/KernelUpgrader/archive/master.zip
         :alt: ZIP
.. image :: https://img.shields.io/badge/Package%20-Git-green.svg
         :target: https://github.com/Javinator9889/KernelUpgrader.git
         :alt: Git

How it works?
-------------

First of all, I designed this tool for *speed-up* kernel installation
process, as the user has to perform a lot of commands and be careful
(the process can crash your system if any step is not correctly
completed).

So for this reason, I decided to **implement** a
*`Python`* version of this process. The idea
is simple: *download, compile and install a new kernel (if available)
without user interaction, but showing warnings and errors*.

Basically, this program has three blocks:

1. **Kernel downloading and decompression**: the program will look for a
   newer stable version of the kernel at https://kernel.org. If there is
   a newer one, it will *download* and *decompress* it (if there is
   enough space available).
2. **Kernel configuration and compilation**: once the kernel is
   decompressed, this application will look for the *actual boot
   config*, copy it to the new kernel location and *adapt it* to the new
   configuration available at the new version. Then, **this app will
   start compiling kernel**.
3. **Kernel installation**: after all the compiling process, now it is
   the easiest part: *installing the new kernel*. For this, the
   application will use ``dpkg`` in order to adapt and install required
   dependencies for the new kernel.

If you want to know *what commands* is the program using, you can find
them at ``Constants.py`` file.

How to install
--------------

You have some alternatives to install this application (*both requires
admin access - '#'' means admin access granted*):

-  Using ``pip``. For that purpose, just run in your terminal:

   .. code:: bash

       pip install KernelUpgrader # It is important to use "pip" from Python 3

   To use *Python 3 PIP*, you must install ``pip3``:

   .. code:: bash

       apt-get install pip3 # Assuming that you have Python 3 installed
       ### PYTHON 3 NOT INSTALLED ##
       apt-get install python3

   If you find that ``pip`` installs dependencies in *Python 2*, in most
   cases the following syntax works:

   .. code:: bash

       python3 -m pip install KernelUpgrader

-  Using the ``setup.py`` file: First, you have to *obtain* the
   correspondent version. You can get it via ``wget`` or using ``git``
   (as shown below):

   .. code:: bash

       apt-get install wget unzip # If "wget" and "unzip" is not installed
       wget https://github.com/Javinator9889/KernelUpgrader/archive/master.zip
       unzip master.zip
       cd KernelUpgrader-master/

   .. code:: bash

       apt-get install git # If "git" is not installed
       git clone https://github.com/Javinator9889/KernelUpgrader.git
       cd KernelUpgrader

   Now, for *both processes*, we just need to run:

   .. code:: bash

       python3 setup.py install # We are using "python3" as "python" means "Python 2"

How to update?
--------------

In order to update to a newer version of *KernelUpgrader*, we must do:

.. code:: bash

    # If installed via "pip"
    pip install -U KernelUpgrader
    # If the above one not works
    python3 -m pip install -U KernelUpgrader

.. code:: bash

    # If installed via "wget" or "git"
    # We must follow the steps in "How to install" until the "cd" command and then run:
    python3 setup.py install # This automatically updates the application

I found an error or I want to contribute
----------------------------------------

I would *love* to see how my application grows up, so feel free to
create your **own version** of this app. Just *fork it* and make all the
changes you want 😄

Also if you want to *add a new functionality* or *solve a bug*, you are
free to open a **pull request** so I can merge the changes you have
done.

How can I help?
---------------

-  Feel free to *follow me at GitHub* 👥: I create a lot of projects and
   maybe you find someone interesting.
-  *Start* ⭐ this project if you find it helpful 😄
-  *Share it* with the people you think they will find interesting my
   job 🗣

License
-------

This project is under *GNU General Public License v3.0*. You can read
all **permissions**, **limitations** and **conditions** by `clicking
here <https://github.com/Javinator9889/KernelUpgrader/blob/master/LICENSE>`__
