""" SetUp file """
from setuptools import setup, find_packages
from os import path

base = path.abspath(path.dirname(__file__))

# Gets the long description from the README file
long_description = ''
if path.exists('README.md'):
    with open(path.join(base, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()



setup(
    name="treblle-dynasty",
    version="1.0.0",
    long_description=long_description,
    packages=find_packages(),
    install_requires= [
        "annotated-types==0.6.0",
        "certifi==2023.7.22",
        "requests>=2.31.0",
        "fastapi>=0.103.2",
        "anyio==3.7.1",
        "pydantic>=1.8.2",
        "starlette>=0.27.0",
        "sniffio==1.3.0",
        "python-dotenv==1.0.0",
        "urllib3==2.0.6",
        "typing_extensions==4.8.0",
        "pydantic_core==2.10.1",
        "charset-normalizer==3.3.0",
        "exceptiongroup==1.1.3",
        "idna==3.4",
        "pymongo==4.5.0",
    ],
    include_package_data=True,
    zip_safe=False,
    author="Dev-Dynasty",
    author_email="mcdonaldamure@gmail.com",
    description="Treblle Python-FastAPI SDK",
    license="MIT",
    keywords="treblle python fastapi sdk api logging monitoring error-tracking performance",
)
