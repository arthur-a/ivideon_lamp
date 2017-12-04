from setuptools import setup, find_packages


setup(name='ivideon_lamp',
    version='0.1',
    description='ivideon_lamp',
    classifiers=[
        "Programming Language :: Python :: 3.5",
    ],
    author='Arthur',
    author_email='',
    url='',
    packages=find_packages('ivideon_lamp'),
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'lamp_client = ivideon_lamp.lamp_client:main'
        ]
    },
)
