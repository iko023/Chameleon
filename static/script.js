async function sendNameToServer(name) {
    await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
}

// On page load: if no name stored, show overlay
window.addEventListener('DOMContentLoaded', () => {
    const stored = sessionStorage.getItem('playerName');
    if (stored) {
        sendNameToServer(stored).then(() => {
        document.getElementById('register-overlay').style.display = 'none';
        poll(); // start status/game polling
        });
    }
});

// Register button handler
document.getElementById('register-btn').addEventListener('click', async () => {
    const input = document.getElementById('name-input');
    const name  = input.value.trim() || 'Guest';
    sessionStorage.setItem('playerName', name);
    await sendNameToServer(name);
    document.getElementById('register-overlay').style.display = 'none';
    poll();  // begin polling now that name is set
});

// Poll for status every second
async function poll() {
    // Fetch status
    const stat = await fetch('/status').then(res => res.json());

    // Update only the viewer count
    document.getElementById('count').innerText = stat.count;

    // Fetch game state (unchanged)
    const gs = await fetch('/game_state').then(r => r.json());
    const display = document.getElementById('word-display');

    if (!gs.started) {
        display.innerText = 'Press "New Game" to start!';
    } else if (gs.you_mole) {
        display.innerText = 'You are the Mole!';
    } else {
        display.innerText = gs.word;
    }
}

// Refresh every second
setInterval(poll, 1000);
poll();

// New Game button
document.getElementById('newgame-btn').onclick = async () => {
    // First clear out any running game
    await fetch('/reset', { method: 'POST' });

    // Then immediately start a fresh one
    await fetch('/start', { method: 'POST' });

    // Re-poll instantly so UI jumps right in
    poll();
};

