from battle_estimator import probable_outcome
import pytest

# Check values match the Osborne figures
@pytest.mark.parametrize("i,j,k,value", [
    (1, 1, 1, 0.417),
    (1, 1, 0, 0.583),
    (1, 2, 1, 0.255),
    (1, 2, 0, 0.745),
    (2, 1, 1, 0.579),
    (2, 1, 0, 0.421),
    (2, 2, 2, 0.228),
    (2, 2, 1, 0.324),
    (2, 2, 0, 0.448),
    (3, 2, 2, 0.372),
    (3, 2, 1, 0.336),
    (3, 2, 0, 0.293),
])
def test_probable_outcome(i, j, k, value):
    assert round(probable_outcome(i, j, k), 3) == value
