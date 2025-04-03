from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="csvalchemy_sdk",
    version="0.1.1",
    author="Unsiloed.Ai",
    author_email="hello@unsiloed.ai",
    description="This API provides integration with OpenAI's LLM services alongside Excel processing capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Unsiloed-AI/spreadsheet-llm",
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
        "openai",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "zipfile36",
        "gunicorn",
    ],
) 