Description
-----------
This is a simple chess AI made based on minimax decision making. The algorithm is modified by limiting the depth of
search in the minimax tree (based on difficulty level of AI) and by pruning sections of the decision tree when they
are determined to be obsolete.  It also remembers "boards" (game states of positions of pieces) so that it doesn't
have to evaluate the same states repeatedly.  Due to this, the speed of decision making increases as the AI learns
more board states.

Heuristic
---------
This AI evaluates the score of a board based on a few basic criteria, including the number of enemy pieces it is able
to strike, the number of its own pieces that are threatened, and counting the number of its own pieces and the number
of enemy pieces on the board. The pieces are also weighted in terms of importance, which is used when counting and
comparing the number of pieces from each team on the board.  This score is used for the minimax calculations of each
board state.

How to play
-----------
To run this game, you can run the game.py file.  It is preset to have two AI's play against eachother, so you can
watch how the game works and spectate on how they perform.  The AI's settings can be changed to alter the depth in
which it explores the decision tree (the deeper the depth, the theoretically smarter the AI is).

Performance Notes
-----------------
This is a very simple concept for a chess AI, as minimax is not the most effective implementation for this type of
dynamic game, so the moves made are a bit silly looking to anyone who knows how to play chess. Since the AI does not
have any pre-coded preferences for play styles or types of defense/offense structures, it makes its decision purely
based on its heuristic, which results in lots of short sighted decision making.