from gpiozero import Button
from pygame import mixer

stopMusicButton = Button(16)

mixer.init()
mixer.music.load('Birds on a wire - Sur la place.mp3')
mixer.music.play()

while True:
    if stopMusicButton.is_pressed == True:
        mixer.music.stop()