from typing import Dict

import pandas as pd
from nomad.datamodel import EntryArchive
from nomad.datamodel.metainfo.basesections import ElementalComposition
from nomad.parsing import MatchingParser

from nomad_catalysis.parsers.utils import create_archive
from nomad_catalysis.schema_packages.catalysis import (
    CatalystSample,
    CatalyticReaction,
    Preparation,
    SurfaceArea,
)


class CatalysisParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger=None,
        child_archives: Dict[str, EntryArchive] = None,
    ) -> None:
        
        filename = mainfile.split('/')[-1]
        logger.info(f'MyParser called {filename}')
        catalytic_reaction = CatalyticReaction(
            data_file=filename,
        )

        #archive.data = catalytic_reaction
        create_archive(catalytic_reaction, archive, f'{filename}.archive.json')

class CatalystCollectionParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger=None,
        child_archives: Dict[str, EntryArchive] = None,
    ) -> None:
        logger.info('Catalyst Collection Parser called')

        self.creates_children = True

        data_frame =pd.read_excel(mainfile)

        for col in data_frame.columns:
            if col in ['Name', 'name', 'catalyst']:
                data_frame.rename(columns={col: 'name'}, inplace=True)
            if col in ['Storing Institution', 'storing_institution']:
                data_frame.rename(columns={col: 'storing_institution'}, inplace=True)
            if col in ['datetime', 'date']:
                data_frame.rename(columns={col: 'datetime'}, inplace=True)
            if col in ['lab_id', 'sample_id']:
                data_frame.rename(columns={col: 'lab_id'}, inplace=True)
        for n,row in data_frame.iterrows():
            catalyst_sample = CatalystSample(
                name=row['name'],
                storing_institution=row['storing_institution'],
                datetime = row['datetime'],
                lab_id=row['lab_id'],
                form = row['form'],
                catalyst_type=[],
                support = row['support'],
            )
            catalyst_sample.catalyst_type.append(row['catalyst_type'])

            elements = row['Elements'].split(',')
            mass_fractions = row['mass_fractions'].split(',')
            for n, element in enumerate(elements):
                elemental_composition = ElementalComposition(
                    element=element,
                    # atom_fraction=row['atom_fraction'],
                    mass_fraction=float(mass_fractions[n]),
                )
                catalyst_sample.elemental_composition.append(elemental_composition)
        

            preparation_details = Preparation(
                preparation_method=row['preparation_method'],
                preparator=row['preparator'],
                preparing_institution=row['preparing_institution'],
            )

            surface = SurfaceArea(
                surface_area=row['surface_area'],
                method_surface_area_determination=row['surface_area_method'],
                # dispersion=row['dispersion'],
            )
            catalyst_sample.preparation_details = preparation_details
            catalyst_sample.surface = surface

            # archive.data = catalyst_sample
            create_archive(catalyst_sample, archive, f'{row["name"]}_catalyst_sample.archive.json')
        