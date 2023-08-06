from setuptools import setup, find_packages

__version__ = '0.0.2'


setup(name='wobble',
      version=__version__,
      description='wobble: Deployment utility for DCOS+Marathon managed '
                  'clusters',
      author='Matt Rasband',
      author_email='matt.rasband@gmail.com',
      license='Apache-2.0',
      # url='https://github.com/nextgearcapital/wobble',
      packages=find_packages(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Software Development',
          'Topic :: System :: Software Distribution',
          'Topic :: Utilities',
      ],
      setup_requires=[
          'pytest-runner',
      ],
      install_requires=[
          'requests>=2.0.0,<3.0.0',
      ],
      tests_require=[
          'pytest',
          'pytest-cov',
      ],
      entry_points={
        'console_scripts': [
            'wobble=wobble.__main__:main',
        ],
      },
      zip_safe=False)
