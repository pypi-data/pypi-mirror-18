from distutils.core import setup
setup(
  name = 'solar-correlation-map',
  packages = ['solar-correlation-map'],
  version = '0.1',
  description = 'A new way to visualize correlations.',
  author = 'Stefan Zapf & Christopher Kraushaar',
  author_email = 'daebwae@gmail.com',
  url = 'https://github.com/Zapf-Consulting/solar-correlation-map', 
  download_url = 'https://github.com/Zapf-Consulting/solar-correlation-map/tarball/0.01', 
  keywords = ['EDA', 'correlation', 'plot', 'data analysis'],
  classifiers = [],
  install_requires=['matplotlib', 'numpy']
)