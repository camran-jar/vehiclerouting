# vehiclerouting
Solve vehicle routing problem using heuristics.

Ran with a virtual enviroment
to activate venv

/path/to/directory source /venv/bin/activate

To test on the different VRP files, comment/uncomment in the main.py file

    # Paths to the data and solution files.
    #vrp_file = "n32-k5.vrp"  # "data/n80-k10.vrp"
    #sol_file = "n32-k5.sol"  # "data/n80-k10.sol"

    vrp_file = "n80-k10.vrp"
    sol_file = "n80-k10.sol"

The program will run the Nearest Neighbour Heuristic and the Savings Heuristic on the file
Output the Optimal solution as well as an outpur for Nearest Neighbour and Savings Heuristic
