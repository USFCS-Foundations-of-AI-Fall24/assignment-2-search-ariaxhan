from ortools.sat.python import cp_model

def run():
    # Instantiate model and solver
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    # Frequencies: 0: f1, 1: f2, 2: f3
    frequencies = {0: 'f1', 1: 'f2', 2: 'f3'}

    # Define the antennae variables (A1 to A9)
    A1 = model.NewIntVar(0, 2, 'A1')
    A2 = model.NewIntVar(0, 2, 'A2')
    A3 = model.NewIntVar(0, 2, 'A3')
    A4 = model.NewIntVar(0, 2, 'A4')
    A5 = model.NewIntVar(0, 2, 'A5')
    A6 = model.NewIntVar(0, 2, 'A6')
    A7 = model.NewIntVar(0, 2, 'A7')
    A8 = model.NewIntVar(0, 2, 'A8')
    A9 = model.NewIntVar(0, 2, 'A9')

    # Add adjacency constraints (no two adjacent antennas should have the same frequency)
    model.Add(A1 != A2)
    model.Add(A1 != A3)
    model.Add(A1 != A4)
    model.Add(A2 != A1)
    model.Add(A2 != A3)
    model.Add(A2 != A5)
    model.Add(A2 != A6)
    model.Add(A3 != A1)
    model.Add(A3 != A2)
    model.Add(A3 != A6)
    model.Add(A3 != A9)
    model.Add(A4 != A1)
    model.Add(A4 != A5)
    model.Add(A5 != A2)
    model.Add(A5 != A4)
    model.Add(A6 != A2)
    model.Add(A6 != A3)
    model.Add(A6 != A7)
    model.Add(A6 != A8)
    model.Add(A7 != A6)
    model.Add(A7 != A8)
    model.Add(A8 != A7)
    model.Add(A8 != A9)
    model.Add(A9 != A3)
    model.Add(A9 != A8)

    # Solve the model
    status = solver.Solve(model)

    # Output results if solution is found
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Antenna 1: %s" % frequencies[solver.Value(A1)])
        print("Antenna 2: %s" % frequencies[solver.Value(A2)])
        print("Antenna 3: %s" % frequencies[solver.Value(A3)])
        print("Antenna 4: %s" % frequencies[solver.Value(A4)])
        print("Antenna 5: %s" % frequencies[solver.Value(A5)])
        print("Antenna 6: %s" % frequencies[solver.Value(A6)])
        print("Antenna 7: %s" % frequencies[solver.Value(A7)])
        print("Antenna 8: %s" % frequencies[solver.Value(A8)])
        print("Antenna 9: %s" % frequencies[solver.Value(A9)])
    else:
        print("No solution found.")
