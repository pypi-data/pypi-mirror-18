from setuptools import setup, find_packages

__author__ = 'netanelrevah'

main_namespace = {}
with open('pkt/version.py') as version_file:
    exec(version_file.read(), main_namespace)
version = main_namespace['__version__']

REQUIREMENTS = ['typing', 'nicer']


setup(
    name='pkt',
    version=version,
    packages=find_packages(),

    install_requires=REQUIREMENTS,

    author='netanelrevah',
    author_email='netanelrevah@outlook.com',
    description='Pkt: Abstract network package',
    license='GNU General Public License, version 2',
    keywords="network packet pkt",
    url='https://github.com/netanelrevah/pkt'
)
