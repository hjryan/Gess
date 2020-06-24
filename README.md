## This is a game of Gess!
It was made for my Introduction to CS II class as a text-based game.  
I just grafted on a GUI, which is my first ever GUI 🤠

![Gess Game](https://j.gifs.com/ROmBlK.gif "Gess")

### Rules:
The goal of the game is to be the last player with a ring of their own stones.  
You play by selecting the center of the 3x3 square you'd like to move, and then selecting your proposed destination center.  
There are a number of reasons why a move may not be valid -- if this is the case, the interface will print the applicable reason at the bottom of the console.

The majority of the game rules are available [here](https://www.chessvariants.com/crossover.dir/gess.html).  

This implementation has a couple of extra rules -- a player cannot:
   - make a move that leaves them without a ring (forfeiture)
   - chose a piece whose center is off the board, in an outermost row or an outermost column
   
### How to run:
The GUI is implemented in Pygame.  
Pygame does not work with Python 3.8 and above  
  - to correct, run with Python 3.7 or lower  
  
Additionally, the version of Pygame that is installed by default does not work with the current Mac OS.  
  - to correct, pip install pygame==2.0.0.dev6
  
If you don't want to do all that, [here's](https://www.youtube.com/watch?v=P5TjF6mPT5I) a video of a full game.  
