import pathlib

import pytest

from codingame.training.medium.advanced_tree import main

cases = dirs = [p for p in pathlib.Path(__file__).parent.iterdir() if p.is_dir() and p.name.startswith("0")]


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
        expected_output = output_file.read()
        while expected_output[-1] == "\n":
            expected_output = expected_output[:-1]

    res = main(s, f, n, lines)
    failed_res_path = expected_path.parent / "failed_res"
    if expected_output != res:
        with failed_res_path.open("w") as failed_res_file:
            failed_res_file.write(res)
    elif failed_res_path.exists():
        failed_res_path.unlink()

    assert res == expected_output
