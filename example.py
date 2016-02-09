
from tempfile import mkstemp
from shutil import move
from os import remove, close
import re

def replace(filename, pattern, subst):
    #create temp file
    fh, abs_path = mkstemp()
    #open file
    with open(abs_path,'w') as new_file:
        with open(filename) as old_file:
            for line in old_file:
                #new_file.write(line.replace(pattern, subst))
                if "ReserveForce" in line:
                    new_file.write(re.sub('\d', '1', line))
                # if ".clientSubnet" in line:
                #     new_file.write(line)
                #     line = old_file.next()
                #     new_file.write(re.sub('{.*?}', "{true}", line))
                else:
                     new_file.write(line)
    close(fh)
    #Remove original file
    #remove(file_path)
    #Move new file
    move(abs_path, filename)
pattern = r'hello'
pattern = '{.*?}'
filepath = "C:/tmp/fileplay/config.tcl"
filepath = "C:/AvalancheExeDir/config.tcl"
replace(filepath, pattern, 'false')