import os, shutil, binascii, codecs, configparser

version = "v0.1"

def welcome_message():
    print("Paintjob Packer %s" % version)
    print("Developed with love <3 by Carsmaniac")
    print("https://github.com/Carsmaniac/paintjob-packer")

def convert_string_to_hex(string_input): # returns a hexified version of an input string, e.g. "hello" -> "68656c6c6f"
    if isinstance(string_input, int):
        string_input = bytes([string_input])
    elif isinstance(string_input, str):
        string_input = string_input.encode()
    string_output = binascii.hexlify(string_input) # TEMP: If I need to reverse, unhexlify. If not, delete this comment
    string_output = string_output.decode()
    return string_output

def generate_tobj_string(path, alternate=False):
    if alternate:
        tobj_string = "010AB170000000000000000000000000000000000100000002000303030002020000000000010000" # new_truck_format vehicle
    else:
        tobj_string = "010AB170000000000000000000000000000000000000000002000303030002020000000000883900" # material & non-new_truck_format vehicle
    tobj_string += convert_string_to_hex(len(path))
    tobj_string += "00000000000000"
    tobj_string += convert_string_to_hex(path)
    tobj_file = codecs.decode(tobj_string, "hex_codec")
    return tobj_file

def get_accessory_list(accessory_type, database_name):
    accessories_ini = configparser.ConfigParser()
    accessories_ini.read("accessories.ini")
    return accessories_ini[database_name][accessory_type].split(",")

