import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import dearpygui_ext.themes as themes
import random

dpg.create_context()


def button_pressed():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	dpg.set_viewport_clear_color([r, g, b, 255])


dpg.create_viewport(title="Tema3", width=1270, height=720)

dark_theme = themes.create_theme_imgui_dark()
light_theme = themes.create_theme_imgui_light()

dpg.bind_theme(dark_theme)

dpg.setup_dearpygui()
dpg.show_style_editor()
demo.show_demo()


with dpg.window(label="Ni ba", width=500, height=200, pos=(100, 100)):
	dpg.add_text("O waw")
	dpg.add_button(label="Uite un buton", callback=button_pressed)
	dpg.add_input_text(label="aci putem scrie")
	dpg.add_slider_float(label="de asta putem trage")

with dpg.window(label="Fereastra", width=500, height=150, pos=(100, 100)):
	dpg.add_button(label="Uite alt buton", callback=button_pressed)
	dpg.add_text("Nuj dc am atatea butoane si ferestre")
	dpg.add_input_text(label="aci putem scrie si mai mult")
	dpg.add_slider_float(label="de asta putem trage si mai mult", max_value=100, default_value=50)

	with dpg.collapsing_header(label="Node Editor"):
		dpg.add_text("Ctrl+Click to remove a link.", bullet=True)

		with dpg.node_editor(callback=lambda sender, app_data: dpg.add_node_link(app_data[0], app_data[1], parent=sender),
							 delink_callback=lambda sender, app_data: dpg.delete_item(app_data), minimap=True,
							 minimap_location=dpg.mvNodeMiniMap_Location_BottomRight):
			with dpg.node(label="Node 1", pos=[10, 10]):
				with dpg.node_attribute():
					dpg.add_input_float(label="F1", width=150)

				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
					dpg.add_input_float(label="F2", width=150)

			with dpg.node(label="Node 2", pos=[300, 10]):
				with dpg.node_attribute() as na2:
					dpg.add_input_float(label="F3", width=200)

				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
					dpg.add_input_float(label="F4", width=200)

			with dpg.node(label="Node 3", pos=[25, 150]):
				with dpg.node_attribute():
					dpg.add_input_text(label="T5", width=200)
				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
					dpg.add_simple_plot(label="Node Plot", default_value=(0.3, 0.9, 2.5, 8.9), width=200, height=80,
										histogram=True)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
