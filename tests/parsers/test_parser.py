import os.path

from nomad.client import normalize_all, parse


def test_parser():
    test_file = os.path.join('tests', 'data', 'template_CatalystSampleCollection.xlsx')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert (
        entry_archive.metadata.entry_name
        == 'template_CatalystSampleCollection data file'
    )
    number_of_samples = 2
    assert len(entry_archive.data.samples) == number_of_samples

    test_file = os.path.join('tests', 'data', 'template_CatalyticReaction.xlsx')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.metadata.entry_name == 'template_CatalyticReaction data file'
    assert entry_archive.metadata.entry_type == 'RawFileData'
