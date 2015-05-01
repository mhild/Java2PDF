'''
Created on 11.04.2015

@author: mhild
'''

import fnmatch
import argparse
import os
import pdfkit
from PyPDF2 import PdfFileReader, PdfFileMerger
import re

def trim_java(lines):
    # remove trailing blanks
    text = ""
    indentcount = 0
    inside_comment = False
    inside_arg = False
    
    for line in lines:
        if '(' in line:
            inside_arg = True

        if inside_arg:
            res = re.match(r'(\([\s\S]+\))', line)
            if res:
                arg = res.group(1)
                new_arg = arg.replace(";","##SKINARG##");
            
                line = line.replace(arg,new_arg);
        
        if ')' in line:
            inside_arg = False
                
        text=text+line.strip()
        
        if "//" in line:
            text=text+"##COMMENT##"
            
        if "/*" in line:
            inside_comment = True
            
        if inside_comment:
            text=text+"##COMMENT##"
        
        if "*/" in line:
            inside_comment = False    
    

            
   
    # remove newlines
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    
    text = text.replace("public", "\npublic")
    text = text.replace("private", "\nprivate")
    
    # insert newlines after ';' & comments
    text = text.replace(";", ";\n")
    
    # replace placeholders
    text = text.replace("##COMMENT##", "\n")
    text = text.replace("##SKINARG##", ";")
    # insert indents 
    out = ""
    indent = ""
    for char in text:
        if char =='{':
            indentcount = indentcount + 1
            indent = indent + " "
            out = out + char + "\n" + indent
        elif char == '}':
            indentcount = indentcount - 1
            indent = indent[:-1]
            out = out + char + "\n" + indent
        elif char == "\n":
            out = out + char + indent
        else:
            out = out + char

        
    return out
    

options = {
    'quiet': ''
    }

cmd_line_parser = argparse.ArgumentParser()
cmd_line_parser.add_argument("source", help="Klausurordner: Pfad zu den Studentenordnern")
cmd_line_parser.add_argument("-d", "--destinationfolder", help="Ziel-Ordner fuer die PDFs")
cmd_line_parser.add_argument("-p", "--prefix", help="Prefix, dass jedem PDF vorangestellt wird")
cmd_line_parser.add_argument("-f", "--force", action='store_true', help="Einzelne Studenten-PDFs werden neu erstellt", )
args = cmd_line_parser.parse_args()

source_folder = args.source.strip("/")

if args.destinationfolder:
    destination_folder =  args.destinationfolder
else:
    destination_folder = source_folder.strip("/")
    
if args.prefix:
    prefix = args.prefix
else:
    prefix = source_folder.split("/")[-1]+"_"
    

if not os.path.exists(source_folder):
    print("source folder existiert nicht")
    exit

student_folders = next(os.walk(source_folder))[1]


pdf_list = []
for folder in student_folders:

    outfile = destination_folder+"/"+prefix+folder.replace(" ","_")+".pdf"
    pdf_list.append(outfile)
    
    if not os.path.exists(outfile) or args.force:
        # umlaute
        html="<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />"
    
        print("#Student/Ordner: "+folder+" => PDF wird erstellt")
        
        html=html+"<h3>Student/Ordner: <b>"+folder+"</b></h3>"
        
        items = os.walk(source_folder+"/"+folder)
        
    
        for i in items:
            for jf in fnmatch.filter(i[2], "*.java"):
    
                html=html+"<h4>"+i[0]+"/"+jf+"</h4><p><pre style='font-size: 10px; font-family: 'Courier New', courier; white-space: pre;'>"
                with open(i[0]+"/"+jf,"r") as f:
                    lines = f.readlines()
                html=html+trim_java(lines)+"</pre></p>"
    
                f.close()
        
        pdfkit.from_string(html.strip().decode('utf-8'), outfile, options=options)
    else:
        print("Student/Ordner: "+folder+" => skipped")
        
merger = PdfFileMerger()

for filename in pdf_list:
    print("adding "+filename)
    merger.append(PdfFileReader(filename, "rb"))

merger.write(os.path.join(destination_folder, prefix+"GESAMT.pdf"))

    
    
