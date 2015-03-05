
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
    concatFile = "concat.txt"
    concatPath = "temp\\" + concatFile
    path1 = directory1 + "\\" + file1
    path2 = directory2 + "\\" + file2


    command = "copy /b " + path1 + "+" + path2 + " " + concatPath
    subp.call(command, shell = True)

    compressedSize1 = compressedSize(directory1, file1)
    compressedSize2 = compressedSize(directory2, file2)
    totalCompressed = float(compressedSize("temp", concatFile))

    return ((totalCompressed - min(compressedSize1, compressedSize2)) \
        /  max(compressedSize1, compressedSize2))

# "main" function
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
            + "\t-c Classes (the directory name for the 'class' directory\n" \
            + "\t-d Data (the directory name for the 'data' directory")
        exit(0)

    # Open the directories
    classList = os.listdir("classes")
    dataList  = os.listdir("data")

    output = []

    for dataFile in dataList:
        # Why this?
        minDist = float("inf")
        result  = "None"
        for classFile in classList:
            distance = normalizedCompressedDistance("classes", classFile,
                "data", dataFile)

            if distance < minDist:
                minDist = distance
                result = classFile

        if "-v" in sys.argv:
            #print("" + dataFile + "  matches " + result + " by a" \
            #    + " distance of " + distance)
            #print("{} matches {} by a distance of {:.2f}".format(
            #    dataFile, result, distance))
            output.append("{} matches {} by a distance of {:.2f}".format(
                dataFile, result, distance))
        else:
            output.append("{}: {}, {:.2f}".format(dataFile, result, distance))
            #output.append(dataFile + ": " + result + " " + distance)

    for string in output:
        print string





    #print(normalizedCompressedDistance("classes", "omg.txt", \
    #    "data", "omg2.txt"))

