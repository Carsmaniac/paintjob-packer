extends TabContainer

const VehicleTab := preload("res://interface/VehicleTab.tscn")


func load_tabs() -> void:
	for child in get_children():
		remove_child(child)
	
	var list_dict: Dictionary = {
		"Trucks": VehicleDatabase.trucks, 
		"Trailers": VehicleDatabase.trailers, 
		"Truck Mods": VehicleDatabase.truck_mods, 
		"Trailer Mods": VehicleDatabase.trailer_mods, 
		"Bus Mods": VehicleDatabase.bus_mods, 
		"Car Mods": VehicleDatabase.car_mods
	}
	
	for tab in list_dict.keys():
		if len(list_dict[tab]) > 0:
			var tab_node: Node = VehicleTab.instantiate()
			tab_node.name = tab
			tab_node.init(list_dict[tab], true)
			add_child(tab_node)
	update_localisation()

func update_localisation() -> void:
	var tab_index: int = 0
	var tab_names: Array[Array] = [
		[VehicleDatabase.trucks, "TAB_TRUCKS"], [VehicleDatabase.trailers, "TAB_TRAILERS"],
		#[VehicleDatabase.buses, "TAB_BUSES"], [VehicleDatabase.cars, "TAB_CARS"],
		[VehicleDatabase.truck_mods, "TAB_TRUCK_MODS"], [VehicleDatabase.trailer_mods, "TAB_TRAILER_MODS"], 
		[VehicleDatabase.bus_mods, "TAB_BUS_MODS"], [VehicleDatabase.car_mods, "TAB_CAR_MODS"]]
	for tab in tab_names:
		if len(tab[0]) > 0:
			if tab_index < get_tab_count():
				set_tab_title(tab_index, tr(tab[1]))
				tab_index += 1
