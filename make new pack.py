import configparser
from library.paintjob import *

clear_output_folder()

pack = Pack("new")

make_manifest_sii(pack)
copy_mod_manager_image()
make_material_folder()

for pj in pack.paintjobs:
    print("")
    print("Making paintjob: "+pj.name)

    copy_paintjob_icon(pj)
    make_paintjob_icon_tobj(pj)
    make_paintjob_icon_mat(pj)

    for veh in pj.vehicles:
        print("Adding vehicle: "+veh.name)

        make_def_folder(veh)
        make_settings_sui(veh, pj)
        make_vehicle_folder(veh, pj)
        copy_shared_colour_dds(veh, pj)
        make_shared_colour_tobj(veh, pj)

        if veh.separate_paintjobs:
            for cab in veh.cabins:
                cab_size = cab
                cab_name = veh.cabins[cab]
                make_cabin_sii(veh, pj, cab_size, cab_name)
                make_cabin_tobj(pj, veh, cab_size)
                if veh.uses_accessories:
                    make_cabin_acc_sii(veh, pj, cab_size)
        else:
            make_only_sii(veh, pj)
            make_only_tobj(pj, veh)
            if veh.uses_accessories:
                make_only_acc_sii(veh, pj)

        if not veh.trailer:
            copy_cabin_dds(pj, veh)

        if veh.uses_accessories:
            make_acc_tobj(veh, pj)

print("")
print("Finished")
