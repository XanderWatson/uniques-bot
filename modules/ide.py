import subprocess

def run(filename, extension, language, code):
    with open(f"{filename}.{extension}", "w") as c:
        c.write(code)
    c.close()

    CompileError = ''
    Output = ''
    RuntimeError = ''

    if language == "python" or language == "py":
        process = subprocess.Popen(
            ["python", f"{filename}.{extension}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        Output, RuntimeError = process.communicate()

        return [CompileError, Output, RuntimeError]

    elif language == "c":
        process = subprocess.Popen(
            ["gcc", "-o", f"{filename}c", f"{filename}.{extension}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        output, CompileError = process.communicate()

        if CompileError is None:
            process = subprocess.Popen(
                [f"./{filename}c"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            Output, RuntimeError = process.communicate()

        return [CompileError, Output, RuntimeError]

    elif language == "c++" or language == "cpp":
        process = subprocess.Popen(
            ["g++", "-o", f"{filename}cpp", f"{filename}.{extension}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        output, CompileError = process.communicate()

        if CompileError is None:
            process = subprocess.Popen(
                [f"./{filename}cpp"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            Output, RuntimeError = process.communicate()

        return [CompileError, Output, RuntimeError]
