'''
Created on 01.05.2015

@author: mhild
'''

import os
from setuptools import setup
import subprocess
import re

print("checking wkhtmltopdf")
ret = subprocess.call(["which","wkhtmltopdf"])
if ret == 0:
    # is installed
    # check versio
    ret = subprocess.check_output(["which","wkhtmltopdf"])
    wkhtmltopdf = ret
    
    versionRaw = subprocess.check_output([ "wkhtmltopdf" ,"-V"])
    matchObj = re.match(r'Name:[\n\r]\s+wkhtmltopdf\s([0-9\.]+)', versionRaw)
    
    if matchObj:
        version = matchObj.group(1)
        # version check
        matchObj2 = re.match(r'([0-9]+)\.([0-9]+)\.([0-9]+)', version)
        if matchObj2:
            if int(matchObj2.group(1))==0 and int(matchObj2.group(2))<=9 and int(matchObj2.group(3))<=9:
                print("correct version of wkhtmltopdf installed")
            else:
                print("installing wkhtmltopdf (you are prompted for the sudo-password)")
                os.system("sudo gem install wkhtmltopdf-binary -v 0.9.9")
else:
    print("installing wkhtmltopdf (you are prompted for the sudo-password)")
    os.system("sudo gem install wkhtmltopdf-binary -v 0.9.9")            


setup(name='Java2PDF',
      version='0.1',
      description='Java2PDF',
      url='http://github.com/mhild/Java2PDF',
      author='mhild',
      license='GPL',
      install_requires=[
          'PyPDF2',
          'pdfkit',
      ],
      zip_safe=False)