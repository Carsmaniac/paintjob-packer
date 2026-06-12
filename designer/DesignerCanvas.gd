extends Control

var width: int = 4096
var height: int = 4096


func _ready() -> void:
	resize_canvas(Vector2(4096, 4096))


func resize_canvas(new_size: Vector2i) -> void:
	get_node("CanvasViewportContainer").size = new_size * 2
	get_node("%FilteredViewport").size = new_size * 2
	get_node("%CroppedViewport").size = new_size * 2
	get_node("%CropTexture").size = new_size * 2
	get_node("%CropTexture").scale = Vector2(2, 2)
	get_node("%CropTexture").position = -new_size
	for node in ["%BackgroundColour", "%BackgroundTemplate", "%ForegroundTemplate"]:
		get_node(node).size = new_size
		get_node(node).position = new_size / 2.0
	width = new_size.x
	height = new_size.y
