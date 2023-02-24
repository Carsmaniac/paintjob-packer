extends TabContainer

const VehicleTab := preload("res://interface/VehicleTab.tscn")
var game: String = "ets"


func _ready():
	VehicleDatabase.load_vehicle_lists()
	var list_dict = {
		"Trucks": VehicleDatabase.trucks, 
		"Trailers": VehicleDatabase.trailers, 
		"Truck Mods": VehicleDatabase.truck_mods, 
		"Trailer Mods": VehicleDatabase.trailer_mods, 
		"Bus Mods": VehicleDatabase.bus_mods, 
		"Car Mods": VehicleDatabase.car_mods
	}
	
	for tab in list_dict.keys():
		if len(list_dict[tab]) > 0:
			var tab_node: Node = VehicleTab.instance()
			tab_node.name = tab
			tab_node.init(list_dict[tab], true)
			add_child(tab_node)
