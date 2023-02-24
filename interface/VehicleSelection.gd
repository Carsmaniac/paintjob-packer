extends Control

export var vehicle_name: String
export var author_name: String

var vehicle_checkbox: Node
var cabins_container: Node

var vehicle_dict: Dictionary


func init(vehicle: Dictionary, show_cabins: bool, show_author: bool) -> Control:
	vehicle_checkbox = get_node("%VehicleCheckbox")
	cabins_container = get_node("%CabinsContainer")
	vehicle_dict = vehicle

	vehicle_checkbox.text = vehicle["name"]
	get_node("%AuthorName").text = "(" + vehicle["mod_author"] + ")"
	get_node("%AuthorNameRow").visible = show_author
	if show_cabins:
		var cabins_list: Array = vehicle["cabins"]
		if len(cabins_list) > 0:
			for i in range(len(cabins_list)):
				var cabin_checkbox := CheckBox.new()
				cabin_checkbox.text = cabins_list[i]["designation"].substr(6)
				cabin_checkbox.hint_tooltip = "{0} ({1})".format([
						cabins_list[i]["designation"], cabins_list[i]["name"]])
				cabin_checkbox.focus_mode = FOCUS_NONE
				cabins_container.add_child(cabin_checkbox)
	
	return self


func _on_panel_gui_input(event: InputEvent) -> void:
	if (event is InputEventMouseButton) and event.pressed and event.button_index == 1:
		vehicle_checkbox.pressed = !vehicle_checkbox.pressed


func _set_cabin_checkbox_visibility(show_cabins: bool) -> void:
	cabins_container.visible = show_cabins
