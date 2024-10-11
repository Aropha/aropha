from setuptools import find_namespace_packages, setup

__version__ = "1.0.0"

# Load README
with open('README.md', encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = 'aropha',
    version = '1.0.0',
    author = 'Sadjad Fakouri Baygi',
    author_email = 'sadjad.fakouri@aropha.com',
    description = 'Process aropha data',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com//aropha',
    project_urls = {
        'Source': 'https://github.com/aropha'
    },
    license = 'Copyright (c) 2024  Inc., all rights reserved.',
    packages = find_namespace_packages(include=['aropha', 'aropha.*']),
    include_package_data = False,
    install_requires = [
        'requests', 'bcrypt'
    ],
    python_requires = '>=3.8',
    classifiers = [
        'Programming Language :: Python :: 3.8',
        'License :: CC BY-ND'
    ],
    keywords = [
        'Cheminformatics',
        'Biodegradation',
        'Polymer',
        'SMILES'
    ]
)