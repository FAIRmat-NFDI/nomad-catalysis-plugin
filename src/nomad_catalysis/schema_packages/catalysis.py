from typing import (
    TYPE_CHECKING,
)

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from ase.data import chemical_symbols
from nomad.config import config
from nomad.datamodel.data import ArchiveSection, EntryDataCategory, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.basesections import (
    CompositeSystem,
    CompositeSystemReference,
    Instrument,
    Measurement,
    MeasurementResult,
    PubChemPureSubstanceSection,
)
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.datamodel.results import (
    Catalyst,
    CatalyticProperties,
    Material,
    Product,
    Properties,
    Reactant,
    Reaction,
    ReactionConditions,
    Results,
)
from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
)
from nomad.metainfo.metainfo import Category

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )


configuration = config.get_plugin_entry_point(
    'nomad_catalysis.schema_packages:catalysis'
)

m_package = SchemaPackage()


class CatalysisElnCategory(EntryDataCategory):
    m_def = Category(label='Catalysis', categories=[EntryDataCategory])


def add_catalyst(archive: 'EntryArchive') -> None:
    """
    Adds metainfo structure for catalysis data to the results section of the supplied
    archive.
    """
    if not archive.results:
        archive.results = Results()
    if not archive.results.properties:
        archive.results.properties = Properties()
    if not archive.results.properties.catalytic:
        archive.results.properties.catalytic = CatalyticProperties()
    if not archive.results.properties.catalytic.catalyst:
        archive.results.properties.catalytic.catalyst = Catalyst()


def add_catalyst_characterization(archive: 'EntryArchive') -> None:
    """
    Adds empty list for catalysis characterization methods to the results
    section of the supplied archive.
    """
    if not archive.results.properties.catalytic.catalyst.characterization_methods:
        archive.results.properties.catalytic.catalyst.characterization_methods = []


def add_activity(archive):
    """Adds metainfo structure for catalysis activity test data."""
    if not archive.results:
        archive.results = Results()
    if not archive.results.properties:
        archive.results.properties = Properties()
    if not archive.results.properties.catalytic:
        archive.results.properties.catalytic = CatalyticProperties()
    if not archive.results.properties.catalytic.reaction:
        archive.results.properties.catalytic.reaction = Reaction()
    if not archive.results.properties.catalytic.reaction.reaction_conditions:
        archive.results.properties.catalytic.reaction.reaction_conditions = (
            ReactionConditions()
        )


def get_nested_attr(obj, attr_path):
    """helper function to retrieve nested attributes"""
    for attr in attr_path.split('.'):
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    return obj


def set_nested_attr(obj, attr_path, value):
    """helper function to set nested attributes"""
    for attr in attr_path.split('.'):
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    setattr(obj, attrs[-1], value)


