from FGAme.signals import global_signal

player_death_signal = global_signal('player-death')
player_death_signal.connect(exit)

next_level_signal = global_signal('next-level')

enemy_on_rope_signal = global_signal('enemy-on-rope')