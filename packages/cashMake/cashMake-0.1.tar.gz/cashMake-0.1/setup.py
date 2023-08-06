from setuptools import setup, find_packages

setup(name='cashMake',
      version='0.1',
      url='https://www.baidu.com',
      license='GPL',
      author='Zrush Zhang',
      author_email='mrzhzr2004@sina.com',
      description='Manage configuration files',
      packages=find_packages(exclude=['tests', 'migrations']),
      package_data={'requirements': ['*.txt']},
      long_description=open('README.md').read(),
      zip_safe=False)
