from setuptools import setup, find_packages
setup(
    name="rino",
    version="0.0.5",
    packages=find_packages(),
    include_package_data=True,
    description='Rinocloud CLI tool',
    author='Eoin Murray',
    author_email='eoin@rinocloud.com',
    install_requires=[
        "rinocloud>=0.0.8",
        "gitpython",
        "keyring",
        "Click"
    ],
    entry_points='''
        [console_scripts]
        rino=rino.cli:cli
    ''',
)
