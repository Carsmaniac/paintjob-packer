extends Node
	
var vehicle_list: Array[Dictionary]
var trucks: Array[Dictionary]
var trailers: Array[Dictionary]
var truck_mods: Array[Dictionary]
var trailer_mods: Array[Dictionary]
var bus_mods: Array[Dictionary]
var car_mods: Array[Dictionary]

var vehicle_format_version: int = 1
# TODO: ensure this is false for release
var test_accessories: bool = true


func load_vehicle_lists(game: String) -> void:
	vehicle_list = []
	for file_name in get_file_list("res://vehicles/" + game):
		var vehicle_dict: Dictionary = load_vehicle_file(file_name)
		if vehicle_dict != {}:
			if vehicle_dict["format_version"] == vehicle_format_version:
				vehicle_dict["file_path"] = file_name.substr(19, len(file_name) - 24) # <res...>author/make.model<.json>
				
				if test_accessories:
					vehicle_dict["uses_accessories"] = true
					for i in range(10):
						vehicle_dict["accessories"]["test%s" % str(i)] = []
				
				vehicle_list.append(vehicle_dict)
			else:
				pass # For future use, when the format changes

	trucks = []
	trailers = []
	truck_mods = []
	trailer_mods = []
	bus_mods = []
	car_mods = []
	for vehicle in vehicle_list:
		if vehicle["mod"]:
			if vehicle["trailer"]:
				trailer_mods.append(vehicle)
			elif vehicle["bus"]:
				bus_mods.append(vehicle)
			elif vehicle["car"]:
				car_mods.append(vehicle)
			else:
				truck_mods.append(vehicle)
		else:
			if vehicle["trailer"]:
				trailers.append(vehicle)
			else:
				trucks.append(vehicle)

	truck_mods.sort_custom(func(a, b): return a["name"] < b["name"])
	trailer_mods.sort_custom(func(a, b): return a["name"] < b["name"])
	bus_mods.sort_custom(func(a, b): return a["name"] < b["name"])
	car_mods.sort_custom(func(a, b): return a["name"] < b["name"])


func load_vehicle_file(file_path: String) -> Dictionary:
	var file := FileAccess.open(file_path, FileAccess.READ)
	var test_json_conv = JSON.new()
	test_json_conv.parse(file.get_as_text())
	file.close()
	var content = test_json_conv.get_data()
	
	if content is Dictionary:
		return content
	else:
		return {}


func get_file_list(scan_dir: String) -> PackedStringArray:
	var file_list: PackedStringArray = []
	var folders := ResourceLoader.list_directory(scan_dir)
	for folder in folders:
		var files := ResourceLoader.list_directory("%s/%s" % [scan_dir, folder])
		for file in files:
			file_list.append("%s/%s%s" % [scan_dir, folder, file])
	return file_list
