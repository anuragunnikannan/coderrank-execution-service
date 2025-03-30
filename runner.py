import subprocess
import sys
import json

mode = sys.argv[1]
language = sys.argv[2]

input_file = ""
stdout = ""
stderr = ""
output = ""
test_cases = []
result = {"compilation_status": "", "outputs": []}

if mode == "run":

    with open("/codes/input.txt", "rb") as f:
        input_file = f.read()

    if language == "java":
        output = subprocess.run(["java", "/codes/Solution.java"],
                                input=input_file, capture_output=True, timeout=10)
    elif language == "python":
        output = subprocess.run(["python3", "/codes/solution.py"],
                                input=input_file, capture_output=True, timeout=10)
    elif language == "c++":
        output = subprocess.run(
            ["g++ -o solution", "/codes/solution.cpp"], capture_output=True)
        if output.returncode == 0:
            output = subprocess.run(
                ["/codes/solution"], input=input_file, capture_output=True, timeout=10)

    stdout = output.stdout.decode().strip()
    stderr = output.stderr.decode().strip()

    if len(stderr) > len(stdout):
        print(stderr)
    else:
        print(stdout)

elif mode == "submit":
    with open("/codes/test_cases.json", "r") as f:
        test_cases = json.loads(f.read())

    is_compiled = False
    for i in test_cases["inputs"]:
        if language == "java":
            if is_compiled:
                output = subprocess.run(["java", "-cp", "/codes/", "Solution"],
                                        input=i.encode("utf-8"), capture_output=True, timeout=10)
            else:
                output = subprocess.run(
                    ["javac", "/codes/Solution.java"], capture_output=True)

                if output.returncode == 0:
                    output = subprocess.run(
                        ["java", "-cp", "/codes/", "Solution"], input=i.encode("utf-8"), capture_output=True, timeout=10)
                    is_compiled = True
                else:
                    result["compilation_status"] = "failed"
                    result["outputs"].append(output.stderr.decode().strip())
                    break
        elif language == "c++":
            if is_compiled:
                output = subprocess.run(
                    ["/codes/solution"], input=i.encode("utf-8"), capture_output=True, timeout=10)
            else:
                output = subprocess.run(
                    ["g++ -o solution", "/codes/solution.cpp"], capture_output=True)

                if output.returncode == 0:
                    output = subprocess.run(
                        ["/codes/solution"], input=i.encode("utf-8"), capture_output=True, timeout=10)
                    is_compiled = True
                else:
                    result["compilation_status"] = "failed"
                    result["outputs"].append(output.stderr.decode().strip())
                    break

        elif language == "python":
            output = subprocess.run(["python3", "/codes/solution.py"], input=i.encode(
                encoding="utf-8"), capture_output=True, timeout=10)

        stdout = output.stdout.decode().strip()
        stderr = output.stderr.decode().strip()

        if len(stderr) > len(stdout):
            result["outputs"].append(stderr)
        else:
            result["outputs"].append(stdout)

    print(json.dumps(result))
