extends Control

var vehicles_selected: Array = []


func _ready() -> void:
	var __ = $Name/TextInput.connect("text_changed", Callable(get_parent(), "rename_tab"))
	__ = $CabinSupport/DropdownInput.connect("item_selected", _on_cabin_dropdown_change)
	__ = $SplitPaintJobs/DropdownInput.connect("item_selected", Callable($InternalName, "validate_text_input"))
	__ = $Unlock/CheckboxInput.connect("toggled", enable_disable_unlock_level)


func get_vehicle_selections() -> Array:
	var selections: Array = []
	for tab in $VehicleTabContainer.get_children():
			for selection in tab.find_child("VBoxContainer").get_children():
				if selection is VehicleSelection:
					selections.append(selection)
	return selections


func _on_cabin_dropdown_change(tab_index) -> void:
	if tab_index == 2:
		$SplitPaintJobs.visible = true
		for selection in get_vehicle_selections():
			selection._set_cabin_checkbox_visibility(true)
	else:
		for selection in get_vehicle_selections():
			selection._set_cabin_checkbox_visibility(false)
		if tab_index == 1:
			$SplitPaintJobs.visible = true
		else:
			$SplitPaintJobs.visible = false
			$SplitPaintJobs/DropdownInput.selected = 0
	
	
func update_vehicles_selected_number() -> void:
	var total_vehicles: int = 0
	for selection in get_vehicle_selections():
		if selection.find_child("VehicleCheckbox").button_pressed:
			total_vehicles += 1
	$SelectedLabel.text = "Vehicles Supported (%s)" % total_vehicles


func enable_disable_unlock_level(unlock_default: bool) -> void:
	$Unlock/TextInput.visible = !unlock_default
	if unlock_default:
		$Unlock/HelpButton.position = Vector2(321, 39)
	else:
		$Unlock/HelpButton.position = Vector2(321, 80)


func validate_field(field_contents: String, field_type: String) -> String:
	
	return ""

#func validate_text_input(__) -> void:
	#var string: String = $TextInput.text
	#if input_type in ["text_number", "checkbox"]:
		#if string != "" and not string.is_valid_int():
			#warning = "Must be a number with no decimal point or other characters."
			#$WarningButton.visible = true
		#else:
			#$WarningButton.visible = false
			#
	#elif input_type == "text_alphanumeric":
		#var not_alphanumeric: bool = false
		#for letter in string:
			#if letter not in "abcdefghijklmnopqrstuvwxyz0123456789_":
				#not_alphanumeric = true
		#var max_length: int = 12
		#if get_node("../SplitPaintJobs/DropdownInput").selected == 1:
			#max_length = 10
		#
		#if string != "":
			#if not_alphanumeric:
				#warning = "Must consist of only lowercase letters, numbers and underscores.\n\nPermitted characters:\nabcdefghijklmnopqrstuvwxyz0123456789_"
				#$WarningButton.visible = true
			#elif len(string) > max_length:
				#warning = "Must be %s characters or fewer." % max_length
				#$WarningButton.visible = true
			## TODO: detect non-unique internal names
			## elif not_unique:
			##     warning = "Must be unique, cannot be the same as the internal name of any other paint job."
			##     $WarningButton.visible = true
			#else:
				#$WarningButton.visible = false
		#else:
			#$WarningButton.visible = false
