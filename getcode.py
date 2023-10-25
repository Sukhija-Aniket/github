from github import Github
import re
import os
from compile import cppCompiler, javaCompiler, pythonCompiler

#################### Testing Urls ####################

# https://github.com/Sukhija-Aniket/StockPortfolioManager
# https://github.com/AbdullahShahid01/Rent-a-Car-Management-System
# https://github.com/Sukhija-Aniket/ns3-mtp-project

#################### Comparators ####################

def cmp_library(path):
    fullPath = path[0] + path[1]
    return fullPath

def cmp_file(path):
    return path

#################### Utility Functions ####################

def extract_repository_name(url):
    pattern = r'https://github.com/([^/]+/[^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_repository_contents(repository, path='', depth=0):
    contents = repository.get_contents(path)
    for content in contents:
        if content.type == "dir":
            filePaths.append(content.path) # think about it
            get_repository_contents(repository, content.path, depth + 1)
        else:
            extension = os.path.splitext(content.path)[1]
            if (extension == '.c' or extension == '.cc' or extension == '.cpp' or extension == '.h'):
                print(content.path)
                filePaths.append(content.path)
                libraries = cppCompiler(content.decoded_content.decode('utf-8'))
            elif extension == '.java':
                print(content.path)
                filePaths.append(content.path)
                libraries = javaCompiler(content.decoded_content.decode('utf-8'))
            elif extension == '.py':
                print(content.path)
                filePaths.append(content.path)
                libraries = pythonCompiler(content.decoded_content.decode('utf-8'))
            else:
                libraries = []
            for library in libraries:
                libPaths.append((content.path, library))

def tokenize(str):
    words = []
    temp = ''
    for x in str:
        if x == '/':
            words.append(temp)
            temp = ''
        else:
            temp += x

    if temp != '':
        words.append(temp)

    return words 
 
# going string by string for now, will change if need be.
def get_prefix(a, b):
    i = 0
    str = ""
    l1 = tokenize(a)
    l2 = tokenize(b)
    k = min(len(l1), len(l2))
    while(i < k):
        if l1[i] == l2[i]:
            i+=1
        else:
            for j in range(i,l2):
                str += l2[j]
            return i, str

    for j in range(k,l2):
        str += l2[j]
    return k, str

def get_completion(a, b):
    i, j = 0, 0
    l1 = tokenize(a)
    l2 = tokenize(b)
    m, n = len(l1), len(l2)
    while i < m and j < n:
        if l1[i] == l2[j]:
            i+=1
            j+=1
        else:
            i+=1    
    return j

def check_match(a, b):
    path, _ = os.path.splitext(a)
    lib = ""
    for x in b[1]:
        if x == '.':
            lib += '/'
        else:
            lib += x
    
    # we will divide it into two parts such that the complete string can be obtained from these two parts
    l, remainingPath = get_prefix(b[0], path)
    r = get_completion(lib, remainingPath)
    checker = l+r
    if checker >= len(tokenize(path)) and r > 0:
        return 0
    if b[0] < path:
        return 1
    return -1    

def get_external_lib(sortedFilePaths, sortedLibPaths):
    libraries = set() # use a set here
    badList = []
    for i, y in enumerate(sortedLibPaths):
        for x in sortedFilePaths:
            if y[1] == '':
                badList.append(i)
                continue
            val = check_match(x, y)
            if val == 0:
                badList.append(i)

    for i in range(len(sortedLibPaths)):
        if i in badList:
            continue
        libraries.add(sortedLibPaths[i][1])
    print(f"ok ok ok so let's see, {libraries}\n\n")
    return

#################### Main Working ####################

libPaths = []
filePaths = []
repository_url = input("Enter Repository URL: ")
repository_name = extract_repository_name(repository_url)

if repository_name:
    g = Github()
    repository = g.get_repo(repository_name)
    get_repository_contents(repository)
    sortedLibPaths = sorted(libPaths, key=cmp_library)
    sortedFilePaths = sorted(filePaths, key=cmp_file)
    externalLib = get_external_lib(sortedFilePaths, sortedLibPaths)
else:
    print(f"Invalid Repository Url")