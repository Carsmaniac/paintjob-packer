import os
import shutil
import PyInstaller.__main__

for file in ["../library/paint-job-tracker.txt", "../library/misc-utilities.py", "../library/mod links.md"]:
    if os.path.exists(file):
        os.remove(file)

# Get the current PJP version
version = ""
version_ini = open("../library/version.ini", "r")
for line in version_ini.readlines():
    if line.startswith("installed version"):
        version = line.replace("installed version: ", "").rstrip()
version_ini.close()

# Package into .exe and create installer, without templates
PyInstaller.__main__.run(["../packer.py", "--onefile", "--windowed",
    "--icon=../library/packer-images/icon-squircle.ico", "--name=Paint Job Packer",
    "--add-data=../library:library", "--add-data=../theme:theme", "--add-data=../lang:lang",
    "--add-data=../sun-valley.tcl:."])

os.remove("dist/Paint Job Packer")
shutil.make_archive("Paint-Job-Packer-v{}-Mac".format(version), "zip", "dist")
shutil.rmtree("build")
shutil.rmtree("dist")
os.remove("Paint Job Packer.spec")
