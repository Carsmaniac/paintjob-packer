extends Tabs

func _ready() -> void:
	var __ = $Name/TextInput.connect("text_changed", get_parent(), "rename_tab")
