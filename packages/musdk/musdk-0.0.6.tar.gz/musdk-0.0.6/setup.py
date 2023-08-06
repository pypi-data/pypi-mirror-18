from setuptools import setup

install_requires = [
    "requests >= 2.5.0",
    "requests-toolbelt >= 0.5.1",
    "setuptools >= 0.7.0",
    "simplejson >= 3.1.0",
]

packages = [
    'musdk',
]

setup(
    name="musdk",
    version="0.0.6",
    license='MIT',
    description="ss-panel mu api sdk for python",
    author='orvice',
    author_email='orvice@orx.me',
    url='https://github.com/orvice/mu-py-sdk',
    package_data={
        'mu=sdk': ['README.md', 'LICENSE']
    },
    packages=packages,
    install_requires=install_requires,
    long_description="",
    classifiers=[
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
