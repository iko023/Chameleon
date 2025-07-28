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
        display.innerText = 'Waiting to start…';
    } else if (gs.you_mole) {
        display.innerText = 'You are the Mole!';
    } else {
        display.innerText = gs.word;
    }
}

// Refress every two seconds
setInterval(poll, 2000);
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