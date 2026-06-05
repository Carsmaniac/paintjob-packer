extends SubViewportContainer

var canvas: Node
var layer_list: Node
var toolbar: Node
var tool_buttons: Node
var temp_layer: Node

var zoom_amount: float = 1.04
var pan_amount: float = 20.0
var canvas_view_scale: float = 1.0

var drawing_shape: bool = false
var drawing_shape_node: Node
var drawing_shape_starting_pos: Vector2
var drawing_shape_type: String
var drawing_shape_theme: Theme
var drawing_shape_style: StyleBoxFlat
var drawing_shape_texture: ImageTexture
var drawing_shape_colour: Color


func _ready() -> void:
	canvas = get_node("%DesignerCanvas")
	layer_list = get_node("%LayerList")
	toolbar = get_node("%Toolbar")
	tool_buttons = get_node("%ToolButtons")
	temp_layer = canvas.get_node("%TempLayer")


func fit_to_view() -> void:
	var fit_width_scale: float = self.size.x / canvas.width
	var fit_height_scale: float = self.size.y / canvas.height
	canvas_view_scale = min(fit_width_scale, fit_height_scale)
	canvas.scale = Vector2(canvas_view_scale, canvas_view_scale)
	if fit_width_scale < fit_height_scale:
		canvas.position = Vector2(0, self.size.y/2 - (canvas_view_scale * canvas.height / 2))
	else:
		canvas.position = Vector2(self.size.x/2 - (canvas_view_scale * canvas.width / 2), 0)


func _gui_input(event: InputEvent) -> void:
	if Input.is_key_pressed(KEY_SPACE):
		toolbar.selected_tool = "ToolHand"
	
	# Pan with middle-click drag
	if event is InputEventMouseMotion and event.button_mask == 4:
			canvas.position += event.relative
	
	# Hand tool
	elif toolbar.selected_tool == "ToolHand":
		if event is InputEventMouseMotion and event.button_mask == 1:
			canvas.position += event.relative
		elif event is InputEventMouseButton and event.button_index == 4:
			zoom_to_pos(true, event.position)
		elif event is InputEventMouseButton and event.button_index == 5:
			zoom_to_pos(false, event.position)
	
	# Scrolling
	elif event is InputEventMouseButton and event.button_index in [4, 5]:
		# Alt-scroll to zoom
		if Input.is_key_pressed(KEY_ALT) and event.button_index == 4:
			zoom_to_pos(true, event.position)
		elif Input.is_key_pressed(KEY_ALT) and event.button_index == 5:
			zoom_to_pos(false, event.position)
		
		# Ctrl-scroll to pan horizontal
		elif Input.is_key_pressed(KEY_CTRL) and event.button_index == 4:
			canvas.position.x += pan_amount
		elif Input.is_key_pressed(KEY_CTRL) and event.button_index == 5:
			canvas.position.x -= pan_amount
		
		# Scroll to pan vertical
		elif event.button_index == 4:
			canvas.position.y += pan_amount
		elif event.button_index == 5:
			canvas.position.y -= pan_amount
	
	# Move tool
	elif toolbar.selected_tool == "ToolMove":
		# Select on click
		if event is InputEventMouseButton and event.button_index == 1 and event.pressed and \
		((Input.is_key_pressed(KEY_CTRL) and tool_buttons.get_node("MoveButtons/AutoSelect").button_pressed == false) or \
		(Input.is_key_pressed(KEY_CTRL) == false and tool_buttons.get_node("MoveButtons/AutoSelect").button_pressed)):
			var selecting_layer: bool = false
			for layer in layer_list.get_children():
				if layer.linked_node.get_rect().has_point(get_canvas_position(event.position)):
					layer_list.select_layer(layer.get_index(), true)
					selecting_layer = true
					break
			if not selecting_layer:
				layer_list.deselect_all()
		
		# Move on drag
		elif event is InputEventMouseMotion and event.button_mask == 1:
			for layer in layer_list.selected_layers:
				layer.linked_node.position += (event.relative / canvas_view_scale)
				layer.update_selection_box()
				layer_list.update_transform_buttons()
	
	# Text tool
	elif toolbar.selected_tool == "ToolText":
		if event is InputEventMouseButton and event.button_index == 1 and event.pressed:
			var editing_text: bool = false
			for layer in layer_list.get_children():
				if layer.layer_type == "text":
					if layer.linked_node.get_rect().has_point(get_canvas_position(event.position)):
						layer_list.select_layer(layer.get_index())
						sync_tool_to_layer()
						layer.change_text_layer()
						editing_text = true
						break
			if not editing_text:
				layer_list.add_text_layer(get_canvas_position(event.position), tool_buttons.get_node("TextButtons/TextColour").color)
	
	elif toolbar.selected_tool == "ToolShape":
		if event is InputEventMouseButton and event.button_index == 1 and not event.pressed:
			drawing_shape = false
			if event.position == drawing_shape_starting_pos:
				drawing_shape_node.queue_free()
			else:
				pass # add a new layer with the shape
				layer_list.add_shape_layer(drawing_shape_node, drawing_shape_type, drawing_shape_colour)
		elif event is InputEventMouseButton and event.button_index == 1 and event.pressed:
			if tool_buttons.get_node("ShapeButtons/ShapeSelect").selected == 0:
				drawing_shape_type = "rect"
				drawing_shape_node = Panel.new()
				drawing_shape_theme = Theme.new()
				drawing_shape_style = StyleBoxFlat.new()
				drawing_shape_colour = tool_buttons.get_node("ShapeButtons/ShapeColour").color
				drawing_shape_style.bg_color = drawing_shape_colour
				drawing_shape_style.set_corner_radius_all(tool_buttons.get_node("ShapeButtons/CornerRadius").value)
				drawing_shape_theme.set_stylebox("panel", "Panel", drawing_shape_style)
				drawing_shape_node.theme = drawing_shape_theme
			elif tool_buttons.get_node("ShapeButtons/ShapeSelect").selected == 1:
				drawing_shape_type = "ellipse"
				drawing_shape_node = TextureRect.new()
				drawing_shape_texture = ImageTexture.create_from_image(Image.load_from_file("res://designer/circle-svg/10.svg"))
				drawing_shape_node.set_texture(drawing_shape_texture)
				drawing_shape_node.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
				drawing_shape_colour = tool_buttons.get_node("ShapeButtons/ShapeColour").color
				drawing_shape_node.modulate = drawing_shape_colour
			drawing_shape = true
			drawing_shape_node.position = get_canvas_position(event.position)
			drawing_shape_starting_pos = get_canvas_position(event.position)
			temp_layer.add_child(drawing_shape_node)
		elif event is InputEventMouseMotion and event.button_mask == 1:
			drawing_shape_node.position = drawing_shape_starting_pos.min(get_canvas_position(event.position))
			drawing_shape_node.size = (drawing_shape_starting_pos - get_canvas_position(event.position)).abs()


