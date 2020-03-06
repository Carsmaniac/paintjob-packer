import configparser, os, time

uni_ini = configparser.ConfigParser(allow_no_value = True)
uni_ini.read("unifier.ini")

paintjobs_before_unifying = 0
paintjobs_after_unifying = 0

paintjobs = list(uni_ini["paintjobs"].keys())
for pj in paintjobs:
    print("Unifying "+pj)
    vehicles = list(uni_ini[pj].keys())
    for veh in vehicles:
        path = uni_ini[veh]["path"]
        accessories = uni_ini[veh].getboolean("accessories")
        orig_cab_sizes = uni_ini[veh]["cabins"].split(",")
        cab_dict = {}
        tobj_cab_sizes = {}
        for cab_size in orig_cab_sizes:
            cab_name = uni_ini[veh][cab_size]
            cab_dict[cab_size] = cab_name
            file = open("vehicle/truck/upgrade/paintjob/%s/%s/cabin_%s.tobj" % (pj, veh, cab_size), "rb")
            this_tobj = str(file.read())[-6:-5]
            file.close()
            if this_tobj not in tobj_cab_sizes:
                tobj_cab_sizes[this_tobj] = []
            tobj_cab_sizes[this_tobj].append(cab_size)
            os.remove("def/vehicle/truck/%s/paint_job/%s_%s.sii" % (path, pj, cab_size))
            if accessories and cab_size not in tobj_cab_sizes:
                os.remove("def/vehicle/truck/%s/paint_job/accessory/%s_%s.sii" % (path, pj, cab_size))
            paintjobs_before_unifying += 1

        for cab_size in tobj_cab_sizes:
            cab_pj_name = "%s_%s" % (pj, cab_size)
            file = open("def/vehicle/truck/%s/paint_job/%s.sii" % (path, cab_pj_name), "w")
            file.write("SiiNunit\n")
            file.write("{\n")
            file.write("accessory_paint_job_data: %s.%s.paint_job\n" % (cab_pj_name, path))
            file.write("{\n")
            file.write("@include \"%s_settings.sui\"\n" % pj)
            for each_cab in tobj_cab_sizes[cab_size]:
                cab_name = cab_dict[each_cab]
                file.write("    suitable_for[]: \"%s.%s.cabin\"\n" % (cab_name, path))
            file.write("    paint_job_mask: \"/vehicle/truck/upgrade/paintjob/%s/%s/cabin_%s.tobj\"\n" % (pj, veh, cab_size))
            file.write("}\n")
            file.write("}\n")
            file.close()
            paintjobs_after_unifying += 1
print("")
percentage_reduction = str( 100 * ( 1 - ( paintjobs_after_unifying / paintjobs_before_unifying ) ) )[:2]+"%"
print("Total paintjobs reduced from %s to %s (reduction of %s)" % (paintjobs_before_unifying, paintjobs_after_unifying, percentage_reduction))
time.sleep(2)
