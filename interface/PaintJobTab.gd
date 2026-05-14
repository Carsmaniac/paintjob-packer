extends Control

var warnings: Array = []


func _ready() -> void:
	var __ = $Name/TextInput.connect("text_changed", Callable(get_parent(), "rename_tab"))
	__ = $CabinSupport/DropdownInput.connect("item_selected", _on_cabin_dropdown_change)
	__ = $SplitPaintJobs/DropdownInput.connect("item_selected", Callable($InternalName, "validate_text_input"))
	__ = $Unlock/CheckboxInput.connect("toggled", enable_disable_unlock_level)
	__ = $SearchBar.connect("text_changed", filter_vehicles)
	__ = $AdvancedButton.connect("pressed", switch_to_advanced)


func get_vehicle_selections() -> Array:
	var selections: Array = []
	for tab in $VehicleTabContainer.get_children():
			for selection in tab.find_child("VBoxContainer").get_children():
				if selection is VehicleSelection:
					selections.append(selection)
	return selections


func switch_to_advanced() -> void:
	get_node("../../..").switch_screen(true, false, 4)


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
	$SelectedLabel.text = tr("PJOB_VEHICLES") % total_vehicles


func filter_vehicles(filter_string: String) -> void:
	for selection in get_vehicle_selections():
		if filter_string != "":
			if filter_string.to_lower() in selection.vehicle_name.to_lower() or \
				filter_string.to_lower() in selection.author_name.to_lower() or \
				filter_string.to_lower() in selection.vehicle_display_name.to_lower():
				selection.visible = true
			else:
				selection.visible = false
		else:
			selection.visible = true


func show_hide_warning_button() -> void:
	if len(warnings) > 0:
		$WarningButton.visible = true
	else:
		$WarningButton.visible = false


func show_warnings() -> void:
	var popup := AcceptDialog.new()
	popup.title = tr("WARNING_TITLE")
	var dialogue_text = ""
	for warning in warnings:
		dialogue_text += "%s\n%s\n\n" % [warning[0], warning[1]]
	dialogue_text = dialogue_text.substr(0, len(dialogue_text) - 1)
	popup.dialog_text = dialogue_text
	popup.size.y = 0
	popup.ok_button_text = tr("BUTTON_OKAY")
	popup.theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDark.tres")
	self.add_child(popup)
	popup.popup_centered()


func enable_disable_unlock_level(unlock_default: bool) -> void:
	$Unlock/NumberInput.visible = !unlock_default
	if unlock_default:
		$Unlock/HelpButton.position = Vector2(321, 39)
	else:
		$Unlock/HelpButton.position = Vector2(321, 80)
