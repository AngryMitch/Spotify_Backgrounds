from setuptools import setup, find_packages

setup(
    name='spotify_backgrounds',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pillow>=10.4.0',
    ],
    include_package_data=True,
    python_requires='>=3.6',
)
