extends Tabs

const VehicleSelection := preload("res://interface/VehicleSelection.tscn")


func _ready():
	create_selections_from_list(VehicleDatabase.truck_mods, true)


func create_selections_from_list(vehicle_list: Array, show_cabins: bool):
	var show_author: bool = vehicle_list[0]["mod"]
	if vehicle_list[0]["trailer"]:
		show_cabins = false

	for i in ceil(len(vehicle_list) / 2.0):
		var hor_container := HBoxContainer.new()
		for j in range(2):
			var vehicle: Dictionary = vehicle_list[i * 2 + j]
			var selection: Node = VehicleSelection.instance().init(
					vehicle, show_cabins, show_author)
			selection.author_row = show_author
			selection.cabin_row = show_cabins
			hor_container.add_child(selection)
		$ScrollContainer/VBoxContainer.add_child(hor_container)
