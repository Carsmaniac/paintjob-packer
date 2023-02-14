extends Node
	
var vehicle_list: Array


func _ready() -> void:
	vehicle_list = _load_vehicle_list("ets")
	

func _load_vehicle_list(game: String) -> Array:
	vehicle_list = []
	for file_name in get_filelist("res://vehicles/" + game):
		var vehicle_dict: Dictionary = _load_vehicle_file(file_name)
		if vehicle_dict != {}:
			vehicle_list.append(vehicle_dict)
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