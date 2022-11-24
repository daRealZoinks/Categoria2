import dearpygui.dearpygui as dpg
import random


def button_pressed():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    dpg.set_viewport_clear_color([r, g, b, 255])


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Ni ba", width=500, height=500, pos=(100, 100), modal=True):
    dpg.add_text("O waw")
    dpg.add_button(label="Uite un buton", callback=button_pressed)
    dpg.add_input_text(label="aci putem scrie")
    dpg.add_slider_float(label="de asta putem trage")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
