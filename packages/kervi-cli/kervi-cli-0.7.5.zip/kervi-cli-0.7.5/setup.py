import distutils
from setuptools import setup
from kervi_cli.version import VERSION

try:
    distutils.dir_util.remove_tree("dist")
except:
    pass

setup(
    name='kervi-cli',
    version=VERSION,
    packages=["kervi_cli", "kervi_cli/scripts"],
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        kervi=kervi_cli.scripts.kervi:cli
    ''',
)