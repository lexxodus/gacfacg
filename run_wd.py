from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummy.simulation import Simulation
# from app import app

PLAYER_AMOUNT = 6

# app.run(debug=True)
s = Simulation()
# s.create_players(6)
s.load_players(PLAYER_AMOUNT)
s.start_level()
s.perform_actions(20 * PLAYER_AMOUNT)
# s.perform_actions(1)
s.end_level()
