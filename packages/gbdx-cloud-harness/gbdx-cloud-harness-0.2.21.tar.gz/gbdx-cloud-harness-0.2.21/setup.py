from setuptools import setup, find_packages


setup(
    name='gbdx-cloud-harness',
    version='0.2.21',
    packages=find_packages(exclude=['docs', 'examples', 'docker_runner']),
    include_package_data=True,
    install_requires=[
        'boto3>=1.3.0',
        'docopt>=0.6.2',
        'jsonschema==2.4.0',
        'future>=0.15.2',
        'gbdx-auth>=0.2.0'
    ],
    url='https://github.com/TDG-Platform/cloud-harness',
    license='MIT',
    description='GBDX Cloud Harness',
    long_description=open('README.rst').read(),
    author='GBDX (Michael Connor)',
    author_email='mike@sparkgeo.com',
    entry_points={
        'console_scripts': ['cloud-harness=gbdx_cloud_harness.controller:main'],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    tests_require=['pytest', 'vcrpy', 'moto', 'coverage']
)
