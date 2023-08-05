#!/usr/bin/env python3
import setuptools
setuptools.setup(
    name = 'docker-network-capture',
    version = open('VERSION').read(),
    scripts = ['docker-network-capture'],
    packages = setuptools.find_packages(),
    install_requires = ['docker-py==1.9.0', 'pypcapfile==0.12.0'],
    package_data = {
	    '': ['LICENSE', 'README.md', 'VERSION']
    },
    author = 'Pavel Odvody',
    author_email = 'podvody@redhat.com',
    description = 'Thin wrapper around Docker and tcpdump to get traffic coming from/to a container',
    license = 'GNU/GPLv2',
    keywords = 'docker cli network traffic capture',
    url = 'https://github.com/shaded-enmity/docker-network-capture',
    classifiers=[
        "Programming Language :: Python :: 3 :: Only"
    ]
)
