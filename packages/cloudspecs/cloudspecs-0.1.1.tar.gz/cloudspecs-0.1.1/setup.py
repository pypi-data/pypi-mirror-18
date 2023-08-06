from setuptools import setup, find_packages
import os


def load_data_files(directory='data'):
    return [(root, [os.path.join(root, f) for f in files])
            for root, dirs, files in os.walk(directory)]

setup(
    name='cloudspecs',
    version='0.1.1',
    author='Mihir Singh (@citruspi)',
    author_email='hello@mihirsingh.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    data_files=load_data_files()
)
