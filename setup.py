from setuptools import setup, find_packages

setup(
    name='runescape_helper',
    version='0.1.0',
    packages=find_packages(),
    author='SilentDevCoPro',
    description='A helper application for Runescape 3, compatible with Silicon Mac computers.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SilentDevCoPro/rs3helper',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
)
