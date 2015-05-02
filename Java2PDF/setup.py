'''
Created on 01.05.2015

@author: mhild
'''

import os
from setuptools import setup
import subprocess
import re

print("checking for wkhtmltopdf")
print("installing wkhtmltopdf (you are prompted for the sudo-password)")
os.system("sudo gem install wkhtmltopdf-binary-edge")    
# ret = subprocess.call(["which","wkhtmltopdf"])
# if ret == 0:
#     print("wkhtmltopdf  found, checking version")
#     # is installed
#     # check versio
#     ret = subprocess.check_output(["which","wkhtmltopdf"])
#     wkhtmltopdf = ret
#     
#     versionRaw = subprocess.check_output([ "wkhtmltopdf" ,"-V"])
#     matchObj = re.match(r'([0-9\.]+\.){3}', versionRaw)
#     
#     if matchObj:
#         version = matchObj.group(1)
#         print("wkhtmltopdf version found: "+version)
#         # version check
#         matchObj2 = re.match(r'([0-9]+)\.([0-9]+)\.([0-9]+)(?:\.[0-9]+)', version)
#         if matchObj2:
#             if int(matchObj2.group(1))==0 and int(matchObj2.group(2))<=12 and int(matchObj2.group(3))<=2:
#                 print("correct version of wkhtmltopdf installed")
#             else:
#                 print("installing wkhtmltopdf (you are prompted for the sudo-password)")
#                 os.system("sudo gem install wkhtmltopdf-binary-edge") # -v 0.12.2.1")
# else:
#     print("installing wkhtmltopdf (you are prompted for the sudo-password)")
#     os.system("sudo gem install wkhtmltopdf-binary-edge")          


setup(name='Java2PDF',
      version='0.1',
      description='Java2PDF',
      url='http://github.com/mhild/Java2PDF',
      author='mhild',
      license='GPL',
      install_requires=[
                        'pdfkit',
      ],
      zip_safe=False)