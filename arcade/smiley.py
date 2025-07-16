import arcade 

arcade.open_window (1000 , 1000 , "test")
arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

arcade.start_render()

arcade.draw_arc_filled(325,675,250,250,arcade.color.BLACK,45,275)
arcade.draw_arc_filled(690,655,250,250,arcade.color.BLACK,0,360)

arcade.draw_circle_filled(500, 500, 300, arcade.color.YELLOW)

arcade.draw_circle_filled(350, 625, 50, arcade.color.BLACK)
arcade.draw_circle_filled(650, 625, 50, arcade.color.BLACK)

arcade.draw_arc_filled(500,350,200,200,arcade.color.BLACK,0,360)
arcade.draw_arc_filled(500,350,200,200,arcade.color.YELLOW,0,180)

arcade.draw_triangle_filled(450, 450, 550, 450, 500, 550, arcade.color.BLACK)


arcade.finish_render()
arcade.run()
