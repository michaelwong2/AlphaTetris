# AlphaTetris

This AI will outfitted to compete on a national level in Tetris (single and multiplayer). We will make a custom API for performance on any platform. We demonstrate use of the API with two implementations: a custom made renderer and the online Tetris Battle 2p.

https://www.engadget.com/2015/04/29/tetris-is-a-cruel-mistress/

http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.55.8562&rep=rep1&type=pdf

### TO DO:
* fix rotating on client
* fix drop delay on client for soft dropping
* make tool to read website data
	- must report next pieces
	- must report lines received
* make AIs

### Dependencies:
* python3
* pygame

## Four modes:
1. "Local" Search -- tree based search
2. Evolved -- Genetic algorithm
3. Magic -- LSTM (?) or Deep Neural Net (supervised)

## Optimize for:
* Combos
* T-spins
* Perfect clears
	- http://math.mit.edu/~rstan/papers/tilings.pdf

#### Previous work
Most of these just use local search or genetic algorithms. I think only MisaMino (the best in the world?) can T-Spin and uses a local tree search approach which we will implement as our base ai.
* https://github.com/Hohol/TetrisPlayer
* https://www.reddit.com/r/programming/comments/3djn3c/state_of_the_art_tetris_ai_misamino_source_code/
	- https://github.com/misakamm/MisaMino
	- https://www.youtube.com/watch?v=C1Lm5jltMOQ
* https://medium.com/python-pandemonium/building-a-tetris-bot-part-1-the-stupid-bot-2cbc38d6e32b
* https://www.sciencedirect.com/science/article/pii/S1877050915022942
* https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
* http://cs231n.stanford.edu/reports/2016/pdfs/121_Report.pdf

#### Competitive Platforms
- Tetris Friends
- Puyo Puyo Tetris
- Cultris II
- Tetris Online Poland
