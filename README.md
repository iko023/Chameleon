# Chameleon

Welcome to Chameleon: a real-time, browser-based social-deduction game.
One player is the Chameleon and tries to blend in, while everyone else knows the secret word.
Spot the imposter before the chameleon figures out the secret word!

## Features

- Join with a simple URL, no login required
- Live viewer count and "New Game" button
- One-round word assignment with one hidden Chameleon
- Mobile-friendly, responsive layout


## How to run

1. Clone the repository
2. Create and activate a virtual environment
3. Install the requirements with `pip install -r requirements.txt`
4. Run the app with `flask run --host=0.0.0.0`, this will show a message like: `* Running on http://localhost:5000/ (Press CTRL+C to quit)`
5. Open your browser and go to `http://localhost:5000`

## How to play

1. Open your browser. (mobile phone recommended)
2. Share got to the URL `http://localhost:5000`.
3. Wait till the number of players reaches the number of people in the room. (requires at least 3 players)
4. Press "New Game".
5. Players take turns describing the word they see with a single word.
6. The Chameleon tries to blend in without revealing that they are the Chameleon.
7. After each round, players can discuss and vote on who they think the Chameleon is. At least half the players must agree to vote someone out or the game continues.
8. Continue until the Chameleon is identified, the word is guessed, or an innocent player is voted out.
9. Press "New Game" again to start the next game.
