import sys
import subprocess
import re
import math




"""
runs metrix++ against file location
"""

def parse_metrics(location):
    subprocess.call(str.format("{} /metrixpp/metrix++.py collect --std.code.length.total --std.code.lines.code --std.code.lines.comments --std.code.complexity.cyclomatic --std.code.complexity.maxindent --std.code.magic.numbers --ll=ERROR {}",sys.executable,location))
    #subprocess.call("pwd",shell=True)
    
    subprocess.call("{} /metrixpp/metrix++.py export --db-file=metrixpp.db > temp.csv".format(sys.executable),shell=True)

"""
parses csv file from mpp
returns list of lists representing each function and its metrics
""" 

def collect_data(filename):
    FUNCLINES = 2
    FUNCLINEE = 3
    FUNCNAME = 1
    FUNCFILE = 0
    metrics = []
    classfiles = dict()
    with open(filename) as csv:
            for line in csv:
                s = line.split(',')
                #store class in classfiles dict
                if(s[2] == 'class' or s[2] == 'interface'):
                    if s[0] not in classfiles:
                        classfiles[s[0]] = []
                    classfiles[s[0]].append(s)
                elif s[2] == 'global':
                    match = re.search(r'.*/(.*).java',s[0],re.I)      
                    s[1] = match.group(1)
                    if s[0] not in classfiles:
                        classfiles[s[0]] = []
                    classfiles[s[0]].append(s)
                if s[2] == 'function':
                    #match = re.search(r'.*/(.*).java',s[0],re.I)      # original regex to extract filename from path
                    #filename = match.group(1)
                    for i in range(len(s)):
                        if s[i] == '':
                            s[i] = '0'
                    metrics.append([s[0],s[1],float(s[4]),float(s[5]),abs(float(s[6])),abs(float(s[7])),abs(float(s[8])),abs(float(s[9])),abs(float(s[10])),abs(float(s[11]))])
            for func in metrics:
                catstring = ''
                with open(func[0]) as fp:
                        for i, line in enumerate(fp):
                            if i >= func[2]-1 and i <= func[3]+1:
                                catstring += line.strip()
                #print(catstring)
                match = re.search(r'{}\s*\((.*?)\)'.format(func[1]),catstring,re.I)
                params = '('
                try:
                    if match.group(1) != '':
                        
                        paramlist = match.group(1).split(',')
                        firstParam = paramlist[0].split()
                        params += firstParam[len(firstParam) -2]
                        for i in range(1,len(paramlist)):
                            sparam = paramlist[i].split(' ')
                            params += (',' + sparam[len(sparam)-1 ])
                    params += ')'
                    func[1] = func[1] + params
                    #print(newname) 
                except AttributeError:
                    print('ERROR unable to find parameters!!')
                    print(func[1])
                    print('-----------------------------')
                    print(catstring)
                    func[1] += '()'
                mostspecific = 0
                for c in classfiles[func[0]]:
                    lstart = int(c[4])
                    lend = int(c[5])
                    if lstart < func[FUNCLINES] and lend > func[FUNCLINEE]:
                        if mostspecific == 0:
                            mostspecific = c
                        if int(mostspecific[5]) - int(mostspecific[4]) > lstart - lend:
                            mostspecific = c
                
                ind = metrics.index(func)
                if mostspecific == 0:
                    metrics.pop(ind)
                else:
                    metrics[ind].pop(FUNCLINEE)
                    metrics[ind].pop(FUNCLINES)
                    metrics[ind][FUNCFILE] = str.format('{0}.{1}',mostspecific[1],metrics[ind][FUNCNAME])
                    metrics[ind].pop(FUNCNAME)

                
                    
    return metrics
"""
compares functions 

returns a list representing pair
"""

def compare_functions(fA,fB):
    GlobalMetrics = ['Metrix++:numbers','Metrix++:cyclomatic','Metrix++:maxindent','Metrix++:code','Metrix++:comments','Metrix++:total']
    distance = 0
    pairList = [fA[0],fB[0],distance]
    names = iter(GlobalMetrics)
    for i in range(3,len(fA)):
        pairList.append((names.next(),abs(fA[i]-fB[i])))
        distance = distance + ((fA[i] - fB[i]) ** 2.0)
    pairList[2] = math.sqrt(distance) 
    return pairList

"""
Compares all functions in the list to each other once
"""

def get_comparisons(allFun,threshold):
    SCORE = 2
    allComp = []
    #print('Number of functions found')
    #print(len(allFun))
    largest = 0
    for i in range(len(allFun)):
        for j in range(i+1,len(allFun)-1):
            comp = (compare_functions(allFun[i],allFun[j]))
            if comp[SCORE] > largest:
                largest = comp[SCORE]
            if comp[SCORE] <= threshold:
                allComp.append(comp)
    for i in allComp:
        if threshold > 50:
            normscore = (i[SCORE]/threshold) * 100
        else:
            normscore = (i[SCORE]/50) * 100
        i[SCORE] = normscore
    return allComp        


"""
Runs data collection and returns relationship set
Arguments:
location - String
path to source code to be parsed
threshold - int
maximum distance value to be included in output
"""

def get_metrix(location,threshold=10):
    parse_metrics(location)
    data = collect_data('temp.csv')
    return get_comparisons(data,threshold)
    
    
"""
parse_metrics("../../../kse")
met = collect_data('temp.csv')
print(compare_functions(met[0],met[1]))
test = get_comparisons(met,.5)
for i in test:
print(i)
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        a = []
        if len(sys.argv) > 2:
            a = get_metrix(sys.argv[1],int(sys.argv[2]))
        else:
            a = get_metrix(sys.argv[1])
        print('Number of comparisons created')
        print(len(a))
        print(a[0])