import csv
from operator import itemgetter
L1 = [('method7', 'method8', 45, ('complexity', 78)), ('method1', 'method2', 58, ('complexity', 78)),
('method10', 'method12', 55, ('complexity', 78))]


L2 = [('method7','method8', 55, ('data', 55)),('method5','method6', 45, ('complexity', 78)),
('method1','method2', 55,('complexity',78))]


headerString = ['Method1','Method2','Final Score','score 1','score 2','Metrixpp:numbers','Metrix++:cyclomatic','Metrixpp:maxindent','Metrixpp:code','Metrixpp:comments','Metrixpp:total']


	
def CombineAndExportData(L1):
    finalList = L1
    truefinal = list()
    for i in finalList:
        truefinal.append(i)
    
    clear_file = "Results.csv"
    f = open(clear_file, "w")
    f.close()
    with open('Results.csv', 'w') as myFile:
        wr = csv.writer(myFile)
        wr.writerow(headerString)
        for value in truefinal:
            wr.writerow(value)
		
'''finalList = mergeLists(L1,L2)
with open('path.csv', 'w') as myFile:
    wr = csv.writer(myFile, dialect='excel')
    wr.writerow(finalList)'''
