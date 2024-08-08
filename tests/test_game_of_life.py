import pytest

import game_of_life

from game_of_life import Cell, CellState


@pytest.mark.parametrize(
    "cell_state, num_live_neighbors, expected",
    (
        # only 2 or 3 live neighbors stay alive
        (CellState.ALIVE, 0, CellState.DEAD),
        (CellState.ALIVE, 1, CellState.DEAD),
        (CellState.ALIVE, 2, CellState.ALIVE),
        (CellState.ALIVE, 3, CellState.ALIVE),
        (CellState.ALIVE, 4, CellState.DEAD),
        (CellState.ALIVE, 5, CellState.DEAD),
        (CellState.ALIVE, 6, CellState.DEAD),
        (CellState.ALIVE, 7, CellState.DEAD),
        (CellState.ALIVE, 8, CellState.DEAD),  # max 8 neighbors

        # only dead with 3 live neighbors becomes alive
        (CellState.DEAD, 0, CellState.DEAD),
        (CellState.DEAD, 1, CellState.DEAD),
        (CellState.DEAD, 2, CellState.DEAD),
        (CellState.DEAD, 3, CellState.ALIVE),
        (CellState.DEAD, 4, CellState.DEAD),
        (CellState.DEAD, 5, CellState.DEAD),
        (CellState.DEAD, 6, CellState.DEAD),
        (CellState.DEAD, 7, CellState.DEAD),
        (CellState.DEAD, 8, CellState.DEAD),
    ),
)
def test_next_cell_state(cell_state, num_live_neighbors, expected):
    assert game_of_life.get_next_cell_state(cell_state, num_live_neighbors) == expected


@pytest.mark.parametrize(
    "live_cell, expected",
    (
        (
            Cell(2, 3),
            {
                Cell(1, 2), Cell(2, 2), Cell(3, 2),
                Cell(1, 3),             Cell(3, 3),
                Cell(1, 4), Cell(2, 4), Cell(3, 4),
            },
        ),
        (
            Cell(3, 4),
            {
                Cell(2, 3), Cell(3, 3), Cell(4, 3),
                Cell(2, 4),             Cell(4, 4),
                Cell(2, 5), Cell(3, 5), Cell(4, 5),
            },
        ),
    )
)
def test_generate_signals_for_live_cell(live_cell, expected):
    assert game_of_life.get_signals_for_live_cell(live_cell) == expected


@pytest.mark.parametrize(
    "live_cells, expected",
    (
        ([], {}),
        (
            {Cell(2, 3)},
            {
                Cell(1, 2): 1,
                Cell(2, 2): 1,
                Cell(3, 2): 1,
                Cell(1, 3): 1,
                Cell(3, 3): 1,
                Cell(1, 4): 1,
                Cell(2, 4): 1,
                Cell(3, 4): 1,
            },
        ),
        (
            {Cell(2, 3), Cell(3, 4)},
            {
                Cell(1, 2): 1,
                Cell(2, 2): 1,
                Cell(2, 3): 1,
                Cell(3, 2): 1,
                Cell(1, 3): 1,
                Cell(3, 3): 2,
                Cell(1, 4): 1,
                Cell(2, 4): 2,
                Cell(3, 4): 1,
                Cell(4, 3): 1,
                Cell(4, 4): 1,
                Cell(2, 5): 1,
                Cell(3, 5): 1,
                Cell(4, 5): 1,
            },
        ),
    ),
)
def test_count_signals_for_live_cells(live_cells, expected):
    assert game_of_life.get_count_of_signals_for_next_universe(live_cells) == expected


block = {Cell(2, 2), Cell(3, 2), Cell(2, 3), Cell(3, 3)}
horiz = {Cell(2, 3), Cell(3, 3), Cell(4, 3)}
vert = {Cell(3, 2), Cell(3, 3), Cell(3, 4)}


@pytest.mark.parametrize(
    "universe, expected",
    (
        (set(), set()),
        ({Cell(2, 3)}, set()),
        ({Cell(2, 3), Cell(3, 3)}, set()),
        (block, block),
        (horiz, vert),
        (vert, horiz),
    )
)
def test_next_universe(universe, expected):
    assert game_of_life.get_next_universe_of_live_cells(universe) == expected
