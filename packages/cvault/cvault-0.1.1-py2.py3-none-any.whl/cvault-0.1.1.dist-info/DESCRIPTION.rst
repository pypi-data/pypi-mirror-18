Cvault: Credential Vault
========================

Credential Vault (cvault) is a place where you can save your memory about credentials, e.g. account and password, along with some helpful description.


Installation
------------

Run the installer script to install dependencies and the cvault program.

.. code-block:: bash

    $ ./install.sh

Then initialize the vault (database).

.. code-block:: bash

    $ cvault init </path/to/vault>


Usage
-----

There are two modes in cvault:

1. interactive mode: cvault will open up a dialog, and you can interact with it
2. non-interactive mode: saves entry with one shot, no more dialog

**Interactive Mode**

.. code-block:: bash

    $ cvault

And follow the instructions to achieve the goal.

**Non-interactive Mode**

.. code-block:: bash

    $ cvault save <account> <password> <description> # save a new entry
    $ cvault remove <id> # remove certain entry
    $ cvault list [-v] # list all the entries reside in the vault
    $ cvault show <id> # show the exact entry


