extends Button

var vehicle_model: MeshInstance3D


func _ready() -> void:
	connect("pressed", fit_canvas_to_view)
	vehicle_model = get_node("%VehicleModel")


func fit_canvas_to_view() -> void:
	#get_node("../../TwoUp/ViewCanvas").fit_to_view()
	vehicle_model.mesh = ResourceLoader.load("res://designer/untitled2.obj")
	
	#var new_model := MeshInstance3D.new()
	#new_model.mesh = ResourceLoader.load("res://designer/untitled2.obj")
	#var new_tex := ImageTexture.create_from_image(Image.load_from_file("res://designer/temp-canvas.jpg"))
	#var new_mat := StandardMaterial3D.new()
	#new_mat.albedo_texture = new_tex
	#new_model.set_surface_override_material(0, new_mat)
	#vehicle_model.get_parent().add_child(new_model)
