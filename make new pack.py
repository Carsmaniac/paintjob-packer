import configparser
from library.paintjob import *

print("Reading input file")
input_file = configparser.ConfigParser(allow_no_value = True)
input_file.read("new pack.ini")

game = input_file["pack info"]["game"]

mod_name = input_file["pack info"]["name"]
mod_version = input_file["pack info"]["version"]

list_of_paintjobs = input_file["pack info"]["paintjobs"].split(",")
main_paintjob = input_file["pack info"]["main paintjob"]

related_mods = input_file["pack info"]["related mods"].split(",")
mod_link = input_file["pack info"]["link"]

description = input_file["pack info"]["description"]
more_info = input_file["pack info"]["more info"]
suggested_by = input_file["pack info"]["suggested by"].split(",")
