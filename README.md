# where to start?

minimize state, eliminate if possible - instead focus on action/behavior

Start with core logic:
* a cell is dead/alive
* determined by num neighbors

```
f(current_state, num_live_neighbors) -> next state
```

# infinite / unbounded universe

* Start with a set of live cells
* Each live cell generates a signal to its neighbors (gives off heat)
* We want to go from a set of live cells to a list of signals
* Count number of signals per cell


universe of live cells -> next universe
