
import pandas as pd
from nomad.datamodel import EntryArchive
from nomad.datamodel.metainfo.basesections import ElementalComposition
from nomad.parsing import MatchingParser

from nomad_catalysis.parsers.utils import create_archive
from nomad_catalysis.schema_packages.catalysis import (
    CatalystSample,
    CatalystSampleCollectionParserEntry,
    CatalyticReaction,
    Preparation,
    RawFileData,
    SurfaceArea,
)


class CatalysisParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger=None,
        child_archives: dict[str, EntryArchive] = None,
    ) -> None:
        filename = mainfile.split('/')[-1]
        name = filename.split('.')[0]
        logger.info(f' Catalysis Parser called {filename}')

        catalytic_reaction = CatalyticReaction(
            data_file=filename,
        )

        archive.data = RawFileData(
            measurement=create_archive(
                catalytic_reaction, archive, f'{name}.archive.json'
            )
        )
        archive.metadata.entry_name = f'{name} data file'


class CatalystCollectionParser(MatchingParser):
    def unify_columnnames(self, data_frame) -> pd.DataFrame:
        """
        This function unifies the column names of the data frame to a common format
        by renaming the columns to a standard format that is used in the rest of
        the code.
        """
        for col in data_frame.columns:
            if col in ['Name', 'name', 'catalyst']:
                data_frame.rename(columns={col: 'name'}, inplace=True)
            if col in ['Storing Institution', 'storing_institution']:
                data_frame.rename(columns={col: 'storing_institution'}, inplace=True)
            if col in ['datetime', 'date']:
                data_frame.rename(columns={col: 'datetime'}, inplace=True)
            if col in ['lab_id', 'sample_id']:
                data_frame.rename(columns={col: 'lab_id'}, inplace=True)
            if col in ['surface_area_method']:
                data_frame.rename(
                    columns={col: 'method_surface_area_determination'}, inplace=True
                )
            if col in ['comment', 'comments']:
                data_frame.rename(columns={col: 'description'}, inplace=True)
                
        return data_frame
    
    def extract_elemental_composition(self, row, catalyst_sample) -> ElementalComposition:
        """
        This function extracts the elemental composition from a row of the data frame.
        It returns an ElementalComposition object with the element and its mass and atom
        fractions.
        """
        elements = row['Elements'].split(',')
        for m, element in enumerate(elements):
            elemental_composition = ElementalComposition(
                element=element,
            )
            try:
                mass_fractions = row['mass_fractions'].split(',')
                elemental_composition.mass_fraction = float(
                    mass_fractions[m]
                )
            except KeyError:
                pass
            try:
                atom_fractions = row['atom_fractions'].split(',')
                elemental_composition.atom_fraction = float(
                    atom_fractions[m]
                )
            except KeyError:
                pass
            catalyst_sample.elemental_composition.append(
                elemental_composition
            )
        
    
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger=None,
        child_archives: dict[str, EntryArchive] = None,
    ) -> None:
        
        logger.info('Catalyst Collection Parser called')

        filename = mainfile.split('/')[-1]
        name = filename.split('.')
        archive.data = CatalystSampleCollectionParserEntry(
            data_file=filename,
        )
        archive.metadata.entry_name = f'{name[0]} data file'
        samples = []
        if name[1] == 'xlsx':
            data_frame = pd.read_excel(mainfile)
        elif name[1] == 'csv':
            data_frame = pd.read_csv(mainfile)
        else:
            return
        logger.info(f'Parsing {filename} with {data_frame.shape[0]} rows')
        data_frame = self.unify_columnnames(data_frame)
        
        for n, row in data_frame.iterrows():
            row.dropna(inplace=True)
            catalyst_sample = CatalystSample()
            surface = SurfaceArea()
            preparation_details = Preparation()
            for key in row.keys():
                if key in [
                    'name',
                    'storing_institution',
                    'datetime',
                    'lab_id',
                    'form',
                    'support',
                    'description',
                ]:
                    setattr(catalyst_sample, key, row[key])
                if key in ['catalyst_type']:
                    setattr(catalyst_sample, key, [row[key]])
                if key in ['Elements']:
                    self.extract_elemental_composition(row, catalyst_sample)
                    
                if key in ['preparation_method', 'preparator', 'preparing_institution']:
                    setattr(preparation_details, key, row[key])
                if key in [
                    'surface_area',
                    'method_surface_area_determination',
                    'dispersion',
                ]:
                    setattr(surface, key, row[key])

            if preparation_details.m_to_dict():
                catalyst_sample.preparation_details = preparation_details
            if surface.m_to_dict():
                catalyst_sample.surface = surface

            samples.append(
                create_archive(
                    catalyst_sample,
                    archive,
                    f'{row["name"]}_catalyst_sample.archive.json',
                )
            )

        archive.data.samples = samples
