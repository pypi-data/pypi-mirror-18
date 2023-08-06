from setuptools import setup, find_packages

__author__ = 'netanelrevah'

main_namespace = {}
with open('nicer/version.py') as version_file:
    exec(version_file.read(), main_namespace)
version = main_namespace['__version__']

REQUIREMENTS = []

setup(
    name='nicer',
    version=version,
    packages=find_packages(),

    install_requires=REQUIREMENTS,

    author='netanelrevah',
    author_email='netanelrevah@users.noreply.github.com',
    description='Nicer: Utils package',
    license='GNU General Public License, version 2',
    keywords="utils nicer",
    url='https://github.com/netanelrevah/nicer'
)
