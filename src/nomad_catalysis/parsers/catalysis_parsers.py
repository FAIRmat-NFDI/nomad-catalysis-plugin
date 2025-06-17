
import numpy as np
import pandas as pd
from nomad.datamodel import EntryArchive
from nomad.datamodel.metainfo.basesections import ElementalComposition
from nomad.parsing import MatchingParser
from nomad.units import ureg

from nomad_catalysis.parsers.utils import create_archive
from nomad_catalysis.schema_packages.catalysis import (
    CatalysisCollectionParserEntry,
    CatalystSample,
    CatalyticReaction,
    CatalyticReactionData,
    CompositeSystemReference,
    Preparation,
    ProductData,
    RatesData,
    RawFileData,
    ReactantData,
    ReactionConditionsData,
    ReactorFilling,
    Reagent,
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


class CatalysisCollectionParser(MatchingParser):
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
            if col in ['lab_id', 'lab-id','sample_id']:
                data_frame.rename(columns={col: 'lab_id'}, inplace=True)
            if col in ['surface_area_method']:
                data_frame.rename(
                    columns={col: 'method_surface_area_determination'}, inplace=True
                )
            if col in ['comment', 'comments']:
                data_frame.rename(columns={col: 'description'}, inplace=True)
                
        return data_frame
    
    def extract_elemental_composition(self, row, catalyst_sample) -> None:
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
    
    def extract_reaction_entries(self, data_frame, archive, logger) -> None:
        "This function extracts information for catalytic reaction entries with a single"
        "measurement from the data frame and adds them to the archive."
        reactions = []
        
        data_frame.dropna(axis=1, how='all', inplace=True)
        for n, row in data_frame.iterrows():
            reaction = CatalyticReaction()
            feed = ReactionConditionsData()
            reactor_filling = ReactorFilling()
            cat_data = CatalyticReactionData()
            sample = CompositeSystemReference()
            reagents = []
            reagent_names = []
            products = []
            product_names = []
            conversions = []
            conversion_names = []
            rates = []

            for key in row.keys():
                print(key, row[key])

                col_split = key.split(' ')

                if key in [
                    'datetime',
                    'lab_id',
                    'description',
                    'reaction_name',
                    'experimenter',
                    'location',
                ]:
                    setattr(reaction, key, row[key])
                if key in ['catalyst', 'catalyst_name']:
                    setattr(sample, 'name', row[key])
                    setattr(reactor_filling, 'catalyst_name', str(row[key]))
                if key in ['sample_id']:
                    setattr(sample, 'lab_id', row[key])
                if key in ['reaction_type']:
                    reaction.reaction_type = []
                    types= row[key].split(',')
                    if isinstance(types, list):
                        reaction.reaction_type.extend(types)
                    else:
                        reaction.reaction_type.append(types)

                if key.casefold() == 'c-balance':
                    cat_data.c_balance = [np.nan_to_num(row[key])]

                if len(col_split) < 2:  # noqa: PLR2004
                    continue

                if col_split[0].casefold() == 'c-balance' and ('%' in col_split[1]):
                    cat_data.c_balance = [np.nan_to_num(row[key])] / 100

                if col_split[0].casefold() == 'x':
                    if len(col_split) == 3 and ('%' in col_split[2]):  # noqa: PLR2004
                        gas_in = [row[key] / 100.]
                    else:
                        gas_in = [row[key]]
                    reagent = Reagent(name=col_split[1], fraction_in=gas_in)
                    reagent_names.append(col_split[1])
                    reagents.append(reagent)

                if col_split[0].casefold() == 'mass':
                    if '(g)' in col_split[1]:
                        reactor_filling.catalyst_mass = row[key] * ureg.gram
                    elif 'mg' in col_split[1]:
                        reactor_filling.catalyst_mass = (
                            row[key] * ureg.milligram
                        )
                if col_split[0].casefold() == 'set_temperature':
                    if 'K' in col_split[1]:
                        feed.set_temperature = [np.nan_to_num(row[key])]
                    elif 'C' in col_split[1] or 'celsius' in col_split[1].casefold():
                        feed.set_temperature = [float(np.nan_to_num(row[key]))+273.15]
                if col_split[0].casefold() == 'temperature':
                    if 'K' in col_split[1]:
                        cat_data.temperature = [np.nan_to_num(row[key])]
                    elif 'C' in col_split[1] or 'celsius' in col_split[1].casefold():
                        cat_data.temperature = [np.nan_to_num(row[key])+273.15]

                if col_split[0].casefold() == 'tos' or col_split[0].casefold() == 'time':
                    if 's' in col_split[1]:
                        cat_data.time_on_stream = [np.nan_to_num(row[key])] * ureg.second
                        feed.time_on_stream = [np.nan_to_num(row[key])] * ureg.second
                    elif 'min' in col_split[1]:
                        cat_data.time_on_stream = [np.nan_to_num(row[key])] * ureg.minute
                        feed.time_on_stream = [np.nan_to_num(row[key])] * ureg.minute
                    elif 'h' in col_split[1]:
                        cat_data.time_on_stream = [np.nan_to_num(row[key])] * ureg.hour
                        feed.time_on_stream = [np.nan_to_num(row[key])] * ureg.hour
                    else:
                        logger.warning('Time on stream unit not recognized.')

                if col_split[0] == 'GHSV':
                    if '1/h' in col_split[1] or 'h^-1' in col_split[1]:
                        feed.gas_hourly_space_velocity = (
                            [np.nan_to_num(row[key])] * ureg.hour**-1
                        )
                    else:
                        logger.warning('Gas hourly space velocity unit not recognized.')
                if col_split[0] == 'WHSV':
                    if 'ml/g/h' in col_split[1] or 'ml/(g*h)' in col_split[1]:
                        feed.weight_hourly_space_velocity = (
                            [np.nan_to_num(row[key])] * ureg.milliliter / (ureg.gram * ureg.hour)
                        )

                if col_split[0] == 'Vflow' or col_split[0] == 'flow_rate':
                    if 'mL/min' in col_split[1] or 'mln' in col_split[1]:
                        feed.set_total_flow_rate = (
                            [np.nan_to_num(row[key])] * ureg.milliliter / ureg.minute
                        )

                if col_split[0] == 'set_pressure' and 'bar' in col_split[1]:
                    feed.set_pressure = [np.nan_to_num(row[key])] * ureg.bar
                if col_split[0].casefold() == 'pressure' and 'bar' in col_split[1]:
                    cat_data.pressure = [np.nan_to_num(row[key])] * ureg.bar

                if len(col_split) < 3:  # noqa: PLR2004
                    continue

                if col_split[0] == 'r':  # reaction rate
                    unit = col_split[2].strip('()')
                    unit_conversion = {
                        'mmol/g/h': 'mmol / (g * hour)',
                        'mmol/g/min': 'mmol / (g * minute)',
                        'µmol/g/min': 'µmol / (g * minute)',
                        'mmolg^-1h^-1': 'mmol / (g * hour)',
                    }
                    try:
                        rate = RatesData(
                            name=col_split[1],
                            reaction_rate=ureg.Quantity(
                                [np.nan_to_num(row[key])], unit_conversion.get(unit, unit)
                            ),
                        )
                    except Exception as e:
                        logger.warning(f"""Reaction rate unit {unit} not recognized. 
                                    Error: {e}""")
                    rates.append(rate)

                if col_split[0] == 'r_specific_mass':  # specific reaction rate
                    unit = col_split[2].strip('()')
                    unit_conversion = {
                        'mol/(h*gMetal': 'mol / (hour * g)',
                    }
                    try:
                        rate = RatesData(
                            name=col_split[1],
                            specific_mass_rate=ureg.Quantity(
                                [np.nan_to_num(row[key])], unit_conversion.get(unit, unit)
                            ),
                        )
                    except Exception as e:
                        logger.warning(f"""Specific reaction rate per mass unit {unit} not recognized. 
                                    Error: {e}""")
                    rates.append(rate)

                if col_split[2] != '(%)':
                    continue

                if col_split[0] == 'x_p':  # conversion, based on product detection
                    conversion = ReactantData(
                        name=col_split[1],
                        conversion=np.nan_to_num(row[key]),
                        conversion_type='product-based conversion',
                        conversion_product_based=np.nan_to_num(row[key]),
                    )
                    for i, p in enumerate(conversions):
                        if p.name == col_split[1]:
                            conversion = conversions.pop(i)

                    conversion.conversion_product_based = np.nan_to_num(row[key])
                    conversion.conversion = np.nan_to_num(row[key])
                    conversion.conversion_type = 'product-based conversion'

                    conversion_names.append(col_split[1])
                    conversions.append(conversion)

                if col_split[0] == 'x_r':  # conversion, based on reactant detection
                    try:
                        conversion = ReactantData(
                            name=col_split[1],
                            conversion=[np.nan_to_num(row[key])],
                            conversion_type='reactant-based conversion',
                            conversion_reactant_based=[np.nan_to_num(row[key])],
                            fraction_in=(
                                np.nan_to_num(float(row['x ' + col_split[1] + ' (%)']) / 100
                            ),
                        )
                        )
                    except KeyError:
                        conversion = ReactantData(
                            name=col_split[1],
                            conversion=[np.nan_to_num(row[key])],
                            conversion_type='reactant-based conversion',
                            conversion_reactant_based=[np.nan_to_num(row[key])],
                            fraction_in=[np.nan_to_num(row['x ' + col_split[1]])],
                        )

                    for i, p in enumerate(conversions):
                        if p.name == col_split[1]:
                            conversion = conversions.pop(i)
                            conversion.conversion_reactant_based = [np.nan_to_num(row[key])]
                    conversions.append(conversion)

                if col_split[0].casefold() == 'x_out':  # concentration out
                    if col_split[1] in reagent_names:
                        conversion = ReactantData(
                            name=col_split[1],
                            fraction_in=[np.nan_to_num(row['x ' + col_split[1] + ' (%)'])]
                            / 100,
                            fraction_out=[np.nan_to_num(row[key])] / 100,
                        )
                        conversions.append(conversion)
                    else:
                        product = ProductData(
                            name=col_split[1],
                            fraction_out=[np.nan_to_num(row[key])] / 100,
                        )
                        products.append(product)
                        product_names.append(col_split[1])

                if col_split[0].casefold() == 's_p':  # selectivity
                    product = ProductData(
                        name=col_split[1], selectivity=[np.nan_to_num(row[key])]
                    )
                    for i, p in enumerate(products):
                        if p.name == col_split[1]:
                            product = products.pop(i)
                            product.selectivity = [np.nan_to_num(row[key])]
                            break
                    products.append(product)
                    product_names.append(col_split[1])

                if col_split[0].casefold() == 'y':  # product yield
                    product = ProductData(
                        name=col_split[1], product_yield=[np.nan_to_num(row[key])]
                    )
                    for i, p in enumerate(products):
                        if p.name == col_split[1]:
                            product = products.pop(i)
                            product.product_yield = [np.nan_to_num(row[key])]
                            break
                    products.append(product)
                    product_names.append(col_split[1])

                
            reaction.samples = []
            reaction.samples.append(sample)
            print(reaction,reaction.samples, reaction.samples[0].lab_id)

            cat_data.products = products
            if conversions != []:
                cat_data.reactants_conversions = conversions
            if rates != []:
                cat_data.rates = rates

            reaction.reaction_conditions = feed
            reaction.results = []
            reaction.results.append(cat_data)

            if reactor_filling:
                print(reactor_filling)
                reaction.reactor_filling = reactor_filling

            reactions.append(
                create_archive(
                    reaction,
                    archive,
                    f'{row["name"]}_catalytic_reaction.archive.json',
                )
            )

        archive.data.measurements = reactions
        return

    
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger=None,
        child_archives: dict[str, EntryArchive] = None,
    ) -> None:
        
        logger.info('Catalysis Collection Parser called')

        filename = mainfile.split('/')[-1]
        name = filename.split('.')

        archive.data = CatalysisCollectionParserEntry(
            data_file=filename,
        )
        archive.metadata.entry_name = f'{name[0]} data file'

        if name[-1] == 'xlsx':
            data_frame = pd.read_excel(mainfile)
        elif name[-1] == 'csv':
            data_frame = pd.read_csv(mainfile)
        else:
            return
        logger.info(f'Parsing {filename} with {data_frame.shape[0]} rows')
    
        
        if 'CatalyticReactionCollection' in name[-2]:
            self.extract_reaction_entries(data_frame, archive, logger)
            logger.info(
                f'File {filename} matches the expected format for a reaction collection.'
                'Only reaction entries are extracted.'
            )
            return
        elif 'CatalysisCollection' in name[-2]:
            try:
                self.extract_reaction_entries(data_frame, archive, logger)
                logger.info(
                    f'File {filename} matches the expected format for a catalysis collection.'
                    'reaction entries are extracted. And sample entries will be extracted next'
                )
            except Exception as e:
                logger.error(f'Error extracting reaction entries: {e}')
                logger.error(
                    f'File {filename} does not match the expected format'
                    'for a catalyst sample collection.'
                )
                return
        
        data_frame = self.unify_columnnames(data_frame)
        samples = []
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
        return
