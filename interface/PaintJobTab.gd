extends Tabs

func _ready():
	var __ = $Name.get_node("TextInput").connect("text_changed", get_parent(), "rename_tab")
