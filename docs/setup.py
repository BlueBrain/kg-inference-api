import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


setup(
    name="kg-inference-docs",
    author="Blue Brain Project, EPFL",
    use_scm_version={
        "relative_to": __file__,
        "write_to": "version.py",
        "write_to_template": "__version__ = '{version}'\n",
    },
    description="KG Inference Docs",
    keywords="ontology knowledge graph data science inference api",
    packages=find_packages(),
    python_requires=">=3.8",
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "sphinx==7.0.1",
        "sphinx-bluebrain-theme==0.4.1"
    ],
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
    ]
)
