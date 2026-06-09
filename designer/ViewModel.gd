extends SubViewportContainer


func _ready() -> void:
	get_node("%FilteredViewport").world_2d = get_node("%DesignerCanvas/%CanvasViewport").world_2d


func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and event.button_mask == 1:
		get_node("SubViewport/PreviewModel/CameraOrbiter").rotation.y -= event.relative.x * 0.01
		get_node("SubViewport/PreviewModel/CameraOrbiter").rotation.x -= event.relative.y * 0.01
