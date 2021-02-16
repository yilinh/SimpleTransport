
from model import BangladeshModel

# ---------------------------------------------------------------
# run time 5 x 24 hours; 1 tick 1 minute
# run_length = 5 * 24 * 60

# run time 100 ticks
run_length = 100

sim_model = BangladeshModel()
for i in range(run_length):
    sim_model.step()
