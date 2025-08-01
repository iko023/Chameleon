from flask import Flask, render_template, request, session, jsonify
import random, uuid, time
from words import word_list

app = Flask(__name__)
app.secret_key = 'ogisuhvm32989wifkasnmqi0ewnwfe'

#################################################
# VARIABLES
#################################################

players = {}
bag = []
game = {
  'started' : False,
  'word' : None,
  'mole' : None,
  'words' : bag
}

#################################################
# FUNCTIONS
#################################################


def init_bag():
  """ Initiate bag of words. """
  global bag
  bag = list(set(word_list.copy()))
  random.shuffle(bag)


def draw_word():
  """ Draw and remove word from bag. """
  global bag
  if not bag:
    init_bag()
  return bag.pop()


def register_player():
  """ Registers new ip adresses as players. """
  sid = session.get('sid') or str(uuid.uuid4())
  session['sid'] = sid
  name = session.get('name', 'Guest')
  players[sid] = {
    'name': name,
    'last_seen': time.time()
  }


@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  name = data.get('name', '').strip() or 'Guest'
  session['name'] = name
  return jsonify(status='ok'), 200


@app.route('/status')
def status():
  """ Registers player and removes inactive players after 5 sec. Returns player count. """
  register_player()
  cutoff = time.time() - 5                  
  for sid, info in list(players.items()):
    if info['last_seen'] < cutoff:
      players.pop(sid)                   
  return jsonify(
    count=len(players),
    players=[info['name'] for info in players.values()]
  )


@app.route('/start', methods=['POST'])
def start_game():
  """ Assigns the mole, draws word and starts game. """
  if not game['started'] and players:
    sids = list(players.keys())
    game['mole'] = random.choice(sids)
    game['word'] = draw_word()
    game['started'] = True
  return jsonify({'status': 'ok'})


@app.route('/game_state')
def game_state():
  """ Retreaves game state and registes player. """
  register_player()
  sid = session.get('sid')
  payload = {
    'started': game['started'],
    'word': game['word'] if sid != game['mole'] else None,
    'you_mole': sid == game['mole']
  }
  return jsonify(payload)


@app.route('/reset', methods=['POST'])
def reset_game():
  """ Restarts game and clears game state. """
  game.update({'started': False, 'word': None, 'mole': None})
  return jsonify({'status': 'reset'})


@app.route('/')
def index():
  """ Renders html. """
  return render_template('index.html', players=players)




if __name__ == '__main__':
  init_bag()                # Initiates bag of words
  app.run(debug=True)       # Runs app