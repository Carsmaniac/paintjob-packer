extends VBoxContainer

const Layer := preload("res://designer/Layer.tscn")
var selected_layers: Array[Node]
var previous_selected: int

var layer_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDarkLayer.tres")
var layer_selected_theme = ResourceLoader.load("res://simple-box-theme/pjp-dark/PJPDarkLayerSelected.tres")

var layer_nodes: Node
var transform_buttons: Node
var layer_buttons: Node
var tool_buttons: Node
var toolbar: Node
var view_canvas: Node


func _ready() -> void:
	layer_nodes = get_node("%DesignerCanvas/%LayerNodes")
	transform_buttons = get_node("%DesignerCanvas/%TransformButtons")
	layer_buttons = get_node("%LayerControlButtons")
	tool_buttons = get_node("%ToolButtons")
	toolbar = get_node("%Toolbar")
	view_canvas = get_node("%ViewCanvas")
	layer_buttons.get_node("ButtonDelete").connect("pressed", delete_selected_layers)
	update_layer_buttons()


func remove_layer(index: int) -> void:
	remove_child(get_child(index))
	update_buttons()


func update_buttons() -> void:
	for child in get_children():
		child.update_buttons()


func add_text_layer(new_position: Vector2, text_colour: Color) -> void:
	var new_layer: Node = Layer.instantiate()
	new_layer.layer_type = "text"
	new_layer.layer_name = "Text"
	new_layer.layer_colour = text_colour
	var layer_node = Label.new()
	layer_node.text = "Text"
	layer_node.position = new_position
	layer_node.scale = Vector2(0.1, 0.1)
	layer_node.add_theme_color_override("font_color", text_colour)
	var text_size = get_node("%ToolButtons/TextButtons/FontSize").value
	layer_nodes.add_child(layer_node)
	new_layer.linked_node = layer_node
	new_layer.change_text_size(text_size)
	add_child(new_layer)
	move_child(new_layer, 0)
	update_buttons()
	new_layer.change_text_layer()


func add_shape_layer(shape_node: Node, layer_type: String, shape_colour: Color) -> void:
	var new_layer: Node = Layer.instantiate()
	new_layer.layer_type = layer_type
	new_layer.layer_name = "New Shape"
	new_layer.layer_colour = shape_colour
	new_layer.linked_node = shape_node
	shape_node.reparent(layer_nodes)
	add_child(new_layer)
	move_child(new_layer, 0)
	update_buttons()


func select_layer(index: int, select_from_canvas: bool = false) -> void:
	# Shift + auto-select adds or removes selection
	if select_from_canvas and Input.is_key_pressed(KEY_CTRL) and Input.is_key_pressed(KEY_SHIFT):
		if get_child(index) not in selected_layers:
			add_selection(get_child(index))
		else:
			remove_selection(get_child(index))
	
	# Shift-click layer adds range to selection
	elif not select_from_canvas and Input.is_key_pressed(KEY_SHIFT):
		for i in range(min(index, previous_selected), max(index, previous_selected) + 1):
			if get_child(i) not in selected_layers:
				add_selection(get_child(i))
	
	# Ctrl-click layer adds or removes selection
	elif not select_from_canvas and Input.is_key_pressed(KEY_CTRL):
		if get_child(index) not in selected_layers:
			add_selection(get_child(index))
		else:
			remove_selection(get_child(index))
	
	# Select a single layer otherwise
	else:
		deselect_all()
		add_selection(get_child(index))
	view_canvas.sync_tool_to_layer()
	previous_selected = index


func deselect_all() -> void:
	selected_layers = []
	for layer in get_children():
		remove_selection(layer)


func add_selection(layer: Node) -> void:
	selected_layers.append(layer)
	layer.selection_box_node.visible = true
	update_selected_themes()
	update_transform_buttons()
	update_layer_buttons()


