extends Node


"""
Example project data:
var pjp_save_format = 1 # For future use, if the save format changes, and also to identify this vs any other JSON file
var mod_data: Dictionary = {
	mod_name = "",
	author = "",
	version = "",
	description = ""
}
var paint_jobs: Array[Dictionary] = []
var example_paint_job: Dictionary = {
	paint_job_name = "",
	price = 0,
	unlocked_by_default = false,
	unlock_level = 0,
	internal_name = "",
	cabin_support = 0,
	split_cabins = 0,
	trucks: Dictionary = {
		"scs/scania.r" = ["a", "8"],
		"scs/volvo.fh16_2012" = ["b"]
	},
	truck_mods: Dictionary = {},
	trailers: PackedStringArray = ["scs/box", "krone/dryliner"],
	trailer_mods: PackedStringArray = [],
	bus_mods: Dictionary = {}
}
"""


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
	FileAccess.open("/home/emjay/Desktop/test.json", FileAccess.WRITE).store_line(JSON.stringify(paint_jobs))
