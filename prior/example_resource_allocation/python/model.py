# Import from Google OR Tools
from __future__ import print_function
from ortools.linear_solver import pywraplp


class Model():
    # **************************************************************
    # CONSTRUCTOR: Instantiate model and set constraints based on instance
    # ***************************************************************
    def __init__(self, shipments, num_days, worker_capacity, worker_cost):
        # Create the mip solver with the CBC backend.
        self.solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        time_limit_minutes = 1
        self.solver.SetTimeLimit(time_limit_minutes * 60 * 1000)  # Milliseconds

        nVariables = {}
        # *******************************************************************
        # VARIABLES: create a variable for each (shipment, day) pair
        # ***************************************************************
        for shipment in shipments.values():
            for d in range(0, shipment.latest_possible_processing_day):
                var_name = 'p_' + shipment.shipment_id + '_' + str(d)
                p = self.solver.IntVar(0.0, 1.0, var_name)  # integer variable with min value of 0 and max of 1
                shipment.pVariables[d] = p

        for d in range(0, num_days):
            var_name = 'n_' + str(d)
            n = self.solver.IntVar(0.0, 1.0, var_name)  # integer variable with min value of 0 and max of 1
            nVariables[d] = n


        # *******************************************************************
        # OBJECTIVE FUNCTION: Minimize the expected cost
        # ***************************************************************
        objective = self.solver.Objective()
        objective.SetMinimization()

        for shipment in shipments.values():
            for d in range(0, shipment.latest_possible_processing_day):
                objective_coefficient = float(shipment.cost_vector[d])
                objective.SetCoefficient(shipment.pVariables[d], objective_coefficient)


        for d in range(0, num_days):
            objective.SetCoefficient(nVariables[d], worker_cost)

        # *******************************************************************
        # CONSTRAINT: Each shipment must be processed on one of the days
        # ***************************************************************
        for shipment in shipments.values():
            constraint = self.solver.Constraint(1, 1)  # Equality constraint with right-hand-side value of 1
            for d in range(0, shipment.latest_possible_processing_day):
                constraint.SetCoefficient(shipment.pVariables[d], 1)

        # *******************************************************************
        # CONSTRAINT: At most C_d shipments can be processed on day d
        # ***************************************************************
        for d in range(0, num_days):
            constraint = self.solver.Constraint(-self.solver.infinity(), 0)
            constraint.SetCoefficient(nVariables[d], -worker_capacity)
            for shipment in shipments.values():
                if d < shipment.latest_possible_processing_day:
                    constraint.SetCoefficient(shipment.pVariables[d], 1)
