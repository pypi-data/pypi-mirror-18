from setuptools import setup
from dlogr import __version__

BASE_CVS_URL = 'http://github.com/filwaitman/dlogr'

setup(
    name='dlogr',
    packages=['dlogr', ],
    version=__version__,
    author='Filipe Waitman',
    author_email='filwaitman@gmail.com',
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    url=BASE_CVS_URL,
    download_url='{}/tarball/{}'.format(BASE_CVS_URL, __version__),
    test_suite='tests',
    tests_require=[x.strip() for x in open('requirements_test.txt').readlines()],
    package_data={'dlogr': ['gd_bundle-g2-g1.crt']},
    include_package_data=True,
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
