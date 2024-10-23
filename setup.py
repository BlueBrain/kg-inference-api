"""Setup.py file"""

import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

setup(
    name="kg-inference-api",
    author="Blue Brain Project, EPFL",
    description="KG Inference API",
    packages=["api"],
    python_requires=">=3.9",
    install_requires=[
        "fastapi==0.95.0",
        "uvicorn==0.21.1",
        "gunicorn==21.2.0",
        "fastapi-camelcase==1.0.5",
        "pyJWT==2.6.0",
        "pydantic==1.10.6",
        "nexusforge@git+https://github.com/BlueBrain/nexus-forge",
        "knowledge-graph-inference==0.1.4",
        "python-dotenv==1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.2.1",
            "black==23.11.0",
            "pylint==3.0.2",
            ],
    },
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
    ],
)
