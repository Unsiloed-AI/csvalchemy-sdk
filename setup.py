from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="CSVAlchemy_sdk",
    version="0.1.3",
    author="Unsiloed.Ai",
    author_email="hello@unsiloed.ai",
    description="This API provides Excel processing encoding techniqeus to make Excel files LLM ready.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Unsiloed-AI/csvalchemy-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pandas",
        "numpy",
        "openpyxl",
        "sentence-transformers",
        "pathlib",
        "fastapi",
        "uvicorn",
        "python-multipart",
        "psutil",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "zipfile36",
        "gunicorn",
    ],
) 