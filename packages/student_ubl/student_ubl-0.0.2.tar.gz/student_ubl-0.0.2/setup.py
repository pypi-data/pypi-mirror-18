from setuptools import setup


def readme():
    with open('READMES.rst') as f:
        return f.read()

setup(name='student_ubl',
      version='0.0.2',
      description='Simple API for accessing data student budiluhur site',
      long_description=readme(),
      url='https://github.com/yanwarsolah/student-ubl',
      author='Yanwar Solahudin',
      author_email='yanwarsolah@gmail.com',
      license='MIT',
      packages=['student_ubl'],
      install_requires=[
          'beautifulsoup4==4.5.1',
          'requests==2.12.3'
      ],
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
      ],
      include_package_data=True,
      zip_safe=False)