class Preparation(ArchiveSection):
    m_def = Section(
        description="""A section for general information about the
          preparation of a catalyst sample.""",
    )

    preparation_method = Quantity(
        type=str,
        shape=[],
        description="""
          Classification of the dominant preparation step
          in the catalyst synthesis procedure.
          """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'precipitation',
                    'hydrothermal',
                    'flame spray pyrolysis',
                    'impregnation',
                    'calcination',
                    'unknown',
                ]
            ),
            links=['https://w3id.org/nfdi4cat/voc4cat_0007016'],
        ),
    )

    preparator = Quantity(
        type=str,
        shape=[],
        description="""
        The person or persons preparing the sample in the lab.
        """,
        a_eln=dict(component='EnumEditQuantity'),
    )

    preparing_institution = Quantity(
        type=str,
        shape=[],
        description="""
        institution at which the sample was prepared
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Fritz-Haber-Institut Berlin / Abteilung AC',
                    'Fritz-Haber-Institut Berlin / ISC',
                ]
            ),
        ),
    )


class SurfaceArea(ArchiveSection):
    m_def = Section(
        description="""
        A section for specifying the specific surface area or dispersion of a catalyst
        sample and the method that was used determining this quantity.
        """,
        label_quantity='method_surface_area_determination',
        a_eln=ELNAnnotation(label='Surface Area'),
    )

    surface_area = Quantity(
        type=np.float64,
        unit=('m**2/g'),
        a_eln=dict(
            component='NumberEditQuantity',
            defaultDisplayUnit='m**2/g',
            description='The specific surface area of the sample in m^2/g.',
            links=['https://w3id.org/nfdi4cat/voc4cat_0000013'],
        ),
    )

    method_surface_area_determination = Quantity(
        type=str,
        shape=[],
        description="""
          A description of the method used to measure the surface area of the sample.
          """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'BET',
                    'H2-TPD',
                    'N2O-RFC',
                    'Fourier Transform Infrared Spectroscopy (FTIR)' ' of adsorbates',
                    'unknown',
                ]
            ),
        ),
    )

    dispersion = Quantity(
        type=np.float64,
        shape=[],
        description="""
        The percentage of total atoms which are surface atoms of a particle as a measure
        for the accessibility of the atoms.
        """,
        a_eln=dict(component='NumberEditQuantity'),
    )


class CatalystSample(CompositeSystem, Schema):
    m_def = Section(
        description="""
        An entry schema for specifying general information about a catalyst sample.
        """,
        label='Catalyst Sample',
        categories=[CatalysisElnCategory],
    )

    preparation_details = SubSection(
        section_def=Preparation,
    )

    surface = SubSection(
        section_def=SurfaceArea,
    )

    storing_institution = Quantity(
        type=str,
        shape=[],
        description="""
        The institution at which the sample is stored.
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Fritz-Haber-Institut Berlin / Abteilung AC',
                    'Fritz-Haber-Institut Berlin / ISC',
                    'TU Berlin / BasCat',
                ]
            ),
        ),
    )

    catalyst_type = Quantity(
        type=str,
        shape=['*'],
        description="""
          A classification of the catalyst type.
          """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'bulk catalyst',
                    'supported catalyst',
                    'single crystal',
                    'metal',
                    'oxide',
                    '2D catalyst',
                    'other',
                    'unkown',
                ]
            ),
        ),
        links=['https://w3id.org/nfdi4cat/voc4cat_0007014'],
    )

    form = Quantity(
        type=str,
        shape=[],
        description="""
          classification of physical form of catalyst
          """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['sieve fraction', 'powder', 'thin film']),
        ),
        links=['https://w3id.org/nfdi4cat/voc4cat_0000016'],
    )

    def populate_results(self, archive: 'EntryArchive', logger) -> None:
        """
        This function copies the catalyst sample information specified in the dictionary
        quantities_results_mapping in the function below into the results section of the
        archive of the entry.
        """

        sample_obj = self

        add_catalyst(archive)
        quantities_results_mapping = {
            'name': 'catalyst_name',
            'catalyst_type': 'catalyst_type',
            'preparation_details.preparation_method': 'preparation_method',
            'surface.surface_area': 'surface_area',
            'surface.method_surface_area_determination': 'characterization_methods',
        }

        for ref_attr, catalyst_attr in quantities_results_mapping.items():
            value = get_nested_attr(sample_obj, ref_attr)
            if value is not None:
                try:
                    setattr(
                        archive.results.properties.catalytic.catalyst,
                        catalyst_attr,
                        value,
                    )
                except ValueError:  # workaround for wrong type in yaml schema
                    setattr(
                        archive.results.properties.catalytic.catalyst,
                        catalyst_attr,
                        [value],
                    )
                except Exception as e:
                    logger.warn(
                        f'Error while copying "{ref_attr}" to results: {e}', exc_info=e
                    )

    def add_referencing_methods(
        self, archive: 'EntryArchive', logger: 'BoundLogger', number=10
    ) -> None:
        """
        This function looks for other entries that reference the sample and checks the
        entry type and if it finds a ELNXRayDiffration entry it adds 'XRD' to the
        characterization_methods in result.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger('Bound Logger'): A structlog logger.
            number: specifies the number of referencing entries that are checked,
            set to 10 by default
        """

        if self.lab_id is None:
            logger.warn("""Sample contains no lab_id, automatic linking of measurements
                         to this sample entry does not work.""")

        from nomad.search import MetadataPagination, search

        query = {
            'section_defs.definition_qualified_name:all': [
                'nomad.datamodel.metainfo.basesections.Activity'
            ],
            'entry_references.target_entry_id': archive.metadata.entry_id,
        }
        search_result = search(
            owner='all',
            query=query,
            pagination=MetadataPagination(page_size=number),
            user_id=archive.metadata.main_author.user_id,
        )

        if search_result.pagination.total > 0:
            methods = []
            for entry in search_result.data:
                if entry['results']['eln']['methods'] != ['ELNMeasurement']:
                    method = entry['results']['eln']['methods'][0]
                    methods.append(method)
                else:
                    method = entry['entry_type']
                    methods.append(method)

            if search_result.pagination.total > number:
                logger.warn(
                    f'Found {search_result.pagination.total} entries with entry_id:'
                    f' "{archive.metadata.entry_id}". Will only check the the first '
                    f'"{number}" activity entries found for activity methods.'
                )
            if methods:
                add_catalyst_characterization(archive)
                for method in methods:
                    if method not in (
                        archive.results.properties.catalytic.catalyst.characterization_methods
                    ):
                        (
                            archive.results.properties.catalytic.catalyst.characterization_methods.append(
                                method
                            )
                        )
        else:
            logger.warn(
                f'''Found no entries referencing this entry
                "{archive.metadata.entry_id}."'''
            )

    def normalize(self, archive, logger):
        self.populate_results(archive, logger)

        from nomad.datamodel.context import ClientContext

        if isinstance(archive.m_context, ClientContext):
            return

        super().normalize(archive, logger)
        self.add_referencing_methods(archive, logger)


