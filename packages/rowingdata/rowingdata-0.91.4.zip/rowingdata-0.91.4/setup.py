from setuptools import setup, find_packages

import re

def readme():
    with open('README.rst') as f:
	return f.read()

setup(name='rowingdata',

      version=re.search(

	  '^__version__\s*=\s*"(.*)"',
	  open('rowingdata/rowingdata.py').read(),
	  re.M

	  ).group(1),

      description='The rowingdata library to create colorful plots from CrewNerd, Painsled and other rowing data tools',

      long_description=readme(),

      url='http://rowsandall.wordpress.com',

      author='Sander Roosendaal',

      author_email='roosendaalsander@gmail.com',

      license='MIT',

      packages=['rowingdata'],

      keywords = 'rowing ergometer concept2',
      
      install_requires=[
	  'numpy',
	  'scipy',
	  'matplotlib',
	  'pandas',
	  'mechanize',
	  'python-dateutil',
	  'docopt',
	  'tqdm',
	  'rowingphysics>=0.2.3',
	  'iso8601',
	  ],

      zip_safe=False,
      include_package_data=True,
      # relative to the rowingdata directory
      package_data={
	  'testdata':[
	      'crewnerddata.CSV',
	      'crewnerddata.tcx',
	      'example.csv',
	      'painsled_desktop_example.csv',
	      'RP_testdata.csv',
	      'testdata.csv'
	      ],
	  'bin':[
	      'testdata.csv',
	      'crewnerddata.csv',
	      'crewnerddata.tcx'
	      ],
	  'rigging':[
	      '1x.txt',
	      '2x.txt',
	      '4x-.txt',
	      '4-.txt',
	      '4+.txt',
	      '2-.txt',
	      '8+.txt'
	      ]
	  },

      entry_points = {
	  "console_scripts": [
	      'rowingdata = rowingdata.rowingdata:main',
	      'painsledtoc2 = rowingdata.painsledtoc2:main',
	      'painsledplot = rowingdata.painsledplot:main',
	      'crewnerdplot = rowingdata.crewnerdplot:main',
	      'tcxtoc2 = rowingdata.tcxtoc2:main',
#	      'painsled_desktop_plot = rowingdata.painsled_desktop_plot:main',
	      'painsled_desktop_toc2 = rowingdata.painsled_desktop_toc2:main',
	      'painsledplottime = rowingdata.painsledplottime:main',
	      'painsled_desktop_plottime = rowingdata.painsled_desktop_plottime:main',
	      'crewnerdplottime = rowingdata.crewnerdplottime:main',
	      'roweredit = rowingdata.roweredit:main',
	      'copystats = rowingdata.copystats:main',
	      'tcxplot = rowingdata.tcxplot:main',
	      'tcxplottime = rowingdata.tcxplottime:main',
	      'tcxplot_nogeo = rowingdata.tcxplot_nogeo:main',
	      'tcxplottime_nogeo = rowingdata.tcxplottime_nogeo:main',
	      'speedcoachplot = rowingdata.speedcoachplot:main',
	      'speedcoachplottime = rowingdata.speedcoachplottime:main',
	      'speedcoachtoc2 = rowingdata.speedcoachtoc2:main',
	      'rowproplot = rowingdata.rowproplot:main',
	      'ergdataplot = rowingdata.ergdataplot:main',
	      'ergdataplottime = rowingdata.ergdataplottime:main',
	      'ergdatatotcx = rowingdata.ergdatatotcx:main',
	      'ergstickplot = rowingdata.ergstickplot:main',
	      'ergstickplottime = rowingdata.ergstickplottime:main',
	      'ergsticktotcx = rowingdata.ergsticktotcx:main',
	      'windcorrected = rowingdata.windcorrected:main',
	      'boatedit = rowingdata.boatedit:main',
	      'rowproplottime = rowingdata.rowproplottime:main'
	      ]
	  },

      scripts=[
	  'bin/painsledplot2.py',
	  ]

      )
