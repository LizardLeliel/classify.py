# This file should include:
# -compressFile()
# -getCompressedSize()
# -getSize()
# -getDirectoryEnding()
# -cleanHash()
# -moveToTemp()

# Note: Useful function:
#  -os.path.isdir("hello")
#  -Also! /y for somthing

import subprocess as subp
import os
import sys

# Return the file's size
def fileSize(fileName):
    record = os.stat(fileName)
    return record.st_size

# Return the operating system's directory ending
def dirEnding():
    if os.name == "nt":
        return "\\"
    # Hopefully everything else has just "/"?
    # That being said, it works for linux and mac, which is useful enoughs
    else:
        return "/"

def concat(path1, path2, resultPath):
    if os.name == "nt":
        # May not work =c
        temporaryName = os.tmpnam()
        command = "copy /b /y " + path1 + "+" + path2 + " " + temporaryName
        subp.call(command)
        command = temporaryName + " > " resultPath
        subp.call(command)
        os.remove(temporaryName)
    else:
        temporaryName = os.tmpnam()
        command = "cat " + path1 + " " + path2 + " > " + temporaryName
        subp.call(command)
        command = temporaryName " > " resultPath
        subp.call(command)
        os.remove(temporaryName)


