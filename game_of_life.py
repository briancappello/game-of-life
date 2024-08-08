from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    DEAD = "DEAD"
    ALIVE = "ALIVE"


@dataclass
class Cell:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


def get_next_cell_state(cell_state: CellState, num_live_neighbors: int) -> CellState:
    """Given the number of live neighbors of a cell, determine its next state (alive or dead)"""
    if cell_state == CellState.ALIVE and num_live_neighbors in {2, 3}:
        return CellState.ALIVE
    elif cell_state == CellState.DEAD and num_live_neighbors == 3:
        return CellState.ALIVE
    return CellState.DEAD


def get_signals_for_live_cell(cell: Cell) -> set[Cell]:
    """Given a live cell, return all of its neighboring cells."""
    x = cell.x
    y = cell.y
    return {
        Cell(x - 1, y - 1), Cell(x, y - 1), Cell(x + 1, y - 1),
        Cell(x - 1, y),                     Cell(x + 1, y),
        Cell(x - 1, y + 1), Cell(x, y + 1), Cell(x + 1, y + 1),
    }


def get_count_of_signals_for_next_universe(universe_of_live_cells: set[Cell]) -> dict[Cell, int]:
    """Given the current universe of live cells, returns the count of neighboring cell signals."""
    count_of_signals: dict[Cell, int] = defaultdict(int)
    for live_cell in universe_of_live_cells:
        for signal_cell in get_signals_for_live_cell(live_cell):
            count_of_signals[signal_cell] += 1
    return dict(count_of_signals)


def get_next_universe_of_live_cells(universe_of_live_cells: set[Cell]) -> set[Cell]:
    """Given the current universe of live cells, returns the next universe of live cells."""
    return {
        Cell(signal_cell.x, signal_cell.y)
        for signal_cell, num_live_signals
        in get_count_of_signals_for_next_universe(universe_of_live_cells).items()
        if get_next_cell_state(
            cell_state=(
               CellState.ALIVE
               if signal_cell in universe_of_live_cells
               else CellState.DEAD
            ),
            num_live_neighbors=num_live_signals,
        ) == CellState.ALIVE
    }
