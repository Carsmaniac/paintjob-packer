extends VBoxContainer
var selected_tool: String


func _ready() -> void:
	for child in get_children():
		if child is Button and child is not ColorPickerButton:
			child.connect("pressed", switch_button.bind(child))
	switch_button(get_node("ToolMove"))


func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_V:
			switch_button(get_node("ToolMove"))
		#elif event.keycode == KEY_T and event.ctrl_pressed:
			#switch_button(get_node("ToolTransform"))
		#elif event.keycode == KEY_B:
			#switch_button(get_node("ToolBrush"))
		#elif event.keycode == KEY_E:
			#switch_button(get_node("ToolEraser"))
		elif event.keycode == KEY_U:
			switch_button(get_node("ToolShape"))
		elif event.keycode == KEY_T:
			switch_button(get_node("ToolText"))
		elif event.keycode == KEY_H:
			switch_button(get_node("ToolHand"))


func switch_button(pressed_button: Node) -> void:
	for child in get_children():
		if child is Button:
			if child == pressed_button:
				child.button_pressed = true
				selected_tool = child.name
			else:
				child.button_pressed = false
	
	var tool_buttons: Node = get_node("../../TopPanel/HBoxContainer/ToolButtons")
	for group in tool_buttons.get_children():
		group.visible = false
	if pressed_button.name == "ToolMove":
		tool_buttons.get_node("MoveButtons").visible = true
	elif pressed_button.name == "ToolTransform":
		tool_buttons.get_node("TransformButtons").visible = true
	elif pressed_button.name == "ToolShape":
		tool_buttons.get_node("ShapeButtons").visible = true
	elif pressed_button.name == "ToolText":
		tool_buttons.get_node("TextButtons").visible = true
	
	get_node("../../TwoUp/ViewCanvas").sync_tool_to_layer()
