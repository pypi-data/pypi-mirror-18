from setuptools import setup

setup(
    name="admitad",
    packages=['admitad', 'admitad.items'],
    version='1.1.1',
    author='Admitad Dev Bot',
    author_email='dev@admitad.com',
    description='A Python wrapper around the Admitad API',
    license='MIT',
    url='https://github.com/admitad/admitad-python-api',
    download_url='https://github.com/admitad/admitad-python-api/tarball/1.1.1',
    keywords=['admitad'],
    install_requires=['requests>=2.0', 'future'],
    tests_require=['nose2', 'responses'],
    test_suite='nose2.collector.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications',
        'Topic :: Internet',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)
