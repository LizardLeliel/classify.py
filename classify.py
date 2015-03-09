
import subprocess as subp
import os
import sys

# Return the file's size
def fileSize(fileName):
    record = os.stat(fileName)
    return record.st_size

# Make a compressed file into the directory of \temp
#  Using the gzip compressor; then returns the size of
#  the compressed file's size
def compressedSize(directoryName, fileName):
    temporaryDirectory = "temp\\"
    directoryName      = directoryName + "\\"

    if directoryName != temporaryDirectory:
        subp.call("copy " \
            + directoryName + fileName + " " \
            + temporaryDirectory + fileName, shell=True)

    compressedFileName = temporaryDirectory + fileName + ".gz"
    subp.call("gzip -f " + temporaryDirectory + fileName, shell = True)
    size = fileSize(compressedFileName)

    os.remove(compressedFileName)
    return size

# Find the normalized compressed file
def normalizedCompressedDistance(directory1, file1, directory2, file2):
    # Initialize some things; mostly path names
    concatFile = "concat"
    concatPath = "temp\\" + concatFile
    path1 = directory1 + "\\" + file1
    path2 = directory2 + "\\" + file2

    # Make a concatenated file, windows style
    command = "copy /b " + path1 + "+" + path2 + " " + concatPath
    subp.call(command, shell = True)

    # Calculate sizes
    compressedSize1 = compressedSize(directory1, file1)
    compressedSize2 = compressedSize(directory2, file2)
    totalCompressed = float(compressedSize("temp", concatFile))

    # Calculate the distance
    return ((totalCompressed - min(compressedSize1, compressedSize2)) \
        /  max(compressedSize1, compressedSize2))

# "main" function
# ... Is there a better way to do -h? 
if __name__ == "__main__":
    if ("-h" in sys.argv):
        print("\nSynopsis: winclassify.py -[vh] [-c classesDirectory] [-d" \
            + " dataDirectory]\n\n" \
            + "This program uses normalized complexity distance to compare" \
            + " a file agaisnt other, and comparing the information in" \
            + " common.\n\n" \
            + "In other words, it will try to match files in the data" \
            + " directory to files in classes. If you have d.txt in data" \
            + " and c.txt, c.mp3, and c.jpeg in classes, the program will" \
            + " attempt to say d.txt is a .txt file, assuming each file has" \
            + " the appriopriate contents as their file extension.\n\n" \
            + "The directories given in the command line arguements must" \
            + " exist, and the directory temp must exist in the program's" \
            + " directory. Files in temp MAY be overwritten.\n\n" \
            + "If the arguements to -c or -d are not provided, then the" \
            + " program will assume the parameters to be 'classes' and" \
            + " data respectivly\n\n" \
            + "gzip.exe must also be in the current working directory\n\n"
            + "The options are:\n" \
            + "\t-h Help (this file)\n" \
            + "\t-v Verbose (will print the processes performed)\n" \
            + "\t-c Classes (the directory name for the 'class' directory -" \
            + " must be followed by a directory name)\n" \
            + "\t-d Data (the directory name for the 'data' directory - " \
            + " must be followed by a directory name)")
        sys.exit(0)

    # If the user specified a classes directory for the program
    if "-c" in sys.argv:
        cOptionIndex = sys.argv.index("-c")
        if cOptionIndex == len(sys.argv) - 1:
            print("Error: option -c must be followed by a directory name" \
                + " parameter (none found)")
            sys.exit(1)

        classDirectory = sys.argv[cOptionIndex + 1]
    else:
        classDirectory = "classes"

    # If the user specified a data directory for the program
    if "-d" in sys.argv:
        cOptionIndex = sys.argv.index("-d")
        if cOptionIndex == len(sys.argv) - 1:
            print("Error: option -d must be followed by a directory name" \
                + " parameter (none found)")
            sys.exit(1)

        dataDirectory = sys.argv[cOptionIndex + 1]
    else:
        dataDirectory = "data"


    # Open the directories
    classList = os.listdir(classDirectory)
    dataList  = os.listdir(dataDirectory)

    output = []

    # for each data file
    for dataFile in dataList:
        minDist = float("inf")
        result  = "None"

        # Determine the distance from the data files to the class files
        for classFile in classList:
            distance = normalizedCompressedDistance(classDirectory, classFile,
                dataDirectory, dataFile)

            # Set the distance is shorter then previous ones, set it as the
            #  shortest distance
            if distance < minDist:
                minDist = distance
                result  = classFile

        # The above is the verbose syntax; below is the non-verbose version
        if "-v" in sys.argv:
            output.append("{} matches {} by a distance of {:.2f}".format(
                dataFile, result, distance))
        else:
            output.append("{} {} {:.2f}".format(dataFile, result, distance))

    for string in output:
        print string

