saga-config
===========

This module replicates some features from the node.js `config
module <https://www.npmjs.com/package/config>`__.

Currently supports \*.py config files in a config folder in the current
working directory. Other features will be added as they become
necessary.

testing
-------

``docker-compose up`` will automatically test the project and watch for
changes.

To generate html coverage reports run:
``docker-compose run py tox -e html``

To run only the syntax linter run: ``docker-compose run py tox -e lint``

For more advanced testing see the tox.ini file.
