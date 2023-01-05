import pygame, os

# tell pygame that we want to use sounds.
pygame.mixer.init()
# find where the main python file is located in directory so we can use that to find assets.
relative_directory = os.path.dirname(os.path.realpath(__file__));

class Sound():
    file_directory = None
    def __init__(self, file_name):
        # add the directory to the sounds, than add the specific sound we want. All sound files should be in assets folder.
        self.pygame_sound = pygame.mixer.Sound(relative_directory + "\\assets\\" + file_name)

    def play(self):
        pygame.mixer.Sound.play(self.pygame_sound)
        pygame.mixer.music.stop()


