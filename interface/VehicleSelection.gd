extends Control

export var vehicle_name: String
export var author_name: String
export var author_row: bool
export var cabin_row: bool

var vehicle_checkbox: Node
var author_name_label: Node


func _ready() -> void:
	$BackgroundPanel.set_size(get_size())


func init(vehicle: Dictionary, show_cabins: bool, show_author: bool) -> Control:
	vehicle_checkbox = $VBoxContainer/VehicleCheckbox
	author_name_label = $VBoxContainer/AuthorName
	author_row = show_author
	cabin_row = show_cabins

	vehicle_checkbox.text = vehicle["name"]
	author_name_label.text = "     (" + vehicle["mod_author"] + ")"
	author_name_label.visible = author_row
	if show_cabins:
		var cabins_list: Array = vehicle["cabins"]
		if len(cabins_list) > 0:
			for i in range(len(cabins_list)): # I need the index and the cabin, hence this abomination
				var cabin_checkbox := CheckBox.new()
				cabin_checkbox.text = cabins_list[i]["designation"].substr(6)
				cabin_checkbox.hint_tooltip = "{0} ({1})".format([
						cabins_list[i]["designation"], cabins_list[i]["name"]])
				cabin_checkbox.focus_mode = FOCUS_NONE
				$VBoxContainer/HBoxContainer.add_child(cabin_checkbox)

	if show_cabins and show_author:
		rect_min_size = Vector2(338, 70)
	elif show_cabins:
		rect_min_size = Vector2(338, 53)
	elif show_author:
		rect_min_size = Vector2(338, 49)
	else:
		rect_min_size = Vector2(338, 25)
	
	return self


func _on_panel_gui_input(event: InputEvent) -> void:
	if (event is InputEventMouseButton) and event.pressed and event.button_index == 1:
		vehicle_checkbox.pressed = !vehicle_checkbox.pressed
