from github import Github
import re
import os
from compile import cppCompiler, javaCompiler, pythonCompiler


def extract_repository_name(url):
    pattern = r'https://github.com/([^/]+/[^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def suitableExtension(path):
    _, fileExtension = os.path.splitext(path)
    return fileExtension 

libPaths = []
filePaths = []
def get_repository_contents(repository, path='', depth=0):
    contents = repository.get_contents(path)
    for content in contents:
        filePaths.append(content.path)
        if content.type == "dir":
            get_repository_contents(repository, content.path, depth + 1)
        else:
            extension = os.path.splitext(content.path)[1]
            if (extension == '.c' or extension == '.cc' or extension == '.cpp'):
                libraries = cppCompiler(content.decoded_content.decode('utf-8'))
            elif extension == '.java':
                libraries = javaCompiler(content.decoded_content.decode('utf-8'))
            elif extension == '.py':
                print(content.path)
                libraries = pythonCompiler(content.decoded_content.decode('utf-8'))
            else:
                libraries = []
            for library in libraries:
                libPaths.append((content.path, library))

repository_url = 'https://github.com/Sukhija-Aniket/StockPortfolioManager'
repository_name = extract_repository_name(repository_url)

def cmpLib(path):
    fullPath = path[0] + path[1]
    return fullPath

def cmpFile(path):
    return path

def getExternalLib(sortedFilePaths, sortedLibPaths):
    print(sortedFilePaths, sortedLibPaths)
    pass

if repository_name:
    g = Github()
    repository = g.get_repo(repository_name)
    print(f"Repository: {repository_name}")
    get_repository_contents(repository)
    sortedLibPaths = sorted(libPaths, key=cmpLib)
    sortedFilePaths = sorted(filePaths, key=cmpFile)
    externalLib = getExternalLib(sortedFilePaths, sortedLibPaths)

else:
    print(f"Invalid Repository Url")