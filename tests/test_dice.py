from risk.dice import roll_dice

def test_roll_dice():
    for i in range(10):
        results = roll_dice(i)
        assert len(results) == i
        assert all([r > 0 and r < 7 for r in results])
