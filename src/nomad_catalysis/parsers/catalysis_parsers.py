
import numpy as np
import pandas as pd
from nomad.datamodel import EntryArchive
from nomad.datamodel.metainfo.basesections import (
    CompositeSystemReference,
    ElementalComposition,
    SectionReference,
)
from nomad.parsing import MatchingParser
from nomad.units import ureg

from nomad_catalysis.parsers.utils import create_archive
from nomad_catalysis.schema_packages.catalysis import (
    CatalysisCollectionParserEntry,
    CatalystSample,
    CatalyticReaction,
    CatalyticReactionData,
    Preparation,
    ProductData,
    RatesData,
    RawFileData,
    ReactantData,
    ReactionConditionsData,
    ReactorFilling,
    ReactorSetup,
    Reagent,
    SurfaceArea,
)


def get_time_unit(string) -> any:
    """
    This function extracts the time unit (h/min/s) from a string.
    It returns a ureg.Quantity object with the time unit.
    """
    if 'h' in string:
        return ureg.hour
    elif 's' in string:
        return ureg.second
    elif 'min' in string:
        return ureg.minute
    else:
        raise ValueError('Time unit not recognized.')

def get_mass_unit(string) -> any:
    """
    This function extracts the mass unit (g/mg/kg) from a string.
    It returns a ureg.Quantity object with the mass unit.
    """
    string = string.strip('([])').casefold()
    if 'mg' in string:
        return ureg.milligram
    elif 'kg' in string:
        return ureg.kilogram
    elif string in ['g', 'gram']:
        return ureg.gram
    else:
        raise ValueError('Mass unit not recognized.')
    

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
        the code *for a sample entry*. Here, the column 'name' is droped if a 
        column 'catalyst' is present, as the focus is on the sample entry which is
        the catalyst.
        """

        for col in data_frame.columns:
            if col in ['catalyst name','catalyst_name', 'catalyst']:
                try:
                    data_frame.drop(columns=['name'], inplace=True)
                except KeyError:
                    pass
                data_frame.rename(columns={col: 'name'}, inplace=True)
            if col in ['storing institution', 'storing_institute']:
                data_frame.rename(columns={col: 'storing_institution'}, inplace=True)
            if col in ['date', 'sample date']:
                data_frame.rename(columns={col: 'datetime'}, inplace=True)
            if col in ['lab-id','sample_id', 'catalyst_id']:
                data_frame.rename(columns={col: 'lab_id'}, inplace=True)
            if col in ['surface_area_method']:
                data_frame.rename(
                    columns={col: 'method_surface_area_determination'}, inplace=True
                )
            if col in ['surface_area (m2/g)']:
                data_frame.rename(
                    columns={col: 'surface_area'}, inplace=True
                )
            if col in ['preparation']:
                data_frame.rename(columns={col: 'preparation_method'}, inplace=True)
            if col in ['comment', 'comments']:
                data_frame.rename(columns={col: 'description'}, inplace=True)
                
        return data_frame
    
    def check_zero_elements(
        self, el, logger) -> bool:
        """
        Checks if the element has a zero atomic or mass fraction.
        If it does, this will not be written in the results section of the reaction.
        """
        if el.atomic_fraction == 0.0 or el.mass_fraction == 0.0:
            logger.info(
                f'''{el.element} has a zero atomic or mass fraction and will not be
                appended to the elemental composition.'''
            )
            return True
        else:
            return False
    
    def extract_elemental_composition(self, row, catalyst_sample, logger) -> None:
        """
        This function extracts the elemental composition from a row of the data frame.
        It returns an ElementalComposition object with the element and its mass and atom
        fractions.
        """
        if 'elements' in row.keys():
            elements = row['elements'].split(',')
        elif 'element' in row.keys():
            elements = []
            elements.append(row['element'])
            if 'element.1' in row.keys():
                for key in row.keys():
                    if key.startswith('element.'):
                        elements.append(row[key])

        for m, element in enumerate(elements):
            elemental_composition = ElementalComposition(
                element=element.strip(),
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
            zero_element = self.check_zero_elements(
                elemental_composition, logger
            )
            if zero_element:
                continue
            catalyst_sample.elemental_composition.append(
                elemental_composition
            )

    def extract_reaction_feed(self, row, logger) -> ReactionConditionsData:
        """
        This function extracts the reaction feed from a row of the data frame.
        It returns a ReactionConditionsData object with the feed information.
        """
        feed = ReactionConditionsData()
        for key in row.keys():
            col_split = key.split(' ')

            if col_split[0].casefold() == 'set_temperature':
                if 'k' in col_split[1]:
                    feed.set_temperature = [np.nan_to_num(row[key])]
                elif 'c' in col_split[1]:
                    feed.set_temperature = [float(np.nan_to_num(row[key]))+273.15]

            if col_split[0].casefold() == 'tos' or (
                col_split[0].casefold() == 'time'):
                unit = get_time_unit(col_split[1])
                feed.time_on_stream = [np.nan_to_num(row[key])] * unit

            if col_split[0] == 'ghsv':
                if '1/h' in col_split[1] or 'h^-1' in col_split[1]:
                    feed.gas_hourly_space_velocity = (
                        [np.nan_to_num(row[key])] * ureg.hour**-1
                    )
                else:
                    logger.warning('Gas hourly space velocity unit not recognized.')

            if col_split[0] == 'whsv':
                if 'ml/g/h' in col_split[1] or 'ml/(g*h)' in col_split[1]:
                    feed.weight_hourly_space_velocity = (
                        [np.nan_to_num(row[key])]
                        * ureg.milliliter
                        / (ureg.gram * ureg.hour)
                    )

            if ((col_split[0] == 'vflow' or col_split[0] == 'flow_rate')
                and ('ml/min' in col_split[1] or 'mln' in col_split[1])):
                    feed.set_total_flow_rate = (
                        [np.nan_to_num(row[key])] * ureg.milliliter / ureg.minute
                    )

            if col_split[0] == 'set_pressure' and 'bar' in col_split[1]:
                feed.set_pressure = [np.nan_to_num(row[key])] * ureg.bar

        return feed
    
    def extract_catalytic_results(self, row, logger) -> CatalyticReactionData:
        """
        This function extracts the catalytic results from a row of the data frame.
        It returns a CatalyticReactionData object with the results information.
        """
        cat_data = CatalyticReactionData()
        
        for key in row.keys():
            col_split = key.split(' ')

            if key == 'c-balance':
                cat_data.c_balance = [np.nan_to_num(row[key])]
            elif col_split[0] == 'c-balance' and ('%' in col_split[1]):
                cat_data.c_balance = [np.nan_to_num(row[key])] / 100

            if col_split[0] == 'temperature':
                if 'k' in col_split[1]:
                    cat_data.temperature = [np.nan_to_num(row[key])]
                elif 'c' in col_split[1]:
                    cat_data.temperature = [float(np.nan_to_num(row[key]))+273.15]
                else:
                    logger.warning('Temperature unit not recognized.')

            if col_split[0] == 'pressure':
                if 'bar' in col_split[1]:
                    cat_data.pressure = [np.nan_to_num(row[key])] * ureg.bar
                else:
                    logger.warning('Pressure unit not recognized.')

            if col_split[0] == 'tos' or col_split[0] == 'time':
                unit = get_time_unit(col_split[1])
                cat_data.time_on_stream = [np.nan_to_num(row[key])] * unit

        return cat_data
    
    def extract_reactor_setup(self, row, logger) -> ReactorSetup:
        """
        This function extracts the reactor setup information from a row of the data
        frame. It returns a ReactorSetup object with the reactor setup information.
        """
        reactor_setup = ReactorSetup()
        
        for key in row.keys():
            col_split = key.split(' ')

            if key == 'reactor_type':
                    reactor_setup.reactor_type = row[key]
            if key.startswith('reactor_volume'):
                unit = col_split[1].strip('()')
                try:
                    reactor_setup.reactor_volume = ureg.Quantity(
                        np.nan_to_num(row[key]), unit
                    )
                except Exception as e:
                    logger.warning(f"""Reactor volume unit {unit} not recognized. 
                                Error: {e}""")
            if key.startswith('reactor_diameter'):
                unit = col_split[1].strip('()')
                try:
                    reactor_setup.reactor_diameter = ureg.Quantity(
                        np.nan_to_num(row[key]), unit
                    )
                except Exception as e:
                    logger.warning(f"""Reactor diameter unit {unit} not recognized. 
                                Error: {e}""")
            if key == 'reactor_lab_id':
                reactor_setup.lab_id = row[key]
            if key == 'reactor_name':
                reactor_setup.name = row[key]

        return reactor_setup

    def extract_pretreatment(self, row, logger) -> ReactionConditionsData:  # noqa: PLR0912, PLR0915
        """
        This function extracts the pretreatment information from a row of the data
        frame. It returns a ReactorFilling object with the pretreatment information.
        """
        pretreatment = ReactionConditionsData()
        pretreatment_reagents = []
        logger.info('Extracting pretreatment information from the data frame')
        for key in row.keys():
            col_split = key.split(' ')

            if col_split[0] == 'pretreatment':
                if col_split[1].startswith('set_temperature'):
                    if pretreatment.set_temperature is None:
                        pretreatment_temperature = [row[key]]
                    else:
                        pretreatment_temperature.append(row[key])
                    if 'c' in col_split[2]:
                        pretreatment_temperature_np = np.array(pretreatment_temperature)
                        pretreatment.set_temperature = (
                        pretreatment_temperature_np + 273.15)
                    elif 'k' in col_split[2]:
                        pretreatment.set_temperature= pretreatment_temperature
                    else:
                        logger.warning('Temperature unit not recognized.')

                if col_split[1].startswith('time'):
                    if pretreatment.time_on_stream is None:
                        tos = []
                    if len(col_split) == 3:  # noqa: PLR2004
                        unit = get_time_unit(col_split[2])
                    else:
                        logger.error('Time unit missing.')
                    tos.append(np.nan_to_num(row[key]))
                    pretreatment.time_on_stream = tos * unit
                if col_split[1].startswith('set_pressure'):
                    if not pretreatment.set_pressure:
                        pretreatment.set_pressure = []
                    if 'bar' in col_split[2]:
                        pretreatment.set_pressure.append(
                            np.nan_to_num(row[key])) # * ureg.bar
                    else:
                        logger.warning('Pressure unit not recognized.')
                if col_split[1].startswith('set_flow_rate'):
                    if not pretreatment.set_total_flow_rate:
                        pretreatment.set_total_flow_rate = []
                    if 'ml/min' in col_split[2] or 'mln' in col_split[2]:
                        total_flow=np.append(pretreatment.set_total_flow_rate.to('milliliter/minute').magnitude,
                                    row[key])
                        pretreatment.set_total_flow_rate = (
                            total_flow * ureg.milliliter / ureg.minute
                        )
                    else:
                        logger.warning(f'Flow rate unit not recognized from {key}.')
                if col_split[1].startswith('gas_flow'):
                    try:
                        if len(col_split) == 4 and (  # noqa: PLR2004
                            'ml/min' in col_split[3] or 'mln' in col_split[3]):
                            if col_split[2] not in pretreatment_reagents :
                                reagent = Reagent(
                                    name=col_split[2],
                                    flow_rate=(
                                            [np.nan_to_num(row[key])]
                                            * ureg.milliliter
                                            / ureg.minute
                                        ),
                                )
                                pretreatment_reagents.append(col_split[2])
                                pretreatment.reagents.append(reagent)
                            else:
                                index = pretreatment_reagents.index(col_split[2])
                                gas_flow = np.append(
                                    pretreatment.reagents[index].flow_rate.to('milliliter/minute').magnitude,
                                    row[key]
                                )
                                pretreatment.reagents[index].flow_rate = (
                                    gas_flow * ureg.milliliter / ureg.minute
                                )
                        else:
                            logger.warning(f'unit in {key} missing or not recognized.')
                            
                    except KeyError:
                        logger.warning(f'Gas flow for {key} not recognized.')

        return pretreatment

    def extract_reaction_entries(self, data_frame, archive, logger) -> None:  # noqa: PLR0912, PLR0915
        "This function extracts information for catalytic reaction entries with a"
        "single measurement from the data frame and adds them to the archive."
        reactions = []
        
        data_frame.dropna(axis=1, how='all', inplace=True)
        for n, row in data_frame.iterrows():
            row.dropna(inplace=True)

            reaction = CatalyticReaction()
            reactor_filling = ReactorFilling()
            sample = CompositeSystemReference()

            reagents = []
            reagent_names = []
            products = []
            product_names = []
            conversions = []
            conversion_names = []
            rates = []

            if 'reaction_type' in row.keys():
                reaction.reaction_type = []
                types= row['reaction_type'].split(',')
                if isinstance(types, list):
                    reaction.reaction_type.extend(types)
                else:
                    reaction.reaction_type.append(types)
            for key in [
                    'datetime',
                    'lab_id',
                    'description',
                    'reaction_name',
                    'experimenter',
                    'location',
                ]:
                if key in row.keys():
                    setattr(reaction, key, row[key])

            if 'datafile' in row.keys():
                reaction.data_file = row['datafile']

                reactions.append(
                        create_archive(
                            reaction,
                            archive,
                            f'{row["name"]}_catalytic_reaction.archive.json',
                        )
                    )
                continue

            feed = self.extract_reaction_feed(row, logger)
            cat_data = self.extract_catalytic_results(row, logger)
            reactor_setup = self.extract_reactor_setup(row, logger)
            pretreatment = self.extract_pretreatment(row, logger)

            for key in row.keys():
                
                col_split = key.split(' ')

                if key in ['catalyst', 'catalyst_name']:
                    setattr(sample, 'name', row[key])
                    setattr(reactor_filling, 'catalyst_name', str(row[key]))
                if key in ['sample_id', 'catalyst_id']:
                    setattr(sample, 'lab_id', row[key])
                
                # if len(col_split) < 2:  # noqa: PLR2004
                #     continue

                if col_split[0].casefold() == 'x':
                    if len(col_split) == 3 and ('%' in col_split[2]):  # noqa: PLR2004
                        try:
                            gas_in = [np.nan_to_num(float(row[key])) / 100.]
                        except (ValueError, TypeError) as e:
                            logger.warning(f"""Non-numeric value for {key}: {row[key]}. 
                                           Error: {e}.""")
                            gas_in = [np.nan]
                    else:
                        gas_in = [row[key]]
                    reagent = Reagent(name=col_split[1], fraction_in=gas_in)
                    reagent_names.append(col_split[1])
                    reagents.append(reagent)

                if col_split[0].casefold() == 'mass':
                    unit=get_mass_unit(col_split[1])
                    try:
                        reactor_filling.catalyst_mass = (row[key] * unit)
                    except Exception as e:
                        logger.warning(f"""Catalyst mass unit {col_split[1]} not 
                                       recognized. Error: {e}""")
                if key == 'diluent':
                    reactor_filling.diluent = row[key]
                    for key2 in row.keys():
                        if key2.startswith('diluent_mass'):
                            col_split = key2.split(' ')
                            unit = get_mass_unit(col_split[1])
                            try:
                                reactor_filling.diluent_mass = row[key2] * unit
                            except Exception as e:
                                logger.warning(f"""Diluents mass unit {col_split[1]} not
                                               recognized. Error: {e}""")

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
                                [np.nan_to_num(row[key])], 
                                unit_conversion.get(unit, unit)
                            ),
                        )
                    except Exception as e:
                        logger.warning(f"""Reaction rate unit {unit} not recognized. 
                                    Error: {e}""")
                    rates.append(rate)

                if col_split[0] == 'r_specific_mass':  # specific reaction rate
                    unit = col_split[2].strip('()')
                    unit_conversion = {
                        'mol/(h*gmetal': 'mol / (hour * g)',
                    }
                    try:
                        rate = RatesData(
                            name=col_split[1],
                            specific_mass_rate=ureg.Quantity(
                                [np.nan_to_num(row[key])], 
                                unit_conversion.get(unit, unit)
                            ),
                        )
                    except Exception as e:
                        logger.warning(f"""Specific reaction rate per mass unit {unit}
                            not recognized. Error: {e}""")
                    rates.append(rate)

                if col_split[2] != '(%)':
                    continue

                if col_split[0] == 'x_p':  # conversion, based on product detection
                    conversion = ReactantData(
                        name=col_split[1],
                        conversion=[np.nan_to_num(row[key])],
                        conversion_type='product-based conversion',
                        conversion_product_based=[np.nan_to_num(row[key])],
                    )
                    for i, p in enumerate(conversions):
                        if p.name == col_split[1]:
                            conversion = conversions.pop(i)

                    conversion.conversion_product_based = [np.nan_to_num(row[key])]
                    conversion.conversion = [np.nan_to_num(row[key])]
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
                            fraction_in=[
                                np.nan_to_num(float(row['x ' + col_split[1] + ' (%)']))
                                / 100],
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
                            conversion.conversion_reactant_based = [
                                np.nan_to_num(row[key])]
                    conversions.append(conversion)

                if col_split[0].casefold() == 'x_out':  # concentration out
                    if col_split[1] in reagent_names:
                        if "%" in key:
                            fraction_in = [
                                np.nan_to_num(float(row['x ' + col_split[1] + ' (%)']))
                                / 100
                            ]
                            fraction_out = [np.nan_to_num(row[key]) / 100]
                        else:
                            fraction_in = [np.nan_to_num(row['x ' + col_split[1]])]
                            fraction_out = [np.nan_to_num(row[key])]
                        
                        conversion = ReactantData(
                            name=col_split[1],
                            fraction_in=fraction_in,
                            fraction_out=fraction_out,
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

            cat_data.products = products
            if conversions != []:
                cat_data.reactants_conversions = conversions
            if rates != []:
                cat_data.rates = rates

            feed.reagents = reagents

            reaction.reaction_conditions = feed
            reaction.results = []
            reaction.results.append(cat_data)

            if reactor_filling != []:
                reaction.reactor_filling = reactor_filling
            if reactor_setup:
                reaction.instruments = []
                reaction.instruments.append(reactor_setup)
            if pretreatment:
                reaction.pretreatment = pretreatment

            reactions.append(
                create_archive(
                    reaction,
                    archive,
                    f'{row["name"]}_catalytic_reaction.archive.json',
                )
            )
        reaction_references = []
        for n, reaction in enumerate(reactions):
            reaction_ref = SectionReference(
                reference=reaction,
                name=data_frame["name"][n]
            )
            reaction_references.append(reaction_ref)
        archive.data.measurements = reaction_references

    def extract_sample_entries(self, data_frame, archive, logger
                               ) -> list[CatalystSample]:
        """ This function extracts information for catalyst sample entries from the
        data frame and adds them to the archive. It returns a list of CatalystSample
        objects."""
        logger.info('Extracting sample entries from the data frame')

        samples = []
        for n, row in data_frame.iterrows():
            row.dropna(inplace=True)
            catalyst_sample = CatalystSample()
            surface = SurfaceArea()
            preparation_details = Preparation()
            
            for key in [
                    'name',
                    'storing_institution',
                    'datetime',
                    'lab_id',
                    'form',
                    'support',
                    'description',
                ]:
                if key in row.keys():
                    setattr(catalyst_sample, key, row[key])
            if 'catalyst_type' in row.keys():
                    catalyst_sample.catalyst_type = []
                    catalyst_sample.catalyst_type.extend([row['catalyst_type']])
                    #setattr(catalyst_sample, key, row['catalyst_type'])
            if 'elements' in row.keys() or 'element' in row.keys():
                self.extract_elemental_composition(row, catalyst_sample, logger)
                    
            for key in ['preparation_method', 'preparator', 'preparing_institution']:
                if key in row.keys():
                    setattr(preparation_details, key, row[key])
            for key in [
                    'surface_area',
                    'method_surface_area_determination',
                    'dispersion',
                ]:
                if key in row.keys():
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
        return samples

    
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
    
        for col in data_frame.columns:
            col_small = col.strip().casefold()
            data_frame.rename(columns={col: col_small}, inplace=True)

        if 'CatalyticReactionCollection' in name[-2]:
            self.extract_reaction_entries(data_frame, archive, logger)
            logger.info(
                f'''File {filename} matches the expected format for a reaction
                collection. Reaction entries are successfully extracted.'''
            )
            return
        elif 'CatalystSampleCollection' in name[-2]:
            try:
                data_frame = self.unify_columnnames(data_frame)
                samples = self.extract_sample_entries(data_frame, archive, logger)
                logger.info(
                    f'''File {filename} matches the expected format for a catalysis
                    collection. Sample entries successfully extracted.'''
                )        
                samples_references = []
                for sample in samples:
                    sample_ref = CompositeSystemReference(
                        reference = sample,
                    )
                    samples_references.append(sample_ref)
                archive.data.samples = samples_references
                return
            except Exception as e:
                logger.error(f'Error extracting sample entries: {e}')
        
        elif 'CatalysisCollection' in name[-2]:
            try:
                self.extract_reaction_entries(data_frame, archive, logger)
                logger.info(
                    f'''File {filename} matches the expected format for a catalysis
                    collection. Reaction entries successfully extracted. And sample 
                    entries will be extracted next'''
                )
            except Exception as e:
                logger.error(f'Error extracting reaction entries: {e}')
                return
            
            try:
                data_frame = self.unify_columnnames(data_frame)
                samples = self.extract_sample_entries(data_frame, archive, logger)
                logger.info(
                    f'''File {filename} matches the expected format for a catalysis
                    collection. Sample entries successfully extracted.'''
                )
                samples_references = []
                for sample in samples:
                    sample_ref = CompositeSystemReference(
                        reference = sample,
                    )
                    samples_references.append(sample_ref)
                archive.data.samples = samples_references

            except Exception as e:
                logger.error(f'Error extracting sample entries: {e}')
        
        return
