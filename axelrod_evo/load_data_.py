import pathlib
from typing import Dict, List, Text, Tuple

import pkg_resources


def axl_filename(path: pathlib.Path) -> pathlib.Path:
    """Given a path under axelrod_evo/, return absolute filepath.

    Parameters
    ----------
    axl_path
        A pathlib.Path object with the relative directory under axelrod_evo/

    Returns
    -------
        A pathlib.Path object with the absolute directory.
    """
    # We go up a dir because this code is located in axelrod_evo/axelrod_evo.
    axl_path = pathlib.Path(__file__).resolve().parent.parent
    return axl_path / path


def load_file(filename: str, directory: str) -> List[List[str]]:
    """Loads a data file stored in the axelrod_evo library's data subdirectory,
    likely for parameters for a strategy."""
    path = "/".join((directory, filename))
    data_bytes = pkg_resources.resource_string(__name__, path)
    data = data_bytes.decode("UTF-8", "replace")
    rows = []
    for line in data.split("\n"):
        if line.startswith("#") or len(line) == 0:
            continue
        s = line.split(", ")
        rows.append(s)
    return rows


def load_weights(
    filename: str = "ann_weights.csv", directory: str = "data"
) -> Dict[str, Tuple[int, int, List[float]]]:
    """Load Neural Network Weights."""
    rows = load_file(filename, directory)
    d = dict()
    for row in rows:
        name = str(row[0])
        num_features = int(row[1])
        num_hidden = int(row[2])
        weights = list(map(float, row[3:]))
        d[name] = (num_features, num_hidden, weights)
    return d


def load_pso_tables(filename="pso_gambler.csv", directory="data"):
    """Load lookup tables."""
    rows = load_file(filename, directory)
    d = dict()
    for row in rows:
        name, a, b, c, = (
            str(row[0]),
            int(row[1]),
            int(row[2]),
            int(row[3]),
        )
        values = list(map(float, row[4:]))
        d[(name, int(a), int(b), int(c))] = values
    return d
