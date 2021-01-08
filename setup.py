from codecs import open

import toml
from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

proj = toml.load("pyproject.toml")["mewo_project"]


url = "https://github.com/feluxe/buildlib"


setup(
    name="buildlib",
    version=proj["version"],
    author="Felix Meyer-Wolters",
    author_email="felix@meyerwolters.de",
    maintainer="Felix Meyer-Wolters",
    maintainer_email="felix@meyerwolters.de",
    url=url,
    description="A library to create build and deployment scripts",
    long_description=long_description,
    download_url=url + "/tarball/" + proj["version"],
    license="unlicensed",
    keywords=["build", "lib"],
    include_package_data=True,
    platforms="",
    classifiers=[],
    install_requires=[
        "headlines",
        "prmt>=4.0.1,<5",
        "cmdi>=1.1.1,<2",
        "oyaml",
        "sty",
        "requests",
    ],
    packages=find_packages(where=".", exclude=("tests", "tests.*")),
    package_dir={"buildlib": "buildlib"},
    package_data={},
    data_files=[],
    entry_points={},
    tests_require=[],
)
