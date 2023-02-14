extends Tabs


const SelectionScene := preload("res://interface/VehicleSelection.tscn")


func _ready():
	for i in range(3):
		for j in range(2):
			var _selection_inst := SelectionScene.instance()
			_selection_inst.set_position(Vector2(1 + (j*346), -2 + (i*73)))
			add_child(_selection_inst)
		
