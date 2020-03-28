import tkinter as tk
from tkinter import messagebox
import configparser, os, sys

root = tk.Tk()
root.state("withdrawn") # I don't think you need to make a Tk() when just using messageboxes, but if one's created automatically I want to make sure it's hidden

paintjobs_before = 0
paintjobs_after = 0

# read ini file
if not os.path.isfile("unifier.ini"):
    messagebox.showerror(title = "File missing", message = "WARNING - File missing: unifier.ini\n\nThe cabin unifier will now quit")
    sys.exit()
uni_ini = configparser.ConfigParser()
uni_ini.read("unifier.ini")

internal_name = uni_ini["paintjob"]["internal name"]
vehicles_to_unify = uni_ini.sections()

# get vehicles from ini file
vehicles = []
for vtu in vehicles_to_unify:
    if vtu != "paintjob":
        cabin_dict = {}
        for cab_size in uni_ini[vtu]["cabins"].split(","):
            cabin_dict[cab_size] = uni_ini[vtu][cab_size]
            paintjobs_before += 1
        vehicles.append({"make_model":vtu,
                         "path":uni_ini[vtu]["path"],
                         "accessories":uni_ini[vtu].getboolean("accessories"),
                         "cabin_dict":cabin_dict})

# determine which DDSs the TOBJs are pointing to
for veh in vehicles:
    veh["tobj_cabin_dict"] = {} # this will contain <cabin_x.dds>:<list of cab_sizes that refer to this dds>
    for cab_size in veh["cabin_dict"]:
        try:
            tobj_file = open("vehicle/truck/upgrade/paintjob/{}/{}/cabin_{}.tobj".format(internal_name, veh["make_model"], cab_size), "rb")
        except FileNotFoundError:
            messagebox.showerror(title = "File missing", message = "WARNING - File missing: vehicle/truck/upgrade/paintjob/{}/{}/cabin_{}.tobj\n\nThe cabin unifier will now quit".format(internal_name, veh["make_model"], cab_size))
            sys.exit()
        else:
            dds_cab_size = str(tobj_file.read())[-6:-5] # gets just the letter of the DDS referred to, e.g. "b" from cabin_b.dds
            tobj_file.close()
            if dds_cab_size not in veh["cabin_dict"]:
                messagebox.showerror(title = "Incorrectly named file", message = "WARNING - Incorrectly named file: vehicle/truck/upgrade/paintjobs/{}/{}/cabin_{}.dds\n\nAll .dds files need to be named similarly to an existing .tobj file, e.g. \"cabin_b.dds\" is fine, but \"cabin_2.dds\" or \"small_cabin.dds\" is not\n\nThe cabin unifier will now quit".format(internal_name, veh["make_model"], dds_cab_size))
                sys.exit()
            if dds_cab_size not in veh["tobj_cabin_dict"]:
                veh["tobj_cabin_dict"][dds_cab_size] = []
            veh["tobj_cabin_dict"][dds_cab_size].append(cab_size)

    # check that all the required files exist
    for cab_size in veh["cabin_dict"]:
        if not os.path.isfile("def/vehicle/truck/{}/paint_job/{}_{}.sii".format(veh["path"], internal_name, cab_size)):
            messagebox.showerror(title = "File missing", message = "WARNING - File missing: def/vehicle/truck/{}/paint_job/{}_{}.sii\n\nThe cabin unifier will now quit".format(veh["path"], internal_name, cab_size))
            sys.exit()
        if veh["accessories"]:
            if not os.path.isfile("def/vehicle/truck/{}/paint_job/accessory/{}_{}.sii".format(veh["path"], internal_name, cab_size)):
                messagebox.showerror(title = "File missing", message = "WARNING - File missing: def/vehicle/truck/{}/paint_job/accessory/{}_{}.sii\n\nThe cabin unifier will now quit".format(veh["path"], internal_name, cab_size))
                sys.exit()

# double check the user wants to proceed before affecting any files, if something goes wrong the blood is on their hands
answer = messagebox.askokcancel(title = "Ready to proceed", message = "Looks like everything's in order, ready to unify {} for {} vehicles\n\nNote that continuing will delete and re-generate a number of .sii files\n\nPress OK to continue".format(internal_name, len(vehicles)))
if not answer:
    sys.exit()

for veh in vehicles:
    # delete old SIIs
    for cab_size in veh["cabin_dict"]:
        os.remove("def/vehicle/truck/{}/paint_job/{}_{}.sii".format(veh["path"], internal_name, cab_size))
        if veh["accessories"] and cab_size not in veh["tobj_cabin_dict"]: # instead of re-generating the accessory files, simply delete the ones no longer required
            os.remove("def/vehicle/truck/{}/paint_job/accessory/{}_{}.sii".format(veh["path"], internal_name, cab_size))

    # generate new SIIs
    for cab_size in veh["tobj_cabin_dict"]:
        file = open("def/vehicle/truck/{}/paint_job/{}_{}.sii".format(veh["path"], internal_name, cab_size), "w")
        file.write("SiiNunit\n")
        file.write("{\n")
        file.write("accessory_paint_job_data: {}_{}.{}.paint_job\n".format(internal_name, cab_size, veh["path"]))
        file.write("{\n")
        file.write("@include \"{}_settings.sui\"\n".format(internal_name))
        for each_cab in veh["tobj_cabin_dict"][cab_size]: # there's the magic, ultimately the unifier is only pushing around suitable_for[] lines and deleting some unneeded files
            file.write("    suitable_for[]: \"{}.{}.cabin\"\n".format(veh["cabin_dict"][each_cab], veh["path"]))
        file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/{}/{}/cabin_{}.tobj\"\n".format(internal_name, veh["make_model"], cab_size))
        file.write("}\n")
        file.write("}\n")
        file.close()
        paintjobs_after += 1

percentage_reduction = str(100 * (1 - (paintjobs_after / paintjobs_before))).split(".")[0]
messagebox.showinfo(title = "All done", message = "Total paintjobs reduced from {} to {} (reduction of {}%)\n\nYou may now delete the cabin unifier and unifier.ini\n\nIf you want to upload your mod to Steam Workshop, you will HAVE to delete them, or the SCS Workshop Uploader will get upset\n\nThe cabin unifier will now quit".format(paintjobs_before, paintjobs_after, percentage_reduction))
sys.exit()
