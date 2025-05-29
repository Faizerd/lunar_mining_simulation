from simulation.truck import MiningTruck, TruckState

class TestTruck:

    def test_initialization(self):
        """
        Test initializing an instance of a Mining Truck.
        """
        test_id = 0
        test_truck = MiningTruck(test_id)
        assert test_truck.truck_id == test_id
        assert test_truck.state == TruckState.LOADING
        assert test_truck.minutes_elapsed_in_state == 0
        assert test_truck.minutes_required_in_state <= 60 * 5
        assert test_truck.minutes_required_in_state >= 60 * 1

    def test_loading(self):
        """
        Test LOADING state of a Mining Truck.
        """
        # Test initial state
        test_id = 0
        test_truck = MiningTruck(test_id)
        assert test_truck.state == TruckState.LOADING

        # Test after 1 tick
        test_truck.tick()
        assert test_truck.state == TruckState.LOADING
        assert test_truck.minutes_elapsed_in_state == 1

        # Test after enough ticks to finish loading
        # Use a fixed length for-loop with a break to avoid infinite loop
        for i in range(5 * 60):
            if test_truck.state != TruckState.LOADING:
                break
            else:
                test_truck.tick()
        assert test_truck.state == TruckState.SITE_TO_STATION
                
    def test_travel_to_station(self):
        """
        Test SITE_TO_STATION state of a Mining Truck.
        """
        # Test initial state
        test_id = 0
        test_truck = MiningTruck(test_id)
        assert test_truck.state == TruckState.LOADING

        # Skip ahead to loading complete
        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()

        assert test_truck.state == TruckState.SITE_TO_STATION
        assert test_truck.minutes_elapsed_in_state == 0
        assert test_truck.minutes_required_in_state == 30

        # Test that travel takes 30 minutes
        for _ in range(30):
            test_truck.tick()
        assert test_truck.state == TruckState.QUEUED

    def test_unload(self):
        """
        Test UNLOADING state of a Mining Truck.
        """
        # Test initial state
        test_id = 0
        test_truck = MiningTruck(test_id)
        assert test_truck.state == TruckState.LOADING

        # Skip ahead to queued
        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()
        assert test_truck.state == TruckState.SITE_TO_STATION

        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()
        assert test_truck.state == TruckState.QUEUED

        # A station would move the truck to UNLOADING
        test_truck.state = TruckState.UNLOADING

        # Test that unloading takes 5 minutes
        for _ in range(5):
            test_truck.tick()
        assert test_truck.state == TruckState.STATION_TO_SITE

    def test_travel_to_site(self):
        """
        Test STATION_TO_SITE state of a Mining Truck.
        """
        # Test initial state
        test_id = 0
        test_truck = MiningTruck(test_id)
        assert test_truck.state == TruckState.LOADING

        # Skip ahead to queued
        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()
        assert test_truck.state == TruckState.SITE_TO_STATION

        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()
        assert test_truck.state == TruckState.QUEUED

        # A station would move the truck to UNLOADING
        test_truck.state = TruckState.UNLOADING

        # Skip ahead to STATION_TO_SITE
        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()
        assert test_truck.state == TruckState.STATION_TO_SITE

        # Test that travel takes 30 minutes
        for _ in range(30):
            test_truck.tick()
        assert test_truck.state == TruckState.LOADING

    def test_long_queue(self):
        """
        Test that a queued truck will stay queued indefinitely
        """
        # Test initial state
        test_id = 0
        test_truck = MiningTruck(test_id)
        assert test_truck.state == TruckState.LOADING

        # Skip ahead to queued
        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()
        assert test_truck.state == TruckState.SITE_TO_STATION

        test_truck.minutes_elapsed_in_state = test_truck.minutes_required_in_state - 1
        test_truck.tick()
        assert test_truck.state == TruckState.QUEUED

        # Test that truck stays in queue for the full 72 hours if no station starts unloading
        for _ in range(72 * 60):
            test_truck.tick()
            assert test_truck.state == TruckState.QUEUED