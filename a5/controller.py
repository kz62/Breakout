# controller.py
# Kai Feng Zhang kz62 Daniel Chun dhc62
# 5/5/2014
"""Primary module for Breakout application

This module contains the controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in the model 
module. If you are ensure about where a new class should go, post a
question on Piazza."""
from constants import *
from game2d import *
from model import *


class Breakout(Game):
    """Instance is a Breakout Application
    
    This class extends Game and implements the various methods necessary
    for running the game.
    
        Method init starts up the game.
        
        Method update updates the model objects (e.g. move ball, remove bricks)
        
        Method draw displays all of the models on the screen
    
    Most of the work handling the game is actually provided in the class Model.
    Model should have a method called moveBall() that moves the ball and processes
    all of the game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    Instance Attributes:
        view:   the game view, used in drawing 
                [Immutable instance of GView, it is inherited from Game]
        _state: the current state of the game
                [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, 
                 STATE_ACTIVE, or STATE_COMPLETE]
        _model: the game model, which stored the paddle, ball, and bricks
                [GModel, or None if there is no game currently active
                 It is only None if _state is STATE_INACTIVE]
        _message: message displayed on screen
                  [description of the game, initialized as "Press to play"]
        _previous: the previous touch
                  [initialized as None]
        _timer: a float number representing the time, in seconds,
                 since the start of STATE_COUNTDOWN)
                 [initialized as 0]
        _lives: an int number representing the number of lives
                 [initalized as 3]
        score: an int representing how many bricks are hit
                 [initialized as 0]
        _header: a GLabel that contains the score and lives left
                 [initialized to contain "Score: 0  Lives left: 3"]
    """
    # You may add more attributes to this class, such as an attribute to store
    # any text messages you display on the screen. Any attributes that you add,
    # along with their invariants, must be documented here.
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # METHODS
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message saying that the user should press to
        play a game."""
        # IMPLEMENT ME
        
        self._state = STATE_INACTIVE
        self._model = None
        self._message = GLabel(text="Press to play", font_size = 50,
                               valign = "middle", halign = "center",
                               center_x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        self._previous = None
        self._timer = 0.0
        self._lives = NUMBER_TURNS
        self.score = 0
        self._header = GLabel(text="Score: "+str(self.score)+\
                "    Lives left: "+str(self._lives), x=0, y=GAME_HEIGHT-40)

    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, and
        others belong in class Model.
        
        The first thing this method should do is to check the state of the
        game. One thing that you can do here to organize your code is to
        have a helper method for each of your states, as the game must do
        different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse. If so, it starts a new game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        starting a whole new game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        This state should delay three seconds.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are lives left, it switches to STATE_PAUSED.  If the ball is lost 
        with no lives left, the game is over and it switches to
        STATE_COMPLETE. It should also switch to STATE_COMPLETE once there
        are no bricks left, since that means the player has won.
        
        While in STATE_COMPLETE, this method does nothing.
        
        You are allowed to add more states if you wish. Should you do so,
        you must describe them here.
        
        Precondition: dt is the time since last update (a float). This
        parameter can be safely ignored most of the time. It is only
        relevant for debugging if your game is running really slowly."""
        # IMPLEMENT ME
        
        if self.view.touch is not None and self._state == STATE_INACTIVE:
            self._state = STATE_COUNTDOWN
            self._previous = self.view.touch
            self._model = Model()
        if self._state == STATE_COUNTDOWN or self._state == STATE_ACTIVE:
            self.movepaddle()
            self._header.text = "Score: "+str(self.score)+\
            "    Lives left: "+str(self._lives)
        if self._state == STATE_COUNTDOWN:
            self._timer += dt
            if self._timer > 3.0:
                self._state = STATE_ACTIVE
                self._timer = 0
        if self._state == STATE_ACTIVE:
            self.addball()
            for ball in self._model.balls:
                if self._model.moveBall(ball):
                    self.score += 1
                    self._header.text = "Score: "+str(self.score)+\
                    "    Lives left: "+str(self._lives)
            for ball in self._model.balls:
                if ball.bottom <= 0:
                    self._model.balls.remove(ball)
                if len(self._model.balls) ==0:
                    self._lives -= 1
                    if self._lives > 0:
                        self._state = STATE_PAUSED
                    else:
                        self._state = STATE_COMPLETE
            if len(self._model.bricks) == 0:
                self._state = STATE_COMPLETE
        if self._state == STATE_PAUSED:
            self.pause()
        if self._state == STATE_COMPLETE:
            self.complete()
            self.tryagain()

    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Model. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Model.  Which one you do is up to you."""
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self._message.draw(self.view)
        if self._state == STATE_COUNTDOWN or self._state == STATE_ACTIVE:
            for i in self._model.bricks:
                i.draw(self.view)
            self._model.paddle.draw(self.view)
            self._header.draw(self.view)
        if self._state == STATE_ACTIVE:
            for ball in self._model.balls:
                ball.draw(self.view)
            self._header.draw(self.view)
        if self._state == STATE_PAUSED or self._state == STATE_COMPLETE:
            self._message.draw(self.view)
    
    # ADD HELPER METHODS HERE
    def movepaddle(self):
        """Moves the paddle during the game.
        
        This method uses the paddle's x-position to make it move.
        The paddle moves once the user clicks the mouse.
        The position of the paddle moves by the difference
        between the current touch and the previous touch.
        The paddle stays within the bounds of the game;
        that is, the minimum x position value is 0
        and the maximum is GAME_WIDTH - PADDLE_WIDTH.
        """
        if self._previous == None and self.view.touch is not None:
            self._previous = self.view.touch
        if self.view.touch is not None:
            if self._model.paddle.x + self.view.touch.x - \
            self._previous.x < 0:
                self._model.paddle.x = 0
            elif self._model.paddle.x + self.view.touch.x - \
            self._previous.x > GAME_WIDTH - PADDLE_WIDTH:
                self._model.paddle.x = GAME_WIDTH - PADDLE_WIDTH
            else:
                self._model.paddle.x += self.view.touch.x - \
                                        self._previous.x
                self._previous = self.view.touch
        else:
            self._previous = None
    
    def pause(self):
        """Pauses the game after a death.
        
        Displays a message that tells you the number of lives left.
        Additionally, it will inform the user to press in order to play.
        After the user presses the mouse, it changes the state to
        STATE_COUNTDOWN and initializes the ball.
        """
        if self.view.touch is None:
            self._previous = None
        if self._lives > 1:
            self._message = GLabel(text=str(self._lives)+
                                   " LIVES LEFT, PRESS TO PLAY",
                                   font_size = 30, valign = "middle",
                                   halign = "center",
                                   center_x = GAME_WIDTH/2,
                                   y = GAME_HEIGHT/2)
        else:
            self._message = GLabel(text="1 LIFE LEFT, PRESS TO PLAY",
                                   font_size = 30, valign = "middle",
                                   halign = "center",
                                   center_x = GAME_WIDTH/2,
                                   y = GAME_HEIGHT/2)
        if self.view.touch is not None and self._previous is None:
            self._state = STATE_COUNTDOWN
            self._model.balls = [Ball()]
    
    def tryagain(self):
        """Allows the user to restart the game.
        
        When a user presses the mouse, it reinitializes Class Model,
        thereby restarting the game. Also sets the state to STATE_COUNTDOWN.
        Sets score to 0 and lives back to full lives
        """
        if self.view.touch is None:
            self._previous = None
        if self.view.touch is not None and self._previous is None:
            self._state = STATE_COUNTDOWN
            self._model = Model()
            self.score = 0
            self._lives = NUMBER_TURNS
            self._header.text = "Score: "+str(self.score)+\
            "    Lives left: "+str(self._lives)
    
    def addball(self):
        """Adds ball to game when 10 bricks are destroyed."""
        if self.score % 10 == 0 and self._model.numballs < self.score/10 +1:
            self._model.balls.append(Ball())
            self._model.numballs += 1
    
    def complete(self):
        """Displays win or lose message, depending on game outcome.
        
        If all the bricks are destroyed, displays a win message.
        Otherwise, displays a lose message."""
        if len(self._model.bricks) == 0:
            self._message = GLabel(text="You won! Press to play again!",
                                       font_size = 30,
                                       valign = "middle", halign = "center",
                                       center_x = GAME_WIDTH/2,
                                       y = GAME_HEIGHT/2)
        else:
            self._message = GLabel(text="You lost ): Press to play again!",
                                       font_size = 30,
                                       valign = "middle", halign = "center",
                                       center_x = GAME_WIDTH/2,
                                       y = GAME_HEIGHT/2)