class ReactorFilling(ArchiveSection):
    m_def = Section(
        description='A class containing information about the catalyst'
        ' and filling in the reactor.',
        label='Reactor Filling',
    )

    catalyst_name = Quantity(
        type=str, shape=[], a_eln=ELNAnnotation(component='StringEditQuantity')
    )

    sample_section_reference = Quantity(
        type=CompositeSystemReference,
        description='A reference to the sample used in the measurement.',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity', label='Sample Reference'
        ),
    )

    catalyst_mass = Quantity(
        type=np.float64,
        shape=[],
        unit='mg',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mg'),
    )

    catalyst_density = Quantity(
        type=np.float64,
        shape=[],
        unit='g/mL',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='g/mL'),
    )

    apparent_catalyst_volume = Quantity(
        type=np.float64,
        shape=[],
        unit='mL',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mL'),
    )

    catalyst_sievefraction_upper_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='micrometer',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )
    catalyst_sievefraction_lower_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='micrometer',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )
    particle_size = Quantity(
        type=np.float64,
        shape=[],
        unit='micrometer',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )
    diluent = Quantity(
        type=str,
        shape=[],
        description="""
        A component that is mixed with the catalyst to dilute and prevent transport
        limitations and hot spot formation.
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(suggestions=['SiC', 'SiO2', 'unknown']),
        ),
    )
    diluent_sievefraction_upper_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='micrometer',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )
    diluent_sievefraction_lower_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='micrometer',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        if self.sample_section_reference is None:
            if self.m_root().data.samples:
                first_sample = self.m_root().data.samples[0]
                if hasattr(first_sample, 'reference'):
                    self.sample_section_reference = first_sample

        if self.catalyst_name is None and self.sample_section_reference is not None:
            self.catalyst_name = self.sample_section_reference.name

        if (
            self.apparent_catalyst_volume is None
            and self.catalyst_mass is not None
            and self.catalyst_density is not None
        ):
            self.apparent_catalyst_volume = self.catalyst_mass / self.catalyst_density


class ReactorSetup(Instrument, ArchiveSection):
    m_def = Section(
        description='Specification about the type of reactor used in the measurement.',
        label_quantity='name',
    )

    name = Quantity(type=str, shape=[], a_eln=dict(component='EnumEditQuantity'))

    reactor_type = Quantity(
        type=str,
        shape=[],
        a_eln=dict(component='EnumEditQuantity'),
        props=dict(
            suggestions=[
                'plug flow reactor',
                'batch reactor',
                'continuous stirred-tank reactor',
                'fluidized bed',
            ]
        ),
    )

    bed_length = Quantity(
        type=np.float64,
        shape=[],
        unit='mm',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    reactor_cross_section_area = Quantity(
        type=np.float64,
        shape=[],
        unit='mm**2',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mm**2'),
    )

    reactor_diameter = Quantity(
        type=np.float64,
        shape=[],
        unit='mm',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    reactor_volume = Quantity(
        type=np.float64,
        shape=[],
        unit='ml',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='ml'),
    )


class Reagent(ArchiveSection):
    m_def = Section(
        label_quantity='name',
        description='A chemical substance present in the initial reaction mixture.',
    )
    name = Quantity(
        type=str,
        a_eln=ELNAnnotation(label='reagent name', component='StringEditQuantity'),
        description='reagent name',
    )
    gas_concentration_in = Quantity(
        type=np.float64,
        shape=['*'],
        description="""Volumetric fraction of reactant in feed. The value must be
        between 0 and 1""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    flow_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mL/minutes',
        description='Flow rate of reactant in feed.',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mL/minute'
        ),
    )

    pure_component = SubSection(section_def=PubChemPureSubstanceSection)

    def normalize(self, archive, logger):
        """
        The normalizer will run for the subsection `PureSubstanceComponent` class.
        A few exceptions are set here for reagents with ambiguous names or missing
        entries in the PubChem database. A time.sleep(1) is set to prevent blocked IP
        due to too many requests to the PubChem database.
        If none is set, the normalizer will set the name of the component to be the
        molecular formula of the substance.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger ('BoundLogger'): A structlog logger.
        """
        super().normalize(archive, logger)

        if self.name is None:
            return
        if self.name in ['C5-1', 'C6-1', 'nC5', 'nC6', 'Unknown', 'inert', 'P>=5C']:
            return
        elif self.name == 'n-Butene':
            self.name = '1-butene'
        elif self.name == 'MAN':
            self.name = 'maleic anhydride'
        elif '_' in self.name:
            self.name = self.name.replace('_', ' ')

        if self.name and self.pure_component is None:
            import time

            self.pure_component = PubChemPureSubstanceSection(name=self.name)
            if self.name == 'propionic acid':
                self.pub_chem_id = 1032
                self.pure_component.iupac_name = 'propanoic acid'
                self.pure_component.molecular_formula = 'C3H6O2'
                self.pure_component.molecular_mass = 74.08
                return
            elif self.name in ['CO', 'carbon monoxide']:
                self.pub_chem_id = 281
                self.pure_component.iupac_name = 'carbon monoxide'
                self.pure_component.molecular_formula = 'CO'
                self.pure_component.molecular_mass = 28.01
                self.pure_component.inchi = 'InChI=1S/CO/c1-2'
                self.pure_component.inchi_key = 'UGFAIRIUMAVXCW-UHFFFAOYSA-N'
                self.pure_component.cas_number = '630-08-0'
                return
            elif self.name in ['CO2', 'carbon dioxide']:
                self.pub_chem_id = 280
                self.pure_component.iupac_name = 'carbon dioxide'
                self.pure_component.molecular_formula = 'CO2'
                self.pure_component.molecular_mass = 44.01
                self.pure_component.inchi = 'InChI=1S/CO2/c2-1-3'
                self.pure_component.inchi_key = 'CURLTUGMZLYLDI-UHFFFAOYSA-N'
                self.pure_component.cas_number = '124-38-9'
                return
            else:
                time.sleep(1)
                self.pure_component.normalize(archive, logger)

        if self.name is None and self.pure_component is not None:
            self.name = self.pure_component.molecular_formula


