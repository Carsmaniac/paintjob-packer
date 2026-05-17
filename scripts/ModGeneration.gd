extends Node

var output_path: String
var workshop_path: String
var template_zip := ZIPReader.new()
var using_templates: bool = true


func _ready() -> void:
	if OS.has_feature("standalone"):
		if FileAccess.file_exists(OS.get_executable_path().get_base_dir() + "/templates.zip"):
			var _error = template_zip.open(OS.get_executable_path().get_base_dir() + "/templates.zip")
		else:
			using_templates = false
	else:
		if FileAccess.file_exists("res://templates.zip"):
			var _error = template_zip.open("res://templates.zip")
		else:
			using_templates = false


func make_folder(path: String) -> void:
	if not DirAccess.dir_exists_absolute(output_path + path):
		DirAccess.make_dir_recursive_absolute(output_path + path)


func extract_file(zip_path: String, file_path: String) -> void:
	if using_templates and template_zip.file_exists(zip_path):
		var file := FileAccess.open(output_path + file_path, FileAccess.WRITE)
		file.store_buffer(template_zip.read_file(zip_path))
	else:
		var placeholder_folder := DirAccess.open("res://placeholders")
		placeholder_folder.copy("res://placeholders/empty.dds", output_path + file_path)


func int_to_hex(input: int) -> String:
	var hex_num: String = String.num_uint64(input, 16, true)
	if len(hex_num) == 1:
		hex_num = "0" + hex_num
		# This is in case the dds path is shorter than 16 characters
		# If over 255, we're toast anyway
	return hex_num


func string_to_hex(input: String) -> String:
	var hex: String = ""
	for character in input:
		hex += String.num_uint64(int(ord(character)), 16, true)
	return hex


func make_tobj(dds_path: String, path: String) -> void:
	var tobj_string: String = "010AB170000000000000000000000000000000000100020002000303030002020001000000010000"
	tobj_string += int_to_hex(len(dds_path) + 1)
	tobj_string += "00000000000000"
	tobj_string += string_to_hex("/" + dds_path)
	var file := FileAccess.open(output_path + path, FileAccess.WRITE)
	if len(tobj_string) % 2 == 0:
		for i in range(len(tobj_string) / 2.0):
			file.store_8(("0x" + tobj_string.substr(i * 2, 2)).hex_to_int())


func make_workshop_folder() -> void:
	make_folder("Workshop Uploading")


func copy_workshop_files() -> void:
	var placeholder_folder := DirAccess.open("res://placeholders")
	placeholder_folder.copy("res://placeholders/workshop.jpg", workshop_path + "Workshop Image.jpg")
	placeholder_folder.copy("res://placeholders/versions.sii", workshop_path + "versions.sii")


func make_manifest_sii(mod_version: String, mod_name: String, mod_author: String, workshop: bool) -> void:
	var file = FileAccess.open(output_path + "manifest.sii", FileAccess.WRITE)
	file.store_line("SiiNunit")
	file.store_line("{")
	file.store_line("mod_package: .package_name")
	file.store_line("{")
	file.store_line("\tpackage_version: \"%s\"" % mod_version)
	if workshop:
		file.store_line("\tdisplay_name: \"%s\"" % mod_name)
	file.store_line("\tauthor: \"%s\"" % mod_author)
	file.store_line("")
	file.store_line("\tcategory[]: \"paint_job\"")
	file.store_line("")
	file.store_line("\ticon: \"Image.jpg\"")
	file.store_line("\tdescription_file: \"Description.txt\"")
	file.store_line("}")
	file.store_line("}")


func make_description_file(mod_description: String) -> void:
	var file = FileAccess.open(output_path + "Description.txt", FileAccess.WRITE)
	file.store_line(mod_description)


func copy_mod_image() -> void:
	var placeholder_folder := DirAccess.open("res://placeholders")
	placeholder_folder.copy("res://placeholders/mod-manager.jpg", "%sImage.jpg" % output_path)


func make_material_folder() -> void:
	make_folder("material/ui/accessory")


func make_paint_job_folder(paint_job_name: String) -> void:
	make_folder(paint_job_name)


func copy_paint_job_icon(paint_job_name: String) -> void:
	var placeholder_folder := DirAccess.open("res://placeholders")
	placeholder_folder.copy("res://placeholders/icon.dds", "%s%s/Icon.dds" % [output_path, paint_job_name])


func make_paint_job_icon_tobj(paint_job_name: String, internal_name: String) -> void:
	make_tobj("%s/Icon.dds" % paint_job_name, "material/ui/accessory/%s_icon.tobj" % internal_name)


func make_paint_job_icon_mat(internal_name: String) -> void:
	var file := FileAccess.open(output_path + "material/ui/accessory/%s_icon.mat" % internal_name, FileAccess.WRITE)
	file.store_line("material: \"ui\"")
	file.store_line("{")
	file.store_line("\ttexture: \"%s_icon.tobj\"" % internal_name)
	file.store_line("\ttexture_name: \"texture\"")
	file.store_line("}")


