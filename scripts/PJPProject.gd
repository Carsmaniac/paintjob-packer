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


func save() -> void:
	# TODO: make save dialogue, get file path
	var save_dict: Dictionary = {}
	save_dict["a"] = "Hello! This is a save file. If you edit it, bad things might happen and Paint Job Packer might crash. Continue at your own risk :)"
	
	var mod_info: Dictionary = {mod_name = "", author = "", version = "", description = "", game = "ets"}
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
				trailer_mods = get_list_from_tab(paint_job, 3),
				bus_mods = get_dict_from_tab(paint_job, 4)
			}
			paint_jobs.append(paint_job_dict)
	save_dict["paint_jobs"] = paint_jobs
	
	FileAccess.open("/home/emjay/Desktop/test.json", FileAccess.WRITE).store_line(JSON.stringify(save_dict))


func load() -> void:
	# TODO: make load dialogue
	var loaded_dict: Dictionary
	var json_data := JSON.new()
	if json_data.parse(FileAccess.get_file_as_string("/home/emjay/Desktop/test.json")) == OK:
		if json_data.data is Dictionary:
			loaded_dict = json_data.data
		
	VehicleDatabase.load_vehicle_lists(loaded_dict["mod_info"]["game"])
	
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
		var bus_mod_tab: Node = paint_job_node.get_node("VehicleTabContainer/Bus Mods")
		for vehicle in paint_job["bus_mods"]:
			var vehicle_selection: Node = bus_mod_tab.find_child(vehicle.replace(".", "_").replace("/", "_"), true, false)
			for cab in paint_job["bus_mods"][vehicle]:
				vehicle_selection.find_child(cab, true, false).button_pressed = true
