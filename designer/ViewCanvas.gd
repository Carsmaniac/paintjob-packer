extends SubViewportContainer

var canvas: Node
var layer_list: Node
var toolbar: Node
var tool_buttons: Node

var zoom_amount: float = 1.04
var pan_amount: float = 20.0
var canvas_view_scale: float = 1.0


func _ready() -> void:
	canvas = get_node("SubViewport/DesignerCanvas")
	layer_list = get_node("../../RightPanel/ScrollContainer/LayerList")
	toolbar = get_node("../../LeftPanel/Toolbar")
	tool_buttons = get_node("../../TopPanel/HBoxContainer/ToolButtons")


func fit_to_view() -> void:
	var fit_width_scale: float = self.size.x / canvas.width
	var fit_height_scale: float = self.size.y / canvas.height
	if fit_width_scale < fit_height_scale:
		canvas.position = Vector2(0, self.size.y/2 - (canvas_view_scale * canvas.height / 2))
	else:
		canvas.position = Vector2(self.size.x/2 - (canvas_view_scale * canvas.width / 2), 0)
	canvas_view_scale = min(fit_width_scale, fit_height_scale)
	canvas.scale = Vector2(canvas_view_scale, canvas_view_scale)


func _gui_input(event: InputEvent) -> void:
	if Input.is_key_pressed(KEY_SPACE):
		toolbar.selected_tool = "ToolHand"
	
	# Hand tool
	if toolbar.selected_tool == "ToolHand":
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
			for layer in layer_list.get_children():
				if layer.linked_node.get_rect().has_point(get_canvas_position(event.position)):
					layer_list.select_layer(layer.get_index(), true)
					break
		
		# Move on drag
		elif event is InputEventMouseMotion and event.button_mask == 1:
			for layer in layer_list.selected_layers:
				layer.linked_node.position += (event.relative / canvas_view_scale)
	
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
				layer_list.add_text_layer(get_canvas_position(event.position))


func sync_tool_to_layer() -> void:
	if len(layer_list.selected_layers) == 1:
		var selected_layer = layer_list.selected_layers[0]
		if toolbar.selected_tool == "ToolShape" and selected_layer.layer_type == "shape":
			pass
		elif toolbar.selected_tool == "ToolText" and selected_layer.layer_type == "text":
			tool_buttons.get_node("TextButtons/FontSize").value = selected_layer.text_size


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