func make_def_folder(vehicle_dict: Dictionary) -> void:
	if vehicle_dict["uses_accessories"]:
		make_folder("def/vehicle/%s/%s/paint_job/accessory" % [vehicle_dict["type"], vehicle_dict["path"]])
	else:
		make_folder("def/vehicle/%s/%s/paint_job" % [vehicle_dict["type"], vehicle_dict["path"]])


func make_def_sii(vehicle_dict: Dictionary, paint_job_name: String, internal_name: String, indiv_name: String, cabins: Array, main_dds_name: String) -> void:
	var file := FileAccess.open(output_path + "def/vehicle/%s/%s/paint_job/%s.sii" % [vehicle_dict["type"], vehicle_dict["path"], indiv_name], FileAccess.WRITE)
	file.store_line("SiiNunit")
	file.store_line("{")
	file.store_line("accessory_paint_job_data: %s.%s.paint_job" % [indiv_name, vehicle_dict["path"]])
	file.store_line("{")
	file.store_line("@include \"%s_settings.sui\"" % internal_name)
	if vehicle_dict["separate_paint_jobs"]:
		for cabin in cabins:
			for cabin_internal in cabin["internal_name"]:
				file.store_line("\tsuitable_for[]: \"%s.%s.cabin\"" % [cabin_internal, vehicle_dict["path"]])
	if vehicle_dict["mod"]:
		file.store_line("\tpaint_job_mask: \"/%s/%s [%s]/%s.tobj\"" % [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], main_dds_name])
	else:
		file.store_line("\tpaint_job_mask: \"/%s/%s/%s.tobj\"" % [paint_job_name, vehicle_dict["name"], main_dds_name])
	file.store_line("}")
	file.store_line("}")


func make_settings_sui(vehicle_dict: Dictionary, internal_name: String, paint_job_name: String, price: int, unlock_level: int, advanced: Dictionary) -> void:
	var file := FileAccess.open(output_path + "def/vehicle/%s/%s/paint_job/%s_settings.sui" % [vehicle_dict["type"], vehicle_dict["path"], internal_name], FileAccess.WRITE)
	file.store_line("\tname: \"%s\"" % paint_job_name)
	file.store_line("\tprice: %s" % str(price))
	file.store_line("\tunlock: %s" % str(unlock_level))
	file.store_line("\ticon: \"%s_icon\"" % internal_name)
	if advanced["changeable_enabled"]:
		file.store_line("\tairbrush: false")
	else:
		file.store_line("\tairbrush: true")
	file.store_line("\tbase_color: %s" % advanced["base_colour"])
	if vehicle_dict["colour_picker"] or advanced["base_colour_unlocked"]:
		file.store_line("\tbase_color_locked: false")
	if advanced["changeable_enabled"]:
		if advanced["changeable1_enabled"]:
			file.store_line("\tmask_r_color: %s" % advanced["changeable1_colour"])
			file.store_line("\tmask_r_locked: %s" % str(not advanced["changeable1_unlocked"]))
		if advanced["changeable2_enabled"]:
			file.store_line("\tmask_g_color: %s" % advanced["changeable2_colour"])
			file.store_line("\tmask_g_locked: %s" % str(not advanced["changeable2_unlocked"]))
		if advanced["changeable3_enabled"]:
			file.store_line("\tmask_b_color: %s" % advanced["changeable3_colour"])
			file.store_line("\tmask_b_locked: %s" % str(not advanced["changeable3_unlocked"]))
	if vehicle_dict["alt_uv"]:
		file.store_line("\talternate_uvset: true")


func make_accessory_sii(vehicle_dict: Dictionary, paint_job_name: String, indiv_name: String) -> void:
	var file := FileAccess.open(output_path + "def/vehicle/%s/%s/paint_job/accessory/%s.sii" % [vehicle_dict["type"], vehicle_dict["path"], indiv_name], FileAccess.WRITE)
	file.store_line("SiiNunit")
	file.store_line("{")
	var ovr_counter: int = 0
	for acc_group in vehicle_dict["accessories"].keys():
		file.store_line("")
		file.store_line("simple_paint_job_data: .ovr" + str(ovr_counter))
		file.store_line("{")
		if vehicle_dict["mod"]:
			file.store_line("\tpaint_job_mask: \"/%s/%s [%s]/%s.tobj\"" % [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], acc_group])
		else:
			file.store_line("\tpaint_job_mask: \"/%s/%s/%s.tobj\"" % [paint_job_name, vehicle_dict["name"], acc_group])
		for acc in vehicle_dict["accessories"][acc_group]:
			file.store_line("\tacc_list[]: \"%s\"" % acc)
		file.store_line("}")
		ovr_counter += 1
	file.store_line("}")