func sync_tool_to_layer() -> void:
	if len(layer_list.selected_layers) == 1:
		var selected_layer = layer_list.selected_layers[0]
		if toolbar.selected_tool == "ToolShape" and selected_layer.layer_type in ["rect", "ellipse"]:
			tool_buttons.get_node("ShapeButtons/ShapeColour").color = selected_layer.layer_colour
		elif toolbar.selected_tool == "ToolText" and selected_layer.layer_type == "text":
			tool_buttons.get_node("TextButtons/FontSize").value = selected_layer.text_size
			tool_buttons.get_node("TextButtons/TextColour").color = selected_layer.layer_colour


func get_canvas_position(rel_pos: Vector2) -> Vector2:
	return (rel_pos - canvas.position) / canvas_view_scale


func zoom_to_pos(zoom_in: bool, mouse_pos: Vector2) -> void:
	var zoom_pos: Vector2 = get_canvas_position(mouse_pos)
	
	if zoom_in:
		canvas_view_scale *= zoom_amount
		canvas.position.x -= zoom_pos.x * (zoom_amount - 1) * canvas_view_scale
		canvas.position.y -= zoom_pos.y * (zoom_amount - 1) * canvas_view_scale
	else:
		canvas_view_scale /= zoom_amount
		canvas.position.x += zoom_pos.x * (zoom_amount - 1) * canvas_view_scale
		canvas.position.y += zoom_pos.y * (zoom_amount - 1) * canvas_view_scale
	canvas.scale = Vector2(canvas_view_scale, canvas_view_scale)
