extends Control

var status_array: PackedStringArray = [tr("EXPORT_SELECT"), "", ""]
var valid_folder: bool = false
var mod_name: String
var current_path: String = ""


func try_desktop_folder() -> void:
	var desktop_dir: String = DirAccess.open(OS.get_user_data_dir() + "/../../../../../Desktop/").get_current_dir()
	if DirAccess.dir_exists_absolute(desktop_dir):
		if not DirAccess.dir_exists_absolute(desktop_dir + "/" + get_node("../ModInfoScreen/Panel/Name/TextInput").text):
			current_path = desktop_dir
	update_localisation()


func update_values() -> void:
	change_image(get_node("Panel/PlaceholderDropdown").selected)
	change_status("")
	change_warning()
	if mod_name != get_node("../ModInfoScreen/Panel/Name/TextInput").text:
		verify_path(current_path)


func change_image(dropdown_index: int) -> void:
	var game: String = get_node("..").loaded_game
	get_node("Panel/PlaceholderImageATS").visible = false
	get_node("Panel/PlaceholderImageETS").visible = false
	get_node("Panel/TemplateImageATS").visible = false
	get_node("Panel/TemplateImageETS").visible = false
	if dropdown_index == 0 and game == "ats":
		get_node("Panel/PlaceholderImageATS").visible = true
	elif dropdown_index == 0 and game == "ets":
		get_node("Panel/PlaceholderImageETS").visible = true
	elif dropdown_index == 1 and game == "ats":
		get_node("Panel/TemplateImageATS").visible = true
	elif dropdown_index == 1 and game == "ets":
		get_node("Panel/TemplateImageETS").visible = true


func choose_path() -> void:
	var export_window := FileDialog.new()
	export_window.title = tr("EXPORT_TTILE")
	export_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	export_window.use_native_dialog = true
	export_window.file_mode = FileDialog.FILE_MODE_OPEN_DIR
	export_window.connect("dir_selected", verify_path)
	get_node("..").add_child(export_window)
	export_window.popup_file_dialog()


func verify_path(file_path: String) -> void:
	mod_name = get_node("../ModInfoScreen/Panel/Name/TextInput").text
	if file_path != "":
		if not DirAccess.dir_exists_absolute(file_path + "/" + mod_name):
			valid_folder = true
			current_path = file_path
		else:
			valid_folder = false
			current_path = ""
			var popup := AcceptDialog.new()
			popup.title = tr("EXPORT_EXISTST")
			popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
			popup.dialog_text = tr("EXPORT_EXISTS") % (file_path + "/" + mod_name) + "\n\n" + tr("EXPORT_EXISTS2") % mod_name + "\n"
			popup.size.y = 0
			popup.ok_button_text = tr("BUTTON_OKAY")
			self.add_child(popup)
			popup.popup_centered()
		update_values()


func change_warning() -> void:
	if current_path == "":
		get_node("Panel/LocationLabel").text = tr("EXPORT_SELECT")
	else:
		get_node("Panel/LocationLabel").text = tr("EXPORT_FOLDER") % (current_path + "/" + mod_name)
	if valid_folder:
		get_node("Panel/WarningLabel").text = tr("EXPORT_CREATE") % mod_name
	else:
		get_node("Panel/WarningLabel").text = ""


func change_status(new_message: String = "") -> void:
	if new_message == "":
		if valid_folder:
			status_array = PackedStringArray([tr("EXPORT_READY"), "", ""])
			get_node("Panel/ExportButton").disabled = false
		else:
			status_array = PackedStringArray([tr("EXPORT_SELECT"), "", ""])
			get_node("Panel/ExportButton").disabled = true
	else:
		var __ = status_array.insert(0, new_message)
		status_array.remove_at(3)
	get_node("Panel/StatusLabel").text = "\n".join(status_array)


func update_localisation() -> void:
	change_status()
	change_warning()


func convert_to_scs(colour: Color) -> String:
	# From Drive Safely's website
	# Formula help from knox_xss
	var red: float = colour.r
	var green: float = colour.g
	var blue: float = colour.b
	for element in [red, green, blue]:
		if element >= 0.04045:
			element = (element + 0.055) / 1.055
			element = element ** 2.4
		else:
			element = element / 12.92
	return "(%s, %s, %s)" % [String.num(red, 4), String.num(green, 4), String.num(blue, 4)]


