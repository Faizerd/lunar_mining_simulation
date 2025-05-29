# Lunar Mining Simulation

A simulation of lunar mining operations with configurable numbers of mining trucks and unloading stations.

## Description

The simulation models a lunar mining operation where trucks load Helium-3 at mining sites, transport it to unloading stations, wait in queue if necessary, unload their cargo, and then return to mining sites to repeat the cycle. 

- The simulation runs for a 72-hour period
- Mining trucks take 1-5 hours to load resources at mining sites
- Travel time between mining sites and stations is 30 minutes each way
- Unloading takes 5 minutes per truck when a truck reaches the front of the queue
- Trucks automatically join the shortest available queue when they arrive at the station area

The simulation collects statistics on truck deliveries, time spent in queues, and station utilization.

## Usage

The simulation can be run from the command line with the following arguments:

```
python simulation/run.py <num_trucks> <num_stations>
```

Where:
- `<num_trucks>` is the number of mining trucks to simulate (must be greater than 0)
- `<num_stations>` is the number of unloading stations to simulate (must be greater than 0)

### Example and Output

To run a simulation with 15 trucks and 2 unloading stations:

```
python simulation/run.py 15 2
```

The simulation will output statistics for each truck and station, including:
- Number of loads delivered by each truck
- Time spent in queue by each truck
- Number of loads received by each station
- Average queue length at each station

```
Running Simulation with 15 trucks and 2 stations
Truck 0: 17 loads delivered, 0 minutes spent queued for an unload station
Truck 1: 16 loads delivered, 3 minutes spent queued for an unload station
Truck 2: 16 loads delivered, 0 minutes spent queued for an unload station
Truck 3: 17 loads delivered, 4 minutes spent queued for an unload station
Truck 4: 17 loads delivered, 3 minutes spent queued for an unload station
Truck 5: 18 loads delivered, 1 minutes spent queued for an unload station
Truck 6: 17 loads delivered, 1 minutes spent queued for an unload station
Truck 7: 18 loads delivered, 4 minutes spent queued for an unload station
Truck 8: 19 loads delivered, 2 minutes spent queued for an unload station
Truck 9: 19 loads delivered, 2 minutes spent queued for an unload station
Truck 10: 16 loads delivered, 0 minutes spent queued for an unload station
Truck 11: 15 loads delivered, 0 minutes spent queued for an unload station
Truck 12: 17 loads delivered, 1 minutes spent queued for an unload station
Truck 13: 17 loads delivered, 6 minutes spent queued for an unload station
Truck 14: 19 loads delivered, 0 minutes spent queued for an unload station
Station 0: 198 loads recieved, average queue length 0.28
Station 1: 60 loads recieved, average queue length 0.08
```

## Project Structure

```
lunar_mining_simulation/
├── simulation/              # Main simulation package
│   ├── __init__.py
│   ├── run.py               # Main simulation runner
│   ├── station.py           # Unloading station implementation
│   └── truck.py             # Mining truck implementation
├── tests/                   # Test directory
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

### Core Components

- `MiningTruck`: Represents a mining truck that cycles through different states (loading, traveling, queued, unloading)
- `MiningUnloadStation`: Represents a station where trucks unload resources
- `LunarMiningSimulation`: Main simulation class that coordinates trucks and stations

## Dependencies

- Python 3.7+
- pytest (for running tests)

## Followup
If the cost of operating a station and truck was known, and the profit per load of helium was known, this could be used to run many simulations and determine the optimal number of stations and trucks to maximize profits.