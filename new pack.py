from library.paintjob import *

pack = Pack("new")

make_pack(pack)
save_new_pack_to_database(pack)
make_description(pack, False)
make_description(pack, True)
