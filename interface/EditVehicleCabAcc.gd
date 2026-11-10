extends VBoxContainer


func _ready() -> void:
	get_node("RemoveButton").pressed.connect(queue_free)
