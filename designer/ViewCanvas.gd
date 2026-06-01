extends SubViewportContainer
var canvas: Node


func _ready() -> void:
	canvas = get_node("SubViewport/DesignerCanvas")


func _gui_input(event: InputEvent) -> void:
	print(event)
	if event is InputEventMouseMotion and event.button_mask == 1:
		canvas.position += event.relative
	elif event is InputEventMouseButton and event.button_index == 4:
		canvas.scale *= 1.05
		#canvas.position -= (event.position - canvas.position) * canvas.scale
	elif event is InputEventMouseButton and event.button_index == 5:
		canvas.scale *= 0.95
