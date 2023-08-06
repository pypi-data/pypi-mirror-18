from setuptools import setup

def readme():
  with open("README.rst") as f:
    return f.read()
setup(name='hng',
      version='0.2',
      description='Python package for open-source healthcare machine learning @hngml',
      long_description = readme(),
      classifiers=['Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      url='https://bitbucket.org/HNGML/hng',
      author='hngml',
      author_email='nilesh.chaudhari@healthnextgen.com',
      license='MIT',
      packages=['hng'],
      install_requires=[
          'markdown',
      ],
      scripts=['bin/hng'],#write a separate script file for a command line call
      #entry_points = {'console_scripts':['test-me-again=test_package.terminal_functions:main'],},
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)