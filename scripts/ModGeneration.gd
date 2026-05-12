extends Node

var output_path: String = "/home/emjay/Desktop/test/"
var templates_path: String


func _ready() -> void:
	if OS.has_feature("standalone"):
		templates_path = OS.get_executable_path().get_base_dir() + "/templates.zip"
	else:
		templates_path = "res://templates.zip"
	#make_tobj("/vehicle/truck/upgrade/paintjob/Paint Job Name/DAF 2021/Cabin A (XG+).dds", "testo.tobj")


func make_folder(path: String) -> void:
	if not DirAccess.dir_exists_absolute(output_path + path):
		DirAccess.make_dir_recursive_absolute(output_path + path)


func int_to_hex(input: int) -> String:
	return String.num_uint64(input, 16, true)


func string_to_hex(input: String) -> String:
	var hex: String = ""
	for character in input:
		hex += String.num_uint64(int(ord(character)), 16, true)
	return hex


func make_tobj(dds_path: String, path: String) -> void:
	var tobj_string: String = "010AB170000000000000000000000000000000000100020002000303030002020001000000010000"
	tobj_string += int_to_hex(len(dds_path))
	tobj_string += "00000000000000"
	tobj_string += string_to_hex(dds_path)
	var file := FileAccess.open(output_path + path, FileAccess.WRITE)
	if len(tobj_string) % 2 == 0:
		for i in range(len(tobj_string) / 2.0):
			file.store_8(("0x" + tobj_string.substr(i * 2, 2)).hex_to_int())


func make_manifest_sii(mod_version: String, mod_name: String, mod_author: String) -> void:
	var file = FileAccess.open(output_path + "manifest.sii", FileAccess.WRITE)
	file.store_line("SiiNunit")
	file.store_line("{")
	file.store_line("mod_package: .package_name")
	file.store_line("{")
	file.store_line("\tpackage_version: \"%s\"" % mod_version)
	file.store_line("\tdisplay_name: \"%s\"" % mod_name)
	file.store_line("\tauthor_name: \"%s\"" % mod_author)
	file.store_line("")
	file.store_line("\tcategory[]: \"paint_job\"")
	file.store_line("\tdescription_file: \"mod_description.txt\"")
	file.store_line("}")
	file.store_line("}")


func make_description_file(mod_description: String) -> void:
	var file = FileAccess.open(output_path + "mod_description.txt", FileAccess.WRITE)
	file.store_line(mod_description)


func make_material_folder() -> void:
	make_folder("material/ui/accessory")


func copy_paint_job_icon(paint_job_name: String) -> void:
	var placeholder_folder := DirAccess.open("res://placeholders")
	placeholder_folder.copy("res://placeholders/icon.dds", "%smaterial/ui/accessory/%s Icon.dds" % [output_path, paint_job_name])


func make_paint_job_icon_tobj(paint_job_name: String) -> void:
	make_tobj("/material/ui/accessory/%s Icon.dds" % paint_job_name, "material/ui/accessory/%s Icon.tobj" % paint_job_name)


func make_paint_job_icon_mat(paint_job_name: String, internal_name: String) -> void:
	var file := FileAccess.open(output_path + "material/ui/accessory/%s_icon.mat" % internal_name, FileAccess.WRITE)
	file.store_line("material: \"ui\"")
	file.store_line("{")
	file.store_line("\ttexture: \"%s Icon.tobj\"" % paint_job_name)
	file.store_line("\ttexture_name: \"texture\"")
	file.store_line("}")


func make_def_folder(vehicle_dict: Dictionary):
	if vehicle_dict["uses_accessories"]:
		make_folder("def/vehicle/%s/%s/paint_job/accessory" % [vehicle_dict["type"], vehicle_dict["path"]])
	else:
		make_folder("def/vehicle/%s/%s/paint_job" % [vehicle_dict["type"], vehicle_dict["path"]])


