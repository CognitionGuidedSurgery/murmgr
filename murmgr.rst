======
murmgr
======

----------------------------------------------------------
management of MSML user packages and repositories
----------------------------------------------------------

:Author: Alexander Weigl <alexander.weigl@student.kit.edu>
:Date:   2015-01-03
:Copyright: gplv3
:Version: 1.0.0-betals
:Manual section: 1
:Manual group: MSML tools

SYNOPSIS
========

murmgr.py [OPTIONS] COMMAND [ARGS]...



DESCRIPTION
===========

murmgr offers various commands for the management of MSML user packages and repositories.
MSML_ is a workflow tool for biomechanical engineering.

:User Package:
    A user package is anthology of operators. It provides the necessary alphabet files,
    the code for operators (python) or executables.

:User Repository: Multiple packages can be packed together.



GLOBAL OPTIONS
==============

  -v, --verbose                   more informations
  -r, --repository PATH           give a path to an repository
  -y, --always-yes / --always-no  do not ask for confirmation, use default value instead
  --help                          Show help message and exit.


COMMANDS
========

  :activate_package:
    activate a package in a repository
  :deactivate_package:
    deactivate a package in a repository
  :download_package:
    download and install a package via git
  :new_package:
    creates a new user package.
  :new_repository:
    creates a new repository
  :show:
    shows the cumulative repository configuration
  :update_repository:
    update every package in a repository


activate_package
----------------


RETURN CODES
============

    :1: No repository

PROBLEMS
========

1. No known problems.

SEE ALSO
========

* `MSML <http://github.com/CoginitionGuidedSurgery/msml>`_
* `man 1 git`

BUGS
====



