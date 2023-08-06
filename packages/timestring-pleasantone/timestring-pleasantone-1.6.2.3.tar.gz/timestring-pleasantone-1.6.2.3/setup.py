import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as stream:
    long_description = stream.read()

with open(os.path.join(here, "timestring/version.py")) as stream:
    exec(stream.read())

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: PyPy"
]

setup(
    name="timestring-pleasantone",
    version=__version__,
    description="Natural language date and date-range parsing (fork stevepeak)",
    long_description=long_description,
    classifiers=classifiers,
    keywords="date time range datetime datestring",
    author="@stevepeak, @paul_traina",
    author_email="steve@stevepeak.net, bulk+github@pst.org",
    url="http://github.com/pleasantone/timestring",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=["timestring"],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "timestring=timestring:main"
        ]
    },
    install_requires=[
        "pytz>=2015.2",
    ],
    tests_require=[
        "nose",
        "rednose",
        "nose-cov",
        "codecov",
        "ddt",
        "six",
    ],
    test_suite="nose.collector",
)
