import os, shutil

class Vehicle:
    def example_variables():
        make = "scania"
        model = "r"
        vehicle_path = "scania.r"
        alt_uvset = False
        name = "Scania R 2009"
        trailer = False
        mod = False
        mod_author = ""
        mod_link = ""
        accessories = True
        cabins = {"a":"topline","b":"highline","c":"normal","8":"tl_8x4"}
        acc_dict = {"rear_bumper":["r_bumper.arbumpermg01","r_bumper.arbumpermg03"],
                    "chassis_cover":["r_chs_cover.chscmg4x203","r_chs_cover.chscmg6x203","r_chs_cover.chscmg6x2403"]}

class Pack:
    def example_variables():
        name = "XPO Logistics Paintjob Pack"
        version = "v1.0"
        game = "ets"
        paintjobs = ["xpo","xpow","waxpo","waxpow"]
        main_paintjob = "xpo"
        related_mods = {"norbert":"A French logistics company that...","globex":"A totally unrelated mod"}
        link = "http://etcetc"
        suggested_by = ["bobman302","that guy"]
        description = "XPO Logistics is an American company....."
        more_info = "XPO uses many paintjobs...."

def clear_output_folder():
    print("Clearing output folder")
    shutil.rmtree("output")
    os.makedirs("output")

def make_folder(path):
    if not os.path.exists("output/" + path):
        os.makedirs("output/" + path)

def make_material_folder():
    make_folder("material/ui/accessory/paintjob_icons")

def get_ini_list(list_string):
    out_list = list_string.split(",")
    for item in out_list:
        pass
