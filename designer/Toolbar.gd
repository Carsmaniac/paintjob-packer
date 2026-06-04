extends VBoxContainer

var selected_tool: String
var layer_list: Node
var tool_buttons: Node


func _ready() -> void:
	layer_list = get_node("../../RightPanel/ScrollContainer/LayerList")
	tool_buttons = get_node("../../TopPanel/HBoxContainer/ToolButtons")
	for child in get_children():
		if child is Button and child is not ColorPickerButton:
			child.connect("pressed", switch_button.bind(child))
	switch_button(get_node("ToolMove"))
	get_node("ColourPrimary").connect("color_changed", change_colours)
	tool_buttons.get_node("ShapeButtons/ShapeColour").connect("color_changed", change_shape_colour)
	tool_buttons.get_node("TextButtons/TextColour").connect("color_changed", change_text_colour)


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
		elif event.keycode == KEY_X:
			var temp_colour: Color = get_node("ColourPrimary").color
			get_node("ColourPrimary").color = get_node("ColourSecondary").color
			get_node("ColourSecondary").color = temp_colour
		elif event.keycode == KEY_D:
			get_node("ColourPrimary").color = Color.BLACK
			get_node("ColourSecondary").color = Color.WHITE


func switch_button(pressed_button: Node) -> void:
	for child in get_children():
		if child is Button:
			if child == pressed_button:
				child.button_pressed = true
				selected_tool = child.name
			else:
				child.button_pressed = false
	
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


func change_colours(new_colour: Color) -> void:
	if selected_tool == "ToolShape":
		var shape_selected: bool = false
		for layer in layer_list.selected_layers:
			if layer.layer_type in ["rect", "ellipse"]:
				shape_selected = true
		if not shape_selected:
			tool_buttons.get_node("ShapeButtons/ShapeColour").color = new_colour
	elif selected_tool == "ToolText":
		var text_selected: bool = false
		for layer in layer_list.selected_layers:
			if layer.layer_type == "text":
				text_selected = true
		if not text_selected:
			tool_buttons.get_node("TextButtons/TextColour").color = new_colour


func change_shape_colour(new_colour: Color) -> void:
	for layer in layer_list.selected_layers:
		if layer.layer_type in ["rect", "ellipse"]:
			layer.change_colour(new_colour)


func change_text_colour(new_colour: Color) -> void:
	for layer in layer_list.selected_layers:
		if layer.layer_type == "text":
			layer.change_colour(new_colour)
