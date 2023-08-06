#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-pip-tools',
        version = '1.0.0',
        description = '''PyBuilder plugin to generate and install requirements.txt files from project (build) dependencies''',
        long_description = '''PyBuilder Pip Tools is a PyBuilder plugin which generates
``*requirements*.txt`` files from your project (build) dependencies and keeps
your virtual env in sync with them. This is achieved with `pip-compile` and
`pip-sync` from `pip-tools`_.

.. _pip-tools: https://github.com/nvie/pip-tools

Links
=====

- `Documentation <http://pythonhosted.org/pybuilder-pip-tools/>`_
- `PyPI <https://pypi.python.org/pypi/pybuilder-pip-tools/>`_
- `GitHub <https://github.com/timdiels/pybuilder-pip-tools>`_

Interface stability
===================
While all features are documented (docstrings only) and tested, the API is
changed frequently.  When doing so, the `major version <semver_>`_ is bumped
and a changelog is kept to help upgrade. Fixes will not be backported. It is
recommended to pin the major version in your build.py, e.g. for 1.x.y::

    use_plugin('pypi:pybuilder_pip_tools', '>=1.0.0,<2.0.0')

Changelog
=========

`Semantic versioning <semver_>`_ is used.

v1.0.0
------
Initial release.

.. _semver: http://semver.org/spec/v2.0.0.html
''',
        author = "VIB/BEG/UGent, Tim Diels",
        author_email = "info@psb.ugent.be, timdiels.m@gmail.com",
        license = 'LGPLv3',
        url = 'https://github.com/timdiels/pybuilder_pip_tools',
        scripts = [],
        packages = ['pybuilder_pip_tools'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Build Tools'
        ],
        entry_points = {
            'console_scripts': []
        },
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
        keywords='pybuilder plugin pip-tools requirements.txt',
    )
