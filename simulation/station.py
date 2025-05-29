from simulation.truck import MiningTruck

class MiningUnloadStation:
    def __init__(self, id: int):
        """
        Initialize an instance of a Mining Unload Station.

        Starts the station's truck queue empty

        Args:
            id (int): ID of the station.
        """
        self.station_id = id
        self.truck_queue: list[int] = []
        self.num_trucks_unloaded = 0
        self.queue_length_over_time: list[int] = []

    def __str__(self):
        return f"Station {self.station_id}: {self.truck_queue}"

    def get_queue_length(self):
        """
        Get the current length of the stations truck queue.

        Args:
            length of the truck queue as an integer
        """
        return len(self.truck_queue)
    
    def process_queue(self, trucks: list[MiningTruck]):
        """
        Check the status of the truck queue.

        If the head truck has finished unloading, start unloading the next truck.
        """
        self.queue_length_over_time.append(self.get_queue_length())
        if self.get_queue_length() == 0:
            # Nothing to do for empty truck queue
            return
        if not trucks[self.truck_queue[0]].is_unloading():
            # The head truck has finished unloading, remove it from the queue
            self.truck_queue.pop(0)
            self.num_trucks_unloaded += 1
            if self.get_queue_length() > 0:
                # If there is more trucks in queue, start unloading the next one
                trucks[self.truck_queue[0]].start_unload()

    def get_average_queue_length(self) -> float:
        """
        Get the average length of the truck queue over each minute
        """
        return (sum(self.queue_length_over_time) / len(self.queue_length_over_time))