func make_def_sii(vehicle_dict: Dictionary, paint_job_name: String, internal_name: String, indiv_name: String, cabin_internal_names: PackedStringArray, main_dds_name: String):
	var file := FileAccess.open(output_path + "def/vehicle/%s/%s/paint_job/%s.sii" % [vehicle_dict["type"], vehicle_dict["path"], indiv_name], FileAccess.WRITE)
	file.store_line("SiiNunit")
	file.store_line("{")
	file.store_line("accessory_paint_job_data: %s.%s.paint_job" % [indiv_name, vehicle_dict["path"]])
	file.store_line("{")
	file.store_line("@include \"%s_settings.sui\"" % internal_name)
	for cabin in cabin_internal_names:
		file.store_line("\tsuitable_for[]: \"%s.%s.cabin" % [cabin, vehicle_dict["path"]])
	if vehicle_dict["mod"]:
		file.store_line("\tpaint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s [%s]/%s.tobj" % [vehicle_dict["type"], paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], main_dds_name])
	else:
		file.store_line("\tpaint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s/%s.tobj" % [vehicle_dict["type"], paint_job_name, vehicle_dict["name"], main_dds_name])
	file.store_line("}")
	file.store_line("}")


func make_settings_sui(vehicle_dict: Dictionary, internal_name: String, paint_job_name: String, price: int, unlock_level: int):
	var file := FileAccess.open(output_path + "def/vehicle/%s/%s/paint_job/%s_settings.sui" % [vehicle_dict["type"], vehicle_dict["path"], internal_name], FileAccess.WRITE)
	file.store_line("\tname: \"%s\"" % paint_job_name)
	file.store_line("\tprice: %s" % str(price))
	file.store_line("\tunlock: %s" % str(unlock_level))
	file.store_line("\tairbrush: true")
	if vehicle_dict["colour_picker"]:
		file.store_line("\tbase_color_locked: false")
	if vehicle_dict["alt_uv"]:
		file.store_line("\talternate_uvset: true")


func make_accessory_sii(vehicle_dict: Dictionary, paint_job_name: String, indiv_name: String):
	var file := FileAccess.open(output_path + "def/vehicle/%s/%s/paint_job/accessory/%s.sii" % [vehicle_dict["type"], vehicle_dict["path"], indiv_name], FileAccess.WRITE)
	file.store_line("SiiNunit")
	file.store_line("{")
	var ovr_counter: int = 0
	for acc_group in vehicle_dict["accessories"].keys():
		file.store_line("")
		file.store_line("simple_paint_job_data: .ovr" + str(ovr_counter))
		file.store_line("{")
		if vehicle_dict["mod"]:
			file.store_line("\tpaint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s [%s]/%s.tobj\"" % [vehicle_dict["type"], paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], acc_group])
		else:
			file.store_line("\tpaint_job_mask: \"/vehicle/%s/upgrade/paintjob/%s/%s/%s.tobj\"" % [vehicle_dict["type"], paint_job_name, vehicle_dict["name"], acc_group])
		for acc in vehicle_dict["accessories"][acc_group]:
			file.store_line("acc_list[]: \"%s\"" % acc)
		file.store_line("}")
		ovr_counter += 1
	file.store_line("}")


func make_vehicle_folder(vehicle_dict, paint_job_name):
	if vehicle_dict["mod"]:
		make_folder("vehicle/%s/upgrade/paintjob/%s/%s [%s]" % [vehicle_dict["type"], paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"]])
	else:
		make_folder("vehicle/%s/upgrade/paintjob/%s/%s" % [vehicle_dict["type"], paint_job_name, vehicle_dict["name"]])


#func copy_main_dds():


func make_mod() -> void:
	"""
	mod_version
	mod_name
	mod_author
	mod_description
	paint_job_name
	internal_name
	vehicle_dict(s)
		indiv_name
		main_dds_name
		[cabin_names]
	"""
	make_manifest_sii("mod_version", "mod_name", "mod_author")
	make_description_file("mod_description")
	make_material_folder()
	for paint_job in []:
		copy_paint_job_icon("paint_job_name")
		make_paint_job_icon_tobj("paint_job_name")
		make_paint_job_icon_mat("paint_job_name", "internal_name")
		for vehicle in []:
			make_def_folder({"vehicle_dict":""})
			make_settings_sui({"vehicle_dict":""}, "internal_name", "paint_job_name", 6000, 0)
			make_vehicle_folder({"vehicle_dict":""}, "paint_job_name")
			for indiv_paint_job in []:
				if vehicle["uses_accessories"]:
					make_accessory_sii({"vehicle_dict": ""}, "paint_job_name", "indiv_name")
				make_def_sii({"vehicle_dict":""}, "paint_job_name", "internal_name", "indiv_name", ["cabin_names"], "main_dds_name")
				
