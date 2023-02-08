extends TabContainer

func _on_tab_changed(index: int):
	if get_tab_control(index).name == "+":
		get_tab_control(index).name = "Not plus"

func dynamically_rename_tab(_name: String):
	get_current_tab_control().name = _name
