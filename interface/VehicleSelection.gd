extends Node2D

export var vehicle_name: String
export var author_name: String
export var author_row: bool = true
export var cabin_row: bool = true
var cabins_list: Array = ["Cabin A (Topline)", "Cabin B (Highline)", "Cabin C (Normal)", 
		"Cabin 8x4 (Topline)"] # TEMP


func _ready() -> void:
	$VehicleCheckbox.text = vehicle_name
	$AuthorName.text = "(" + author_name + ")"
	$AuthorName.visible = author_row
	
	set_cabin_checkbox_visibility()


func _on_panel_gui_input(event: InputEvent) -> void:
	if (event is InputEventMouseButton) and event.pressed and event.button_index == 1:
		$VehicleCheckbox.pressed = !$VehicleCheckbox.pressed


func set_cabin_checkbox_visibility() -> void:
	for i in range(7):
		get_node("CabinCheckbox" + str(i + 1)).visible = false
	
	if cabin_row and author_row:
		$BackgroundPanel.set_size(Vector2(337, 66))
	elif cabin_row or author_row:
		$BackgroundPanel.set_size(Vector2(337, 47))
	else:
		$BackgroundPanel.set_size(Vector2(337, 24))
	
	if cabin_row:
		var y_pos: int = 42 if author_row else 23
		var x_pos: int = 0
		for i in range(len(cabins_list)): # I need the index and the cabin, hence this abomination
			var cabin_name = cabins_list[i]
			var cabin_checkbox = get_node("CabinCheckbox" + str(i + 1))
			cabin_checkbox.visible = true
			cabin_checkbox.text = cabin_name.substr(6).get_slice(" (", 0)
			cabin_checkbox.hint_tooltip = cabin_name
			cabin_checkbox.set_position(Vector2(x_pos + (45 * i), y_pos))
