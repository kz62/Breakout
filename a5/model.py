# model.py
# Kai Feng Zhang kz62 Daniel Chun dhc62
# 5/5/2014
"""Model module for Breakout

This module contains the model classes for the Breakout game. Instances of
Model storee the paddle, ball, and bricks.  The model has methods for resolving
collisions between the various game objects.  A lot of your of your work
on this assignment will be in this class.

This module also has an additional class for the ball.  You may wish to add
more classes (such as a Brick class) to add new features to the game.  What
you add is up to you."""
from constants import *
from game2d import *
import random # To randomly generate the ball velocity

class Model(object):
    """An instance is a single game of breakout.  The model keeps track of the
    state of the game.  It tracks the location of the ball, paddle, and bricks.
    It determines whether the player has won or lost the game.  
    
    To support the game, it has the following instance attributes:
    
        bricks:  the bricks still remaining 
                  [list of GRectangle, can be empty]
        paddle:  the paddle to play with 
                  [GRectangle, never None]
        balls:    a list of balls
                  [list of Balls, or [] if waiting for a serve]
        numballs: an int representing amount of balls that have been created
                  [initialized as 1]
    """
    # As with the controller, any attributes that you add to this class
    # must be documented above, along with their invariants.
    
    # INITIALIZER (TO CREATE PADDLES AND BRICKS)
    def __init__(self):
        self.bricks = []
        self.balls = []
        for a in range(BRICK_ROWS):
            if a % 10 < 2:
                color = colormodel.RED
            elif a % 10 < 4:
                color = colormodel.ORANGE
            elif a % 10 < 6:
                color = colormodel.YELLOW
            elif a % 10 < 8:
                color = colormodel.GREEN
            else:
                color = colormodel.CYAN
            for b in range(BRICKS_IN_ROW):
                self.bricks.append(GRectangle(x=BRICK_SEP_H/2+
                                              b*(BRICK_WIDTH+BRICK_SEP_H),
                        y = GAME_HEIGHT-BRICK_Y_OFFSET-a*(BRICK_HEIGHT
                                                          + BRICK_SEP_V),
                            width = BRICK_WIDTH, height = BRICK_HEIGHT,
                            fillcolor = color, linecolor = color))
        self.paddle = GRectangle(center_x = GAME_WIDTH/2, y = PADDLE_OFFSET,
                                 width = PADDLE_WIDTH,
                                 height = PADDLE_HEIGHT,
                                 fillcolor = colormodel.BLACK)
        self.balls.append(Ball())
        self.numballs = 1
    
    # ADD ANY ADDITIONAL METHODS (PROPERLY SPECIFIED) HERE
    def moveBall(self, ball):
        """Precondition: ball is an instance of Ball
        
        Moves balls.
        
        If the ball collides with the paddle while going down,
        the vertical direction of the ball is reversed.
        If the ball collides with a brick,
        the brick is removed
        and the vertical direction of the ball is reversed.
        """
        ball.center_x += ball.vx
        ball.center_y += ball.vy
        if ball.top + ball.vy >= GAME_HEIGHT:
            ball.vy = -ball.vy
            ball.top = GAME_HEIGHT
        #if ball.bottom <= 0:
            #ball.vy = -ball.vy
        if ball.left + ball.vx <= 0:
            ball.left = 0
            ball.vx *= -1
        if ball.right + ball.vx >= GAME_WIDTH:
            ball.right = GAME_WIDTH
            ball.vx *= -1
        if ball.vy < 0 and self._getCollidingObject(ball) is self.paddle:
            if ball.x < self.paddle.x + PADDLE_WIDTH/4 and ball.vx > 0:
                ball.vx *= -1
            if ball.x > self.paddle.x + 3*PADDLE_WIDTH/4 and ball.vx < 0:
                ball.vx *= -1
            ball.vy *= -1
            ball.vy += .05
        if self._getCollidingObject(ball) in self.bricks:
            ball.vy = -ball.vy
            self.bricks.remove(self._getCollidingObject(ball))
            return True

    def _getCollidingObject(self, ball):
        """Precondition: ball is an instance of Ball
        
        Returns: GObject that has collided with the ball

        This method checks the four corners of the ball, one at a
        time. If one of these points collides with either the paddle
        or a brick, it stops the checking immediately and returns the
        object involved in the collision. It returns None if no
        collision occurred."""
        if self.paddle.contains(ball.left, ball.bottom) or \
        self.paddle.contains(ball.right, ball.bottom) or \
        self.paddle.contains(ball.left, ball.top) or \
        self.paddle.contains(ball.right, ball.top):
            return self.paddle
        else:
            for i in self.bricks:
                if i.contains(ball.left, ball.bottom) or \
                i.contains(ball.right, ball.bottom) or \
                i.contains(ball.left, ball.top) or \
                i.contains(ball.right, ball.top):
                    return i


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball needs attributes for
    velocity. This subclass adds these two attributes.
    
    INSTANCE ATTRIBUTES:
        vx: Velocity in x direction [int or float]
        vy: Velocity in y direction [int or float]
    
    You should add two methods to this class: an initializer to set the
    starting velocity  and a method to "move" the ball. The move method
    should adjust the ball position according to the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but then you will have to
    modify the class header up above.
    """
    def __init__(self):
        GEllipse.__init__(self, center_x = GAME_WIDTH/2,
                          center_y = GAME_HEIGHT/2,
                          width = BALL_DIAMETER,
                          height = BALL_DIAMETER,
                          fillcolor = colormodel.BLACK)
    # INITIALIZER TO SET VELOCITY
        self.vx = random.uniform(1.0,5.0) 
        self.vx = self.vx * random.choice([-1, 1])
        self.vy = -5.0
    # METHOD TO MOVE BALL BY PROPER VELOCITY


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY



# ADD ANY ADDITIONAL CLASSES HERE