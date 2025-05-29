from simulation.truck import MiningTruck, TruckState
from simulation.station import MiningUnloadStation

class TestStation:

    def test_initialization(self):
        """
        Test initializing an instance of a Mining Unload Station
        """
        test_id = 0
        test_station = MiningUnloadStation(test_id)
        assert test_station.station_id == test_id
        assert len(test_station.truck_queue) == 0

    def test_process_queue_empty(self):
        """
        Test processing the truck queue when it is empty
        """
        test_id = 0
        test_station = MiningUnloadStation(test_id)
        test_station.process_queue(trucks=[])
        assert test_station.get_queue_length() == 0

    def test_process_queue_with_1_truck_unloading(self):
        """
        Test processing the truck queue when there is only 1 truck that is not done unloading
        """
        test_id = 0
        test_station = MiningUnloadStation(test_id)
        test_truck = MiningTruck(0)
        test_truck.state = TruckState.UNLOADING
        test_station.truck_queue.append(test_truck.truck_id)

        # There should be 1 truck in the queue before and after processing
        assert test_station.get_queue_length() == 1
        test_station.process_queue(trucks=[test_truck])
        assert test_station.get_queue_length() == 1

    def test_process_queue_with_1_truck_done_unloading(self):
        """
        Test processing the truck queue when there is only 1 truck that is done unloading
        """
        test_id = 0
        test_station = MiningUnloadStation(test_id)
        test_truck = MiningTruck(0)
        test_truck.state = TruckState.STATION_TO_SITE
        test_station.truck_queue.append(test_truck.truck_id)

        # There should be 1 truck in the queue before and 0 after processing
        assert test_station.get_queue_length() == 1
        test_station.process_queue(trucks=[test_truck])
        assert test_station.get_queue_length() == 0

    def test_process_queue_with_2_trucks(self):
        """
        Test processing the truck queue when there are 2 or more trucks and the first finished unloading
        """
        test_id = 0
        test_station = MiningUnloadStation(test_id)
        test_truck_0 = MiningTruck(0)
        test_truck_1 = MiningTruck(1)
        test_truck_0.state = TruckState.UNLOADING
        test_truck_1.state = TruckState.QUEUED
        test_station.truck_queue.append(test_truck_0.truck_id)
        test_station.truck_queue.append(test_truck_1.truck_id)

        # There should be 2 truck in the queue before and after processing
        assert test_station.get_queue_length() == 2
        test_station.process_queue(trucks=[test_truck_0, test_truck_1])
        assert test_station.get_queue_length() == 2

        # Truck 0 finishes unloading
        test_truck_0.state = TruckState.STATION_TO_SITE

        # There should be 2 truck in the queue before and 1 after processing
        assert test_station.get_queue_length() == 2
        test_station.process_queue(trucks=[test_truck_0, test_truck_1])
        assert test_station.get_queue_length() == 1
        assert test_truck_1.is_unloading()