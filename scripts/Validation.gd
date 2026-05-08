extends Node


func ends_in_space(input: String) -> bool:
	return input.substr(len(input) - 1) == " "


func ends_in_full_stop(input: String) -> bool:
	return input.substr(len(input) - 1) == "."


func is_alphanumeric(input: String) -> bool:
	var alphanumeric: bool = true
	for letter in input:
		if letter not in "abcdefghijklmnopqrstuvwxyz0123456789_":
			alphanumeric = false
	return alphanumeric


func is_ascii(input: String) -> bool:
	var ascii: bool = true
	for letter in input:
		if letter not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&()-_=+[]{};',`~ ":
			ascii = false
	return ascii


func is_number(input: String) -> bool:
	return input.is_valid_int()


func has_invalid_file_character(input: String) -> bool:
	var invalid_character: bool = false
	for character in ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]:
		if character in input:
			invalid_character = true
	return invalid_character


func has_invalid_sii_character(input: String) -> bool:
	var invalid_character: bool = false
	for character in ["\"", "/", "\\"]:
		if character in input:
			invalid_character = true
	return invalid_character


func is_reserved_file_name(input: String) -> bool:
	var reserved_names: PackedStringArray = ["CON", "PRN", "AUX", "NUL"]
	for i in range(9):
		reserved_names.append("COM" + str(i + 1))
		reserved_names.append("LPT" + str(i + 1))
	var is_reserved: bool = false
	for res_name in reserved_names:
		if input.to_upper() == res_name:
			is_reserved = true
	return is_reserved


func remove_escape_characters(input: String) -> String:
	return input.strip_escapes()


func remove_diacritics(input: String) -> String:
	return TextServerManager.get_primary_interface().strip_diacritics(input)


func internal_name_too_long(paint_job_tab: Node) -> bool:
	if paint_job_tab.find_child("SplitPaintJobs").selected == 0:
		return len(paint_job_tab.find_child("InternalName").find_child("TextInput").text) > 12
	else:
		return len(paint_job_tab.find_child("InternalName").find_child("TextInput").text) > 10


func incompatible_vehicles(paint_job_tab: Node) -> Array:
	var selected_list: Array[PackedStringArray] = []
	for child in paint_job_tab.find_child("VehicleTabContainer").get_children():
		for selection in child.find_child("VBoxContainer").get_children():
			if selection.find_child("VehicleCheckbox").button_pressed:
				selected_list.append(PackedStringArray([selection.vehicle_dict["path"], selection.vehicle_dict["name"]]))
				
	var identical_list: Array[PackedStringArray] = []
	for i in range(len(selected_list)):
		for j in range(i + 1, len(selected_list)):
			if selected_list[i][0] == selected_list[j][0]:
				identical_list.append(PackedStringArray([selected_list[i][1], selected_list[j][1]]))
	return identical_list


func non_unique_internal_names(paint_job_tabs: Array[Node]) -> bool:
	var name_list: PackedStringArray
	var non_unique: bool = false
	for tab in paint_job_tabs:
		name_list.append(tab.find_child("Name").find_child("TextInput").text)
	for i in range(len(name_list)):
		for j in range(i + 1, len(name_list)):
			if name_list[i][0] == name_list[j][0]:
				non_unique = true
	return non_unique

func no_vehicles_selected(paint_job_tab: Node) -> bool:
	var no_vehicles: bool = true
	for child in paint_job_tab.find_child("VehicleTabContainer").get_children():
		for selection in child.find_child("VBoxContainer").get_children():
			if selection.find_child("VehicleCheckbox").button_pressed:
				no_vehicles = false
	return no_vehicles