class ReactantData(Reagent):
    m_def = Section(
        label_quantity='name',
        description='A reagent that has a conversion in a reaction that is not null',
    )

    gas_concentration_out = Quantity(
        type=np.float64,
        shape=['*'],
        description="""Volumetric fraction of reactant in outlet. the value must be
        between 0 and 1""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    reference = Quantity(type=Reagent, a_eln=dict(component='ReferenceEditQuantity'))
    conversion = Quantity(
        type=np.float64,
        shape=['*'],
        description="""The conversion of the reactant in the reaction mixture.
        The value is in %""",
    )
    conversion_type = Quantity(
        type=str,
        a_eln=dict(
            component='StringEditQuantity',
            props=dict(suggestions=['product_based', 'reactant_based', 'unknown']),
        ),
    )
    conversion_product_based = Quantity(type=np.float64, shape=['*'])
    conversion_reactant_based = Quantity(type=np.float64, shape=['*'])


class RatesData(ArchiveSection):
    m_def = Section(label_quantity='name')
    name = Quantity(type=str, a_eln=ELNAnnotation(component='StringEditQuantity'))

    reaction_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mmol/g/hour',
        description="""
        The reaction rate for mmol of product (or reactant) formed (depleted) per
        catalyst (g) per time (hour).
        """,
    )

    specific_mass_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mmol/g/hour',
        description="""
        The specific reaction rate normalized by active (metal) catalyst mass, instead
        of mass of total catalyst.
        """,
    )

    specific_surface_area_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mmol/m**2/hour',
        description="""
        The specific reaction rate normalized by active (metal) surface area of
        catalyst, instead of mass of total catalyst.
        """,
    )
    space_time_yield = Quantity(
        type=np.float64,
        shape=['*'],
        unit='g/g/hour',
        description="""
        The amount of product formed (in g), per total catalyst (g) per time (hour).
        """,
    )
    rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='g/g/hour',
        description="""
        The amount of reactant converted (in g), per total catalyst (g) per time (hour).
        """,
    )

    turn_over_frequency = Quantity(
        type=np.float64,
        shape=['*'],
        unit='1/hour',
        description="""
        The turn oder frequency, calculated from mol of reactant or product, per number
        of sites, over time.
        """,
    )


class ProductData(Reagent, ArchiveSection):
    m_def = Section(
        label_quantity='name',
        description="""
        A chemical substance formed in the reaction mixture during a reaction.""",
    )

    gas_concentration_out = Quantity(
        type=np.float64,
        shape=['*'],
        description="""Volumetric fraction of reactant in outlet.
            The value must be between 0 and 1""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    selectivity = Quantity(
        type=np.float64,
        shape=['*'],
        description="""The selectivity of the product in the reaction mixture. The
        value is in %.""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
        iris=['https://w3id.org/nfdi4cat/voc4cat_0000125'],
    )

    product_yield = Quantity(
        type=np.float64,
        shape=['*'],
        description="""
        The yield of the product in the reaction mixture, calculated as
        conversion x selectivity.""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    rates = SubSection(section_def=RatesData)

    def normalize(self, archive, logger):
        """
        The normalizer for the adjusted `PureSubstanceComponent` class. If none is set,
        the normalizer will set the name of the component to be the molecular formula of
        the substance.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger ('BoundLogger'): A structlog logger.
        """
        super().normalize(archive, logger)


class ReactionConditions_data(PlotSection, ArchiveSection):
    m_def = Section(
        description="""
                    A class containing reaction conditions for a generic reaction."""
    )

    set_temperature = Quantity(
        type=np.float64,
        shape=['*'],
        unit='K',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    set_pressure = Quantity(
        type=np.float64,
        shape=['*'],
        unit='bar',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='bar'),
    )

    set_total_flow_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mL/minute',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mL/minute'
        ),
    )

    weight_hourly_space_velocity = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mL/(g*hour)',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mL/(g*hour)'),
    )

    contact_time = Quantity(
        type=np.float64,
        shape=['*'],
        unit='g*s/mL',
        a_eln=ELNAnnotation(
            label='W|F', defaultDisplayUnit='g*s/mL', component='NumberEditQuantity'
        ),
    )

    gas_hourly_space_velocity = Quantity(
        type=np.float64,
        shape=['*'],
        unit='1/hour',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='1/hour'),
    )

    runs = Quantity(type=np.float64, shape=['*'])

    sampling_frequency = Quantity(  # maybe better use sampling interval?
        type=np.float64,
        shape=[],
        unit='Hz',
        description='The number of measurement points per time.',
        a_eln=dict(component='NumberEditQuantity'),
    )

    time_on_stream = Quantity(
        type=np.float64,
        shape=['*'],
        unit='hour',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    reagents = SubSection(section_def=Reagent, repeats=True)

    def plot_figures(self):
        if self.time_on_stream is not None:
            x = self.time_on_stream.to('hour')
            x_text = 'time (h)'
        elif self.runs is not None:
            x = self.runs
            x_text = 'steps'
        else:
            return

        if self.set_temperature is not None and len(self.set_temperature) > 1:
            figT = px.scatter(x=x, y=self.set_temperature.to('kelvin'))
            figT.update_layout(title_text='Temperature')
            figT.update_xaxes(
                title_text=x_text,
            )
            figT.update_yaxes(title_text='Temperature (K)')
            self.figures.append(
                PlotlyFigure(label='Temperature', figure=figT.to_plotly_json())
            )

        if self.set_pressure is not None and len(self.set_pressure) > 1:
            figP = px.scatter(x=x, y=self.set_pressure.to('bar'))
            figP.update_layout(title_text='Pressure')
            figP.update_xaxes(
                title_text=x_text,
            )
            figP.update_yaxes(title_text='pressure (bar)')
            self.figures.append(
                PlotlyFigure(label='Pressure', figure=figP.to_plotly_json())
            )

        if self.reagents is not None and self.reagents != []:
            if self.reagents[0].flow_rate is not None or (
                self.reagents[0].gas_concentration_in is not None
            ):
                fig5 = go.Figure()
                for i, r in enumerate(self.reagents):
                    if r.flow_rate is not None:
                        y = r.flow_rate.to('mL/minute')
                        fig5.add_trace(go.Scatter(x=x, y=y, name=r.name))
                        y5_text = 'Flow rates (mL/min)'
                        if self.set_total_flow_rate is not None and i == 0:
                            fig5.add_trace(
                                go.Scatter(
                                    x=x,
                                    y=self.set_total_flow_rate,
                                    name='Total Flow Rates',
                                )
                            )
                    elif self.reagents[0].gas_concentration_in is not None:
                        fig5.add_trace(
                            go.Scatter(
                                x=x,
                                y=self.reagents[i].gas_concentration_in,
                                name=self.reagents[i].name,
                            )
                        )
                        y5_text = 'gas concentrations'
                fig5.update_layout(title_text='Gas feed', showlegend=True)
                fig5.update_xaxes(title_text=x_text)
                fig5.update_yaxes(title_text=y5_text)
                self.figures.append(
                    PlotlyFigure(label='Feed Gas', figure=fig5.to_plotly_json())
                )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        for reagent in self.reagents:
            reagent.normalize(archive, logger)

        self.plot_figures()


class CatalyticReaction_core(Measurement, ArchiveSection):
    reaction_class = Quantity(
        type=str,
        description="""
        A highlevel classification of the studied reaction.
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'oxidation',
                    'hydrogenation',
                    'dehydrogenation',
                    'cracking',
                    'isomerisation',
                    'coupling',
                ]
            ),
        ),
        links=['https://w3id.org/nfdi4cat/voc4cat_0007010'],
    )

    reaction_name = Quantity(
        type=str,
        description="""
        The name of the studied reaction.
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'ethane oxidation',
                    'propane oxidation',
                    'butane oxidation',
                    'CO hydrogenation',
                    'methanol synthesis',
                    'Fischer-Tropsch reaction',
                    'water gas shift reaction',
                    'ammonia synthesis',
                    'ammonia decomposition',
                ]
            ),
        ),
        links=['https://w3id.org/nfdi4cat/voc4cat_0007009'],
    )

    experiment_handbook = Quantity(
        description="""
        In case the experiment was performed according to a handbook.
        """,
        type=str,
        shape=[],
        a_eln=dict(component='FileEditQuantity'),
        links=['https://w3id.org/nfdi4cat/voc4cat_0007012'],
    )

    location = Quantity(
        type=str,
        shape=[],
        description="""
        The institution at which the measurement was performed.
        """,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=[
                    'Fritz-Haber-Institut Berlin / Abteilung AC',
                    'Fritz-Haber-Institut Berlin / ISC',
                    'TU Berlin, BASCat',
                    'HZB',
                    'CATLAB',
                ]
            ),
        ),
    )

    experimenter = Quantity(
        type=str,
        shape=[],
        description="""
        The person that performed or started the measurement.
        """,
        a_eln=dict(component='EnumEditQuantity'),
    )


