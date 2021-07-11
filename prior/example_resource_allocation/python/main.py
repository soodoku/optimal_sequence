#!/usr/bin/env python3
from shipment import *
from model import *
import numpy as np

if __name__ == "__main__":

    # Create some dummy data
    num_shipments = 10
    num_days = 7
    daily_capacities = np.random.randint(3, 10, num_days)

    shipments = {}

    num_shipments = 100

    for i in range(0, num_shipments):
        latest_day = 7  # np.random.randint(3,7)
        shipment_id = 'dummy_shipment_' + str(i)
        new_shipment = Shipment(shipment_id, latest_day, np.random.rand(latest_day))

        shipments[new_shipment.shipment_id] = new_shipment

        print(new_shipment.toString())

    print(daily_capacities)

    worker_capacity = 80
    worker_cost = 100

    # Formulate model
    model = Model(shipments, num_days, worker_capacity, worker_cost)
    print(model.solver.NumVariables())
    print(model.solver.NumConstraints())

    # Solve Model
    result_status = model.solver.Solve()

    print(f"Model status = {result_status}")

    if result_status != pywraplp.Solver.INFEASIBLE:
        for shipment in shipments.values():
            for d in range(0, shipment.latest_possible_processing_day):
                if shipment.pVariables[d].solution_value() > 0.99: # Precision errors may result in the value being 0.99999999
                    print(f"shipment {shipment.shipment_id} should be processed on day {d}")
    else:
        print("Model is infeasible.  Make sure there's enough capacity for all shipments to be processed")
