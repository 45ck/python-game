import sys, pygame, pygame.gfxdraw

class GameObject():
    x = 0
    y = 0
    velocity = 0
    move_speed = 1
    color = (255, 255, 255) #default color is white.
    size = 30
    
    #if use constraints is enabled, all maximum limits will apply to this game object
    use_constraints = False
    maximum_x = 0
    maximum_y = 0
    minimum_x = 0
    minimum_y = 0

    #constructor: this will occur when the game object is created.
    def __init__(self, coordinates):
        # coordinates must be in format of (x,y) as in pygame.
        self.x = coordinates[0]
        self.y = coordinates[1]

    #moves the game object in an upwards direction
    def move_up(self):
        # if we have gone over the constraint than go back to the constraint limit
        if self.use_constraints and self.minimum_y >= self.y:
            self.y = self.minimum_y
         # if no constraints are enabled, move as per usual. 
        else:
            self.y -= self.move_speed

    #moves the game object in a downwards direction
    def move_down(self):
        # if we have gone over the constraint than go back to the constraint limit
        if self.use_constraints and self.maximum_y <= self.y:
            self.y = self.maximum_y
         # if no constraints are enabled, move as per usual. 
        else:
            self.y += self.move_speed

    def move_left(self):
        # if we have gone over the constraint than go back to the constraint limit
        if self.use_constraints and self.minimum_x >= self.x:
            self.x = self.minimum_x
         # if no constraints are enabled, move as per usual. 
        else:
            self.y -= self.move_speed

    def move_right(self):
        # if we have gone over the constraint than go back to the constraint limit
        if self.use_constraints and self.maximum_x <= self.x:
            self.x = self.maximum_x
        # if no constraints are enabled, move as per usual. 
        else:   
            self.y += self.move_speed

    def push_y(self):
        #if constraints are enabled, make sure that the object doesn't go outside of the constraints.
        if self.use_constraints and self.maximum_x <= self.x:
            self.x = self.maximum_x
        elif self.use_constraints and self.minimum_x >= self.x:
            self.x = self.minimum_x
        # if object is inside of the constraints or not using constraints than move the object
        else:
            self.y += self.velocity
    
    def push_x(self):
         #if constraints are enabled, make sure that the object doesn't go outside of the constraints.
        if self.use_constraints and self.maximum_x <= self.x:
            self.x = self.maximum_x
        elif self.use_constraints and self.minimum_x >= self.x:
            self.x = self.minimum_x
         # if object is inside of the constraints or not using constraints than move the object
        else:
            self.x += self.velocity