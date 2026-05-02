extends TabBar

var vehicles_selected: Array = []

func _ready() -> void:
	var __ = $Name/TextInput.connect("text_changed", Callable(get_parent(), "rename_tab"))
	__ = $CabinSupport/DropdownInput.connect("item_selected", _on_cabin_dropdown_change)
	__ = $SplitPaintJobs/DropdownInput.connect("item_selected", Callable($InternalName, "validate_text_input"))

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
	
func update_vehicles_selected_number() -> void:
	var total_vehicles: int = 0
	for selection in get_vehicle_selections():
		if selection.find_child("VehicleCheckbox").button_pressed:
			total_vehicles += 1
	$SelectedLabel.text = "Vehicles Supported (%s)" % total_vehicles
