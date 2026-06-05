extends HBoxContainer


func _ready() -> void:
	get_node("TransformControls").connect("toggled", update_transform_buttons)


func update_transform_buttons(_pressed: bool) -> void:
	get_node("%LayerList").update_transform_buttons()
