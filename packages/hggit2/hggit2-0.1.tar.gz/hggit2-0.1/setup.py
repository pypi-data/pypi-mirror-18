try:
      from setuptools import setup
      from setuptools.command.install import install
except:
      from distutils.core import setup
      from distutils.command.install import install

class postinstall(install):
   def run(self):
      install.run(self)
      try:
         from subprocess import check_call,CalledProcessError
         import sys, site
         print("installing HGGIT")
         hggitlocation = site.getsitepackages()[0]
         s = 'python3 ' + hggitlocation +"/hggit2/hggitRun.py"
         check_call(s, shell=True)
      except CalledProcessError as err:
         print("Error occurred while installing hggit",end="")
         print(". Please try again later:",err)
         sys.exit()

setup(
  name = 'hggit2',
  packages = ['hggit2'], # this must be the same as the name above
  version = '0.1',
  description = 'It will install hg-git plugin alongiwth all the required dependencies. Also, since hg-git is implemented in Python2, it will ask the user, do you want it to make Python3 compatible or not?',
  author = 'Vishav Pandhi, Jorge Gonzalez',
  author_email = 'vishavpandhi@gmail.com, jrg13h@my.fsu.edu',
  url = 'https://bitbucket.org/vishav_FSU/fsu_mercurial/branch/default', # use the URL to the github repo
  keywords = ['installing','testing'], # arbitrary keywords
  classifiers = [],
  cmdclass={'install':postinstall}
)
