extends Node


func get_dict_from_tab(paint_job: Node, tab_index: int) -> Dictionary:
	var vehicle_dict: Dictionary = {}
	for vehicle in paint_job.find_child("VehicleTabContainer").get_tab_control(tab_index).find_child("ScrollContainer").find_child("VBoxContainer").get_children():
		if vehicle.find_child("TwoColumns").find_child("LeftColumnPadding").find_child("VehicleCheckbox").button_pressed:
			var cabin_list: PackedStringArray = []
			for cabin in vehicle.find_child("TwoColumns").find_child("RightColumnPadding").find_child("RightColumn").find_child("CabinsContainer").get_children():
				if cabin.button_pressed:
					cabin_list.append(cabin.text)
			vehicle_dict["%s/%s" % [vehicle.author_name, vehicle.vehicle_name]] = cabin_list
	return vehicle_dict


func get_list_from_tab(paint_job: Node, tab_index: int) -> PackedStringArray:
	var vehicle_list: PackedStringArray = []
	for vehicle in paint_job.find_child("VehicleTabContainer").get_tab_control(tab_index).find_child("ScrollContainer").find_child("VBoxContainer").get_children():
		if vehicle.find_child("TwoColumns").find_child("LeftColumnPadding").find_child("VehicleCheckbox").button_pressed:
			vehicle_list.append("%s/%s" % [vehicle.author_name, vehicle.vehicle_name])
	return vehicle_list


func confirm_return() -> void:
	var confirm_window := AcceptDialog.new()
	confirm_window.ok_button_text = tr("BUTTON_CONFIRM")
	confirm_window.add_cancel_button(tr("BUTTON_NEVERMIND"))
	confirm_window.title = tr("CONFIRM_STARTT")
	confirm_window.dialog_text = "%s\n\n%s\n" % [tr("CONFIRM_START"), tr("CONFIRM_TEXT")]
	confirm_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	confirm_window.get_ok_button().connect("pressed", return_to_start)
	get_node("../ScreenLoader").add_child(confirm_window)
	confirm_window.popup_centered()


func return_to_start() -> void:
	get_node("../ScreenLoader").switch_screen(false)


func confirm_load() -> void:
	if get_node("../ScreenLoader").current_screen_index == 0:
		self.load_dialogue()
	else:
		var confirm_window := AcceptDialog.new()
		confirm_window.ok_button_text = tr("BUTTON_CONTINUE")
		confirm_window.add_cancel_button(tr("BUTTON_NEVERMIND"))
		confirm_window.title = tr("CONFIRM_LOADT")
		confirm_window.dialog_text = "%s\n\n%s\n" % [tr("CONFIRM_LOAD"), tr("CONFIRM_TEXT")]
		confirm_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		confirm_window.get_ok_button().connect("pressed", load_dialogue)
		get_node("../ScreenLoader").add_child(confirm_window)
		confirm_window.popup_centered()


func new() -> void:
	get_node("../ScreenLoader").switch_game("none")
	var paint_job_tab_container: Node = get_node("../ScreenLoader/MainScreen/PaintJobTabContainer")
	var paint_jobs: Array[Node] = paint_job_tab_container.get_children()
	paint_jobs.reverse()
	for child in paint_jobs:
		paint_job_tab_container.remove_child(child)
	paint_job_tab_container.add_tab(tr("TAB_NEW"))
	paint_job_tab_container.add_tab("+")
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	mod_screen.find_child("Name").find_child("TextInput").text = ""
	mod_screen.find_child("Author").find_child("TextInput").text = ""
	mod_screen.find_child("Version").find_child("TextInput").text = ""
	mod_screen.find_child("Description").find_child("TextBox").text = ""
	if get_node("../ScreenLoader").current_screen_index == 0:
		get_node("../ScreenLoader").switch_screen(true)


func save_inform() -> void:
	var popup := AcceptDialog.new()
	popup.title = tr("CONFIRM_SAVET")
	popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	popup.dialog_text = "%s\n\n%s\n" % [tr("CONFIRM_SAVE"), tr("CONFIRM_SAVEE")]
	popup.size.y = 0
	popup.ok_button_text = tr("BUTTON_OKAY")
	popup.connect("confirmed", save_dialogue)
	self.add_child(popup)
	popup.popup_centered()


