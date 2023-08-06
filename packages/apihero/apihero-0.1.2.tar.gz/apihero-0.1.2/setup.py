from setuptools import setup

readme = open('README.rst').read()
requirements = [
    'mako',
    'mistune',
]
setup(
    name='apihero',
    version='0.1.2',
    description='RESTful JSON API documentation generator tool with live unit test.',
    long_description=readme,
    install_requires=requirements,
    url='http://github.com/meyt/apihero',
    author='Mahdi Ghane.g',
    license='GPLv3',
    keywords='apihero api_documentation api document_generator',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Documentation',
        'Topic :: Documentation',
        'Topic :: Software Development :: Build Tools'
    ],
    packages=['apihero'],
    scripts=['bin/apihero'],
    include_package_data=True,
    zip_safe=False)