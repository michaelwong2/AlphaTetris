# AlphaTetris

This AI will outfitted to compete on a national level in Tetris (single and multiplayer). We will make a custom API for performance on any platform. We demonstrate use of the API with two implementations: a custom made renderer and the online Tetris Battle 2p. 

https://www.engadget.com/2015/04/29/tetris-is-a-cruel-mistress/

http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.55.8562&rep=rep1&type=pdf

### TO DO:
* fix rotating on client app
* make online streamer
* make AIs

### Dependencies:
* python3
* pygame

## Four modes:
1. Passive v1 -- clearing
2. Passive v2 -- set up
3. Active -- switch between two passive modes
4. Evolved -- Genetic algorithm
5. Magic -- LSTM (?) or Deep Neural Net (supervised)

## Optimize for:
* Combos 
* T-spins
* Perfect clears
	- http://math.mit.edu/~rstan/papers/tilings.pdf

#### Reference for hacking into tetris battle online:
https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

#### Previous work
* https://github.com/Hohol/TetrisPlayer
* https://www.reddit.com/r/programming/comments/3djn3c/state_of_the_art_tetris_ai_misamino_source_code/
	- https://github.com/misakamm/MisaMino
	- https://www.youtube.com/watch?v=C1Lm5jltMOQ
* https://medium.com/python-pandemonium/building-a-tetris-bot-part-1-the-stupid-bot-2cbc38d6e32b
* https://www.sciencedirect.com/science/article/pii/S1877050915022942
* https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