func save_dialogue() -> void:
	var save_window := FileDialog.new()
	save_window.title = tr("SAVE_TITLE")
	save_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	save_window.use_native_dialog = true
	save_window.add_filter("*.pjpproject", "Paint Job Packer project")
	save_window.file_filter_toggle_enabled = false
	save_window.file_mode = FileDialog.FILE_MODE_SAVE_FILE
	save_window.connect("file_selected", verify_save_file_path)
	get_node("../ScreenLoader").add_child(save_window)
	save_window.popup_file_dialog()


func verify_save_file_path(file_path: String) -> void:
	if "." not in file_path.split("/")[-1]:
		file_path += ".pjpproject"
	if file_path.substr(len(file_path) - 11) == ".pjpproject":
		save(file_path)
	else:
		var suggested_path: Array = file_path.split("/")
		var suggested_file_name_array: Array = Array(suggested_path.pop_back().split("."))
		if "." in file_path.split("/")[-1]:
			suggested_file_name_array.pop_back()
		var suggested_file_name: String = ".".join(suggested_file_name_array) + ".pjpproject"
		var invalid_window := AcceptDialog.new()
		invalid_window.title = tr("SAVE_INVALT")
		invalid_window.dialog_text = "%s\n\n%s\n" % [tr("SAVE_INVAL"), tr("SAVE_INVALQ") % suggested_file_name]
		invalid_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		invalid_window.ok_button_text = tr("BUTTON_YES")
		invalid_window.add_cancel_button(tr("BUTTON_NO"))
		invalid_window.get_ok_button().connect("pressed", save.bind("/".join(suggested_path) + "/" + suggested_file_name))
		get_node("../ScreenLoader").add_child(invalid_window)
		invalid_window.popup_centered()


func save(file_path: String) -> void:
	var save_dict: Dictionary = {}
	save_dict["a"] = "Hello! This is a save file. If you edit it, bad things might happen and Paint Job Packer might crash. Continue at your own risk :)"
	save_dict["save_data_version"] = 2
	# 2: added [mod_info][vehicle_list]
	
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	var mod_info: Dictionary = {
		mod_name = mod_screen.find_child("Name").find_child("TextInput").text,
		author = mod_screen.find_child("Author").find_child("TextInput").text,
		version = mod_screen.find_child("Version").find_child("TextInput").text,
		vehicle_list = mod_screen.find_child("Description").find_child("CheckboxInput").button_pressed,
		description = mod_screen.find_child("Description").find_child("TextBox").text,
		game = get_node("../ScreenLoader").loaded_game
	}
	save_dict["mod_info"] = mod_info
	
	var paint_jobs: Array[Dictionary] = []
	for paint_job in get_node("../ScreenLoader/MainScreen/PaintJobTabContainer").get_children():
		if paint_job.name != "+":
			var paint_job_dict: Dictionary = {
				paint_job_name = paint_job.find_child("Name").find_child("TextInput").text,
				price = paint_job.find_child("Price").find_child("NumberInput").value,
				unlocked_by_default = paint_job.find_child("Unlock").find_child("CheckboxInput").button_pressed,
				unlock_level = paint_job.find_child("Unlock").find_child("NumberInput").value,
				internal_name = paint_job.find_child("InternalName").find_child("TextInput").text,
				cabin_support = paint_job.find_child("CabinSupport").find_child("DropdownInput").selected,
				split_cabins = paint_job.find_child("SplitPaintJobs").find_child("DropdownInput").selected,
				trucks = get_dict_from_tab(paint_job, 0),
				trailers = get_list_from_tab(paint_job, 1),
				truck_mods = get_dict_from_tab(paint_job, 2),
				trailer_mods = get_list_from_tab(paint_job, 3)
			}
			if mod_info["game"] == "ets":
				paint_job_dict["bus_mods"] = get_dict_from_tab(paint_job, 4) # TODO: don't hardcode this to ets
			paint_job_dict["advanced"] = {
				base_colour = var_to_str(paint_job.get_node("AdvancedTab/BaseColour").color),
				base_colour_unlocked = paint_job.get_node("AdvancedTab/BaseChangeable").button_pressed,
				changeable_enabled = paint_job.get_node("AdvancedTab/ChangeableEnabled").button_pressed,
				changeable1_enabled = paint_job.get_node("AdvancedTab/ChangeableControls/Changeable1/EnableCheckbox").button_pressed,
				changeable1_colour = var_to_str(paint_job.get_node("AdvancedTab/ChangeableControls/Enabled1/ColourButton").color),
				changeable1_unlocked = paint_job.get_node("AdvancedTab/ChangeableControls/Enabled1/ChangeableCheckbox").button_pressed,
				changeable2_enabled = paint_job.get_node("AdvancedTab/ChangeableControls/Changeable2/EnableCheckbox").button_pressed,
				changeable2_colour = var_to_str(paint_job.get_node("AdvancedTab/ChangeableControls/Enabled2/ColourButton").color),
				changeable2_unlocked = paint_job.get_node("AdvancedTab/ChangeableControls/Enabled2/ChangeableCheckbox").button_pressed,
				changeable3_enabled = paint_job.get_node("AdvancedTab/ChangeableControls/Changeable3/EnableCheckbox").button_pressed,
				changeable3_colour = var_to_str(paint_job.get_node("AdvancedTab/ChangeableControls/Enabled3/ColourButton").color),
				changeable3_unlocked = paint_job.get_node("AdvancedTab/ChangeableControls/Enabled3/ChangeableCheckbox").button_pressed
			}
			paint_jobs.append(paint_job_dict)
	save_dict["paint_jobs"] = paint_jobs
	
	FileAccess.open(file_path, FileAccess.WRITE).store_line(JSON.stringify(save_dict, "\t"))


