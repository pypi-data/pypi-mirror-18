from setuptools import setup, find_packages

setup(
    name="s3go",
    version="0.1",
    description="upload local folder to s3 bucket",
    url="https://github.com/flyfj/s3deploy",
    author="Jie Feng",
    author_email="jiefengdev@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["boto3", "tqdm"])
