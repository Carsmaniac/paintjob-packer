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
	confirm_window.ok_button_text = "Confirm"
	confirm_window.add_cancel_button("Nevermind")
	confirm_window.title = "Return to Start?"
	confirm_window.dialog_text = "You will lose all unsaved progress if you return to the start.\n\nAre you sure you want to continue?\n"
	confirm_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	confirm_window.get_ok_button().connect("pressed", return_to_start)
	get_node("../ScreenLoader").add_child(confirm_window)
	confirm_window.popup_centered()


func return_to_start() -> void:
	get_node("../ScreenLoader").switch_screen(false)


func confirm_load() -> void:
	if get_node("../ScreenLoader").current_screen_index == 0:
		self.load()
	else:
		var confirm_window := AcceptDialog.new()
		confirm_window.ok_button_text = "Confirm"
		confirm_window.add_cancel_button("Nevermind")
		confirm_window.title = "Load Project?"
		confirm_window.dialog_text = "You will lose all unsaved progress if you load a project.\n\nAre you sure you want to continue?\n"
		confirm_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		confirm_window.get_ok_button().connect("pressed", load)
		get_node("../ScreenLoader").add_child(confirm_window)
		confirm_window.popup_centered()


func new() -> void:
	get_node("../ScreenLoader").switch_game("none")
	var paint_job_tab_container: Node = get_node("../ScreenLoader/MainScreen/PaintJobTabContainer")
	var paint_jobs: Array[Node] = paint_job_tab_container.get_children()
	paint_jobs.reverse()
	for child in paint_jobs:
		paint_job_tab_container.remove_child(child)
	paint_job_tab_container.add_tab("New Paint Job")
	paint_job_tab_container.add_tab("+")
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	mod_screen.find_child("Name").find_child("TextInput").text = ""
	mod_screen.find_child("Author").find_child("TextInput").text = ""
	mod_screen.find_child("Version").find_child("TextInput").text = ""
	mod_screen.find_child("Description").find_child("TextBox").text = ""
	if get_node("../ScreenLoader").current_screen_index == 0:
		get_node("../ScreenLoader").switch_screen(true)


func save_dialogue() -> void:
	# TODO: explain save is not for mods
	var save_window := FileDialog.new()
	save_window.title = ("Save Project")
	save_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	save_window.use_native_dialog = true
	save_window.add_filter("*.pjpproject", "Paint Job Packer project")
	#save_window.file_mode = FileDialog.FILE_MODE_OPEN_DIR TODO: for export
	save_window.connect("file_selected", verify_save_file_path)
	get_node("../ScreenLoader").add_child(save_window)
	save_window.popup_file_dialog()


func verify_save_file_path(file_path: String) -> void:
	if file_path.substr(len(file_path) - 11) == ".pjpproject":
		save(file_path)
	else:
		var suggested_path: Array = file_path.split("/")
		var suggested_file_name_array: Array = Array(suggested_path.pop_back().split("."))
		if "." in file_path:
			suggested_file_name_array.pop_back()
		var suggested_file_name: String = ".".join(suggested_file_name_array) + ".pjpproject"
		var invalid_window := AcceptDialog.new()
		invalid_window.title = "Not a Valid Project File"
		invalid_window.dialog_text = "Selected file is not a Paint Job Packer project file.\n\nWould you like to save as %s instead?\n" % suggested_file_name
		invalid_window.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
		invalid_window.ok_button_text = "Yes"
		invalid_window.add_cancel_button("No")
		invalid_window.get_ok_button().connect("pressed", save.bind("/".join(suggested_path) + "/" + suggested_file_name))
		get_node("../ScreenLoader").add_child(invalid_window)
		invalid_window.popup_centered()


