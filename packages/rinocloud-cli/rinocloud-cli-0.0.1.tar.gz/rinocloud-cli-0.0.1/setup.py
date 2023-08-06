from setuptools import setup, find_packages
setup(
    name="rinocloud-cli",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description='Rinocloud python bindings',
    author='Eoin Murray',
    author_email='eoin@rinocloud.com',
    url='https://github.com/rinocloud/rinocloud-python',  # use the URL to the github repo
    download_url='https://github.com/rinocloud/rinocloud-python/tarball/0.1',  # I'll explain this in a second
    keywords=['rinocloud', 'data', 'api'],  # arbitrary keywords
    classifiers=[],
    test_suite='rinocloud.test.all',
    tests_require=['mock'],
    install_requires=[
        "rinocloud>=0.0.8",
        "gitpython",
        "keyring",
        "secretstorage",
        "dbus-python",
        "Click"
    ],
    entry_points='''
        [console_scripts]
        rino=rino.cli:cli
    ''',
)
