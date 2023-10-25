import subprocess
import os

def cppCompiler(content):
    outputArray = []
    mainFile = "Main"
    script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/Cpp"
    os.chdir(script_directory)
    writer = open("temp.cpp", "w")
    writer.write(content)
    reader = open("temp.cpp", "r")
    compile_command = ["java", mainFile]
    try:
        output = subprocess.check_output(compile_command, stdin=reader).decode("utf-8")
        outputArray = output.split("\n")
        print(outputArray)
    except subprocess.CalledProcessError as e:
        print("Error while running C++ compiler:", e)
        
    writer.close()
    reader.close()
    return outputArray

def javaCompiler(content):
    outputArray = []
    mainFile = "Main"
    script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/Java"
    os.chdir(script_directory)
    writer = open("temp.java", "w")
    writer.write(content)
    reader = open("temp.java", "r")
    compile_command = ["java", mainFile]
    try:
        output = subprocess.check_output(compile_command, stdin=reader).decode("utf-8")
        outputArray = output.split("\n")
        print(outputArray)
    except subprocess.CalledProcessError as e:
        print("Error while running Java compiler:", e)

    writer.close()
    reader.close()
    return outputArray
    

def pythonCompiler(content):   
    outputArray = []
    mainFile = "Main"
    script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/Python"
    os.chdir(script_directory)
    writer = open("temp.py", "w")
    writer.write(content)
    reader = open("temp.py", "r")
    compile_command = ["java", mainFile]
    try:
        output = subprocess.check_output(compile_command, stdin=reader).decode("utf-8")
        outputArray = output.split("\n")
        print(outputArray)
    except subprocess.CalledProcessError as e:
        print("Error while running Python compiler:", e)
    
    writer.close()
    reader.close()
    return outputArray


# content = ""
# with open("temp.py", 'r') as file:
#     content = file.read()
# pythonCompiler(content=content)