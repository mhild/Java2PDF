'''
Created on 11.04.2015

@author: mhild
'''

import fnmatch
import argparse
import os
import pdfkit
import re
import textwrap
import time 

from xml.sax.saxutils import escape

def trim_java2(lines):

    return ''.join(lines)


def initialize_html():
    # ##################
    # initialize html
    # ##################
    html = []
    html.append("<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />")
    # reference google-code-prettifier
    html.append("<script src='https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js'></script>")
    # set word wrap
    html.append("<head><style>.pb { page-break-before: always;word-wrap:break-word;}</style></head>")
    html.append("<body>")
    
    return html


def finalize_html():
    return "</body>"

def escape_code(code_string):
    
    return escape(code_string)


def parse_student_folder(source_folder, folder):
    print("Parsing folder '"+folder+"'")  
    
    student_html = []
    student_html.append("<div class='pb'><h3>Student/Ordner: <b>"+folder+"</b></h3>")
    
    # get folder items 
    items = os.walk(source_folder+"/"+folder)
    
    for i in items:
        for jf in fnmatch.filter(i[2], "*.java"):
            student_html.append("<h4>"+i[0]+"/"+jf+"</h4><p><pre class='prettyprint lang-java'>")
            #student_html.append("<![CDATA[")
            with open(i[0]+"/"+jf,"r") as f:
                lines = f.readlines()
                # escape_code method before pretty-print rendering ("<a" -> "< a") 
                student_html.append(escape_code(''.join(lines))+"</pre></p>")
                                    
            f.close()
        
    student_html.append("</div>")
    
    return student_html
    
    
options = {
    'quiet': '',
    'javascript-delay': '5000',
    }

cmd_line_parser = argparse.ArgumentParser()
cmd_line_parser.add_argument("source", help="Klausurordner: Pfad zu den Studentenordnern")
cmd_line_parser.add_argument("-d", "--destinationfolder", help="Ziel-Ordner das PDF")
cmd_line_parser.add_argument("-o", "--outfile", help="Name des PDFs")
cmd_line_parser.add_argument("-v", "--verbose", action="store_true")
cmd_line_parser.add_argument("-D", "--debug", action="store_true")

args = cmd_line_parser.parse_args()

source_folder = args.source.strip("/")
prefix = source_folder.split("/")[-1]+"_"

if args.destinationfolder:
    destination_folder =  args.destinationfolder
else:
    destination_folder = "."

if args.debug:
    debug = True
else:
    debug = False

if args.outfile:
    outfile = args.outfile
    if not outfile.endswith(".pdf"):
        outfile=outfile+".pdf"
else:
    outfile = destination_folder+"/"+prefix+"GESAMT.pdf"
    
if not os.path.exists(source_folder):
    print("source folder '"+source_folder+"' existiert nicht")
    exit


# get student-subfolders
student_folders = next(os.walk(source_folder))[1]

html = initialize_html()

for folder in student_folders:
    html.extend(parse_student_folder(source_folder, folder))
    
html.append(finalize_html())

html_string = ''.join(html)

if debug:
    print("<!-- " +folder + "-->")
    print(html_string+"\n\n")

print("Building PDF: " + outfile )
pdfkit.from_string(html_string.strip().decode('utf-8'), outfile, options=options)       