class CatalyticReactionData(PlotSection, MeasurementResult, ArchiveSection):
    temperature = Quantity(
        type=np.float64,
        shape=['*'],
        unit='°C',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    pressure = Quantity(
        type=np.float64,
        shape=['*'],
        unit='bar',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    runs = Quantity(
        type=np.float64,
        shape=['*'],
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    time_on_stream = Quantity(
        type=np.float64,
        shape=['*'],
        unit='hour',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    c_balance = Quantity(
        type=np.dtype(np.float64),
        shape=['*'],
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    reactants_conversions = SubSection(section_def=ReactantData, repeats=True)
    rates = SubSection(section_def=RatesData, repeats=True)

    products = SubSection(section_def=ProductData, repeats=True)

    def normalize(self, archive, logger):
        if self.products is not None:
            for product in self.products:
                if product.pure_component is None or product.pure_component == []:
                    product.normalize(archive, logger)


class CatalyticReaction(CatalyticReaction_core, PlotSection, Schema):
    m_def = Section(
        label='Catalytic Reaction (filled manual/ by json directly)',
        a_eln=ELNAnnotation(
            properties=dict(
                order=[
                    'name',
                    'data_file',
                    'reaction_name',
                    'reaction_class',
                    'experimenter',
                    'location',
                    'experiment_handbook',
                ]
            )
        ),
        categories=[CatalysisElnCategory],
    )

    reactor_setup = SubSection(
        section_def=ReactorSetup, a_eln=ELNAnnotation(label='Reactor Setup')
    )
    reactor_filling = SubSection(
        section_def=ReactorFilling, a_eln=ELNAnnotation(label='Reactor Filling')
    )

    pretreatment = SubSection(
        section_def=ReactionConditions_data, a_eln=ELNAnnotation(label='Pretreatment')
    )
    reaction_conditions = SubSection(
        section_def=ReactionConditions_data,
        a_eln=ELNAnnotation(label='Reaction Conditions'),
    )
    results = Measurement.results.m_copy()
    results.section_def = CatalyticReactionData
    results.a_eln = ELNAnnotation(label='Reaction Results')
    # results = SubSection(section_def=CatalyticReactionData,
    #           a_eln=ELNAnnotation(label='Reaction Results'))

    def populate_reactivity_info(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        """
        Maps and copies the reaction data from data to the results archive
        of the measurement.
        """
        add_activity(archive)
        quantities_results_mapping = {
            'reaction_conditions.set_temperature': 'reaction_conditions.temperature',
            'reaction_conditions.set_pressure': 'reaction_conditions.pressure',
            'reaction_conditions.weight_hourly_space_velocity': 'reaction_conditions.weight_hourly_space_velocity',  # noqa: E501
            'reaction_conditions.gas_hourly_space_velocity': 'reaction_conditions.gas_hourly_space_velocity',  # noqa: E501
            'reaction_conditions.set_total_flow_rate': 'reaction_conditions.flow_rate',
            'reaction_conditions.time_on_stream': 'reaction_conditions.time_on_stream',
            'results[0].temperature': 'reaction_conditions.temperature',
            'results[0].pressure': 'reaction_conditions.pressure',
            'results[0].time_on_stream': 'reaction_conditions.time_on_stream',
            'reaction_name': 'name',
            'reaction_class': 'type',
        }

        # Loop through the mapping and assign the values
        for ref_attr, reaction_attr in quantities_results_mapping.items():
            value = get_nested_attr(self, ref_attr)
            if value is not None:
                try:
                    set_nested_attr(
                        archive.results.properties.catalytic.reaction,
                        reaction_attr,
                        value,
                    )
                except ValueError:
                    set_nested_attr(
                        archive.results.properties.catalytic.reaction,
                        reaction_attr,
                        [value],
                    )
                except Exception:
                    logger.warn(f'Failed to set {reaction_attr} with value {value}')

    def populate_catalyst_sample_info(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        """
        Copies the catalyst sample information from a reference
        into the results archive of the measurement.
        """
        sample_obj = self.samples[0].reference

        add_catalyst(archive)
        quantities_results_mapping = {
            'name': 'catalyst_name',
            'catalyst_type': 'catalyst_type',
            'preparation_details.preparation_method': 'preparation_method',
            'surface.surface_area': 'surface_area',
        }

        # Loop through the mapping and assign the values
        for ref_attr, catalyst_attr in quantities_results_mapping.items():
            value = get_nested_attr(sample_obj, ref_attr)
            if value is not None:
                try:
                    setattr(
                        archive.results.properties.catalytic.catalyst,
                        catalyst_attr,
                        value,
                    )
                except ValueError:
                    setattr(
                        archive.results.properties.catalytic.catalyst,
                        catalyst_attr,
                        [value],
                    )
                except Exception:
                    logger.warn('Something else went wrong when trying setattr')

        if self.samples[0].reference.name is not None:
            if not archive.results.material:
                archive.results.material = Material()
            archive.results.material.material_name = self.samples[0].reference.name

        if self.samples[0].reference.elemental_composition is not None:
            if not archive.results.material:
                archive.results.material = Material()
        try:
            archive.results.material.elemental_composition = self.samples[
                0
            ].reference.elemental_composition

        except Exception as e:
            logger.warn('Could not analyse elemental compostion.', exc_info=e)

        for i in self.samples[0].reference.elemental_composition:
            if i.element not in chemical_symbols:
                logger.warn(
                    f"'{i.element}' is not a valid element symbol and this "
                    'elemental_composition section will be ignored.'
                )
            elif i.element not in archive.results.material.elements:
                archive.results.material.elements += [i.element]

    def determine_x_axis(self):
        """Helper function to determine the x-axis data for the plots."""
        if self.results[0].time_on_stream is not None:
            x = self.results[0].time_on_stream.to('hour')
            x_text = 'time (h)'
        elif self.results[0].runs is not None:
            x = self.results[0].runs
            x_text = 'steps'
        else:
            number_of_runs = len(self.reaction_conditions.set_temperature)
            x = np.linspace(1, number_of_runs, number_of_runs)
            x_text = 'steps'
        return x, x_text

    def get_y_data(self, plot_quantities_dict, var):
        """Helper function to get the y data for the plots.
        Args:
            plot_quantities_dict (dict): a dictionary with the plot quantities
            var (str): the variable to be plotted
        Returns:
            y (np.array): the y-axis data
            var (str): the variable to be plotted
        """
        y = get_nested_attr(self.results[0], plot_quantities_dict[var])
        if y is not None:
            return y, var
        y = get_nested_attr(self.reaction_conditions, plot_quantities_dict[var])
        if y is not None:
            return y, var
        y = get_nested_attr(
            self.reaction_conditions, 'set_' + plot_quantities_dict[var]
        )
        if y is not None:
            return y, 'set ' + var
        return None, var

    def conversion_plot(self, x, x_text, logger: 'BoundLogger') -> None:
        """This function creates a conversion plot.
        Args:
            x (np.array): the x-axis data
            x_text (str): the x-axis label
            logger ('BoundLogger'): A structlog logger.
        Returns:
            fig1 (plotly.graph_objs.Figure): the plotly figure

        """
        if not self.results[0].reactants_conversions:
            logger.warn('no conversion data found, so no plot is created')
            return
        if not self.results[0].reactants_conversions[0].conversion:
            logger.warn('no conversion data found, so no plot is created')
            return
        fig1 = go.Figure()
        for i, c in enumerate(self.results[0].reactants_conversions):
            fig1.add_trace(
                go.Scatter(
                    x=x,
                    y=self.results[0].reactants_conversions[i].conversion,
                    name=self.results[0].reactants_conversions[i].name,
                )
            )
        fig1.update_layout(title_text='Conversion', showlegend=True)
        fig1.update_xaxes(title_text=x_text)
        fig1.update_yaxes(title_text='Conversion (%)')
        return fig1

    def single_plot(self, x, x_text, y, y_text, title):
        """This function creates a single figure object.
        Args:
            x (np.array): the x-axis data
            x_text (str): the x-axis label
            y (np.array): the y-axis data
            y_text (str): the y-axis label
            title (str): the title of the plot
        Returns:
            fig (plotly.graph_objs.Figure): the plotly figure
        """
        fig = go.Figure()
        fig = px.line(x=x, y=y, markers=True)
        fig.update_layout(title_text=title)
        fig.update_xaxes(title_text=x_text)
        fig.update_yaxes(title_text=y_text)
        return fig

    def plot_figures(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        This function creates the figures for the CatalyticReaction class.
        """
        self.figures = []
        x, x_text = self.determine_x_axis()

        plot_quantities_dict = {
            'Temperature': 'temperature',
            'Pressure': 'pressure',
            'Weight hourly space velocity': 'weight_hourly_space_velocity',
            'Gas hourly space velocity': 'gas_hourly_space_velocity',
            'Total flow rate': 'total_flow_rate',
        }

        unit_dict = {
            'Temperature': '°C',
            'Pressure': 'bar',
            'Weight hourly space velocity': 'mL/(g*hour)',
            'Gas hourly space velocity': '1/hour',
            'Total flow rate': 'mL/minute',
        }
        for var in plot_quantities_dict:
            title = var
            y, y_text = self.get_y_data(plot_quantities_dict, var)
            if y is None:
                logger.warn(f"no '{var}' data found, so no plot is created")
                continue
            y.to(unit_dict[var])
            fig = self.single_plot(x, x_text, y.to(unit_dict[var]), y_text, title)
            self.figures.append(PlotlyFigure(label=title, figure=fig.to_plotly_json()))

        if self.results[0].products[0].selectivity:
            fig0 = go.Figure()
            for i, c in enumerate(self.results[0].products):
                fig0.add_trace(
                    go.Scatter(
                        x=x,
                        y=self.results[0].products[i].selectivity,
                        name=self.results[0].products[i].name,
                    )
                )
            fig0.update_layout(title_text='Selectivity', showlegend=True)
            fig0.update_xaxes(title_text=x_text)
            fig0.update_yaxes(title_text='Selectivity (%)')
            self.figures.append(
                PlotlyFigure(label='Selectivity', figure=fig0.to_plotly_json())
            )
        fig1 = self.conversion_plot(x, x_text, logger)
        if fig1 is not None:
            self.figures.append(
                PlotlyFigure(label='Conversion', figure=fig1.to_plotly_json())
            )

        if self.results[0].rates:
            fig = go.Figure()
            for i, c in enumerate(self.results[0].rates):
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=self.results[0].rates[i].rate,
                        name=self.results[0].rates[i].name,
                    )
                )
            fig.update_layout(title_text='Rates', showlegend=True)
            fig.update_xaxes(title_text=x_text)
            fig.update_yaxes(title_text='rates (g product/g cat/h)')
            self.figures.append(
                PlotlyFigure(label='Rates', figure=fig.to_plotly_json())
            )
        if not self.results[0].reactants_conversions:
            return
        if self.results[0].reactants_conversions[0].conversion and (
            self.results[0].products[0].selectivity
        ):
            for i, c in enumerate(self.results[0].reactants_conversions):
                name = self.results[0].reactants_conversions[i].name
                fig = go.Figure()
                for j, p in enumerate(self.results[0].products):
                    fig.add_trace(
                        go.Scatter(
                            x=self.results[0].reactants_conversions[i].conversion,
                            y=self.results[0].products[j].selectivity,
                            name=self.results[0].products[j].name,
                            mode='markers',
                        )
                    )
                fig.update_layout(title_text='S-X plot ' + str(i), showlegend=True)
                fig.update_xaxes(title_text=name + ' Conversion (%)')
                fig.update_yaxes(title_text='Selectivity (%)')
                self.figures.append(
                    PlotlyFigure(
                        label='S-X plot ' + name + ' Conversion',
                        figure=fig.to_plotly_json(),
                    )
                )

    def normalize_reaction_conditions(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        if self.reaction_conditions is not None:
            reagents = []
            for reagent in self.reaction_conditions.reagents:
                if reagent.pure_component is None or reagent.pure_component == []:
                    reagent.normalize(archive, logger)
                reagents.append(reagent)
            self.reaction_conditions.reagents = reagents

            if self.reactor_filling is not None:
                if (
                    self.reaction_conditions.set_total_flow_rate is not None
                    and self.reactor_filling.catalyst_mass is not None
                    and self.reaction_conditions.weight_hourly_space_velocity is None
                ):
                    self.reaction_conditions.weight_hourly_space_velocity = (
                        self.reaction_conditions.set_total_flow_rate
                        / self.reactor_filling.catalyst_mass
                    )

    def return_conversion_results(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        """
        This function returns the conversion results of the reactants for the results
        section of the archive.
        It checks if the the name of the reactant is not in the list of the inert gases
        and if the name is in the list of the reaction_conditions.reagents, it will try
        to replace the name of the reactant with the IUPAC name of the reagent.

        return: a list of the reactants with the conversion results.
        """
        if self.results[0].reactants_conversions is not None:
            conversions_results = []
            for i in self.results[0].reactants_conversions:
                if i.name in ['He', 'helium', 'Ar', 'argon', 'inert']:
                    continue
                else:
                    for j in self.reaction_conditions.reagents:
                        if i.name == j.name:
                            if j.pure_component.iupac_name is not None:
                                i.name = j.pure_component.iupac_name
                            if i.gas_concentration_in is None:
                                i.gas_concentration_in = j.gas_concentration_in
                            react = Reactant(
                                name=i.name,
                                conversion=i.conversion,
                                gas_concentration_in=i.gas_concentration_in,
                                gas_concentration_out=i.gas_concentration_out,
                            )
                            conversions_results.append(react)
                            if (
                                np.allclose(
                                    i.gas_concentration_in, j.gas_concentration_in
                                )
                                is False
                            ):
                                logger.warn(f"""Gas concentration of '{i.name}' is not
                                            the same in reaction_conditions and
                                            results.reactants_conversions.""")
        return conversions_results

    def check_sample(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if self.samples:
            if self.samples[0].lab_id is not None and self.samples[0].reference is None:
                sample = CompositeSystemReference(
                    lab_id=self.samples[0].lab_id, name=self.samples[0].name
                )
                sample.normalize(archive, logger)
                self.samples = []
                self.samples.append(sample)
            if self.samples[0].reference is not None:
                self.populate_catalyst_sample_info(archive, logger)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        self.normalize_reaction_conditions(archive, logger)

        self.populate_reactivity_info(archive, logger)
        self.check_sample(archive, logger)

        if self.results is None or self.results == []:
            return

        self.results[0].normalize(archive, logger)
        if len(self.results) > 1:
            logger.warn(
                """Several instances of results found. Only the first result
                is considered for normalization."""
            )
        conversions_results = self.return_conversion_results(archive, logger)

        product_results = []
        if self.results[0].products is not None:
            for i in self.results[0].products:
                if i.pure_component is not None:
                    if i.pure_component.iupac_name is not None:
                        i.name = i.pure_component.iupac_name
                prod = Product(
                    name=i.name,
                    selectivity=i.selectivity,
                    gas_concentration_out=i.gas_concentration_out,
                )
                product_results.append(prod)

        add_activity(archive)

        set_nested_attr(
            archive.results.properties.catalytic.reaction,
            'reactants',
            conversions_results,
        )
        set_nested_attr(
            archive.results.properties.catalytic.reaction, 'products', product_results
        )

        self.plot_figures(archive, logger)
