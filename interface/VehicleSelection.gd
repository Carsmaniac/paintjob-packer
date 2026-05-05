extends Control
class_name VehicleSelection

var vehicle_name: String
var author_name: String

var vehicle_checkbox: Node
var cabins_container: Node

var vehicle_dict: Dictionary


func init(vehicle: Dictionary, show_cabins: bool, show_author: bool) -> Control:
	vehicle_checkbox = get_node("%VehicleCheckbox")
	cabins_container = get_node("%CabinsContainer")
	for placeholder in cabins_container.get_children():
		cabins_container.remove_child(placeholder)
		placeholder.queue_free()
	vehicle_dict = vehicle
	
	name = vehicle_dict["file_path"]
	author_name = vehicle_dict["file_path"].split("/")[0]
	vehicle_name = vehicle_dict["file_path"].split("/")[1]

	vehicle_checkbox.text = vehicle["name"]
	if show_author:
		vehicle_checkbox.text += "\n(%s)" % vehicle["mod_author"]
	if show_cabins:
		var cabins_list: Array = vehicle["cabins"]
		if len(cabins_list) > 0:
			for i in range(len(cabins_list)):
				var cabin_checkbox := CheckBox.new()
				cabin_checkbox.text = cabins_list[i]["designation"].substr(6)
				cabin_checkbox.name = cabin_checkbox.text
				cabin_checkbox.tooltip_text = "{0} ({1})".format([
						cabins_list[i]["designation"], cabins_list[i]["name"]])
				cabin_checkbox.focus_mode = FOCUS_NONE
				cabin_checkbox.connect("toggled", sync_checkboxes.bind(false))
				cabins_container.add_child(cabin_checkbox)
				
	vehicle_checkbox.connect("toggled", sync_checkboxes.bind(true))
	
	return self


func _on_panel_gui_input(event: InputEvent) -> void:
	if (event is InputEventMouseButton) and event.pressed and event.button_index == 1:
		vehicle_checkbox.button_pressed = !vehicle_checkbox.pressed


func _set_cabin_checkbox_visibility(show_cabins: bool) -> void:
	cabins_container.visible = show_cabins
	
	
func sync_checkboxes(enabled: bool, vehicle: bool) -> void:
	if len($%CabinsContainer.get_children()) > 0:
		if vehicle:
			if enabled:
				var cabin_selected: bool = false
				for cabin_selection in $%CabinsContainer.get_children():
					if cabin_selection.button_pressed:
						cabin_selected = true
				if not cabin_selected:
					$%CabinsContainer.get_child(0).button_pressed = true
			else:
				for cabin_selection in $%CabinsContainer.get_children():
					cabin_selection.button_pressed = false
		else:
			if enabled:
				$%VehicleCheckbox.button_pressed = true
			else:
				var cabin_selected: bool = false
				for cabin_selection in $%CabinsContainer.get_children():
					if cabin_selection.button_pressed:
						cabin_selected = true
				if not cabin_selected:
					$%VehicleCheckbox.button_pressed = false
	get_node("../../../../..").update_vehicles_selected_number()
