def to_human_state_name(state):
    """Simple conversion of MPD state labels to nicer ones."""
    return {'play': 'playing', 'pause': 'paused', 'stop': 'stopped'}[state]
