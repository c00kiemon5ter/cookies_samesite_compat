from setuptools import setup
from setuptools import find_packages


setup(
    name="cookies_samesite_compat",
    version="0.0.1",
    description="WSGI Middleware to duplicate the configured cookies and remove the SameSite attribute",
    license="Apache 2.0",
    url="https://github.com/c00kiemon5ter/cookies_samesite_compat",
    packages=find_packages("src/"),
    package_dir={"": "src"},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
