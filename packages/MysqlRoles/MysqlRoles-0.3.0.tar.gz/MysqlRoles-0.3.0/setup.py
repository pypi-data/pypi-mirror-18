from distutils.core import setup

setup(name='MysqlRoles',
      version='0.3.0',
      description='Role Based Access Control (RBAC) for mysql',
      author='Ryan Birmingham',
      author_email='birm@rbirm.us',
      url='http://rbirm.us',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Database',
                   'Intended Audience :: Information Technology',
                   'Programming Language :: SQL',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Security',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      long_description=open('README.md', 'r').read(),
      packages=['MysqlRoles'],
      )
