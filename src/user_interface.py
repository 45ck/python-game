import sys, pygame, pygame.gfxdraw

class UserInterface():
    display = None

    def __init__(self, display):
        self.display = display
    
    #creates text on the screen for the user to see.
    def create_text(self, text, coordinates, size=30, color=(0,0,0), font="Comic Sans MS"):
        font = pygame.font.SysFont(font, size)
        text_ui = font.render(text, True, color)
        self.display.blit(text_ui, coordinates)


