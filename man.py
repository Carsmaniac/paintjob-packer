import paintjob, configparser

print("\n"*50)
paintjob.welcome_message()
print("")
print("=== Manual Paintjob Generator ===")
print("")
print("Generating paintjob from preset parameters...")
manual = configparser.ConfigParser()
manual.read("truck lists/manual.ini")

make = manual["Params"]["make"]
model = manual["Params"]["model"]
cabins = manual["Params"]["cabins"]
cabins = cabins.split(",")

internal_name = manual["Params"]["internal_name"]

ingame_name = manual["Params"]["ingame_name"]
price = manual["Params"]["price"]
unlock_level = manual["Params"]["unlock_level"]

pack_name = manual["Params"]["pack_name"]
pack_version = manual["Params"]["pack_version"]
pack_author = manual["Params"]["pack_author"]

database_name = manual["Params"]["database_name"]
vehicle_type = "euro"
new_truck_format = manual["Params"].getboolean("new_truck_format")
# TODO: vehicle_type (if need be)

if new_truck_format:
    accessory_names = manual["Params"][accessory_names].split(",")
    accessories = dict(item.split("=") for item in manual["Params"][accessories].split(","))

print("Generating paintjob for %s..." % database_name)

print("Creating folders...")
paintjob.Folders.common_mod_folders()
paintjob.Folders.specific_mod_folders(make=make, model=model, new_truck_format=new_truck_format)
print("Generating definition files...")
paintjob.Files.def_sii(make=make, model=model, cabins=cabins, internal_name=internal_name, ingame_name=ingame_name, price=price, unlock_level=unlock_level, new_truck_format=new_truck_format)
if new_truck_format:
    paintjob.Files.def_accessory_sii(make=make, model=model, internal_name=internal_name, accessory_names=accessory_names, accessories=accessories)
paintjob.Files.material_mat(internal_name=internal_name)
paintjob.Files.generate_tobj_files(internal_name=internal_name, new_truck_format=new_truck_format)
paintjob.Files.manifest_sii(pack_version=pack_version, pack_name=pack_name, pack_author=pack_author)
print("Copying images...")
paintjob.Files.copy_image_files(truck_list="manual", internal_name=internal_name, new_truck_format=new_truck_format, make=make, model=models, accessory_names=accessory_names) # TODO: different file name for man skins, for easy save-compile-testing
print("Copying package files...")
paintjob.Files.copy_mod_package_files(truck_list="manual")
print("Compiling mod...")
paintjob.compile_mod_file()
print("Cleaning up...")
paintjob.Folders.clear_output_folder()
print("Done!")
