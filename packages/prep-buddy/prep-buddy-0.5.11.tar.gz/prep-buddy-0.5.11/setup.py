from setuptools import setup, find_packages

version_string = '0.5.0'
JAR_FILE = 'prep-buddy-' + version_string + '-jar-with-dependencies.jar'

setup(
    name='prep-buddy',
    description='A library for cleaning, transforming and executing all other preparation tasks for large datasets on Apache Spark',
    author='data-commons',
    author_email='data-commons-toolchain@googlegroups.com',
    url='https://github.com/data-commons/prep-buddy',
    version=version_string+'11',
    packages=find_packages(),
    license="Apache 2.0",
    include_package_data=True,
    classifiers=[],
    keywords=['spark', 'cleaning', 'transforming', 'data', 'preparation'],
    install_requires=[
        'numpy >= 1.9.2'
    ],
    test_requires=[
        'nose == 1.3.7'
    ]
)
