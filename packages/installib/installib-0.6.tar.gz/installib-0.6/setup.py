from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = []

REQUIRES = ["pypiwin32==219"]


setup(
    name='installib',
    version='0.6',
    description='Install helper library',
    author='Ivan Martin',
    author_email='ivanprjcts@gmail.com',
    url='https://github.com/ivanprjcts/installib',
    install_requires=REQUIRES,
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    zip_safe=False,
)
