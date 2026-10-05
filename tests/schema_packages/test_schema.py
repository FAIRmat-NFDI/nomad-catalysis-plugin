import os.path

import pytest
from nomad.client import normalize_all, parse
from nomad.datamodel.context import ClientContext


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


def test_read_upload_from_root_and_subfolder(caplog):
    upload_dir = os.path.join('tests', 'data')
    mainfile = os.path.join('subfolder', 'test_reaction_clean_data.archive.yaml')

    def normalize_with_data_file(data_file):
        caplog.clear()
        entry_archive = parse(os.path.join(upload_dir, mainfile))[0]
        entry_archive.m_context = ClientContext(local_dir=upload_dir)
        entry_archive.metadata.mainfile = mainfile
        entry_archive.data.data_file = data_file
        normalize_all(entry_archive)
        return entry_archive

    # data file only next to the mainfile
    entry_archive = normalize_with_data_file('MoO3_C2_performance_kelvin.xlsx')
    assert entry_archive.data.data_file == 'subfolder/MoO3_C2_performance_kelvin.xlsx'
    assert entry_archive.data.results

    # data file only relative to the upload root
    entry_archive = normalize_with_data_file(
        'subfolder/MoO3_C2_performance_kelvin.xlsx'
    )
    assert entry_archive.data.data_file == 'subfolder/MoO3_C2_performance_kelvin.xlsx'
    assert entry_archive.data.results

    # data file both in the upload root and next to the mainfile
    entry_archive = normalize_with_data_file('MoO3_C2_performance_kelvin_also_outside.xlsx')
    assert entry_archive.data.data_file == 'MoO3_C2_performance_kelvin_also_outside.xlsx'
    assert 'found both in the upload root and next to the mainfile' in caplog.text

    # data file neither in the upload root nor next to the mainfile
    entry_archive = normalize_with_data_file('missing.xlsx')
    assert 'FileNotFoundError' in caplog.text
