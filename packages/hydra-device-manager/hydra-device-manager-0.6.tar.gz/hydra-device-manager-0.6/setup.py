from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='hydra-device-manager',
      version='0.6',
      description='The funniest joke in the world',
      long_description=readme(),
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://github.com/lordoftheflies/hydra-device-manager',
      author='lordoftheflies',
      author_email='heglas11@gmail.com',
      license='MIT',
      packages=['devicemanager'],
      install_requires=[
            'pyvisa',
      ],
      entry_points = {
          'console_scripts': [
              'devicemanager-joke=devicemanager.main:main'
          ]
      },
      zip_safe=False)

