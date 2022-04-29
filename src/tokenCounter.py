#read a file and count tokens
import os
import re
Example1FilesQ =["quatusExamples2/simpleFifo_hw.tcl","quatusExamples2/Example1.qsys","exampleFIFOs.json","exampleFIFOs3.json"]

regex = "(\w|\.)+"

for file in Example1FilesQ:
    with open(file) as f:
        content = f.readlines()
        #flatten
        content = "".join(content)
        #find all words matching regex
        content = [m.group() for m in re.finditer(regex,content)]
        
        #remove empty strings
        content = [x for x in content if x != '']
        #count
        #print(content)
        content = len(content)
        
        print(file,content)
