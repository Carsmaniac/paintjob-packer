extends VBoxContainer
var selected_tool: String


func _ready() -> void:
	for child in get_children():
		child.connect("pressed", switch_button.bind(child))


func switch_button(pressed_button: Node) -> void:
	for child in get_children():
		if child == pressed_button:
			child.button_pressed = true
			selected_tool = child.name
		else:
			child.button_pressed = false
	
	var tool_buttons: Node = get_node("../TopPanel/HBoxContainer/ToolButtons")
	for group in tool_buttons.get_children():
		group.visible = false
	if pressed_button.name == "ToolMove":
		tool_buttons.get_node("MoveButtons").visible = true
	elif pressed_button.name == "ToolTransform":
		tool_buttons.get_node("TransformButtons").visible = true
	elif pressed_button.name == "ToolRectangle":
		tool_buttons.get_node("RectangleButtons").visible = true
