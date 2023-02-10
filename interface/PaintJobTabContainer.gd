extends TabContainer

var max_tabs = 5


func _on_tab_changed(index: int):
	if get_tab_control(index).name == "+":
		rename_tab("New Paint Job", index)
		if get_tab_count() < max_tabs:
			var tab_scene = preload("res://interface/PaintJobTab.tscn")
			var tab_inst = tab_scene.instance()
			add_child(tab_inst)
			get_tab_control(get_tab_count() - 1).name = "+"


func _get_tab_names():
	var tab_names = []
	for index in get_tab_count():
		tab_names.append(get_tab_control(index).name)
	return tab_names


func rename_tab(new_name: String, index: int=current_tab):
	if new_name == "":
		new_name = "New Paint Job"
	var tab_names = _get_tab_names()
	if new_name in tab_names:
		for i in range(max_tabs):
			if not (new_name + " " + str(i + 2) in tab_names):
				get_tab_control(index).name = new_name + " " + str(i + 2)
				break
	else:
		get_tab_control(index).name = new_name
