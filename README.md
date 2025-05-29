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

### Example

To run a simulation with 10 trucks and 3 unloading stations:

```
python simulation/run.py 10 3
```

### Output

The simulation will output statistics for each truck and station, including:
- Number of loads delivered by each truck
- Time spent in queue by each truck
- Number of loads received by each station
- Average queue length at each station

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