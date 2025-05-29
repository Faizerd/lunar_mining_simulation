import pytest
from simulation.run import LunarMiningSimulation
from simulation.truck import MiningTruck, TruckState


class TestLunarMiningSimulation:
    def test_initialization(self):
        """
        Test initializing an instance of LunarMiningSimulation
        """
        sim = LunarMiningSimulation(3, 2)
        assert sim.num_trucks == 3
        assert sim.num_stations == 2
        assert len(sim.trucks) == 3
        assert len(sim.stations) == 2
        assert sim.simulation_minutes == 72 * 60  # 72 hours in minutes
        
        # Verify truck IDs are assigned correctly
        for i, truck in enumerate(sim.trucks):
            assert truck.truck_id == i
            
        # Verify station IDs are assigned correctly
        for i, station in enumerate(sim.stations):
            assert station.station_id == i
            
        # Test with different numbers
        sim2 = LunarMiningSimulation(5, 3)
        assert sim2.num_trucks == 5
        assert sim2.num_stations == 3
        assert len(sim2.trucks) == 5
        assert len(sim2.stations) == 3

    def test_initialization_invalid_args(self):
        """
        Test the constructor with invalid inputs
        """
        # Test with invalid truck count
        with pytest.raises(ValueError, match="Invalid value passed for number of trucks to simulation. Value must be > 0"):
            LunarMiningSimulation(0, 2)
            
        with pytest.raises(ValueError, match="Invalid value passed for number of trucks to simulation. Value must be > 0"):
            LunarMiningSimulation(-1, 2)
            
        # Test with invalid station count
        with pytest.raises(ValueError, match="Invalid value passed for number of stations to simulation. Value must be > 0"):
            LunarMiningSimulation(2, 0)
            
        with pytest.raises(ValueError, match="Invalid value passed for number of stations to simulation. Value must be > 0"):
            LunarMiningSimulation(2, -1)

    def test_get_station_id_shortest_queue(self):
        """
        Test finding the station with the shortest queue
        """
        sim = LunarMiningSimulation(2, 3)
        
        # Initially all queues are empty, so first station should be returned
        station = sim.get_station_id_shortest_queue()
        assert station.station_id == 0
        
        # Add trucks to station queues
        sim.stations[0].truck_queue.append(0)  # Add one truck to station 0
        sim.stations[1].truck_queue.append(1)  # Add one truck to station 1
        sim.stations[1].truck_queue.append(0)  # Add another truck to station 1
        
        # Station 2 should now have the shortest queue (empty)
        station = sim.get_station_id_shortest_queue()
        assert station.station_id == 2
        
        # Add trucks to all stations
        sim.stations[2].truck_queue.append(0)  # Add one truck to station 2
        
        # Station 0 and 2 now have 1 truck each, station 1 has 2 trucks
        # Station 0 should be returned as it's checked first when equal length
        station = sim.get_station_id_shortest_queue()
        assert station.station_id == 0

    def test_assign_truck_to_station(self):
        """
        Test assigning a truck to a station
        """
        sim = LunarMiningSimulation(2, 2)
        truck = sim.trucks[0]
        
        # Set truck state to QUEUED (ready to be assigned)
        truck.state = TruckState.QUEUED
        
        # Assign truck to a station
        sim.assign_truck_to_station(truck)
        
        # Verify truck is assigned to a station (should be station 0 since all queues are empty)
        assert truck.station_id == 0
        assert 0 in sim.stations[0].truck_queue  # Truck ID should be in station's queue
        assert truck.state == TruckState.UNLOADING  # First truck in queue starts unloading
        
        # Test with a second truck
        truck2 = sim.trucks[1]
        truck2.state = TruckState.QUEUED
        
        # Assign second truck to a station
        sim.assign_truck_to_station(truck2)
        
        # Second truck should go to station 1 as it now has shorter queue
        assert truck2.station_id == 1
        assert 1 in sim.stations[1].truck_queue
        assert truck2.state == TruckState.UNLOADING  # First truck in queue starts unloading
        
        # Add a third truck
        truck3 = MiningTruck(2)
        truck3.state = TruckState.QUEUED
        sim.trucks.append(truck3)
        
        # Assign third truck
        sim.assign_truck_to_station(truck3)
        assert truck3.station_id == 0
        assert 2 in sim.stations[0].truck_queue
        assert truck3.state == TruckState.QUEUED

    def test_run_simulation(self):
        """
        Test running the simulation for a short duration
        """
        # Create a simulation with a very short duration for testing
        sim = LunarMiningSimulation(2, 1)
        sim.simulation_minutes = 3  # Run for only 3 minutes
        
        # Run the simulation
        sim.run()
        