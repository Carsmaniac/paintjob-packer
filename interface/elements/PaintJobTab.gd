extends Tabs

#signal name_field_changed(name)

func _ready():
	var __ = $Name.get_node("TextInput").connect("text_changed", get_parent(), "dynamically_rename_tab")
#	self.connect("name_field_changed", get_parent(), "dynamically_rename_tab")
#
#func _rename_tab(_new_name: String):
#	emit_signal("name_field_changed", _new_name)
