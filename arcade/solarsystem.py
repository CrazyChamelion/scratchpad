import arcade 
win_len = 1000
win_wid = 1000
sun_posx = win_len/2
sun_posy = win_wid/2
#based on orbit or mars
def autp(au):
    return au*450/1.5

arcade.open_window (win_len , win_wid , "test")
arcade.set_background_color(arcade.color.BLACK)

arcade.start_render()
arcade.draw_circle_filled(sun_posx,sun_posy,30,arcade.color.YELLOW) 
#due to size limitations we focus on inner solar system 
##Neptune orbit
#arcade.draw_circle_outline(sun_posx,sun_posy,autp(31),arcade.color.NEON_FUCHSIA) 
##Urinus 
#arcade.draw_circle_outline(sun_posx,sun_posy,autp(19.2),arcade.color.NEON_FUCHSIA)
##Saturn
#arcade.draw_circle_outline(sun_posx,sun_posy,autp(9.56),arcade.color.NEON_FUCHSIA)
##Jupiter 
#arcade.draw_circle_outline(sun_posx,sun_posy,autp(5.21),arcade.color.NEON_FUCHSIA)
#Mars 
arcade.draw_circle_outline(sun_posx,sun_posy,autp(1.52),arcade.color.NEON_FUCHSIA)
marsposx = sun_posx + autp(1.52)
marsposy = sun_posy
arcade.draw_circle_filled(marsposx,marsposy,10,arcade.color.ORANGE)
#Earth 
arcade.draw_circle_outline(sun_posx,sun_posy,autp(1),arcade.color.NEON_FUCHSIA)
earthposx = sun_posx + autp(1)
earthposy = sun_posy
arcade.draw_circle_filled(earthposx,earthposy,10,arcade.color.BLUE)
#venus
arcade.draw_circle_outline(sun_posx,sun_posy,autp(0.722),arcade.color.NEON_FUCHSIA)
venusposx = sun_posx + autp(0.722)
venusposy = sun_posy
arcade.draw_circle_filled(venusposx,venusposy,10,arcade.color.LIGHT_BLUE)
#mercury
arcade.draw_circle_outline(sun_posx,sun_posy,autp(0.387),arcade.color.NEON_FUCHSIA)
mercuryposx = sun_posx + autp(0.387)
mercuryposy = sun_posy
arcade.draw_circle_filled(mercuryposx,mercuryposy,10,arcade.color.RED)
arcade.finish_render()
print (autp(0.387))
arcade.run()