func load_dialogue() -> void:
	var load_window := FileDialog.new()
	load_window.title = (tr("LOAD_TITLE"))
	load_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	load_window.use_native_dialog = true
	load_window.add_filter("*.pjpproject", "Paint Job Packer project")
	load_window.file_filter_toggle_enabled = false
	load_window.overwrite_warning_enabled = false
	load_window.file_mode = FileDialog.FILE_MODE_OPEN_FILE
	load_window.connect("file_selected", verify_loaded_file)
	get_node("../ScreenLoader").add_child(load_window)
	load_window.popup_file_dialog()


func verify_loaded_file(file_path: String) -> void:
	var json_data := JSON.new()
	if file_path.substr(len(file_path) - 11) == ".pjpproject" and json_data.parse(FileAccess.get_file_as_string(file_path)) == OK:
		self.load(file_path)
	else:
		var invalid_window := AcceptDialog.new()
		invalid_window.title = tr("SAVE_INVALT")
		invalid_window.dialog_text = "%s\n\n%s\n" % [tr("SAVE_INVAL"), tr("LOAD_INVAL")]
		invalid_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		get_node("../ScreenLoader").add_child(invalid_window)


func load(file_path: String) -> void:
	var loaded_dict: Dictionary
	var json_data := JSON.new()
	if json_data.parse(FileAccess.get_file_as_string(file_path)) == OK:
		if json_data.data is Dictionary:
			loaded_dict = json_data.data
		
	VehicleDatabase.load_vehicle_lists(loaded_dict["mod_info"]["game"])
	
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	mod_screen.find_child("Name").find_child("TextInput").text = loaded_dict["mod_info"]["mod_name"]
	mod_screen.find_child("Author").find_child("TextInput").text = loaded_dict["mod_info"]["author"]
	mod_screen.find_child("Version").find_child("TextInput").text = loaded_dict["mod_info"]["version"]
	if loaded_dict["save_data_version"] >= 2:
		mod_screen.find_child("Description").find_child("CheckboxInput").button_pressed = loaded_dict["mod_info"]["vehicle_list"]
	else:
		mod_screen.find_child("Description").find_child("CheckboxInput").button_pressed = false
	mod_screen.find_child("Description").find_child("TextBox").text = loaded_dict["mod_info"]["description"]
	get_node("../ScreenLoader").switch_game(loaded_dict["mod_info"]["game"])
	
	var paint_job_tab_container: Node = get_node("../ScreenLoader/MainScreen/PaintJobTabContainer")
	for child in paint_job_tab_container.get_children():
		paint_job_tab_container.remove_child(child)
	for paint_job in loaded_dict["paint_jobs"]:
		paint_job_tab_container.add_tab(paint_job["paint_job_name"])
		var paint_job_node: Node = paint_job_tab_container.get_child(len(paint_job_tab_container.get_children()) - 1)
		paint_job_node.find_child("Name").find_child("TextInput").text = paint_job["paint_job_name"]
		paint_job_node.find_child("Price").find_child("NumberInput").value = paint_job["price"]
		paint_job_node.find_child("Unlock").find_child("CheckboxInput").button_pressed = paint_job["unlocked_by_default"]
		paint_job_node.find_child("Unlock").find_child("NumberInput").value = paint_job["unlock_level"]
		paint_job_node.find_child("InternalName").find_child("TextInput").text = paint_job["internal_name"]
		paint_job_node.find_child("CabinSupport").find_child("DropdownInput").selected = paint_job["cabin_support"]
		paint_job_node.find_child("SplitPaintJobs").find_child("DropdownInput").selected = paint_job["split_cabins"]
		paint_job_node._on_cabin_dropdown_change(paint_job["cabin_support"])
		
		paint_job_node.get_node("AdvancedTab/BaseColour").color = str_to_var(paint_job["advanced"]["base_colour"])
		paint_job_node.get_node("AdvancedTab/BaseChangeable").button_pressed = paint_job["advanced"]["base_colour_unlocked"]
		paint_job_node.get_node("AdvancedTab/ChangeableEnabled").button_pressed = paint_job["advanced"]["changeable_enabled"]
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Changeable1/EnableCheckbox").button_pressed = paint_job["advanced"]["changeable1_enabled"]
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Enabled1/ColourButton").color = str_to_var(paint_job["advanced"]["changeable1_colour"])
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Enabled1/ChangeableCheckbox").button_pressed = paint_job["advanced"]["changeable1_unlocked"]
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Changeable2/EnableCheckbox").button_pressed = paint_job["advanced"]["changeable2_enabled"]
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Enabled2/ColourButton").color = str_to_var(paint_job["advanced"]["changeable2_colour"])
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Enabled2/ChangeableCheckbox").button_pressed = paint_job["advanced"]["changeable2_unlocked"]
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Changeable3/EnableCheckbox").button_pressed = paint_job["advanced"]["changeable3_enabled"]
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Enabled3/ColourButton").color = str_to_var(paint_job["advanced"]["changeable3_colour"])
		paint_job_node.get_node("AdvancedTab/ChangeableControls/Enabled3/ChangeableCheckbox").button_pressed = paint_job["advanced"]["changeable3_unlocked"]

		var truck_tab: Node = paint_job_node.get_node("VehicleTabContainer/Trucks")
		for vehicle in paint_job["trucks"]:
			var vehicle_selection: Node = truck_tab.find_child(vehicle.replace(".", "_").replace("/", "_"), true, false)
			for cab in paint_job["trucks"][vehicle]:
				vehicle_selection.find_child(cab, true, false).button_pressed = true
		var trailer_tab: Node = paint_job_node.get_node("VehicleTabContainer/Trailers")
		for vehicle in paint_job["trailers"]:
			var vehicle_selection: Node = trailer_tab.find_child(vehicle.replace(".", "_").replace("/", "_"), true, false)
			vehicle_selection.find_child("VehicleCheckbox").button_pressed = true
		var truck_mod_tab: Node = paint_job_node.get_node("VehicleTabContainer/Truck Mods")
		for vehicle in paint_job["truck_mods"]:
			var vehicle_selection: Node = truck_mod_tab.find_child(vehicle.replace(".", "_").replace("/", "_"), true, false)
			for cab in paint_job["truck_mods"][vehicle]:
				vehicle_selection.find_child(cab, true, false).button_pressed = true
		var trailer_mod_tab: Node = paint_job_node.get_node("VehicleTabContainer/Trailer Mods")
		for vehicle in paint_job["trailer_mods"]:
			var vehicle_selection: Node = trailer_mod_tab.find_child(vehicle.replace(".", "_").replace("/", "_"), true, false)
			vehicle_selection.find_child("VehicleCheckbox").button_pressed = true
		if loaded_dict["mod_info"]["game"] == "ets":
			var bus_mod_tab: Node = paint_job_node.get_node("VehicleTabContainer/Bus Mods")
			for vehicle in paint_job["bus_mods"]:
				var vehicle_selection: Node = bus_mod_tab.find_child(vehicle.replace(".", "_").replace("/", "_"), true, false)
				for cab in paint_job["bus_mods"][vehicle]:
					vehicle_selection.find_child(cab, true, false).button_pressed = true
					
	if get_node("../ScreenLoader").current_screen_index == 0:
		get_node("../ScreenLoader").switch_screen(true)
