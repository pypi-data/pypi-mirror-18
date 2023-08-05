from setuptools import setup


with open('README.rst') as f:
    readme = f.read()


setup(name='businessoptics',
      version='0.1.1',
      description='Client for the BusinessOptics API',
      long_description=readme,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
      url='https://github.com/BusinessOptics/businessoptics_client',
      author='BusinessOptics',
      author_email='alex.mojaki@gmail.com',
      license='MIT',
      packages=['businessoptics'],
      install_requires=[
          'requests>=2,<3',
      ],
      include_package_data=True,
      zip_safe=False)
