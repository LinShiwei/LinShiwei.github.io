def generateSectionNumbersWithXCounts(xcountList):
	sectionNumbers = []
	for index in range(len(xcountList)):
		if index == 0:
			sectionNumbers.append('1')
		else:
			if xcountList[index]==xcountList[index-1]:
				pre = sectionNumbers[index-1][:-1]
				suf = sectionNumbers[index-1][-1]
				sectionNumbers.append(pre+str(int(suf)+1))
			else:
				if xcountList[index] > xcountList[index-1]:
					temp = sectionNumbers[index-1]
					for count in range(xcountList[index]-xcountList[index-1]):
						temp = temp+'1'
					sectionNumbers.append(temp)
				else:
					temp = sectionNumbers[index-1][:xcountList[index]-xcountList[index-1]]
					pre = temp[:-1]
					suf = temp[-1]
					sectionNumbers.append(pre+str(int(suf)+1))
	return sectionNumbers


def insertALabelInLine(line,xcount,num):
	return line[:xcount+1]+'<a id="'+str(num)+'"></a>'+line[xcount+1:]

def deleteALabelInLine(line):
	index1 = line.find('<a ',0)
	index2 = line.find('</a>',0)
	if index1 > -1 and index1 < index2:
		return line[:index1]+line[index2+4:]
	else:
		return line
