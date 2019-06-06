from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(), # tells Python what directories to include automagically
    include_package_data=True, # include other files ie. static and template directories
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)