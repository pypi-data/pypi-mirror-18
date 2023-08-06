import ast
from setuptools import find_packages, setup


install_requires = ['MarkupSafe >= 0.23']
tests_require = [
    'pytest >= 2.7.0',
    'pytest-xdist',
    'tox',
]
dev_require = [
    'import-order',
    'flake8',
]


def readme():
    with open('README.rst') as f:
        try:
            return f.read()
        except (IOError, OSError):
            return None


def get_version():
    filename = 'linkfy/__init__.py'
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
        for node in tree.body:
            if (isinstance(node, ast.Assign) and
                    node.targets[0].id == '__version_info__'):
                version = '.'.join(
                    str(x) for x in ast.literal_eval(node.value)
                )
                return version
        else:
            raise ValueError('could not find __version_info__')


setup(
    name='linkfy',
    version=get_version(),
    packages=find_packages(),
    url='https://github.com/admire93/linky',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'tests': tests_require,
        'dev': dev_require,
    },
    maintainer='Kang Hyojun',
    maintainer_email='iam.kanghyojun' '@' 'gmail.com',
    description='Change plain text into HTML.',
    long_description=readme(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ]
)