func export_mod() -> void:
	var mod_panel: Node = get_node("../ModInfoScreen/Panel")
	var mod_dict: Dictionary = {
		"mod_name": mod_panel.get_node("Name/TextInput").text,
		"mod_author": mod_panel.get_node("Author/TextInput").text,
		"mod_version": mod_panel.get_node("Version/TextInput").text,
		"mod_description": mod_panel.get_node("Description/TextBox").text,
		"game": get_node("..").loaded_game,
		"paint_jobs": []
	}
	if get_node("Panel/WorkshopDropdown").selected == 0:
		mod_dict["workshop"] = false
	else:
		mod_dict["workshop"] = true
	for paint_job_tab in get_node("../MainScreen/PaintJobTabContainer").get_children():
		if paint_job_tab.name != "+":
			var paint_job_dict: Dictionary = {
				"paint_job_name": paint_job_tab.get_node("Name/TextInput").text,
				"price": int(paint_job_tab.get_node("Price/NumberInput").value),
				"unlock_level": int(paint_job_tab.get_node("Unlock/NumberInput").value),
				"internal_name": paint_job_tab.get_node("InternalName/TextInput").text,
				"advanced": {
					"base_colour": convert_to_scs(paint_job_tab.get_node("AdvancedTab/BaseColour").color),
					"base_colour_unlocked": paint_job_tab.get_node("AdvancedTab/BaseChangeable").button_pressed,
					"changeable_enabled": paint_job_tab.get_node("AdvancedTab/ChangeableEnabled").button_pressed,
					"changeable1_enabled": paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable1/EnableCheckbox").button_pressed,
					"changeable1_colour": convert_to_scs(paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable1/Enabled/ColourButton").color),
					"changeable1_unlocked": paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable1/Enabled/ChangeableCheckbox").button_pressed,
					"changeable2_enabled": paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable2/EnableCheckbox").button_pressed,
					"changeable2_colour": convert_to_scs(paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable2/Enabled/ColourButton").color),
					"changeable2_unlocked": paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable2/Enabled/ChangeableCheckbox").button_pressed,
					"changeable3_enabled": paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable3/EnableCheckbox").button_pressed,
					"changeable3_colour": convert_to_scs(paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable3/Enabled/ColourButton").color),
					"changeable3_unlocked": paint_job_tab.get_node("AdvancedTab/ChangeableControls/Changeable3/Enabled/ChangeableCheckbox").button_pressed
				},
				"vehicles": []
			}
			if paint_job_tab.get_node("CabinSupport/DropdownInput").selected == 0:
				paint_job_dict["cabins"] = "largest"
			elif paint_job_tab.get_node("CabinSupport/DropdownInput").selected == 1:
				paint_job_dict["cabins"] = "all"
			elif paint_job_tab.get_node("CabinSupport/DropdownInput").selected == 2:
				paint_job_dict["cabins"] = "selected"
			if paint_job_tab.get_node("SplitPaintJobs/DropdownInput").selected == 0:
				paint_job_dict["split"] = false
			else:
				paint_job_dict["split"] = true
			for vehicle_tab in paint_job_tab.get_node("VehicleTabContainer").get_children():
				for vehicle_selection in vehicle_tab.get_node("ScrollContainer/VBoxContainer").get_children():
					if vehicle_selection.find_child("VehicleCheckbox").button_pressed:
						var vehicle_dict: Dictionary = {
							"vehicle_dict": vehicle_selection.vehicle_dict,
							"indivs": []
						}
						var selected_cabin_dicts: Array[Dictionary]
						if not vehicle_selection.vehicle_dict["trailer"]:
							var selected_cabins: PackedStringArray
							for cabin in vehicle_selection.find_child("CabinsContainer").get_children():
								if cabin.button_pressed:
									selected_cabins.append("Cabin " + cabin.text)
							for cabin_dict in vehicle_selection.vehicle_dict["cabins"]:
								if cabin_dict["designation"] in selected_cabins:
									selected_cabin_dicts.append(cabin_dict)
						if paint_job_dict["split"] and not vehicle_selection.vehicle_dict["trailer"]:
							for cabin_dict in selected_cabin_dicts:
								var indiv_dict: Dictionary = {
									"cabins": [cabin_dict]
								}
								vehicle_dict["indivs"].append(indiv_dict)
						else:
							var indiv_dict: Dictionary = {
								"cabins": selected_cabin_dicts
							}
							vehicle_dict["indivs"].append(indiv_dict)
						for indiv_dict in vehicle_dict["indivs"]:
							if paint_job_dict["split"]:
								indiv_dict["indiv_name"] = paint_job_dict["internal_name"] + "_" + indiv_dict["cabins"][0]["code"]
							else:
								indiv_dict["indiv_name"] = paint_job_dict["internal_name"]
							var source_main_dds: String
							var output_main_dds: String
							if vehicle_selection.vehicle_dict["trailer"]:
								if vehicle_selection.vehicle_dict["uses_accessories"]:
									source_main_dds = "Base"
									output_main_dds = source_main_dds
								else:
									source_main_dds = vehicle_selection.vehicle_dict["name"]
									output_main_dds = source_main_dds
							else:
								if paint_job_dict["split"] and vehicle_dict["vehicle_dict"]["separate_paint_jobs"]:
									if vehicle_dict["vehicle_dict"]["alt_uv"]:
										source_main_dds = "%s (%s, alt uvset)" % [indiv_dict["cabins"][0]["designation"], indiv_dict["cabins"][0]["name"]]
									else:
										source_main_dds = "%s (%s)" % [indiv_dict["cabins"][0]["designation"], indiv_dict["cabins"][0]["name"]]
									output_main_dds = source_main_dds
								else:
									if vehicle_dict["vehicle_dict"]["alt_uv"]:
										source_main_dds = "%s (%s, alt uvset)" % [vehicle_dict["vehicle_dict"]["cabins"][0]["designation"], vehicle_dict["vehicle_dict"]["cabins"][0]["name"]]
									else:
										source_main_dds = "%s (%s)" % [vehicle_dict["vehicle_dict"]["cabins"][0]["designation"], vehicle_dict["vehicle_dict"]["cabins"][0]["name"]]
									if vehicle_selection.vehicle_dict["uses_accessories"]:
										output_main_dds = "Cabin"
									else:
										output_main_dds = vehicle_selection.vehicle_dict["name"]
							indiv_dict["source_dds_name"] = source_main_dds
							indiv_dict["output_dds_name"] = output_main_dds
						paint_job_dict["vehicles"].append(vehicle_dict)
			mod_dict["paint_jobs"].append(paint_job_dict)
	ModGeneration.make_mod(mod_dict, current_path + "/" + mod_name + "/")
