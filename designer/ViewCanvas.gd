extends SubViewportContainer
var canvas: Node
var zoom_amount: float = 1.02
var canvas_view_scale: float = 1.0


func _ready() -> void:
	canvas = get_node("SubViewport/DesignerCanvas")


func _gui_input(event: InputEvent) -> void:
	var selected_tool: String = get_node("../../Toolbar").selected_tool
	if selected_tool == "ToolHand":
		if event is InputEventMouseMotion and event.button_mask == 1:
			canvas.position += event.relative
		elif event is InputEventMouseButton and event.button_index == 4:
			zoom_to_pos(true, event.position)
		elif event is InputEventMouseButton and event.button_index == 5:
			zoom_to_pos(false, event.position)


func zoom_to_pos(zoom_in: bool, mouse_pos: Vector2) -> void:
	var zoom_pos: Vector2 = (mouse_pos - canvas.position) / canvas_view_scale
	
	if zoom_in:
		canvas_view_scale *= zoom_amount
		canvas.scale = Vector2(canvas_view_scale, canvas_view_scale)
		canvas.position.x -= zoom_pos.x * (zoom_amount - 1) * canvas_view_scale
		canvas.position.y -= zoom_pos.y * (zoom_amount - 1) * canvas_view_scale
	else:
		canvas_view_scale /= zoom_amount
		canvas.scale = Vector2(canvas_view_scale, canvas_view_scale)
		canvas.position.x += zoom_pos.x * (zoom_amount - 1) * canvas_view_scale
		canvas.position.y += zoom_pos.y * (zoom_amount - 1) * canvas_view_scale
	print(canvas_view_scale)
