import os
from setuptools import setup, find_packages
import re

HERE = os.path.abspath(os.path.dirname(__file__))


# Get the long description from the README file.
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(HERE, "../version.py"), encoding="utf-8") as f2:
    version_content = f2.read()
    version_template = "__version__ = '(.*)'\n"
    m = re.match(version_template, version_content)
    fallback_version = m.group(1)

setup(
    name="kg-inference-api",
    author="Blue Brain Project, EPFL",
    use_scm_version={
        "relative_to": __file__,
        "write_to": "../version.py",
        "write_to_template": "__version__ = '{version}'\n",
        "fallback_version": fallback_version,
    },
    description="KG Inference API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="ontology knowledge graph data science inference api",
    packages=["api"],
    # package_dir={"api": "source"},
    python_requires=">=3.8",
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "fastapi==0.95.0",
        "uvicorn==0.21.1",
        "fastapi-camelcase==1.0.5",
        "pytest==7.2.1",
        "pyJWT==2.6.0",
        "pydantic==1.10.6",
        "nexusforge@git+https://github.com/BlueBrain/nexus-forge"
    ],
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
    ]
)
