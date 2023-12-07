import os
from setuptools import setup
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
    name="kg-inference-frontend",
    author="Blue Brain Project, EPFL",
    use_scm_version={
        "relative_to": __file__,
        "write_to": "../version.py",
        "write_to_template": "__version__ = '{version}'\n",
        "fallback_version": fallback_version,
    },
    description="KG Inference Frontend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="ontology knowledge graph data science inference ui",
    packages=['frontend'],
    # package_dir={"frontend": "source"},
    python_requires=">=3.8",
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "dash==2.9",
        "dash-bootstrap-components==1.4.0",
        "jsonpath-rw==1.4.0",
        "requests>=2.28.2",
        "neurom==3.2.2",
        "gunicorn==20.1.0",
        "scikit-learn==1.2.2",
        "plotly==5.14.1",
        "pandas==2.0.0",
        "numpy==1.24.2",
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
