import paintjob, configparser

print("\n"*30)
paintjob.welcome_message()
print("")
print("=== Manual Paintjob Generator ===")
print("")
print("Generating paintjob from preset parameters...")
config = configparser.ConfigParser()
config.read("config.ini")

make = config["ManParams"]["make"]
model = config["ManParams"]["model"]
cabins = config["ManParams"]["cabins"]
cabins = cabins.split(",")

internal_name = config["ManParams"]["internal_name"]

ingame_name = config["ManParams"]["ingame_name"]
price = config["ManParams"]["price"]
unlock_level = config["ManParams"]["unlock_level"]

pack_name = config["ManParams"]["pack_name"]
pack_version = config["ManParams"]["pack_version"]
pack_author = config["ManParams"]["pack_author"]

database_name = config["ManParams"]["database_name"]
vehicle_type = "euro"
new_truck_format = False
# TODO: vehicle_type (if need be) and new_truck_format support

print("Generating paintjob for %s..." % database_name)

print("Creating folders...")
paintjob.Folders.common_mod_folders()
paintjob.Folders.specific_mod_folders(make=make, model=model, new_truck_format=new_truck_format)
print("Generating definition files...")
paintjob.Files.def_sii(make=make, model=model, cabins=cabins, internal_name=internal_name, ingame_name=ingame_name, price=price, unlock_level=unlock_level)
paintjob.Files.material_mat(internal_name=internal_name)
paintjob.Files.generate_tobj_files(internal_name=internal_name, new_truck_format=new_truck_format)
paintjob.Files.manifest_sii(pack_version=pack_version, pack_name=pack_name, pack_author=pack_author)
print("Copying images...")
paintjob.Files.copy_image_files(mode="man", internal_name=internal_name) # TODO: different file name for man skins, for easy save-compile-testing
print("Copying package files...")
paintjob.Files.copy_mod_package_files(mode="man")
print("Compiling mod...")
paintjob.compile_mod_file()
print("Cleaning up...")
paintjob.Folders.clear_output_folder()
print("Done!")