func make_vehicle_folder(vehicle_dict: Dictionary, paint_job_name: String) -> void:
	if vehicle_dict["mod"]:
		make_folder("%s/%s [%s]" % [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"]])
	else:
		make_folder("%s/%s" % [paint_job_name, vehicle_dict["name"]])


func copy_main_dds(game: String, vehicle_dict: Dictionary, paint_job_name: String, source_dds_name: String, output_dds_name: String) -> void:
	if vehicle_dict["mod"]:
		extract_file("%s/%s/%s.dds" % [game, vehicle_dict["file_path"], source_dds_name], "%s/%s [%s]/%s.dds"% [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], output_dds_name])
	else:
		extract_file("%s/%s/%s.dds" % [game, vehicle_dict["file_path"], source_dds_name], "%s/%s/%s.dds"% [paint_job_name, vehicle_dict["name"], output_dds_name])


func make_main_tobj(paint_job_name: String, vehicle_dict: Dictionary, source_dds_name: String, output_dds_name: String) -> void:
	if vehicle_dict["mod"]:
		make_tobj("%s/%s [%s]/%s.dds"% [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], source_dds_name], "%s/%s [%s]/%s.tobj"% [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], output_dds_name])
	else:
		make_tobj("%s/%s/%s.dds"% [paint_job_name, vehicle_dict["name"], output_dds_name], "%s/%s/%s.tobj"% [paint_job_name, vehicle_dict["name"], output_dds_name])


func copy_accessory_dds(game: String, vehicle_dict: Dictionary, paint_job_name: String) -> void:
	for accessory_group in vehicle_dict["accessories"]:
		if vehicle_dict["mod"]:
			extract_file("%s/%s/%s.dds" % [game, vehicle_dict["file_path"], accessory_group], "%s/%s [%s]/%s.dds" % [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], accessory_group])
		else:
			extract_file("%s/%s/%s.dds" % [game, vehicle_dict["file_path"], accessory_group], "%s/%s/%s.dds" % [paint_job_name, vehicle_dict["name"], accessory_group])


func make_accessory_tobj(vehicle_dict: Dictionary, paint_job_name: String) -> void:
	pass
	for accessory_group in vehicle_dict["accessories"]:
		if vehicle_dict["mod"]:
			make_tobj("%s/%s [%s]/%s.dds" % [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], accessory_group], "%s/%s [%s]/%s.tobj" % [paint_job_name, vehicle_dict["name"], vehicle_dict["mod_author"], accessory_group])
		else:
			make_tobj("%s/%s/%s.dds" % [paint_job_name, vehicle_dict["name"], accessory_group], "%s/%s/%s.tobj" % [paint_job_name, vehicle_dict["name"], accessory_group])


func make_mod(mod_dict: Dictionary, new_output_path: String) -> void:
	output_path = new_output_path
	if mod_dict["workshop"]:
		workshop_path = new_output_path + "Workshop Uploading/"
		make_workshop_folder()
		copy_workshop_files()
		output_path = new_output_path + mod_dict["mod_name"] + "/"
	make_folder("")
	make_manifest_sii(mod_dict["mod_version"], mod_dict["mod_name"], mod_dict["mod_author"], mod_dict["workshop"])
	make_description_file(mod_dict["mod_description"])
	copy_mod_image()
	make_material_folder()
	for paint_job in mod_dict["paint_jobs"]:
		make_paint_job_folder(paint_job["paint_job_name"])
		copy_paint_job_icon(paint_job["paint_job_name"])
		make_paint_job_icon_tobj(paint_job["paint_job_name"], paint_job["internal_name"])
		make_paint_job_icon_mat(paint_job["internal_name"])
		for vehicle in paint_job["vehicles"]:
			make_def_folder(vehicle["vehicle_dict"])
			make_settings_sui(vehicle["vehicle_dict"], paint_job["internal_name"], paint_job["paint_job_name"], paint_job["price"], paint_job["unlock_level"], paint_job["advanced"])
			make_vehicle_folder(vehicle["vehicle_dict"], paint_job["paint_job_name"])
			for indiv in vehicle["indivs"]:
				if vehicle["vehicle_dict"]["uses_accessories"]:
					make_accessory_sii(vehicle["vehicle_dict"], paint_job["paint_job_name"], indiv["indiv_name"])
					copy_accessory_dds(mod_dict["game"], vehicle["vehicle_dict"], paint_job["paint_job_name"])
					make_accessory_tobj(vehicle["vehicle_dict"], paint_job["paint_job_name"])
				make_def_sii(vehicle["vehicle_dict"], paint_job["paint_job_name"], paint_job["internal_name"], indiv["indiv_name"], indiv["cabins"], indiv["output_dds_name"])
				copy_main_dds(mod_dict["game"], vehicle["vehicle_dict"], paint_job["paint_job_name"], indiv["source_dds_name"], indiv["output_dds_name"])
				make_main_tobj(paint_job["paint_job_name"], vehicle["vehicle_dict"], indiv["source_dds_name"], indiv["output_dds_name"])
	var popup := AcceptDialog.new()
	popup.title = tr("EXPORT_DONET")
	popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	popup.dialog_text = tr("EXPORT_DONE") + "\n%s\n\n" % (output_path) + tr("EXPORT_DONE2")
	popup.size.y = 0
	popup.ok_button_text = tr("BUTTON_OKAY")
	popup.get_ok_button().connect("pressed", quit)
	self.add_child(popup)
	popup.popup_centered()


func quit() -> void:
	get_tree().quit()
