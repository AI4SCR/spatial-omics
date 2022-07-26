"""Install package."""
import io
import re

from pkg_resources import parse_requirements
from setuptools import find_packages, setup


def read_version(filepath: str) -> str:
    """Read the __version__ variable from the file.

    Args:
        filepath: probably the path to the root __init__.py

    Returns:
        the version
    """
    match = re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        io.open(filepath, encoding="utf_8_sig").read(),
    )
    if match is None:
        raise SystemExit("Version number not found.")
    return match.group(1)


# ease installation during development
vcs = re.compile(r"(git|svn|hg|bzr)\+")
try:
    with open("requirements.txt") as fp:
        VCS_REQUIREMENTS = [
            str(requirement)
            for requirement in parse_requirements(fp)
            if vcs.search(str(requirement))
        ]
except FileNotFoundError:
    # requires verbose flags to show
    print("requirements.txt not found.")
    VCS_REQUIREMENTS = []

setup(
    name="ai4scr-spatial-omics",
    version=read_version("spatialOmics/__init__.py"),  # single place for version
    description="Installable spatialOmics package",
    long_description="todo",
    long_description_content_type='text/markdown',
    url="https://github.com/AI4SCR/spatial-omics",
    author="Adriano Martinelli",
    author_email="art@zurich.ibm.com",
    # the following exclusion is to prevent shipping of tests.
    # if you do include them, add pytest to the required packages.
    packages=find_packages(".", exclude=["*tests*"]),
    package_data={"spatialOmics": ["py.typed"]},
    extras_require={
        "vcs": VCS_REQUIREMENTS,
        "test": ["pytest", "pytest-cov"],
        "dev": [
            # tests
            "pytest",
            "pytest-cov",
            # checks
            "black==21.5b0",
            "flake8",
            "mypy",
            # docs
            "sphinx",
            "sphinx-autodoc-typehints",
            "better-apidoc",
            "six",
            "sphinx_rtd_theme",
            "myst-parser",
        ],
    },
    # versions should be very loose here, just exclude unsuitable versions
    # because your dependencies also have dependencies and so on ...
    # being too strict here will make dependency resolution harder
    install_requires=[
        'numpy>=1.22',
        'pandas>=1.2',
        'scikit-image>=0.19.2',
        'seaborn>=0.11.2',
        'tqdm>=4.64.0',
        'h5py>=3.6.0',
        'tables>=3.7.0',
        'scikit-learn>=1.0.2'
    ]
)
