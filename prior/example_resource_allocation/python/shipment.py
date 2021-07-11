class Shipment():

    def __init__(self, shipment_id, latest_possible_processing_day, cost_vector):
        self.shipment_id = shipment_id
        self.latest_possible_processing_day = latest_possible_processing_day
        self.cost_vector = cost_vector
        self.pVariables = {} # key will be the day

    def toString(self):
        return f"shipment {self.shipment_id}; latest_possible_processing_day = {self.latest_possible_processing_day}; cost_vector = {self.cost_vector}"