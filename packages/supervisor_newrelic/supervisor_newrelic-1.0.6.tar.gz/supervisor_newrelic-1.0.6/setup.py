from distutils.core import setup

version = '1.0.6'

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name = 'supervisor_newrelic',
    version = version,
    description = 'Collection of Supervisor plugins to provide metrics and monitoring within New Relic',
    author = 'Sportlobster',
    author_email = 'info@sportlobster.com',
    license = 'MIT',
    url = 'https://github.com/sportlobster/supervisor-newrelic',
    download_url = 'https://github.com/sportlobster/supervisor-newrelic/tarball/%s' % version,
    long_description = readme,
    keywords = ['supervisor', 'supervisord', 'newrelic', 'monitoring'],
    classifiers = [],

    install_requires = ['requests', 'supervisor'],
    tests_require = ['nose', 'mock'],
    test_suite = 'nose.collector',

    packages = ['supervisor_newrelic'],
    include_package_data = True,
    package_data = {
        '': [
            'README.rst',
            'LICENSE.rst',
            'requirements.txt',
        ],
    },
    entry_points = {
        'console_scripts': {
            'supervisor_newrelic_status = supervisor_newrelic.status:main',
        },
    },
)
