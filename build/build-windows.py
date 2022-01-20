import os
import shutil
import PyInstaller.__main__

if os.path.exists("../library/paintjob-tracker.txt"):
    os.remove("../library/paintjob-tracker.txt")

INNO_SETUP_PATH = "C:/Program Files (x86)/Inno Setup 6/ISCC.exe"

# Get the current PJP version
version = ""
version_ini = open("../library/version.ini", "r")
for line in version_ini.readlines():
    if line.startswith("installed version"):
        version = line.replace("installed version: ", "").rstrip()
version_ini.close()

# Update the Inno Setup script with the current version
script_read = open("inno-script.iss", "r")
script_lines = script_read.readlines()
script_read.close()

script_write = open("inno-script.iss", "w")
for line in script_lines:
    if "#define MyAppVersion" in line:
        line = "#define MyAppVersion \"{}\"\n".format(version)
    script_write.write(line)
script_write.close()

# Package into .exe and create installer, without templates
PyInstaller.__main__.run(["../packer.py", "--onedir", "--windowed",
    "--icon=../library/packer-images/icon-circle.ico", "--name=Paint Job Packer",
    "--add-data=../library;library", "--add-data=../theme;theme", "--add-data=../lang;lang",
    "--add-data=../sun-valley.tcl;."])
os.system("\"{}\" inno-script.iss".format(INNO_SETUP_PATH))

shutil.make_archive("paint-job-packer-v{}-windows-no-templates".format(version), "zip", "output")
shutil.rmtree("build")
shutil.rmtree("dist")
shutil.rmtree("output")
os.remove("Paint Job Packer.spec")

# Package into .exe and create installer, with templates
PyInstaller.__main__.run(["../packer.py", "--onedir", "--windowed",
    "--icon=../library/packer-images/icon-circle.ico", "--name=Paint Job Packer",
    "--add-data=../library;library", "--add-data=../theme;theme", "--add-data=../lang;lang",
    "--add-data=../sun-valley.tcl;.", "--add-data=../templates;templates"])
os.system("\"{}\" inno-script.iss".format(INNO_SETUP_PATH))

shutil.make_archive("paint-job-packer-v{}-windows-templates".format(version), "zip", "output")
shutil.rmtree("build")
shutil.rmtree("dist")
shutil.rmtree("output")
os.remove("Paint Job Packer.spec")
