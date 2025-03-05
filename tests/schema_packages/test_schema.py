import os.path

import pytest
from nomad.client import normalize_all, parse


def test_schema():
    test_file = os.path.join('tests', 'data', 'test_sample.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.name == 'MoO3'
    assert entry_archive.results.material.elements == ['Mo', 'O']
    assert entry_archive.results.properties.catalytic.catalyst.catalyst_name == 'MoO3'
    assert (
        entry_archive.results.properties.catalytic.catalyst.preparation_method
        == 'spray-drying'
    )
    assert entry_archive.results.properties.catalytic.catalyst.catalyst_type == [
        'bulk catalyst',
        'oxide',
    ]
    assert (
        entry_archive.results.properties.catalytic.catalyst.characterization_methods
        == ['BET']
    )
    assert entry_archive.results.properties.catalytic.catalyst.surface_area.to(
        'm^2/g'
    ).magnitude == pytest.approx(3.27)

    test_file = os.path.join('tests', 'data', 'test_reaction.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.name == 'methanol dehydrogenation 30'
    assert entry_archive.data.reaction_conditions.set_temperature.to(
        'K'
    ).magnitude == pytest.approx(473)
