import subprocess

dependencies = ["vdf" "steam[client]"]

for package in dependencies:
    subprocess.run(["pip", "install", "--target=deps", package])
print("Dependencies installed locally in 'deps/'")
