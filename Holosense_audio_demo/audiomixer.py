import pygame as pg

pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512) 
sound0 = pg.mixer.Sound('YOASOBIアイドル Official Music Video.mp3')
channel = pg.mixer.Channel(0)

# Play the sound (that will reset the volume to the default).
channel.play(sound0)
# Now change the volume of the specific speakers.
# The first argument is the volume of the left speaker and
# the second argument is the volume of the right speaker.


while True:
    a = float(input("left: ")) / 100
    b = float(input("right: ")) / 100
    channel.set_volume(a, b)