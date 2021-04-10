import subprocess


def runCommand(commandList):
    if commandList[0] == 'sudo':
        process = subprocess.Popen(
            commandList,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output, error = process.communicate(input="X@nl0p3r")

        return [output, error]
    else:
        process = subprocess.Popen(
            commandList,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output, error = process.communicate()

        return [output, error]
