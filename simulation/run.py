import argparse
from simulation.truck import MiningTruck, TruckState
from simulation.station import MiningUnloadStation

class LunarMiningSimulation:
    def __init__(self, num_trucks: int, num_stations: int):
        """
        Initialize Simulation.

        Args:
            num_trucks (int): Number of MiningTrucks to simulate.
            num_stations (int): Number of MiningUnloadStations to simulate.
        """
        # Validate that the number of trucks and unload stations are valid selections
        if num_trucks <= 0:
            raise ValueError("Invalid value passed for number of trucks to simulation. Value must be > 0")
        if num_stations <= 0:
            raise ValueError("Invalid value passed for number of stations to simulation. Value must be > 0")
        self.num_trucks: int = num_trucks
        self.num_stations: int = num_stations

        # Run the simulation for 72 hours
        self.simulation_minutes = 72 * 60

        self.trucks: list[MiningTruck] = []
        for i in range(self.num_trucks):
            self.trucks.append(MiningTruck(i))

        self.stations: list[MiningUnloadStation] = []
        for i in range(self.num_stations):
            self.stations.append(MiningUnloadStation(i))

    def get_station_shortest_queue(self) -> MiningUnloadStation:
        """
        Find the station with the shortest queue.

        Return:
            Mining Unload Station with the shortest queue
        """
        shortest_queue_station = self.stations[0]
        for station in self.stations:
            if station.get_queue_length() < shortest_queue_station.get_queue_length():
                shortest_queue_station = station
        return shortest_queue_station

    def assign_truck_to_station(self, truck: MiningTruck):
        """
        Assign the given truck to the station with the shortest queue.
        If it is at the front of the newly joined queue, start unloading.

        Args:
            truck: Mining Truck to assign to a station
        """
        station = self.get_station_shortest_queue()
        truck.station_id = station.station_id
        station.truck_queue.append(truck.truck_id)
        # If the truck just joined an empty queue, it should start unloading
        if station.get_queue_length() == 1:
            truck.state = TruckState.UNLOADING


    def run(self):
        """
        Run the simulation for 72 hours, checking truck and station status every minute.
        """
        print(f"Running Simulation with {self.num_trucks} trucks and {self.num_stations} stations")
        for minute in range(self.simulation_minutes):
            for truck in self.trucks:
                # For each truck, check for state changes
                truck.tick()
                # If a truck is ready to unload, assign it to the station with the smallest queue
                if truck.needs_unload_station():
                    self.assign_truck_to_station(truck)
            
            for station in self.stations:
                # For each station, check if the line has moved
                station.process_queue(self.trucks)

    def output_results(self):
        """
        Print statistics for each truck and station
        """
        for truck in self.trucks:
            print(f"Truck {truck.truck_id}: {truck.num_batches_delivered} loads delivered, {truck.total_queued_time} minutes spent queued for an unload station")
        for station in self.stations:
            print(f"Station {station.station_id}: {station.num_trucks_unloaded} loads recieved, average queue length {'%.2f' % station.get_average_queue_length()}")


def main():
    # Parse number of trucks and number of unload stations to simulate from command line arguments
    parser = argparse.ArgumentParser(
        prog='LunarMiningSimulation',
        description='Simulates a lunar mining operation with N trucks and M unload sites'
    )
    parser.add_argument('num_trucks', type=int)
    parser.add_argument('num_stations', type=int)
    args = parser.parse_args()

    simulation = LunarMiningSimulation(args.num_trucks, args.num_stations)
    simulation.run()
    simulation.output_results()

if __name__=="__main__":
    main()