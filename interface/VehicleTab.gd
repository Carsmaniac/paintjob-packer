extends Tabs

const VehicleSelection := preload("res://interface/VehicleSelection.tscn")


func init(vehicle_list: Array, show_cabins: bool):
	var show_author: bool = vehicle_list[0]["mod"]
	if vehicle_list[0]["trailer"]:
		show_cabins = false

	for vehicle in vehicle_list:
		var selection: Node = VehicleSelection.instance().init(vehicle, show_cabins, show_author)
		get_node("ScrollContainer/VBoxContainer").add_child(selection)


func update_selection_sizes() -> void:
	for selection in get_node("ScrollContainer/VBoxContainer").get_children():
		selection.set_min_size()
