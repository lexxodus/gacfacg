from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummies.wd_unbalanced import Simulation
# from app import app

PLAYER_AMOUNT = 6

# app.run(debug=True)
s = Simulation()
# s.create_players(6)
s.load_players(PLAYER_AMOUNT)
for e in range(100):
    s.start_level()
    s.run_rounds(20)
    # s.perform_actions(1)
    s.end_level()
