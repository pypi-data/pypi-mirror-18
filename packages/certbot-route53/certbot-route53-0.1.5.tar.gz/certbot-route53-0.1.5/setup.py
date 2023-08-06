import sys

from distutils.core import setup
from setuptools import find_packages

version = '0.1.5'

install_requires = [
    'acme>=0.9.0.dev0',
    'certbot>=0.9.0.dev0',
    'PyOpenSSL',
    'pyparsing>=1.5.5',  # Python3 support; perhaps unnecessary?
    'setuptools',  # pkg_resources
    'zope.interface',
    'boto3',
    'dnspython',
]

if sys.version_info < (2, 7):
    install_requires.append('mock<1.1.0')
else:
    install_requires.append('mock')

docs_extras = [
    'Sphinx>=1.0',  # autodoc_member_order = 'bysource', autodoc_default_flags
    'sphinx_rtd_theme',
]

setup(
    name='certbot-route53',
    version=version,
    description="Route53 plugin for certbot",
    url='https://github.com/lifeonmarspt/certbot-route53',
    author="Hugo Peixoto",
    author_email='hugo@lifeonmars.pt',
    license='Apache2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    keywords=['certbot', 'route53', 'aws'],
    entry_points={
        'certbot.plugins': [
            'auth = certbot_route53.authenticator:Authenticator'
        ],
    },
)
