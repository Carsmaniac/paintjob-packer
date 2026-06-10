extends SubViewportContainer

var canvas: Node
var layer_list: Node
var toolbar: Node
var tool_buttons: Node
var temp_layer: Node
var layer_nodes: Node
var transform_buttons: Node
var colour_button_nodes: Array[Node]

var zoom_amount: float = 1.04
var pan_amount: float = 20.0
var canvas_view_scale: float = 1.0

var selection_theme = ResourceLoader.load("res://simple-box-theme/SelectionTheme.tres")
var selection_button_size: float
var selection_button_size_initial: float = 25
var selection_button_font_initial: float = 15

var drawing_shape: bool = false
var drawing_shape_node: Node
var drawing_shape_starting_pos: Vector2
var drawing_shape_type: String
var drawing_shape_theme: Theme
var drawing_shape_style: StyleBoxFlat
var drawing_shape_texture: ImageTexture
var drawing_shape_colour: Color

var transforming: bool = false
var transform_rotate: bool
var transform_type: String
var transform_starting_position: Vector2
var transform_opposite_position: Vector2
var transform_middle_position: Vector2
var transform_node: Node
var transform_node_starting_position: Vector2
var transform_node_starting_rotation: float
var transform_node_index_dict: Dictionary # {node: index}


func _ready() -> void:
	canvas = get_node("%DesignerCanvas")
	layer_list = get_node("%LayerList")
	toolbar = get_node("%Toolbar")
	tool_buttons = get_node("%ToolButtons")
	temp_layer = canvas.get_node("%TempLayer")
	layer_nodes = canvas.get_node("%LayerNodes")
	transform_buttons = canvas.get_node("%TransformButtons")
	colour_button_nodes = [get_node("%ColourPrimary"), get_node("%ColourSecondary"), get_node("%TextColour"), get_node("%ShapeColour")]
	for button in get_node("%DesignerCanvas/%TransformButtons").get_children():
		button.connect("button_down", start_transform.bind(button.name))
	update_selection_theme()


func fit_to_view() -> void:
	var fit_width_scale: float = self.size.x / canvas.width
	var fit_height_scale: float = self.size.y / canvas.height
	canvas_view_scale = min(fit_width_scale, fit_height_scale)
	canvas.scale = Vector2(canvas_view_scale, canvas_view_scale)
	if fit_width_scale < fit_height_scale:
		canvas.position = Vector2(0, self.size.y/2 - (canvas_view_scale * canvas.height / 2))
	else:
		canvas.position = Vector2(self.size.x/2 - (canvas_view_scale * canvas.width / 2), 0)
	update_selection_theme()
	layer_list.update_transform_buttons()


func update_selection_theme() -> void:
	selection_button_size = max(selection_button_size_initial / canvas_view_scale, selection_button_size_initial)
	for button in transform_buttons.get_children():
		button.size = Vector2(selection_button_size, selection_button_size)
	selection_theme.set_font_size("font_size", "Button", max(selection_button_font_initial / canvas_view_scale, selection_button_font_initial))


func start_transform(button_name: String) -> void:
	if not transforming:
		transforming = true
		transform_starting_position = get_node("%DesignerCanvas/%CanvasViewport").get_mouse_position()
		transform_rotate = false
		transform_type = button_name.substr(6)
		var opposite_type: String
		if transform_type == "R":
			transform_rotate = true
		else:
			if transform_type == "NW":
				opposite_type = "SE"
			elif transform_type == "N":
				opposite_type = "S"
			elif transform_type == "NE":
				opposite_type = "SW"
			elif transform_type == "E":
				opposite_type = "W"
			elif transform_type == "SE":
				opposite_type = "NW"
			elif transform_type == "S":
				opposite_type = "N"
			elif transform_type == "SW":
				opposite_type = "NE"
			elif transform_type == "W":
				opposite_type = "E"
			transform_opposite_position = get_node("%DesignerCanvas/%TransformButtons/Button" + opposite_type).position + Vector2(selection_button_size/2, selection_button_size/2)
			transform_middle_position = (get_node("%DesignerCanvas/%TransformButtons/Button" + transform_type).position + transform_opposite_position) / 2 + Vector2(selection_button_size/2, selection_button_size/2)
		for layer in layer_list.selected_layers:
			transform_node_index_dict[layer.linked_node] = layer.linked_node.get_index()
		transform_node = Control.new()
		var bounding_box: Vector4 = layer_list.get_selection_bounding_box()
		transform_node.position = Vector2((bounding_box[0] + bounding_box[2]) / 2, (bounding_box[1] + bounding_box[3]) / 2)
		transform_node_starting_position = transform_node.position
		if len(layer_list.selected_layers) == 1:
			var selected_node: Node = layer_list.selected_layers[0].linked_node
			layer_nodes.add_child(transform_node)
			if selected_node is Sprite2D:
				transform_node.rotation = selected_node.rotation
			layer_nodes.move_child(transform_node, selected_node.get_index())
		elif len(layer_list.selected_layers) > 1:
			layer_nodes.add_child(transform_node)
			transform_node.rotation = 0
			var average_index: float = 0
			for layer in layer_list.selected_layers:
				average_index += layer.linked_node.get_index()
			average_index /= len(layer_list.selected_layers)
			layer_nodes.move_child(transform_node, int(average_index))
		for layer in layer_list.selected_layers:
			layer.linked_node.reparent(transform_node)
		transform_node_starting_rotation = transform_node.rotation


