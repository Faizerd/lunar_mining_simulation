from enum import Enum
import random


class TruckState(Enum):
    LOADING = 0
    SITE_TO_STATION = 1
    QUEUED = 2
    UNLOADING = 3
    STATION_TO_SITE = 4

    def __str__(self) -> str:
        return self.name

class MiningTruck:
    def __init__(self, id: int):
        """
        Initialize an instance of a Mining Truck.

        Starts the truck empty at a mining site.

        Args:
            id (int): ID of the truck.
        """
        self.truck_id = id
        self.state = TruckState.LOADING
        self.minutes_elapsed_in_state = 0
        self.minutes_required_in_state = self.get_load_time()
        self.station_id = None
        self.num_batches_delivered = 0
        self.total_queued_time = 0

    def __str__(self) -> str:
        return f"Truck {self.truck_id}: {self.state} {self.minutes_elapsed_in_state}/{self.minutes_required_in_state}"

    @staticmethod
    def get_load_time():
        """
        Randomly generate a time it takes to load a mining truck.

        Returns a duration in minutes between 1 hour and 5 hours.

        Returns:
            duration in minutes between 1 hour and 5 hours.
        """
        return random.randint(1 * 60, 5 * 60)

    def is_unloading(self):
        """
        Check if this truck is unloading

        Returns:
            True if truck is unloading, False otherwise
        """
        return self.state == TruckState.UNLOADING
    
    def start_unload(self):
        """
        Set this trucks state to unloading

        """
        self.state = TruckState.UNLOADING

    def needs_unload_station(self):
        """
        Check if this truck needs to be assigned an unload station

        """
        return self.state == TruckState.QUEUED and self.station_id is None

    def tick(self):
        """
        Process 1 unit of time for this truck.

        Check if enough time has passed in the current state that the truck should transition to a new state.
        The state machine is a linear cycle: The truck loads helium, drives to a station, queues up to unload helium, 
        eventually reaching the front of the line and unloading, then drives to a new mining site and the cycle repeats.
        """
        if self.state == TruckState.QUEUED:
            # If the truck is queued up at a station, it does not start unloading until the station changes its state to UNLOADING
            self.total_queued_time += 1
            return
        
        self.minutes_elapsed_in_state += 1
        if self.minutes_elapsed_in_state == self.minutes_required_in_state:
            if self.state == TruckState.LOADING:
                # The truck is done loading, drive to the unloading station takes 30 minutes
                self.state = TruckState.SITE_TO_STATION
                self.minutes_elapsed_in_state = 0
                self.minutes_required_in_state = 30
            elif self.state == TruckState.SITE_TO_STATION:
                # The truck has reached a station, unloading takes 5 minutes
                self.state = TruckState.QUEUED
                self.minutes_elapsed_in_state = 0
                self.minutes_required_in_state = 5
            elif self.state == TruckState.UNLOADING:
                # The truck is done unloading, drive to the mining site takes 30 minutes
                self.state = TruckState.STATION_TO_SITE
                self.minutes_elapsed_in_state = 0
                self.minutes_required_in_state = 30
                self.station_id = None
                self.num_batches_delivered += 1
            elif self.state == TruckState.STATION_TO_SITE:
                # The truck has reached a site, loading takes between 1 and 5 hours
                self.state = TruckState.LOADING
                self.minutes_elapsed_in_state = 0
                self.minutes_required_in_state = self.get_load_time()
            else: # self.state == TruckState.QUEUED
                raise SystemError("Mining Truck somehow unloaded while still in line for an unloading station")
        

