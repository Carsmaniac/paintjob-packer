# Paint Job Packer only collects the following information:
# 1. Installed version
# 2. Operating system (Windows, macOS or Linux)
# 3. System language
# 4. Which vehicle(s) your mod supports

# I've explained what each line of the analytics code does, so you don't need programming experience to understand it



# 1. Installed version
# This lets me know how quickly a new update is downloaded, which helps tell me when I can remove old code online
# For example, v1.7 introduced a new update checker, but the files that supported the old one in v1.6 couldn't be removed, so that older versions could still check
# If anything like that happens again, I'll know when the majority of people have updated to the new version, so I can remove the old files from the previous version

# The installed version is stored in a file called version.ini, so the first step is to open that file
# It's stored in the library folder, hence the "library/"
# "r" means the file is opened in READ mode
version_file = open("library/version.ini", "r")

# Next, the lines of the file need to be read
version_lines = version_file.readlines()

# Since we have the lines, we can close the original file
version_file.close()

# The installed version is stored on the third line
# Computers count from 0 (like 0, 1, 2, 3...) so we actually need line number 2
installed_version_line = version_lines[2]

# The full line looks something like "installed version: 1.9"
# The "installed version" bit is 19 characters long, so to get just the version number we can chop off the first 19 characters
# "rstrip" removes any spaces or other empty characters from the end of the version number
installed_version = installed_version_line[19:].rstrip()



# 2. Operating system
# This lets me know how many people are using each operating system
# At the moment, built-in templates are only offered on Windows, since it's the most popular OS
# If all of a sudden 20% of people are using Linux, it would make sense to offer them on Linux as well

# We'll be using a Python library called "sys", which tells us some information about the system it's running on
# "platform" a string (some text) describing which OS you're using
from sys import platform

# On Windows, the platform is win32
if platform == "win32":
    operating_system = "Windows"

# On macOS, the platform is darwin
# Darwin is the name of an old OS made by Apple in 2000, and is the basis of macOS, iOS and all their other operating systems
if platform == "darwin":
    operating_system = "macOS"

# On Linux, the platform is linux, which is nice and straightforward
if platform == "linux":
    operating_system = "Linux"



# 3. System language
# This lets me know which languages peoples' computers are running, so I can add them to the community Crowdin project
# It also tells me which languages are the most popular, so I can make sure those translations are correct (to the best of my ability)

# We'll be using a Python library called "locale", which is all about translations and languages
# "getdefaultlocale" is a function that tells us how the system handles language
from locale import getdefaultlocale

# We check the system language info
system_language_info = getdefaultlocale()

# getdefault locale actually gives us two things: the default language, and the default character encoding (e.g. ASCII, Unicode etc)
# We only need the default language, and since computers count from 0, we only need the 0th part of the language info
system_language = system_language_info[0]

# Sometimes getdefaultlocale can't access the system language, in which case we report that it couldn't be detected
if system_language == None:
    system_language = "Not detected"



# 4. Which vehicle/s your mod supports
# This lets me know what type of paint job I should focus on when it comes to new features: individual paint jobs or paint job packs, mods or vanilla vehicles, trucks and trailers or buses, etc
# If very few people are making paint jobs for modded vehicles, I should focus on making vanilla trucks/trailers as easy to skin as possible

# The list of vehicles is built in the main script "packer.py" in the make_paintjob function, and sent to the analytics function as "vehicle_list"
# Each vehicle in the list is represented by a four digit number, like this: 5016,7022,7038
# The numbers are listed in library/vehicles/vehicle-codes.ini



# RudderStack is used to collect the analytics data, so we need to import the RudderStack Python API
import library.rudder as rudder

# In order to talk to RudderStack, we need to input two keys
# The data plane URL tells RudderStack to use my (Carsmaniac's) account
rudder.data_plane_url = "https://memickledieqb.dataplane.rudderstack.com"

# The write key tells RudderStack to use the Paint Job Packer data source
rudder.write_key = "241vjwkrtUxeaEmHwuzbTaohsnd"

# We also send the current date along with the analytics data
# RudderStack collects this by itself, but because of the way I'm processing the data we need to send it separately from here
# We'll use a library called datetime
from datetime import date

# We can get today's date using a function called today
# It's formatted as YYYY-MM-DD
todays_date = date.today()



# Finally we can send the data off using a function called send_analytics
# "vehicle_list" is the list of vehicle numbers that packer.py sends over
def send_analytics(vehicle_list):

    # Data is sent to RudderStack using a function called track
    rudder.track(

        # RudderStack requires a user ID to be sent, but since Paint Job Packer analytics is anonymous, we'll use the ID 123456
        "123456",

        # Next we need to name the event being tracked
        "Paint Job Packer Analytics",

        # Now we send a dictionary of all the data we've collected
        {
            "Date": todays_date,
            "Version": installed_version,
            "OS": operating_system,
            "Language": system_language,
            "VehicleList": vehicle_list
        })

# The following function only runs if someone tries to run this file as a program
# It instructs them to run packer.py instead, as that's where the actual program is
if __name__ == "__main__":
    print("Run \"packer.py\" to launch Paintjob Packer")
    print("")
    input("Press enter to quit")
