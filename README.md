# python-tetris
Tetris game using Pygame, taken from tutorial: https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/. 

You can download Pygame using pip or the requirements.txt file: pip install -r requirements.txt  

The game plays within a game loop.  
The logic of game loop is:  

  Create grid  
  
  Move piece down the grid until either:  
    - piece moves into grid square that is already taken   
    - the piece hits the bottom of the grid.   
  
  When the piece is done moving down.   
    - Note down piece’s occupied squares.   
    - Get a new piece.     
    - Get a new ‘next piece’.   
    - Clear rows.   
    - Update score.   
    - Display new ‘next piece’.   
    - Update the screen.   
  
  Check if game is over.  
    - If yes: Update screen with game over message, End game loop, Update score.     
    - If no: Go back to beginning of game loop. 
