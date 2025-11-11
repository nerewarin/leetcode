import pathlib

import pytest

from codingame.training.medium.advanced_tree import main

cases = dirs = [p for p in pathlib.Path(__file__).parent.iterdir() if p.is_dir() and p.name.startswith("case")]


# Write an answer using print
@pytest.mark.parametrize(
    "input_path,expected_path",
    [
        pytest.param(
            case / "input",
            case / "output",
            id=case.name,
        )
        for case in cases
    ],
)
def test(input_path, expected_path):
    with input_path.open("r") as input_file:
        s, f, n_, *lines = input_file.read().splitlines()
        n = int(n_)

    with expected_path.open("r") as output_file:
        expected_output = output_file.read()[:-1]  # cut \n ending

    res = main(s, f, n, lines)
    assert res == expected_output
