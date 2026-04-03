*This project has been created as part of the 42 curriculum by gtourdia*

# Description
42_fly_in is a project of the 42 curriculum that aims to monitor a fleet of drones from a START zone to an END zone, with optimized path-finding.

## Configuration File Format

Configuration files define the drone network topology, zones, and connections. The format is intuitive and supports comments, metadata, and zone/connection constraints.

### Zone Definitions

Each zone line follows the format: `<type>: <name> <x> <y> [metadata]`

- **`start_hub`**: The starting zone where all drones begin. Multiple drones can occupy this zone initially. Only one per topology.
- **`end_hub`**: The destination zone where drones are delivered. Multiple drones can arrive here. Only one per topology.
- **`hub`**: A regular intermediate zone for routing.

### Zone Metadata

All metadata is optional and enclosed in brackets `[...]`. Metadata tags can appear in any order.

#### Zone Type (`zone=<type>`)
Controls the movement cost to enter a zone:
- **`normal`** (default): 1 turn to enter
- **`priority`**: 1 turn to enter, but should be prioritized in pathfinding algorithms
- **`restricted`**: 2 turns to enter (multi-turn movement; drone must reach destination on next turn)
- **`blocked`**: Inaccessible; drones cannot enter or pass through

#### Capacity (`max_drones=<number>`)
- Default: `1` (only one drone per turn)
- Example: `max_drones=3` allows up to 3 drones in the zone simultaneously
- Exceptions: Start and end zones can hold unlimited drones

#### Color (`color=<value>`)
- Optional visual attribute for terminal output or graphical representation
- Any single-word string is valid (e.g., `red`, `blue`, `orange`, `custom_color`)
- Default: no color

### Connection Definitions

Connect zones using: `connection: <zone1>-<zone2> [metadata]`

- Defines a **bidirectional** edge between two zones
- Zone names **cannot contain dashes** (enforced by syntax)
- Connections must link previously defined zones

#### Connection Metadata

#### Link Capacity (`max_link_capacity=<number>`)
- Default: `1` (one drone per turn can traverse)
- Example: `max_link_capacity=2` allows 2 drones to traverse simultaneously
- Applies to the entire traversal (both directions)

### Complete Example

```
# Example: Complex network with capacity and zone type constraints
nb_drones: 6

start_hub: start 0 0 [color=green]
hub: hub1 1 1 [color=yellow max_drones=2]
hub: hub2 2 2 [color=blue]
hub: restricted 3 3 [zone=restricted color=orange]
hub: priority 2 4 [zone=priority color=cyan]
hub: blocked_area 4 4 [zone=blocked color=gray]
end_hub: exit 5 5 [color=red max_drones=3]

connection: start-hub1
connection: start-hub2
connection: hub1-hub2 [max_link_capacity=2]
connection: hub1-priority
connection: hub2-restricted
connection: priority-exit
connection: restricted-exit
```

### Parsing Rules

- **Comments**: Lines starting with `#` are ignored
- **Whitespace**: Extra spaces are tolerated; line structure is strict
- **Zone names**: Any valid characters except dashes and spaces
- **Coordinates**: Positive integers required
- **Duplicates**: The same connection cannot appear more than once (a-b and b-a are duplicates)
- **Validation**: Invalid zone types, negative capacities, or undefined zones cause parsing errors with clear error messages

## Instructions

### Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository_url>
   cd 42_fly_in
   ```

2. **Setup environment with uv**:
   ```bash
   uv install
   ```

### Running the Simulation

1. **Basic execution**:
   ```bash
   make run # Run with default map
   make runargs ARGS='<path_to_config_file>' # Run with custom config file
   ```
   This runs the simulation with the default configuration map.

2. **Run with a specific map without make**:
   ```bash
   uv run main.py -i '/home/gtourdia/Documents/42_fly_in/maps/hard/03_ultimate_challenge.txt'
   ```

3. **Debug mode**:
   ```bash
   make debug
   ```
   Launches the Python debugger for step-by-step execution.

### Code Quality

1. **Run linting checks**:
   ```bash
   make lint
   ```
   Executes `flake8` for style checking and `mypy` for type checking.

2. **Run strict linting** (optional):
   ```bash
   make lint-strict
   ```
   Applies enhanced type checking with mypy's strict mode.

3. **Clean up temporary files**:
   ```bash
   make clean
   ```
   Removes useless files.

1. **Easter egg**:
   ```bash
   make lindt
   ```

## Algorithm & Implementation Strategy

### Overview

The project implements a multi-drone pathfinding and scheduling system using a custom graph-based simulation engine. The core algorithm balances optimal path calculation with real-time constraint satisfaction and dynamic scheduling.

### Key Design Decisions

1. **Object-Oriented Architecture**: 
   - Fully OOP design with dedicated classes for `Zone`, `Drone`, `Connection`, and `State`
   - Clean separation of concerns: parsing, graph modeling, pathfinding, and simulation
   - Extensible design allows for algorithm swaps and enhancements

2. **Pathfinding Strategy**:
   - Uses a modified Dijkstra/A* approach with cost heuristics based on zone types
   - Considers movement costs: normal (1 turn), priority (1 turn), restricted (2 turns)
   - Avoids blocked zones entirely during path computation

3. **Constraint Handling**:
   - Zone occupancy is tracked per turn with capacity enforcement
   - Connection capacity limits prevent congestion on edges
   - Simultaneous movement resolution: drones leaving a zone free capacity before entry conflicts are checked

4. **Optimization Techniques**:
   - Path caching to avoid redundant calculations
   - Greedy scheduling: drones are prioritized based on proximity to goal and remaining path
   - Deadlock detection and avoidance through strategic waiting

5. **Turn Mechanics**:
   - Discrete turn simulation with per-turn movement evaluation
   - Multi-turn restricted zone handling: drone reserves connection traversal
   - Valid movement is determined by turn-by-turn capacity availability

## Visual Representation

The simulation provides real-time feedback through colored terminal output:

![Video](https://github.com/sousampere/42_fly_in/blob/main/assets/visualizer.gif?raw=true)

### Output Format

Each simulation turn is displayed as a line of drone movements in the console:
```
D1-zone_name D2-connection_name D3-goal
```

Where:
- `D<ID>`: Drone identifier (D1, D2, etc.)
- `<zone_name>` or `<connection_name>`: Destination zone/connection

Drones that remain stationary are omitted from the output for clarity.

## Performances targets

The implementation achieves the following reference performance benchmarks:

- **Easy maps**: < 10 turns
- **Medium maps**: 10–30 turns
- **Hard maps**: < 60 turns
- **Challenger map** (optional): Targeting < 41 turns for excellent implementations

## Resources

### Documentation & References
- https://www.youtube.com/watch?v=_lHSawdgXpI for algorithm understanding

### AI Usage

AI tools (GitHub Copilot) were utilized for:

- **Algorithm rewriting**: Rewriting the logic of my first attempt at creating a path finding, which was functionnal but performances consuming
- **Readme**: Creating the base of my readme file

## Technical Choices

### Visualization library

I used pygame as a visualization library. It's not a graph library but it's an eazy to implement library that is not impacting negatively the user experience.

### Algorithm choice

I chose the djikstra algorithm after hearing people talk about it in the 42 Mulhouse campus.
It's made for graphs like this.

## Authors

- [@sousampere](https://github.com/sousampere)


## 🚀 About Me
I am a student at the 42 Mulhouse school. Most of my public projects will be from this school, while I will keep private most of my other projects.
## Contact me !

 - [LinkedIn](https://fr.linkedin.com/in/gaspardtourdiat)
 - [My website](https://gaspardtourdiat.fr/)
 - [For 42 students (my intra profile)](https://profile.intra.42.fr/users/gtourdia)


![Logo](https://github.com/sousampere/sousampere/blob/main/42mulhouse.png?raw=true)