class Files:
    def def_sii(make, model, cabins, internal_name, ingame_name, price, unlock_level, new_truck_format): # wow that's not confusing at all
        file = open("output/def/vehicle/truck/%s.%s/paint_job/%s.sii" % (make, model, internal_name), "w")
        file.write("SiiNunit\n")
        file.write("{\n")
        file.write("accessory_paint_job_data: %s.%s.%s.paint_job\n" % (internal_name, make, model))
        file.write("{\n")
        file.write('    name:                 "%s"\n' % ingame_name)
        file.write("    price:                %s\n" % price)
        file.write("    unlock:               %s\n" % unlock_level)
        file.write('    icon:                 "%s"\n' % internal_name)
        file.write("    airbrush:             true\n")
        file.write("\n")
        if new_truck_format:
            file.write('    paint_job_mask:       "/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.tobj"\n' % (make, model, internal_name, internal_name))
        else:
            file.write('    paint_job_mask:       "/vehicle/truck/upgrade/paintjob/%s.tobj"\n' % internal_name)
        file.write("\n")
        for each_cabin in cabins:
            file.write('    suitable_for[]: "%s.%s.%s.cabin"\n' % (each_cabin, make, model))
        file.write("}\n")
        file.write("}\n")
        file.close()

    def def_accessory_sii(make, model, internal_name, accessory_name_list, accessory_dict, database_name):
        file = open("output/def/vehicle/truck/%s.%s/paint_job/accessory/%s.sii" % (make, model, internal_name), "w")
        file.write("SiiNunit\n")
        file.write("{\n")
        group_counter = 0
        for group in accessory_name_list:
            file.write("simple_paint_job_data: .ovr%s\n" % group_counter)
            file.write("{\n")
            file.write('    paint_job_mask: "/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.tobj"\n' % (make, model, internal_name, group))
            for accessory_type in accessory_dict:
                if accessory_dict[accessory_type] == str(group_counter):
                    for truck_part in get_accessory_list(accessory_type, database_name):
                        file.write('    acc_list[]: "%s"\n' % truck_part)
            file.write("}\n")
            file.write("\n")
            group_counter += 1
        file.write("}\n")
        file.close()

    def manifest_sii(pack_version, pack_name, pack_author):
        file = open("output/manifest.sii", "w")
        file.write("SiiNunit\n")
        file.write("{\n")
        file.write("mod_package: .package_name\n")
        file.write("{\n")
        file.write('    package_version:  "%s"\n' % pack_version)
        file.write('    display_name:     "%s"\n' % pack_name)
        file.write('    author:           "%s"\n' % pack_author)
        file.write("\n")
        file.write('    category[]:       "paint_job"\n')
        file.write("\n")
        file.write('    icon:             "mod_image.jpg"\n')
        file.write('    description_file: "mod_description.txt"\n')
        file.write("}\n")
        file.write("}\n")
        file.close()

    def material_mat(internal_name):
        file = open("output/material/ui/accessory/%s.mat" % internal_name, "w")
        file.write('material: "ui"\n')
        file.write("{\n")
        file.write('    texture:      "%s.tobj"\n' % internal_name)
        file.write('    texture_name: "texture"\n')
        file.write("}\n")
        file.close()

    def copy_image_files(truck_list, internal_name, new_truck_format, make, model, accessory_name_list):
        input_folder = "input/%s" % truck_list
        shutil.copyfile("%s/icon.dds" % input_folder, "output/material/ui/accessory/%s.dds" % internal_name)
        if new_truck_format:
            shutil.copyfile("%s/%s.dds" % (input_folder, internal_name), "output/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.dds" % (make, model, internal_name, internal_name))
            for accessory_name in accessory_name_list:
                shutil.copyfile("%s/%s.dds" % (input_folder, accessory_name), "output/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.dds" % (make, model, internal_name, accessory_name))
        else:
            shutil.copyfile("%s/%s.dds" % (input_folder, internal_name), "output/vehicle/truck/upgrade/paintjob/%s.dds" % internal_name)

    def copy_mod_package_files(truck_list):
        input_folder = "input/%s" % truck_list
        shutil.copyfile("%s/mod_description.txt" % input_folder, "output/mod_description.txt")
        shutil.copyfile("%s/snoop.txt" % input_folder, "output/Snooping as usual I see.txt") # vitally important file
        shutil.copyfile("%s/mod_image.jpg" % input_folder, "output/mod_image.jpg")

    def generate_tobj_files(internal_name, make, model, new_truck_format, accessory_name_list):
        file = open("output/material/ui/accessory/%s.tobj" % internal_name, "wb")
        file.write(generate_tobj_string("/material/ui/accessory/%s.dds" % internal_name))
        file.close()
        if new_truck_format:
            file = open("output/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.tobj" % (make, model, internal_name, internal_name), "wb")
            file.write(generate_tobj_string("/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.dds" % (make, model, internal_name, internal_name), alternate=True))
            file.close()
            for accessory_name in accessory_name_list:
                file = open("output/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.tobj" % (make, model, internal_name, accessory_name), "wb")
                file.write(generate_tobj_string("/vehicle/truck/upgrade/paintjob/%s_%s/%s/%s.dds" % (make, model, internal_name, accessory_name), alternate=True))
                file.close()
        else:
            file = open("output/vehicle/truck/upgrade/paintjob/%s.tobj" % internal_name, "wb")
            file.write(generate_tobj_string("/vehicle/truck/upgrade/paintjob/%s.dds" % internal_name))
            file.close()

class Folders:
    def make_folder(folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def common_mod_folders():
        Folders.make_folder("output")
        Folders.make_folder("output/material/ui/accessory")
        Folders.make_folder("output/vehicle/truck/upgrade/paintjob")

    def specific_mod_folders(make, model, new_truck_format, internal_name):
        Folders.make_folder("output/def/vehicle/truck/%s.%s/paint_job" % (make, model))
        if new_truck_format:
            Folders.make_folder("output/def/vehicle/truck/%s.%s/paint_job/accessory" % (make, model))
            Folders.make_folder("output/vehicle/truck/upgrade/paintjob/%s_%s/%s" % (make, model, internal_name))

    def clear_output_folder():
        shutil.rmtree("output")
        # os.makedirs("output")

def compile_mod_file(truck_list=None):
    shutil.make_archive("paintjob", "zip", "output")
    if truck_list == None:
        mod_name = "Paintjob Packer %s Mod" % version
    else:
        config = configparser.ConfigParser()
        config.read("auto lists/%s.ini" % truck_list)
        mod_name = config["Params"]["list_name"]
    os.rename("paintjob.zip", "%s.scs" % mod_name)