func save(file_path: String) -> void:
	var save_dict: Dictionary = {}
	save_dict["a"] = "Hello! This is a save file. If you edit it, bad things might happen and Paint Job Packer might crash. Continue at your own risk :)"
	
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	var mod_info: Dictionary = {
		mod_name = mod_screen.find_child("Name").find_child("TextInput").text,
		author = mod_screen.find_child("Author").find_child("TextInput").text,
		version = mod_screen.find_child("Version").find_child("TextInput").text,
		description = mod_screen.find_child("Description").find_child("TextBox").text,
		game = get_node("../ScreenLoader").loaded_game
	}
	save_dict["mod_info"] = mod_info
	
	var paint_jobs: Array[Dictionary] = []
	for paint_job in get_node("../ScreenLoader/MainScreen/PaintJobTabContainer").get_children():
		if paint_job.name != "+":
			var paint_job_dict: Dictionary = {
				paint_job_name = paint_job.find_child("Name").find_child("TextInput").text,
				price = paint_job.find_child("Price").find_child("TextInput").text,
				unlocked_by_default = paint_job.find_child("Unlock").find_child("CheckboxInput").button_pressed,
				unlock_level = paint_job.find_child("Unlock").find_child("TextInput").text,
				internal_name = paint_job.find_child("InternalName").find_child("TextInput").text,
				cabin_support = paint_job.find_child("CabinSupport").find_child("DropdownInput").selected,
				split_cabins = paint_job.find_child("SplitPaintJobs").find_child("DropdownInput").selected,
				trucks = get_dict_from_tab(paint_job, 0),
				trailers = get_list_from_tab(paint_job, 1),
				truck_mods = get_dict_from_tab(paint_job, 2),
				trailer_mods = get_list_from_tab(paint_job, 3)
			}
			if mod_info["game"] == "ets":
				paint_job_dict["bus_mods"] = get_dict_from_tab(paint_job, 4)
			paint_jobs.append(paint_job_dict)
	save_dict["paint_jobs"] = paint_jobs
	
	FileAccess.open(file_path, FileAccess.WRITE).store_line(JSON.stringify(save_dict, "\t"))


func load() -> void:
	# TODO: make load dialogue
	var loaded_dict: Dictionary
	var json_data := JSON.new()
	if json_data.parse(FileAccess.get_file_as_string("/home/emjay/Desktop/test.json")) == OK:
		if json_data.data is Dictionary:
			loaded_dict = json_data.data
		
	VehicleDatabase.load_vehicle_lists(loaded_dict["mod_info"]["game"])
	
	var mod_screen: Node = get_node("../ScreenLoader/ModInfoScreen")
	mod_screen.find_child("Name").find_child("TextInput").text = loaded_dict["mod_info"]["mod_name"]
	mod_screen.find_child("Author").find_child("TextInput").text = loaded_dict["mod_info"]["author"]
	mod_screen.find_child("Version").find_child("TextInput").text = loaded_dict["mod_info"]["version"]
	mod_screen.find_child("Description").find_child("TextBox").text = loaded_dict["mod_info"]["description"]
	get_node("../ScreenLoader").switch_game(loaded_dict["mod_info"]["game"])
	
	var paint_job_tab_container: Node = get_node("../ScreenLoader/MainScreen/PaintJobTabContainer")
	for child in paint_job_tab_container.get_children():
		paint_job_tab_container.remove_child(child)
	for paint_job in loaded_dict["paint_jobs"]:
		paint_job_tab_container.add_tab(paint_job["paint_job_name"])
		var paint_job_node: Node = paint_job_tab_container.get_child(len(paint_job_tab_container.get_children()) - 1)
		paint_job_node.find_child("Name").find_child("TextInput").text = paint_job["paint_job_name"]
		paint_job_node.find_child("Price").find_child("TextInput").text = paint_job["price"]
		paint_job_node.find_child("Unlock").find_child("CheckboxInput").button_pressed = paint_job["unlocked_by_default"]
		paint_job_node.find_child("Unlock").find_child("TextInput").text = paint_job["unlock_level"]
		paint_job_node.find_child("InternalName").find_child("TextInput").text = paint_job["internal_name"]
		paint_job_node.find_child("CabinSupport").find_child("DropdownInput").selected = paint_job["cabin_support"]
		paint_job_node.find_child("SplitPaintJobs").find_child("DropdownInput").selected = paint_job["split_cabins"]
		paint_job_node._on_cabin_dropdown_change(paint_job["cabin_support"])
		
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
