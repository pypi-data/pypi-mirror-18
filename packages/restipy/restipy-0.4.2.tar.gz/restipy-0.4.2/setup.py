from setuptools import setup, find_packages

setup(
    version='0.4.2',
    name='restipy',
    description=
        '''
            This CLI tool basically uses Jinja2 and the requests
            library to build dynamic requests based on a template
        ''',
    author='Phil Hachey',
    author_email='phil.hachey@bluespurs.com',
    keywords=['rest', 'requests', 'jinja2', 'jmespath', 'template', 'request'],
    license='MIT',
    package_dir={ '': 'lib' },
    packages=find_packages('lib'),
    install_requires=[
        'requests >= 2.11',
        'pyyaml >= 3.12',
        'jinja2 >= 2.8',
        'jmespath >= 0.9.0',
        'python-jose >= 1.3.2'
    ],
    scripts=[
        'bin/restipy'
    ],
    entry_points={
        'restipy.plugins.jinja2.globals': [
            'jwt = restipy.plugins.jinja2.globals:jwt',
            'time = restipy.plugins.jinja2.globals:time',
            'yaml = restipy.plugins.jinja2.globals:yaml',
            'json = restipy.plugins.jinja2.globals:json',
            'jmespath = restipy.plugins.jinja2.globals:jmespath'
        ],
        'restipy.plugins.jinja2.filters': [
            'jmespath = restipy.plugins.jinja2.filters:jmespath',
            'json = restipy.plugins.jinja2.filters:json',
            'yaml = restipy.plugins.jinja2.filters:yaml',
            'from_json = restipy.plugins.jinja2.filters:from_json',
            'from_yaml = restipy.plugins.jinja2.filters:from_yaml'
        ],
        'restipy.plugins.modules': [
            'requests = restipy.plugins.modules:RequestsModule',
            'store = restipy.plugins.modules:StoreModule',
            'print = restipy.plugins.modules:JsonPrinterModule'
        ]
    }
)
