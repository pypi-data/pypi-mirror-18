from setuptools import setup, find_packages

setup(
    name='kervi-cli',
    version='0.2.0',
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