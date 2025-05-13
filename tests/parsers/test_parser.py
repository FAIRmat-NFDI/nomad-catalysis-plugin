import os.path

import pytest
from nomad.client import normalize_all, parse


def test_parser():
    test_file = os.path.join('tests', 'data', 'template_CatalystSampleCollection.xlsx')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.metadata.entry_name == 'template_CatalystSampleCollection data file'

    assert len(entry_archive.data.samples) == 2
    

    test_file = os.path.join('tests', 'data', 'template_CatalyticReaction.xlsx')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.metadata.entry_name == 'template_CatalyticReaction data file'
    assert entry_archive.metadata.entry_type == 'RawFileData'
