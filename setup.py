"""Simple package setup for the Tourism AI teaching project.

Install from the repository root with: python -m pip install -e .
Start the API with: python -m Service.main
"""
from setuptools import find_namespace_packages, setup


setup(
    name="tourism-ai-service",
    version="1.0.0",
    description="Educational tourism AI microservice using Qwen and FastAPI",
    python_requires=">=3.10,<3.13",
    packages=find_namespace_packages(include=["Service", "Service.*"]),
    package_data={"Service": ["config.json"]},
    include_package_data=True,
    install_requires=[
        "fastapi>=0.115,<1",
        "uvicorn>=0.34,<1",
        "pydantic>=2,<3",
        "python-multipart>=0.0.20",
        "langchain-core>=0.3,<1",
        "langchain-ollama>=0.3,<1",
        "ollama>=0.4,<1",
        "funasr>=1.2,<2",
        "numpy",
        "soundfile",
        "librosa",
        "pyttsx3",
        "opencv-python",
        "requests",
    ],
)
