import os
from helper import*
def countingX_InLine(line):
	count = 0
	while line[count:count+1] == '#' and count < len(line):
		count = count + 1
	if line[count:count+1] == ' ':
		return count
	else:
		return 0

def correctLineFormatOffset(lineFormat):
	smallXCount = 100
	for fm in lineFormat:
		if fm[0] < smallXCount:
			smallXCount = fm[0] 
	for index in range(len(lineFormat)):
		lineFormat[index][1] = lineFormat[index][1][lineFormat[index][0]+1:-1]
		lineFormat[index][0] = lineFormat[index][0] - smallXCount + 1
	return lineFormat
	
def generateLineWith(fm):
	tocLinePrefix = '    ' * (fm[0]-1)
	return tocLinePrefix +'- ['+ fm[1] +']'+'(#'+fm[2] +')\n'


def addTOCtoFileLines(mdFileLines):
	toc = [tocMark1,'\n','## Table of Contents\n']
	insertIndex = -1
	originTocLineFormat = []
	titleLines = []
	titleIndices = []
	counts = []
	for index in range(len(mdFileLines)):
		count = countingX_InLine(mdFileLines[index])
		if count > 0:
			if insertIndex == -1:
				insertIndex = index
			counts.append(count)
			titleIndices.append(index)
	
	if insertIndex == -1:
		return mdFileLines
	else:
		sectionNumbers = generateSectionNumbersWithXCounts(counts)
		for index in range(len(titleIndices)):
			mdFileLines[titleIndices[index]] = deleteALabelInLine(mdFileLines[titleIndices[index]])
			titleLines.append(mdFileLines[titleIndices[index]])
			mdFileLines[titleIndices[index]] = insertALabelInLine(mdFileLines[titleIndices[index]],counts[index],sectionNumbers[index])

		for index in range(len(counts)):
			originTocLineFormat.append([counts[index],titleLines[index],sectionNumbers[index]])

		correctTocLineFormat = correctLineFormatOffset(originTocLineFormat)
		for fm in correctTocLineFormat:
			toc.append(generateLineWith(fm))
		toc.append("\n")
		toc.append(tocMark2)
		toc.append('\n')
		toc.reverse()
		for tocLine in toc:
			mdFileLines.insert(insertIndex,tocLine)
		return mdFileLines

def clearLswTocWithMarkInFile(mdFileLines):
	markIndex1 = 0
	markIndex2 = 0
	for index in range(len(mdFileLines)):
		if tocMark1 in mdFileLines[index]:
		    markIndex1 = index
		if tocMark2 in mdFileLines[index]:
			markIndex2 = index
	if (markIndex2 > markIndex1) and markIndex1 != 0:
		del mdFileLines[markIndex1:markIndex2+2]

	return mdFileLines

def containToc(mdFileLines):
	for line in mdFileLines:
		if '# Table of Contents' in line:
			return True
	return  False



#Main
mdFileNames = []
lines = []
tocMark1 = '<!-- lsw toc mark1. Do not remove this comment so that lsw_toc can update TOC correctly. -->\n'
tocMark2 = '<!-- lsw toc mark2. Do not remove this comment so that lsw_toc can update TOC correctly. -->\n'
for fileName in os.listdir(os.getcwd()):
	if fileName[-3:] == '.md':
		mdFileNames.append(fileName)

for name in mdFileNames:

	with open(name,'r') as f:
		lines = f.readlines()
	lines = clearLswTocWithMarkInFile(lines)
#	with open('test.markdown','w') as test:
#		test.writelines(lines)

	if not(containToc(lines)):

		lines = addTOCtoFileLines(lines)
		os.remove(name)
		with open(name,'w') as g:
			g.writelines(lines)
	else:
		print "{fileName} already contains TOC and without correct lsw_toc mark".format(fileName = name)

