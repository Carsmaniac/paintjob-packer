extends TabContainer

var max_tabs: int = 5
const TabScene := preload("res://interface/PaintJobTab.tscn")


func _ready() -> void:
	get_tab_bar().tab_close_display_policy = TabBar.CLOSE_BUTTON_SHOW_NEVER
	get_tab_bar().connect("tab_close_pressed", remove_tab)
	add_tab("New Paint Job")
	add_tab("+")
	current_tab = 0
	
func add_tab(tab_name: String) -> void:
	var new_tab := TabScene.instantiate()
	load_vehicles_for_tab(new_tab)
	add_child(new_tab)
	rename_tab(tab_name, len(get_children()) - 1)
	
	
func load_tabs() -> void:
	for child in get_children():
		load_vehicles_for_tab(child)
		

func load_vehicles_for_tab(tab: Node) -> void:
	var vehicle_tab_container: Node = tab.find_child("VehicleTabContainer")
	for vehicle_tab in vehicle_tab_container.get_children():
		vehicle_tab_container.remove_child(vehicle_tab)
	vehicle_tab_container.load_tabs()
	tab.update_vehicles_selected_number()
	
	
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
	if index != -1:
		if get_tab_control(index).name == "+":
			rename_tab("New Paint Job", index)
			if get_tab_count() < max_tabs:
				var tab_inst := TabScene.instantiate()
				load_vehicles_for_tab(tab_inst)
				tab_inst.name = "+" 
				add_child.call_deferred(tab_inst)
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
