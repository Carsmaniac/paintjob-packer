extends Node
	
var vehicle_list: Array
var trucks: Array
var trailers: Array
var truck_mods: Array
var trailer_mods: Array
var bus_mods: Array
var car_mods: Array

var vehicle_format_version: int = 1


func _ready() -> void:
	vehicle_list = _load_vehicle_list("ets")
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
	

func _load_vehicle_list(game: String) -> Array:
	vehicle_list = []
	for file_name in get_filelist("res://vehicles/" + game):
		var vehicle_dict: Dictionary = _load_vehicle_file(file_name)
		if vehicle_dict != {}:
			if vehicle_dict["format_version"] == vehicle_format_version:
				vehicle_list.append(vehicle_dict)
			else:
				pass # For future use, when the format changes
	return vehicle_list


func _load_vehicle_file(file_path: String) -> Dictionary:
	var file := File.new()
	var __ = file.open(file_path, File.READ)
	var content: JSONParseResult = JSON.parse(file.get_as_text())
	file.close()
	
	if content.result is Dictionary:
		return content.result
	else:
		return {}


# Get files from all subfolders, from Ratty on the Godot Engine Q&A site
func get_filelist(scan_dir : String) -> Array:
	var my_files : Array = []
	var dir := Directory.new()
	if dir.open(scan_dir) != OK:
		return []
	
	if dir.list_dir_begin(true, true) != OK:
		return []
	
	var file_name := dir.get_next()
	while file_name != "":
		if dir.current_is_dir():
			my_files += get_filelist(dir.get_current_dir() + "/" + file_name)
		else:
			my_files.append(dir.get_current_dir() + "/" + file_name)
	
		file_name = dir.get_next()
	
	return my_files