from __future__ import unicode_literals
__author__ = 'lexxodus'

from dummies.bqq_unbalanced import Simulation
# from app import app

# app.run(debug=True)
s = Simulation()
# s.create_players(6)
s.load_players()
for e in range(90):
    s.run_quiz()
