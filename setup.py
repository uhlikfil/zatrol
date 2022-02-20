from setuptools import find_packages, setup


def get_version():
    return "1.0.1"


def get_reqs():
    with open("requirements.txt") as f:
        return [req for req in f.readlines() if not req.startswith("-")]


setup(
    name="zatrol",
    description="zatrol app",
    author="Filip Uhlík",
    author_email="filipfilauhlik@gmail.com",
    url="https://github.com/uhlikfil/zatrol",
    version=get_version(),
    packages=find_packages(),
    install_requires=get_reqs(),
)
