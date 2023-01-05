import sys, pygame, pygame.gfxdraw, random
from src.game_object import GameObject


# the bouncy ball we are trying to hit.
class Ballon(GameObject):
    def update(self, display):
        # this will draw a cirlcle to represent the ballon
        pygame.gfxdraw.aacircle(display, self.x,self.y, self.size, self.color)
        # as described in the documentation for anti-antialiased drawing, both a filled and non-filled 
        # drawing have to combine to make a filled anti-antialiased drawing.
        pygame.gfxdraw.filled_circle(display, self.x,self.y, self.size, self.color)

        # 1 out of 30 chance each frame to change direction creates sense of randomnesses in the ballon.
        if random.randint(0, 30) == 1:
                self.velocity = (self.velocity) * -1    #invert the velocity / change direction


class Cannon(GameObject):
    def update(self, display):
        # this will draw a cannon-like polygon.
        pygame.gfxdraw.aapolygon(display, 
            (
                (self.x - 50, self.y + 20),
                (self.x - 50, self.y - 10),
                (self.x + 40, self.y - 30),
                (self.x + 40, self.y + 30)
            ), self.color)
        # as described in the documentation for anti-antialiased drawing, both a filled and non-filled 
        # drawing have to combine to make a filled anti-antialiased drawing.
        pygame.gfxdraw.filled_polygon(display,
            (
                (self.x - 50, self.y + 20),
                (self.x - 50, self.y - 10),
                (self.x + 40, self.y - 30),
                (self.x + 40, self.y + 30)
            ), self.color)

class Bullet(GameObject):
    def update(self, display):
        # if the bullet hits the left wall of the window (which is x=0) than don't render the bullet
        if (self.x > 0):
            # this will draw a ballon
            pygame.gfxdraw.aacircle(display, self.x, self.y, self.size, self.color,)
            # as described in the documentation for anti-antialiased drawing, both a filled and non-filled 
            # drawing have to combine to make a filled anti-antialiased drawing.
            pygame.gfxdraw.filled_circle(display, self.x, self.y, self.size, self.color,)
            self.push_x()


