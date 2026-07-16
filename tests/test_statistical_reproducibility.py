from scripts.reproduce_statistical_analysis import minimum_pairs_for_power, paired_t_power


def test_two_sided_paired_power_requires_34_independent_pairs() -> None:
    pairs, achieved_power = minimum_pairs_for_power(effect_size=0.5, alpha=0.05, target_power=0.80)

    assert pairs == 34
    assert paired_t_power(33, effect_size=0.5, alpha=0.05) < 0.80
    assert achieved_power >= 0.80