func remove_selection(layer: Node) -> void:
	if layer in selected_layers:
		selected_layers.remove_at(selected_layers.find(layer))
	layer.selection_box_node.visible = false
	update_selected_themes()
	update_transform_buttons()
	update_layer_buttons()


func delete_selected_layers() -> void:
	while len(selected_layers) > 0:
		selected_layers[0].delete()


func get_selection_bounding_box() -> Vector4:
	var layer_rect: Rect2 = selected_layers[0].bounding_box()
	var bounding_box := Vector4(layer_rect.position.x,
								layer_rect.position.y,
								layer_rect.position.x + layer_rect.size.x,
								layer_rect.position.y + layer_rect.size.y)
	for layer in selected_layers:
		layer_rect = layer.bounding_box()
		if layer_rect.position.x < bounding_box[0]:
			bounding_box[0] = layer_rect.position.x
		if layer_rect.position.y < bounding_box[1]:
			bounding_box[1] = layer_rect.position.y
		if layer_rect.position.x + layer_rect.size.x > bounding_box[2]:
			bounding_box[2] = layer_rect.position.x + layer_rect.size.x
		if layer_rect.position.y + layer_rect.size.y > bounding_box[3]:
			bounding_box[3] = layer_rect.position.y + layer_rect.size.y
	return bounding_box


func update_transform_buttons() -> void:
	if view_canvas.transforming:
		transform_buttons.visible = false
	else:
		for layer in get_children():
			layer.update_selection_box()
		if len(selected_layers) > 0 and ((toolbar.selected_tool == "ToolMove" and tool_buttons.get_node("MoveButtons/TransformControls").button_pressed) or toolbar.selected_tool == "ToolTransform"):
			transform_buttons.visible = true
			var bounding_box: Vector4 = get_selection_bounding_box() 
			
			transform_buttons.get_node("ButtonNW").position = Vector2(bounding_box[0], bounding_box[1])
			transform_buttons.get_node("ButtonN").position = Vector2((bounding_box[0] + bounding_box[2]) / 2, bounding_box[1])
			transform_buttons.get_node("ButtonNE").position = Vector2(bounding_box[2], bounding_box[1])
			transform_buttons.get_node("ButtonE").position = Vector2(bounding_box[2], (bounding_box[1] + bounding_box[3]) / 2)
			transform_buttons.get_node("ButtonSE").position = Vector2(bounding_box[2], bounding_box[3])
			transform_buttons.get_node("ButtonS").position = Vector2((bounding_box[0] + bounding_box[2]) / 2, bounding_box[3])
			transform_buttons.get_node("ButtonSW").position = Vector2(bounding_box[0], bounding_box[3])
			transform_buttons.get_node("ButtonW").position = Vector2(bounding_box[0], (bounding_box[1] + bounding_box[3]) / 2)
			transform_buttons.get_node("ButtonR").position = Vector2((bounding_box[0] + bounding_box[2]) / 2, bounding_box[1] - 50)
			
			for button in transform_buttons.get_children():
				button.position -= Vector2(view_canvas.selection_button_size/2, view_canvas.selection_button_size/2)
		else:
			transform_buttons.visible = false


func update_selected_themes() -> void:
	for layer in get_children():
		if layer in selected_layers:
			layer.theme = layer_selected_theme
		else:
			layer.theme = layer_theme


func update_layer_buttons() -> void:
	if len(selected_layers) > 0:
		layer_buttons.get_node("ButtonDelete").disabled = false
		layer_buttons.get_node("ButtonRasterise").disabled = false
		if len(selected_layers) > 1:
			layer_buttons.get_node("ButtonGroup").disabled = false
		else:
			layer_buttons.get_node("ButtonGroup").disabled = true
	else:
		layer_buttons.get_node("ButtonDelete").disabled = true
		layer_buttons.get_node("ButtonRasterise").disabled = true
		layer_buttons.get_node("ButtonGroup").disabled = true