func stop_transform() -> void:
	for layer in layer_list.selected_layers:
		if layer.layer_type in ["text", "rect", "ellipse"]:
			layer.linked_node.scale *= transform_node.scale
			layer.linked_node.rotation = transform_node.rotation + layer.linked_node.rotation
	layer_nodes.remove_child(transform_node)
	for index in range(len(layer_nodes.get_children()) + len(transform_node.get_children())):
		for key in transform_node_index_dict.keys():
			if transform_node_index_dict[key] == index:
				key.reparent(layer_nodes)
				layer_nodes.move_child(key, transform_node_index_dict[key])
	transforming = false
	transform_node_index_dict = {}
	layer_list.update_transform_buttons()


func _gui_input(event: InputEvent) -> void:
	# Ignore input if colour picker open
	var colour_picker_open: bool = false
	for node in colour_button_nodes:
		if node.get_popup().visible:
			colour_picker_open = true
	if not colour_picker_open:
		
		# Hand tool
		if toolbar.selected_tool == "ToolHand" or Input.is_key_pressed(KEY_SPACE) or (event is InputEventMouseMotion and event.button_mask == 4):
			if event is InputEventMouseMotion and event.button_mask in [1, 4]:
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
			if transforming:
				# Stop transform on mouse release
				if event is InputEventMouseButton and event.button_index == 1 and not event.pressed:
					stop_transform()
				
				# Transform on drag
				elif event is InputEventMouseMotion and event.button_mask == 1:
					if transform_type == "R":
						transform_node.rotation = (transform_node_starting_position - get_canvas_position(event.position)).angle() - PI/2 + transform_node_starting_rotation
						if Input.is_key_pressed(KEY_SHIFT):
							transform_node.rotation = snapped(transform_node.rotation, PI/12)
					else:
						var initial_scale: Vector2 = transform_opposite_position - transform_starting_position
						var current_scale: Vector2 = transform_opposite_position - get_canvas_position(event.position)
						var transform_node_scale_change: Vector2 = current_scale / initial_scale
						if transform_type in ["N", "S"]:
							transform_node_scale_change.x = 1
						elif transform_type in ["E", "W"]:
							transform_node_scale_change.y = 1
						transform_node.scale = transform_node_scale_change
						var transform_node_position_change: Vector2 = (transform_starting_position - get_canvas_position(event.position)) / -2
						if transform_type in ["N", "S"]:
							transform_node_position_change.x = 0
						elif transform_type in ["E", "W"]:
							transform_node_position_change.y = 0
						transform_node.position = transform_node_starting_position + transform_node_position_change
						layer_list.update_transform_buttons()
			
			else:
				# Select on click
				if event is InputEventMouseButton and event.button_index == 1 and event.pressed and \
				((Input.is_key_pressed(KEY_CTRL) and tool_buttons.get_node("MoveButtons/AutoSelect").button_pressed == false) or \
				(Input.is_key_pressed(KEY_CTRL) == false and tool_buttons.get_node("MoveButtons/AutoSelect").button_pressed)):
					var selecting_layer: bool = false
					for layer in layer_list.get_children():
						if layer.bounding_box().has_point(get_canvas_position(event.position)):
							layer_list.select_layer(layer.get_index(), true)
							selecting_layer = true
							break
					if not selecting_layer:
						layer_list.deselect_all()
				
				# Move on drag
				elif event is InputEventMouseMotion and event.button_mask == 1:
					for layer in layer_list.selected_layers:
						layer.linked_node.position += (event.relative / canvas_view_scale)
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
			# Finish drawing shape on mouse release
			if event is InputEventMouseButton and event.button_index == 1 and not event.pressed and drawing_shape:
				drawing_shape = false
				if event.position == drawing_shape_starting_pos:
					drawing_shape_node.queue_free()
				else:
					layer_list.add_shape_layer(drawing_shape_node, drawing_shape_type, drawing_shape_colour)
			
			# Start drawing shape on click
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
			
			# Draw shape on drag
			elif event is InputEventMouseMotion and event.button_mask == 1 and drawing_shape:
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
	update_selection_theme()
	layer_list.update_transform_buttons()
