"""
RAS files from Rigaku XRR are made ready for use with GenX as xy files.

Put all your RAS files in one folder then run the script. The script
only requires the directory of the folder containing your RAS files
as input. The output files names contain _normalized.xy.

Othman
27 Jun 2018
"""

import glob, os, io

#locate files
sourceDir = input("Enter files directory: ")
os.chdir(sourceDir)
allFiles = glob.glob("*.ras")

print('Conversion in progress ...')

def numberize(nums):
    #converts type of items of list comprehension to float
    return [float(n) for n in nums]

for file in range(len(allFiles)):
    #read file as single string
    fileName = str(allFiles[file])
    with io.open(fileName, "r", encoding="latin-1") as fh:
        text = fh.read()
    
	#locate and extract data as row strings; ['x1 y1 z1', 'x2 y2 z2', ...]
    rows = text.splitlines()
    start = rows.index("*RAS_INT_START") + 1
    end = rows.index("*RAS_INT_END")
    data = rows[start:end]
    
	#convert from ['x1 y1 z1', ... ] to [[x1, y1], [x2, y2], ...]
    dataCleaned = [
            numberize(row.split(" ")[:2]) 
            for row in data]
    
	#xy columns: [[x1, y1], [x2, y2], ...] to [[x1, x2, ...], [y1, y2, ...]]
    columns = [list(col) for col in zip(*dataCleaned)]
    
	#normalize y to 1
    maximum = max(columns[1])
    for i in range(len(columns[1])):
        columns[1][i] /= maximum
    
	#convert to xy space-seperated format
    rows = [
            " ".join([str(n) for n in row]) 
            for row in zip(*columns)]
    finalText = "\n".join(rows)
    
	#write output xy file
    outputFileName = fileName.rsplit(".", 1)[0] + "_normalized.xy"
    with open(outputFileName, "w") as fh: 
        fh.write(finalText)

print('Data have been successfuly normalized and converted into XY')