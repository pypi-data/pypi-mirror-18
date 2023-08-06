from setuptools import setup


setup(
    name="goblin",
    version="1.0.0b2",
    url="",
    license="AGPL",
    author="davebshow",
    author_email="davebshow@gmail.com",
    description="Python toolkit for TP3 Gremlin Server",
    packages=["goblin", "goblin.driver", "gremlin_python",
              "gremlin_python.process", "gremlin_python.driver",
              "gremlin_python.structure", "gremlin_python.structure.io",
              "tests"],
    install_requires=[
        "aenum==1.4.5",
        "aiohttp==1.1.5",
        "inflection==0.3.1",
        "PyYAML==3.12"
    ],
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest-asyncio', 'pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3.5",
    ]
)
