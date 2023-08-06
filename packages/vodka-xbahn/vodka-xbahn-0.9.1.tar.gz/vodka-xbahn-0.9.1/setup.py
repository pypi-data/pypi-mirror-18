
from setuptools import find_packages, setup


version = open('facsimile/VERSION').read().strip()
requirements = open('facsimile/requirements.txt').read().split("\n")
test_requirements = open('facsimile/requirements-test.txt').read().split("\n")


setup(
    name='vodka-xbahn',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='xbahn plugin for vodka',
    long_description='',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: Apache Software License',
    ],
    packages = find_packages(),
    include_package_data=True,
    url='https://github.com/20c/vodka-xbahn',
    download_url='https://github.com/20c/vodka-xbahn/%s' % version,
    install_requires=requirements,
    test_requires=test_requirements,
    entry_points={
        'vodka.extend':["xbahn_plugin=vodka_xbahn.plugin"]
    },
    zip_safe=True
)
