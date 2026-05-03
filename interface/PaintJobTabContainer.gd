extends TabContainer

var max_tabs: int = 5
const TabScene := preload("res://interface/PaintJobTab.tscn")


func _ready() -> void:
	get_tab_bar().tab_close_display_policy = TabBar.CLOSE_BUTTON_SHOW_NEVER
	get_tab_bar().connect("tab_close_pressed", remove_tab)
	
func remove_tab(tab_index: int) -> void:
	if len(get_children()) > 2:
		remove_child(get_child(tab_index))
	if get_children()[-1].name != "+":
		var tab_inst := TabScene.instantiate()
		add_child(tab_inst)
		get_tab_control(get_tab_count() - 1).name = "+" 
	if len(get_children()) > 2:
		get_tab_bar().tab_close_display_policy = TabBar.CLOSE_BUTTON_SHOW_ACTIVE_ONLY
	else:
		get_tab_bar().tab_close_display_policy = TabBar.CLOSE_BUTTON_SHOW_NEVER

func _on_tab_changed(index: int) -> void:
	if get_tab_control(index).name == "+":
		rename_tab("New Paint Job", index)
		if get_tab_count() < max_tabs:
			var tab_inst := TabScene.instantiate()
			add_child(tab_inst)
			get_tab_control(get_tab_count() - 1).name = "+" 
			if len(get_children()) > 2:
				get_tab_bar().tab_close_display_policy = TabBar.CLOSE_BUTTON_SHOW_ACTIVE_ONLY
			else:
				get_tab_bar().tab_close_display_policy = TabBar.CLOSE_BUTTON_SHOW_NEVER


func _get_tab_names() -> Array:
	var tab_names: Array = []
	for index in get_tab_count():
		tab_names.append(get_tab_control(index).name)
	return tab_names


func rename_tab(new_name: String, index: int=current_tab) -> void:
	if new_name == "":
		new_name = "New Paint Job"
	var tab_names: Array = _get_tab_names()
	if new_name in tab_names:
		for i in range(max_tabs):
			if not (new_name + " " + str(i + 2) in tab_names):
				get_tab_control(index).name = new_name + " " + str(i + 2)
				break
	else:
		get_tab_control(index).name = new_name
