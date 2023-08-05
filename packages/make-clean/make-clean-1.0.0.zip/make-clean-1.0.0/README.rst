==========
make-clean
==========

If one'd like to make sphinx repository with github-pages sumodule, one shoud
exclude rm ``_build/html/.git``.

``make-clean`` package provide to keep ``.git`` file with it.

Switch ``make.bat`` file clean to below::

  if "%1" == "clean" (
  	.\path\to\make-clean.exe _build --excludes _build\html\.git _build\html\.gitignore
  	goto end
  )

Usage
=====

This package has a `make-clean` command.

.. code-block:: bat

   > .\venv\Scripts\make-clean.exe -h
   usage: make-clean [-h] [-e [EXCLUDE [EXCLUDE ...]]] TARGET_DIR

   clean target dir without excludes

   positional arguments:
     TARGET_DIR            dir to remove recursively

   optional arguments:
     -h, --help            show this help message and exit
     -e [EXCLUDE [EXCLUDE ...]], --excludes [EXCLUDE [EXCLUDE ...]]
                           dir/file to exclude from remove

Test
====

I use `pytest <http://doc.pytest.org/en/latest/>`__.

.. code-block:: bat

   > C:\path\to\python\3.X.Y\python.exe -m venv --clear venv
   > .\venv\Scripts\python.exe setup.py develop easy_install make-clean[test]
   > .\venv\Scripts\python.exe -m pytest
