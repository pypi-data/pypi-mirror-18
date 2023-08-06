from setuptools import setup, find_packages

setup(
    name="labellio_cli2",
    version="0.0.5",
    url="https://github.com/kccsairc/labellio_cli",
    description="Labellio command line interface",
    author="AlpacaDB, Inc.",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='deep learning caffe labellio kccs kyocera',
    packages=find_packages(),
    install_requires=['numpy', 'scikit-image', 'protobuf'],
    scripts=['bin/labellio_classify'],
)
