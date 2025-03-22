import subprocess
import sys

mode = sys.argv[0]
language = sys.argv[1]
user_uuid = sys.argv[2]

if mode == "run":
    input_file = ""
    stdout = ""
    stderr = ""
    output = ""

    with open(f"/app/{user_uuid}/input.txt", "rb") as f:
        input_file = f.read()
    
    if language == "java":
        output = subprocess.run(["java", f"/app/{user_uuid}/Solution.java"], input=input_file, capture_output=True)
    elif language == "python":
        output = subprocess.run(["python3", f"/app/{user_uuid}/app.py"], input=input_file, capture_output=True)

    stdout = output.stdout.decode().strip()
    stderr = output.stderr.decode().strip()
    
    if len(stderr) > len(stdout):
        print(stderr)
    else:
        print(stdout)
