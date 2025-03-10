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
    InstrumentReference,
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
    Rate,
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
from nomad.units import ureg

from .chemical_data import chemical_data

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


threshold_datapoints = 300
threshold2_datapoints = 3000


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
    if not archive.results.material:
        archive.results.material = Material()


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
        if isinstance(obj, list):  # needed for repeating subsection, e.g. results
            if obj == []:
                return None
            from nomad.metainfo.metainfo import MSection

            if isinstance(obj[0], MSection):
                obj = obj[0]  ## only first element is considered for subsections
            else:  # but whole list for list quantities
                return obj
    return obj


def set_nested_attr(obj, attr_path, value):
    """helper function to set nested attributes"""
    attrs = attr_path.split('.')
    for attr in attrs[:-1]:
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    setattr(obj, attrs[-1], value)


def map_and_assign_attributes(self, logger, mapping, target, obj=None) -> None:
    """
    A helper function that loops through a mapping and assigns the values to
    a target object.
    Args:
        mapping (dict): a dictionary with the mapping of the attributes.
        target (object): the target object to which the attributes are assigned.
        obj (object): the object from which the attributes are copied. By default if
        None is defined, it will be set to self, but can also be a linked sample.
    """
    if obj is None:
        obj = self
    for ref_attr, reaction_attr in mapping.items():
        value = get_nested_attr(obj, ref_attr)
        if value is not None:
            try:
                if len(value) > threshold_datapoints:
                    logger.info(
                        f"""The quantity '{ref_attr}' is large and will be reduced for
                        the archive results."""
                    )
                    if threshold_datapoints < len(value) < threshold2_datapoints:
                        value = value[20::10]
                    else:
                        value = value[50::100]
            except TypeError:
                pass
            try:
                set_nested_attr(
                    target,
                    reaction_attr,
                    value,
                )
                logger.info(f""" Mapped attribute '{ref_attr}' into results.""")
            except ValueError:  # workaround for wrong type in yaml schema
                set_nested_attr(
                    target,
                    reaction_attr,
                    [value],
                )


threshold_conc = 1.1


def check_if_concentration_in_percentage(self, conc_array, logger) -> None:
    if conc_array is not None and any(y > threshold_conc for y in conc_array):
        logger.error(
            f'Gas concentration for reagent "{self.name}" is above 1, '
            f'but should be given as fraction.'
        )


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
                    'Fourier Transform Infrared Spectroscopy (FTIR) of adsorbates',
                    'unknown',
                ]
            ),
        ),
    )

    dispersion = Quantity(
        type=np.float64,
        shape=[],
        description="""
        The fraction of total atoms which are surface atoms of a particle as a measure
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
        links=['https://w3id.org/nfdi4cat/voc4cat_0007003'],
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

    support = Quantity(
        type=str,
        shape=[],
        description="""
          The material that the active phase is supported on.
          """,
        a_eln=dict(
            component='StringEditQuantity',
        ),
        links=['https://w3id.org/nfdi4cat/voc4cat_0007034'],
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

        add_catalyst(archive)
        quantities_results_mapping = {
            'name': 'catalyst_name',
            'catalyst_type': 'catalyst_type',
            'support': 'support',
            'preparation_details.preparation_method': 'preparation_method',
            'surface.surface_area': 'surface_area',
            'surface.method_surface_area_determination': 'characterization_methods',
        }
        map_and_assign_attributes(
            self,
            logger,
            mapping=quantities_results_mapping,
            target=archive.results.properties.catalytic.catalyst,
        )

        name_material_mapping = {'name': 'material_name'}
        map_and_assign_attributes(
            self,
            logger,
            mapping=name_material_mapping,
            target=archive.results.material,
        )

    def add_referencing_methods(
        self, archive: 'EntryArchive', logger: 'BoundLogger', number=10
    ) -> None:
        """
        This function looks for other entries that reference the sample and checks the
        results.eln.method of the entry and if it finds a methods other than
        ELNMeasurement or Root, it adds this method to characterization_methods in
        the results section of the sample entry.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger('Bound Logger'): A structlog logger.
            number: specifies the number of referencing entries that are checked,
            set to 10 by default
        """

        if self.lab_id is None:
            logger.warning("""Sample contains no lab_id, automatic linking of
                         measurements to this sample entry might be more difficult.""")

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
                    if entry['results']['eln']['methods'][0] == 'Root' and (
                        len(entry['results']['eln']['methods']) > 1
                    ):
                        method = entry['results']['eln']['methods'][1]
                    else:
                        method = entry['results']['eln']['methods'][0]
                else:
                    method = entry['entry_type']
                methods.append(method)

            if search_result.pagination.total > number:
                logger.warning(
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
            logger.warning(
                f'''Found no activity entries referencing this entry
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
        description='A reference to the sample reference used in the measurement.',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
        ),
    )

    catalyst_mass = Quantity(
        type=np.float64,
        shape=[],
        unit='kg',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mg'),
    )

    catalyst_density = Quantity(
        type=np.float64,
        shape=[],
        unit='kg/m**3',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='g/mL'),
    )

    catalyst_volume = Quantity(
        type=np.float64,
        shape=[],
        unit='m**3',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mL'),
    )

    catalyst_sievefraction_upper_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='m',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )
    catalyst_sievefraction_lower_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='m',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )
    particle_size = Quantity(
        type=np.float64,
        shape=[],
        unit='m',
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

    diluent_mass = Quantity(
        type=np.float64,
        shape=[],
        unit='kg',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mg'),
    )

    diluent_sievefraction_upper_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='m',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )
    diluent_sievefraction_lower_limit = Quantity(
        type=np.float64,
        shape=[],
        unit='m',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='micrometer'),
    )

    def normalize(self, archive, logger):
        """The normalizer for the `ReactorFilling` class. It links the catalyst if a
        sample was referenced in the sample subsection of the entry and
        fills the catalyst name from the sample subsection.
        If catalyst mass and density are given, the catalyst volume is calculated.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger ('BoundLogger'): A structlog logger.
        """

        super().normalize(archive, logger)

        if self.sample_section_reference is None:
            if self.m_root().data.samples:
                pass  # does not seem to work, how can I reference the first sample?
                # first_sample = self.m_root().data.samples[0]
                # if hasattr(first_sample, 'reference'):
                # self.sample_section_reference = '#/data/samples[0]'

        if self.catalyst_name is None and self.sample_section_reference is not None:
            self.catalyst_name = self.sample_section_reference.name

        if (
            self.catalyst_volume is None
            and self.catalyst_mass is not None
            and self.catalyst_density is not None
        ):
            self.catalyst_volume = self.catalyst_mass / self.catalyst_density


class ReactorSetup(InstrumentReference):
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
        unit='m',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    reactor_cross_section_area = Quantity(
        type=np.float64,
        shape=[],
        unit='m**2',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mm**2'),
    )

    reactor_diameter = Quantity(
        type=np.float64,
        shape=[],
        unit='m',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='mm'),
    )

    reactor_volume = Quantity(
        type=np.float64,
        shape=[],
        unit='m**3',
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
    fraction_in = Quantity(
        type=np.float64,
        shape=['*'],
        description="""Volumetric fraction of reactant in feed. The value must be
        between 0 and 1.""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    flow_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='m**3/s',
        description='Flow rate of reactant in feed.',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mL/minute'
        ),
    )
    partial_pressure_in = Quantity(
        type=np.float64,
        shape=['*'],
        unit='Pa',
        description='Partial pressure of reactant in initial reaction mixture.',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='bar'),
    )

    pure_component = SubSection(section_def=PubChemPureSubstanceSection)

    def update_chemical_info(self):
        """
        This function mapps the chemical information of the reagent from a local
        dictionary chemical data and returns a pure_component object.
        """

        # Resolve aliases to primary keys if necessary
        chemical_key = chemical_data.get(self.name)
        # If the value is a string, it refers to another key, so resolve it
        if isinstance(chemical_key, str):
            chemical_key = chemical_data[chemical_key]
        # If the value is not a string or a dictionary, it is not in the database, try
        # to resolve it by removing capital letters
        elif not isinstance(chemical_key, dict):
            chemical_key = chemical_data.get(self.name.lower())
            if isinstance(chemical_key, str):
                chemical_key = chemical_data[chemical_key]
        pure_component = PubChemPureSubstanceSection()
        pure_component.name = self.name
        if chemical_key:
            pure_component.pub_chem_cid = chemical_key.get('pub_chem_id')
            pure_component.iupac_name = chemical_key.get('iupac_name')
            pure_component.molecular_formula = chemical_key.get('molecular_formula')
            pure_component.molecular_mass = chemical_key.get('molecular_mass')
            pure_component.inchi = chemical_key.get('inchi', None)  # Optional
            pure_component.inchi_key = chemical_key.get('inchi_key', None)  # Optional
            pure_component.cas_number = chemical_key.get('cas_number', None)  # Optional

        return pure_component

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
        # super().normalize(archive, logger)

        check_if_concentration_in_percentage(self, self.fraction_in, logger)
        try:
            if (
                self.fraction_in is None
                and self.flow_rate is not None
                and self.m_parent is not None
                and getattr(self.m_parent, 'set_total_flow_rate', None) is not None
            ):
                total_flow = getattr(self.m_parent, 'set_total_flow_rate', None)
                self.fraction_in = self.flow_rate / total_flow
        except (
            TypeError,
            ValueError,
        ) as e:  # because truth value of array is ambiguous
            logger.info(
                f'Could not calculate fraction_in for reagent {self.name} '
                f'from flow rate and total flow rate. Error: {e}'
            )
        if self.name is None:
            return
        if self.name in ['C5-1', 'C6-1', 'nC5', 'nC6', 'Unknown', 'inert', 'P>=5C']:
            return
        elif '_' in self.name:
            self.name = self.name.replace('_', ' ')

        if self.name and (
            self.pure_component is None or self.pure_component.iupac_name is None
        ):
            pure_component = self.update_chemical_info()
            self.pure_component = pure_component

            if self.pure_component.iupac_name:
                logger.info(f'found {self.name} in chemical_data, no pubchem call made')
                return
            else:
                import random
                import time

                time.sleep(random.uniform(0.5, 5))
                self.pure_component.normalize(archive, logger)

        if self.name is None and self.pure_component is not None:
            self.name = self.pure_component.iupac_name


class ReactantData(Reagent):
    m_def = Section(
        label_quantity='name',
        description='A reagent that has a conversion in a reaction that is not null',
    )

    fraction_out = Quantity(
        type=np.float64,
        shape=['*'],
        description="""Volumetric fraction of reactant in outlet. The value must be
        between 0 and 1""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    reference = Quantity(type=Reagent, a_eln=dict(component='ReferenceEditQuantity'))
    conversion = Quantity(
        type=np.float64,
        shape=['*'],
        description="""The conversion of the reactant in the reaction mixture.
        The value is in %""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
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
        a_eln=ELNAnnotation(defaultDisplayUnit='mmol/g/hour'),
    )

    specific_mass_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mmol/g/hour',
        description="""
        The specific reaction rate normalized by active (metal) catalyst mass, instead
        of mass of total catalyst.
        """,
        a_eln=ELNAnnotation(defaultDisplayUnit='mmol/g/hour'),
    )

    specific_surface_area_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='mmol/m**2/hour',
        description="""
        The specific reaction rate normalized by active (metal) surface area of
        catalyst, instead of mass of total catalyst.
        """,
        a_eln=ELNAnnotation(defaultDisplayUnit='mmol/m**2/hour'),
    )

    rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='g/g/hour',
        description="""
        The amount of reactant converted (in g), per total catalyst (g) per time (hour).
        """,
        a_eln=ELNAnnotation(defaultDisplayUnit='g/g/hour'),
    )

    turn_over_frequency = Quantity(
        type=np.float64,
        shape=['*'],
        unit='1/hour',
        description="""
        The turn oder frequency, calculated from mol of reactant or product, per number
        of sites, over time.
        """,
        a_eln=ELNAnnotation(defaultDisplayUnit='1/hour'),
    )


class ProductData(Reagent):
    m_def = Section(
        label_quantity='name',
        description="""
        A chemical substance formed in the reaction mixture during a reaction.""",
    )

    fraction_out = Quantity(
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
        links=['https://w3id.org/nfdi4cat/voc4cat_0000125'],
    )

    product_yield = Quantity(
        type=np.float64,
        shape=['*'],
        description="""
        The yield of the product in the reaction mixture, calculated as
        conversion * selectivity.""",
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    space_time_yield = Quantity(
        type=np.float64,
        shape=['*'],
        unit='1/s',
        description="""
        The amount of product formed (in g), per total catalyst (g) per time (s).
        """,
        links=['https://w3id.org/nfdi4cat/voc4cat_0005006'],
        a_eln=ELNAnnotation(defaultDisplayUnit='g/g/hour'),
    )

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


class ReactionConditionsData(PlotSection):
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
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='bar'),
    )

    set_total_flow_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='m**3/s',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mL/minute'
        ),
    )

    weight_hourly_space_velocity = Quantity(
        description=""" A measure for how often the atmosphere in the reactor is
        replaced over the catalyst. Calculated as the total flow rate divided by the
        catalyst mass.""",
        type=np.float64,
        shape=['*'],
        unit='m**3/(kg*s)',
        a_eln=dict(defaultDisplayUnit='mL/(g*hour)'),
    )

    contact_time = Quantity(
        description="""The time the reactants are in contact with the catalyst. Also
        the reciprocal of the weight hourly space velocity. Calculated as the catalyst
        mass divided by the total flow rate.""",
        type=np.float64,
        shape=['*'],
        unit='kg*s/m**3',
        a_eln=ELNAnnotation(
            label='W|F', defaultDisplayUnit='g*s/mL', component='NumberEditQuantity'
        ),
    )

    gas_hourly_space_velocity = Quantity(
        description="""Similar to WHSV, the volumetric flow rate of the gas divided by
        the control volume. In heterogeneous catalysis the volume of the undiluted
        catalyst bed is conventionally used as the control volume.""",
        links=['https://w3id.org/nfdi4cat/voc4cat_0007023'],
        type=np.float64,
        shape=['*'],
        unit='1/s',
        a_eln=dict(defaultDisplayUnit='1/hour'),
    )

    runs = Quantity(type=np.float64, shape=['*'])

    sampling_frequency = Quantity(
        description='The number of measurement points per time.',
        links=['https://w3id.org/nfdi4cat/voc4cat_0007026'],
        type=np.float64,
        shape=[],
        unit='Hz',
        a_eln=dict(component='NumberEditQuantity'),
    )

    time_on_stream = Quantity(
        description="""The running time of the reaction since gas flow and measurement
        started.""",
        type=np.float64,
        shape=['*'],
        unit='s',
        a_eln=dict(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    reagents = SubSection(section_def=Reagent, repeats=True)

    def plot_figures(self):
        self.figures = []
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
                self.reagents[0].fraction_in is not None
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
                                    y=self.set_total_flow_rate.to('mL/minute'),
                                    name='Total Flow Rates',
                                )
                            )
                    elif self.reagents[0].fraction_in is not None:
                        fig5.add_trace(
                            go.Scatter(
                                x=x,
                                y=self.reagents[i].fraction_in,
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

        if (
            self.set_total_flow_rate is not None
            and self.m_root().data.reactor_filling is not None
            and self.m_root().data.reactor_filling.catalyst_mass is not None
            and self.weight_hourly_space_velocity is None
        ):
            self.weight_hourly_space_velocity = (
                self.set_total_flow_rate
                / self.m_root().data.reactor_filling.catalyst_mass
            )

        self.plot_figures()


class ReagentBatch(Reagent):
    m_def = Section(
        label_quantity='name',
        description='A reagent in a batch reaction.',
        a_eln={'hide': ['flow_rate']},
    )

    amount = Quantity(
        description='The amount n of the reagent in the reaction mixture in mole.',
        type=np.float64,
        shape=[],
        unit='mol',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mmol'),
        links=['https://goldbook.iupac.org/terms/view/A00297'],
    )

    mass = Quantity(
        type=np.float64,
        shape=[],
        unit='kg',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mg'),
    )

    volume = Quantity(
        type=np.float64,
        shape=[],
        unit='m**3',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='mL'),
    )


class ReactionConditionsBatchData(ReactionConditionsData):
    m_def = Section(
        description="""
        A class containing reaction conditions for a batch reaction.""",
        a_eln={
            'hide': [
                'set_total_flow_rate',
                'weight_hourly_space_velocity',
                'contact_time',
                'gas_hourly_space_velocity',
                'time_on_stream',
            ]
        },
    )

    stirring_rate = Quantity(
        type=np.float64,
        shape=[],
        unit='1/s',
        description="""The rate at which the reaction mixture is stirred. The value is
        in 1/s""",
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='1/s'),
    )

    reaction_time = Quantity(
        type=np.float64,
        shape=['*'],
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    reagents = SubSection(section_def=ReagentBatch, repeats=True)

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if self.reaction_time is not None:
            self.time_on_stream = self.reaction_time
        self.plot_figures()


class CatalyticReactionCore(Measurement):
    reaction_type = Quantity(
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


class CatalyticReactionData(PlotSection, MeasurementResult):
    temperature = Quantity(
        type=np.float64,
        shape=['*'],
        unit='K',
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    pressure = Quantity(
        type=np.float64,
        shape=['*'],
        unit='Pa',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='bar'),
    )

    total_flow_rate = Quantity(
        type=np.float64,
        shape=['*'],
        unit='m**3/s',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity', defaultDisplayUnit='mL/minute'
        ),
    )

    runs = Quantity(
        type=np.float64,
        shape=['*'],
        # a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )
    time_on_stream = Quantity(
        type=np.float64,
        shape=['*'],
        unit='s',
        a_eln=ELNAnnotation(component='NumberEditQuantity', defaultDisplayUnit='hour'),
    )

    c_balance = Quantity(
        definition="""Carbon balance is the ratio of detected carbon in the products
        to the carbon in the feed. It is a measure of the quality of the gas analysis or
        could indicate the amount of coke formation""",
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
        if self.runs is None and self.temperature is not None:
            self.runs = np.arange(1, len(self.temperature) + 1)
        
        if self.reactants_conversions is not None:
            for reactant in self.reactants_conversions:
                if (reactant.conversion is None and reactant.fraction_in is not None 
                and reactant.fraction_out is not None):
                    reactant.conversion=np.nan_to_num(
                        100 - (reactant.fraction_out / reactant.fraction_in) * 100)

class CatalyticReaction(CatalyticReactionCore, PlotSection, Schema):
    m_def = Section(
        label='Catalytic Reaction',
        description="""An activity entry containing information about a catalytic
        reaction.""",
        links=['https://w3id.org/nfdi4cat/voc4cat_0005007'],
        a_eln=ELNAnnotation(
            properties=dict(
                order=[
                    'name',
                    'data_file',
                    'reaction_name',
                    'reaction_type',
                    'experimenter',
                    'location',
                    'experiment_handbook',
                ]
            )
        ),
        categories=[CatalysisElnCategory],
    )
    data_file = Quantity(
        type=str,
        description="""
        A file that contains reaction conditions and results of a catalytic measurement.
        Supported file formats are .csv or .xlsx with columns matching the clean data
        standards and hf5 files generated by the automated haber reactor at the FHI.
        More details can be found in the documentation of the nomad-catalysis-plugin.
        """,
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )

    instruments = SubSection(
        section_def=ReactorSetup, a_eln=ELNAnnotation(label='reactor setup')
    )
    reactor_filling = SubSection(section_def=ReactorFilling)

    pretreatment = SubSection(
        section_def=ReactionConditionsData, a_eln=ELNAnnotation(label='pretreatment')
    )
    reaction_conditions = SubSection(
        section_def=ReactionConditionsData,
        a_eln=ELNAnnotation(label='reaction conditions'),
    )

    results = SubSection(
        section_def=CatalyticReactionData, a_eln=ELNAnnotation(label='reaction results')
    )

    def read_clean_data(self, archive, logger):  # noqa: PLR0912, PLR0915
        """
        This function reads the data from the data file and assigns the data to the
        corresponding attributes of the class.
        """
        if self.data_file.endswith('.csv'):
            with archive.m_context.raw_file(self.data_file, 'rt') as f:
                import pandas as pd

                data = pd.read_csv(f).dropna(axis=1, how='all')
        elif self.data_file.endswith('.xlsx'):
            with archive.m_context.raw_file(self.data_file, 'rb') as f:
                import pandas as pd

                data = pd.read_excel(f, sheet_name=0)

        data.dropna(axis=1, how='all', inplace=True)
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
        number_of_runs = 0

        for col in data.columns:
            if len(data[col]) < 2:  # noqa: PLR2004
                continue
            if col.casefold() == 'step':
                feed.runs = data['step']
                cat_data.runs = data['step']

            col_split = col.split(' ')

            if col.casefold() == 'c-balance':
                cat_data.c_balance = np.nan_to_num(data[col])

            if len(col_split) < 2:  # noqa: PLR2004
                continue

            number_of_runs = max(number_of_runs, len(data[col]))

            if col_split[0].casefold() == 'c-balance' and ('%' in col_split[1]):
                cat_data.c_balance = np.nan_to_num(data[col]) / 100

            if col_split[0].casefold() == 'x':
                if len(col_split) == 3 and ('%' in col_split[2]):  # noqa: PLR2004
                    gas_in = data[col] / 100
                else:
                    gas_in = data[col]
                reagent = Reagent(name=col_split[1], fraction_in=gas_in)
                reagent_names.append(col_split[1])
                reagents.append(reagent)

            if col_split[0].casefold() == 'mass':
                catalyst_mass_vector = data[col]
                if '(g)' in col_split[1]:
                    reactor_filling.catalyst_mass = catalyst_mass_vector[0] * ureg.gram
                elif 'mg' in col_split[1]:
                    reactor_filling.catalyst_mass = (
                        catalyst_mass_vector[0] * ureg.milligram
                    )
            if col_split[0].casefold() == 'set_temperature':
                if 'K' in col_split[1]:
                    feed.set_temperature = np.nan_to_num(data[col])
                else:
                    feed.set_temperature = np.nan_to_num(data[col]) * ureg.celsius
            if col_split[0].casefold() == 'temperature':
                if 'K' in col_split[1]:
                    cat_data.temperature = np.nan_to_num(data[col])
                else:
                    cat_data.temperature = np.nan_to_num(data[col]) * ureg.celsius

            if col_split[0].casefold() == 'tos' or col_split[0].casefold() == 'time':
                if 's' in col_split[1]:
                    cat_data.time_on_stream = np.nan_to_num(data[col]) * ureg.second
                    feed.time_on_stream = np.nan_to_num(data[col]) * ureg.second
                elif 'min' in col_split[1]:
                    cat_data.time_on_stream = np.nan_to_num(data[col]) * ureg.minute
                    feed.time_on_stream = np.nan_to_num(data[col]) * ureg.minute
                elif 'h' in col_split[1]:
                    cat_data.time_on_stream = np.nan_to_num(data[col]) * ureg.hour
                    feed.time_on_stream = np.nan_to_num(data[col]) * ureg.hour
                else:
                    logger.warning('Time on stream unit not recognized.')

            if col_split[0] == 'GHSV':
                if '1/h' in col_split[1] or 'h^-1' in col_split[1]:
                    feed.gas_hourly_space_velocity = (
                        np.nan_to_num(data[col]) * ureg.hour**-1
                    )
                else:
                    logger.warning('Gas hourly space velocity unit not recognized.')

            if col_split[0] == 'Vflow' or col_split[0] == 'flow_rate':
                if 'mL/min' in col_split[1] or 'mln' in col_split[1]:
                    feed.set_total_flow_rate = (
                        np.nan_to_num(data[col]) * ureg.milliliter / ureg.minute
                    )

            if col_split[0] == 'set_pressure':
                feed.set_pressure = np.nan_to_num(data[col]) * ureg.bar
            if col_split[0].casefold() == 'pressure':
                cat_data.pressure = np.nan_to_num(data[col]) * ureg.bar

            if len(col_split) < 3:  # noqa: PLR2004
                continue

            if col_split[0] == 'r':  # reaction rate
                unit = col_split[2].strip('()')
                unit_conversion={
                    'mmol/g/h': 'mmol / (g * hour)',
                    'mmol/g/min': 'mmol / (g * minute)',
                    'µmol/g/min': 'µmol / (g * minute)',
                    'mmolg^-1h^-1': 'mmol / (g * hour)',
                }
                try:
                    rate = RatesData(
                        name=col_split[1], 
                        reaction_rate=ureg.Quantity(np.nan_to_num(data[col]),
                                                    unit_conversion.get(unit,unit))
                    )
                except Exception as e:
                    logger.warning(f'''Reaction rate unit {unit} not recognized. 
                                   Error: {e}''')
                rates.append(rate)

            if col_split[2] != '(%)':
                continue

            if col_split[0] == 'x_p':  # conversion, based on product detection
                conversion = ReactantData(
                    name=col_split[1],
                    conversion=np.nan_to_num(data[col]),
                    conversion_type='product-based conversion',
                    conversion_product_based=np.nan_to_num(data[col]),
                )
                for i, p in enumerate(conversions):
                    if p.name == col_split[1]:
                        conversion = conversions.pop(i)

                conversion.conversion_product_based = np.nan_to_num(data[col])
                conversion.conversion = np.nan_to_num(data[col])
                conversion.conversion_type = 'product-based conversion'

                conversion_names.append(col_split[1])
                conversions.append(conversion)

            if col_split[0] == 'x_r':  # conversion, based on reactant detection
                try:
                    conversion = ReactantData(
                        name=col_split[1],
                        conversion=np.nan_to_num(data[col]),
                        conversion_type='reactant-based conversion',
                        conversion_reactant_based=np.nan_to_num(data[col]),
                        fraction_in=(
                            np.nan_to_num(data['x ' + col_split[1] + ' (%)']) / 100
                        ),
                    )
                except KeyError:
                    conversion = ReactantData(
                        name=col_split[1],
                        conversion=np.nan_to_num(data[col]),
                        conversion_type='reactant-based conversion',
                        conversion_reactant_based=np.nan_to_num(data[col]),
                        fraction_in=np.nan_to_num(data['x ' + col_split[1]]),
                    )

                for i, p in enumerate(conversions):
                    if p.name == col_split[1]:
                        conversion = conversions.pop(i)
                        conversion.conversion_reactant_based = np.nan_to_num(data[col])
                conversions.append(conversion)

            if col_split[0].casefold() == 'x_out':  # concentration out
                if col_split[1] in reagent_names:
                    conversion = ReactantData(
                        name=col_split[1],
                        fraction_in=np.nan_to_num(data['x ' + col_split[1] + ' (%)'])
                        / 100,
                        fraction_out=np.nan_to_num(data[col]) / 100,
                    )
                    conversions.append(conversion)
                else:
                    product = ProductData(
                        name=col_split[1],
                        fraction_out=np.nan_to_num(data[col]) / 100,
                    )
                    products.append(product)
                    product_names.append(col_split[1])

            if col_split[0] == 'S_p':  # selectivity
                product = ProductData(
                    name=col_split[1], selectivity=np.nan_to_num(data[col])
                )
                for i, p in enumerate(products):
                    if p.name == col_split[1]:
                        product = products.pop(i)
                        product.selectivity = np.nan_to_num(data[col])
                        break
                products.append(product)
                product_names.append(col_split[1])
            
            if col_split[0].casefold() == 'y':  # product yield
                product = ProductData(
                    name=col_split[1], product_yield=np.nan_to_num(data[col])
                )
                for i, p in enumerate(products):
                    if p.name == col_split[1]:
                        product = products.pop(i)
                        product.product_yield = np.nan_to_num(data[col])
                        break
                products.append(product)
                product_names.append(col_split[1])

        if 'FHI-ID' in data.columns:
            sample.lab_id = str(data['FHI-ID'][0])
        elif 'sample_id' in data.columns:  # is not None:
            sample.lab_id = str(data['sample_id'][0])
        if 'catalyst' in data.columns:  # is not None:
            sample.name = str(data['catalyst'][0])
            reactor_filling.catalyst_name = str(data['catalyst'][0])
        if 'reaction_name' in data.columns:
            self.reaction_name = str(data['reaction_name'][0])
        if 'reaction_type' in data.columns:
            self.reaction_type = str(data['reaction_type'][0])
        if 'experimenter' in data.columns:
            self.experimenter = str(data['experimenter'][0])
        if 'location' in data.columns:
            self.location = str(data['location'][0])

        if (
            (self.samples is None or self.samples == [])
            and sample != []
            and sample is not None
        ):
            from nomad.datamodel.context import ClientContext

            if isinstance(archive.m_context, ClientContext):
                pass
            else:
                sample.normalize(archive, logger)
            samples = []
            samples.append(sample)
            self.samples = samples

        for n, reagent in enumerate(reagents):
            if (
                self.reaction_conditions is not None
                and self.reaction_conditions.reagents is not None
                and self.reaction_conditions.reagents != []
                and self.reaction_conditions.reagents[n].pure_component is not None
                and self.reaction_conditions.reagents[n].pure_component.iupac_name
                is not None
            ):
                continue
            reagent.normalize(archive, logger)
        feed.reagents = reagents

        if cat_data.runs is None:
            cat_data.runs = np.linspace(0, number_of_runs - 1, number_of_runs)
        cat_data.products = products
        if conversions != []:
            cat_data.reactants_conversions = conversions
        cat_data.rates = rates

        self.reaction_conditions = feed
        self.results = []
        self.results.append(cat_data)

        if self.reactor_filling is None and reactor_filling is not None:
            self.reactor_filling = reactor_filling

    def read_haber_data(self, archive, logger):  # noqa: PLR0912, PLR0915
        """
        This function reads the h5 data from the data file and assigns the data to the
        corresponding attributes of the class.
        """
        if self.data_file.endswith('.h5'):
            with archive.m_context.raw_file(self.data_file, 'rb') as f:
                import h5py

                data = h5py.File(f, 'r')

                cat_data = CatalyticReactionData()
                feed = ReactionConditionsData()
                reactor_setup = ReactorSetup()
                reactor_filling = ReactorFilling()
                pretreatment = ReactionConditionsData()
                sample = CompositeSystemReference()
                conversions = []
                rates = []
                reagents = []
                pre_reagents = []
                time_on_stream = []
                time_on_stream_reaction = []
                method = list(data['Sorted Data'].keys())
                for i in method:
                    methodname = i
                header = data['Header'][methodname]['Header']
                feed.sampling_frequency = (
                    header['Temporal resolution [Hz]'] * ureg.hertz
                )
                reactor_setup.name = 'Haber'
                reactor_setup.reactor_type = 'plug flow reactor'
                reactor_setup.reactor_volume = header['Bulk volume [mln]']
                reactor_setup.reactor_cross_section_area = (
                    header['Inner diameter of reactor (D) [mm]'] * ureg.millimeter / 2
                ) ** 2 * np.pi
                reactor_setup.reactor_diameter = (
                    header['Inner diameter of reactor (D) [mm]'] * ureg.millimeter
                )
                reactor_filling.diluent = header['Diluent material'][0].decode()
                reactor_filling.diluent_sievefraction_upper_limit = (
                    header['Diluent Sieve fraction high [um]'] * ureg.micrometer
                )
                reactor_filling.diluent_sievefraction_lower_limit = (
                    header['Diluent Sieve fraction low [um]'] * ureg.micrometer
                )
                reactor_filling.catalyst_mass = (
                    header['Catalyst Mass [mg]'][0] * ureg.milligram
                )
                reactor_filling.catalyst_sievefraction_upper_limit = (
                    header['Sieve fraction high [um]'] * ureg.micrometer
                )
                reactor_filling.catalyst_sievefraction_lower_limit = (
                    header['Sieve fraction low [um]'] * ureg.micrometer
                )
                reactor_filling.particle_size = (
                    header['Particle size (Dp) [mm]'] * ureg.millimeter
                )

                if not self.experimenter:
                    self.experimenter = header['User'][0].decode()

                pre = data['Sorted Data'][methodname]['H2 Reduction']
                pretreatment.set_temperature = (
                    pre['Catalyst Temperature [C°]'] * ureg.celsius
                )
                for col in pre.dtype.names:
                    if (
                        col
                        == 'Massflow3 (H2) Target Calculated Realtime Value [mln|min]'
                    ):
                        pre_reagent = Reagent(
                            name='hydrogen',
                            flow_rate=pre[col] * ureg.milliliter / ureg.minute,
                        )
                        pre_reagents.append(pre_reagent)
                    if (
                        col
                        == 'Massflow5 (Ar) Target Calculated Realtime Value [mln|min]'
                    ):
                        pre_reagent = Reagent(
                            name='argon',
                            flow_rate=pre[col] * ureg.milliliter / ureg.minute,
                        )
                        pre_reagents.append(pre_reagent)

                pretreatment.reagents = pre_reagents
                pretreatment.set_total_flow_rate = (
                    pre['Target Total Gas (After Reactor) [mln|min]']
                    * ureg.milliliter
                    / ureg.minute
                )
                number_of_runs = len(pre['Catalyst Temperature [C°]'])
                pretreatment.runs = np.linspace(0, number_of_runs - 1, number_of_runs)

                time = pre['Relative Time [Seconds]']
                for i in range(len(time)):
                    t = float(time[i].decode('UTF-8')) - float(time[0].decode('UTF-8'))
                    time_on_stream.append(t)
                pretreatment.time_on_stream = time_on_stream * ureg.sec

                analysed = data['Sorted Data'][methodname]['NH3 Decomposition']

                set_total_flow = np.zeros(len(analysed['Relative Time [Seconds]']))
                for col in analysed.dtype.names:
                    if col.endswith('Target Calculated Realtime Value [mln|min]'):
                        name_split = col.split('(')
                        gas_name = name_split[1].split(')')
                        if 'NH3_High' in gas_name or 'NH3_Low' in gas_name:
                            reagent = Reagent(
                                name='ammonia',
                                flow_rate=analysed[col] * ureg.milliliter / ureg.minute,
                                fraction_in=[1.0] * len(analysed[col]),
                            )
                            if reagent.flow_rate.any() > 0.0:
                                reagents.append(reagent)
                        else:
                            reagent = Reagent(
                                name=gas_name[0],
                                flow_rate=analysed[col] * ureg.milliliter / ureg.minute,
                            )
                            if reagent.flow_rate.any() > 0.0:
                                reagents.append(reagent)
                    if col.endswith('Target Setpoint [mln|min]'):
                        set_total_flow += analysed[col] * ureg.milliliter / ureg.minute

                feed.reagents = reagents
                total_flow_rate = np.zeros(len(reagents[0].flow_rate))
                for reagent in reagents:
                    total_flow_rate += reagent.flow_rate
                cat_data.total_flow_rate = total_flow_rate

                feed.set_total_flow_rate = set_total_flow
                feed.contact_time = (
                    analysed['W|F [gs|ml]'] * ureg.second * ureg.gram / ureg.milliliter
                )
                conversion = ReactantData(
                    name='ammonia',
                    conversion=np.nan_to_num(analysed['NH3 Conversion [%]']),
                    conversion_type='reactant-based conversion',
                    fraction_in=[1] * len(analysed['NH3 Conversion [%]']),
                )
                conversions.append(conversion)

                rate = RatesData(
                    name='molecular hydrogen',
                    reaction_rate=np.nan_to_num(
                        analysed['Space Time Yield [mmolH2 gcat-1 min-1]']
                        * ureg.mmol
                        / ureg.g
                        / ureg.minute
                    ),
                )
                rates.append(rate)
                feed.set_temperature = (
                    analysed['Catalyst Temperature [C°]'] * ureg.celsius
                )
                cat_data.temperature = (
                    analysed['Catalyst Temperature [C°]'] * ureg.celsius
                )
                number_of_runs = len(analysed['NH3 Conversion [%]'])
                feed.runs = np.linspace(0, number_of_runs - 1, number_of_runs)
                cat_data.runs = np.linspace(0, number_of_runs - 1, number_of_runs)
                time = analysed['Relative Time [Seconds]']
                for i in range(len(time)):
                    t = float(time[i].decode('UTF-8')) - float(time[0].decode('UTF-8'))
                    time_on_stream_reaction.append(t)
                cat_data.time_on_stream = time_on_stream_reaction * ureg.sec

                cat_data.reactants_conversions = conversions
                cat_data.rates = rates

                self.method = 'Haber measurement ' + str(methodname)
                self.datetime = pre['Date'][0].decode()

                # sample.name = 'catalyst'
                sample.lab_id = str(data['Header']['Header']['SampleID'][0])
                from nomad.datamodel.context import ClientContext

                if isinstance(archive.m_context, ClientContext):
                    pass
                else:
                    sample.normalize(archive, logger)
                    self.samples = []
                    self.samples.append(sample)

                self.results = []
                self.results.append(cat_data)
                self.reaction_conditions = feed
                self.instruments = []
                self.instruments.append(reactor_setup)
                self.pretreatment = pretreatment
                self.reactor_filling = reactor_filling

                products_results = []
                for i in ['molecular nitrogen', 'molecular hydrogen']:
                    product = ProductData(name=i)
                    products_results.append(product)
                self.results[0].products = products_results

                self.reaction_name = 'ammonia decomposition'
                self.reaction_type = 'cracking'
                self.location = 'Fritz-Haber-Institut Berlin / Abteilung AC'

    def check_and_read_data_file(self, archive, logger):
        """This functions checks the format of the data file and assigns the right
        reader function to read the data file or logs a warning if the format is not
        supported.
        """
        if self.data_file is None:
            logger.warning('No data file found.')
            return

        if self.data_file.endswith('.csv') or self.data_file.endswith('.xlsx'):
            self.read_clean_data(archive, logger)
        elif self.data_file.endswith('.h5'):
            if self.data_file.endswith('NH3_Decomposition.h5'):
                self.read_haber_data(archive, logger)
            else:
                try:
                    self.read_haber_data(archive, logger)
                except KeyError:
                    logger.warning(
                        """No data is extracted from this h5 data file as the file is
                        either missing or the format is not (yet) supported.
                        This file contains a different data
                        structure or object names from currently supported h5 files for
                        catalysis. Please check if you can modify the structure or
                        contact the plugin developers if you want to add support for
                        this."""
                    )
        else:
            logger.warning(
                """Data file format not supported. No data is extracted from the
                provided file. Please provide a standadized .csv, .xlsx or .h5 file,
                if you want direct data extraction into the schema."""
            )
            return

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
            'results.temperature': 'reaction_conditions.temperature',
            'results.pressure': 'reaction_conditions.pressure',
            'results.total_flow_rate': 'reaction_conditions.flow_rate',
            'results.time_on_stream': 'reaction_conditions.time_on_stream',
            'reaction_name': 'name',
            'reaction_type': 'type',
        }

        map_and_assign_attributes(
            self,
            logger,
            mapping=quantities_results_mapping,
            target=archive.results.properties.catalytic.reaction,
        )

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
            'support': 'support',
            'preparation_details.preparation_method': 'preparation_method',
            'surface.surface_area': 'surface_area',
        }
        map_and_assign_attributes(
            self,
            logger,
            mapping=quantities_results_mapping,
            obj=sample_obj,
            target=archive.results.properties.catalytic.catalyst,
        )

        if self.samples[0].reference.name is not None:
            if not archive.results.material:
                archive.results.material = Material()
            name_comb = ''
            for i in self.samples:
                if i.reference.name is not None:
                    if len(name_comb) != 0:
                        name_comb += '/ '
                    name_comb += str(i.reference.name)
            archive.results.material.material_name = name_comb
            # archive.results.material.material_name = self.samples[0].reference.name

        if self.samples[0].reference.elemental_composition is not None:
            if not archive.results.material:
                archive.results.material = Material()

            archive.results.material.elemental_composition = self.samples[
                0
            ].reference.elemental_composition

        for i in self.samples[0].reference.elemental_composition:
            if i.element not in chemical_symbols:
                logger.warning(
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
            return y, var.replace('_', ' ')
        y = get_nested_attr(self.reaction_conditions, plot_quantities_dict[var])
        if y is not None:
            return y, var.replace('_', ' ')
        y = get_nested_attr(
            self.reaction_conditions, 'set_' + plot_quantities_dict[var]
        )
        if y is not None:
            return y, 'Set ' + var.replace('_', ' ')
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
            logger.warning('no conversion data found, so no plot is created')
            return
        if self.results[0].reactants_conversions[0].conversion is None:
            logger.warning('no conversion data found, so no plot is created')
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

    def make_rates_plot(self, x, x_text):
        rates_list = [
            'reaction_rate',
            'rate',
            'specific_mass_rate',
            'specific_surface_area_rate',
            'turnover_frequency',
        ]
        rates_units = {
            'reaction_rate': ['mmol reagent/g_cat/h', 'mmol/g/hour'],
            'rate': ['g reagent/g_cat/h', '1/hour'],
            'specific_mass_rate': ['mmol reagent/g_cat/h', '1/hour'],
            'specific_surface_area_rate': [
                'mmol reagent/m**2 cat/h',
                'mmol/m**2/hour',
            ],
            'turnover_frequency': ['1/h', '1/hour'],
        }
        previous_rate = []

        fig = go.Figure()
        for i, c in enumerate(self.results[0].rates):
            if i == 0:
                for rate_str in rates_list:
                    y, y_text = self.get_y_data(
                        {rate_str: 'rates.' + rate_str}, rate_str
                    )
                    if y is not None:
                        y.to(rates_units[rate_str][1])
                        fig.add_trace(
                            go.Scatter(
                                x=x,
                                y=y,
                                name=self.results[0].rates[i].name,
                            )
                        )
                        y_text = y_text + ' (' + rates_units[rate_str][0] + ')'
                        previous_rate = rate_str
                        break
            else:
                y = getattr(self.results[0].rates[i], previous_rate)
                if y is not None:
                    y.to(rates_units[previous_rate][1])
                    fig.add_trace(
                        go.Scatter(
                            x=x,
                            y=y,
                            name=self.results[0].rates[i].name,
                        )
                    )
        fig.update_layout(title_text='Rates', showlegend=True)
        fig.update_xaxes(title_text=x_text)
        fig.update_yaxes(title_text=y_text)
        self.figures.append(PlotlyFigure(label='Rates', figure=fig.to_plotly_json()))

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
                logger.warning(f"no '{var}' data found, so no plot is created")
                continue
            y.to(unit_dict[var])
            y_text = y_text + ' (' + unit_dict[var] + ')'
            fig = self.single_plot(x, x_text, y.to(unit_dict[var]), y_text, title)
            self.figures.append(PlotlyFigure(label=title, figure=fig.to_plotly_json()))

        fig1 = self.conversion_plot(x, x_text, logger)
        if fig1 is not None:
            self.figures.append(
                PlotlyFigure(label='Conversion', figure=fig1.to_plotly_json())
            )

        if self.results[0].rates:
            self.make_rates_plot(x, x_text)

        if not self.results[0].products:
            return
        if (
            self.results[0].products is not None
            and self.results[0].products != []
            and self.results[0].products[0].selectivity is not None
        ):
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

        if not self.results[0].reactants_conversions:
            return
        if self.results[0].reactants_conversions[0].conversion is not None and (
            self.results[0].products[0].selectivity is not None
        ):
            for i, c in enumerate(self.results[0].reactants_conversions):
                if self.results[0].reactants_conversions[i].conversion[0] < 0:
                    continue
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
                fig.update_xaxes(title_text=name + ' conversion (%)')
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
        if self.reaction_conditions is None:
            return

        self.reaction_conditions.normalize(archive, logger)

    def remove_ramps_from_data(self, data_with_ramps: np.array, data) -> np.array:
        """
        This function removes the ramps with changeing conditions from the data.
        Args:
            data_with_ramps (np.array): the data with ramps which is used to determine
            the indices of the ramps, in this case the temperature data
            data (np.array): the data which is supposed to be cleaned from the ramps
        """
        data_ = []
        for i in range(50, len(data_with_ramps) - 50, 10):
            deltaT = data_with_ramps[i] - data_with_ramps[50 + i]
            if abs(deltaT) < 0.05 * ureg.kelvin:
                T = data[i]
                try:
                    data_.append(T.magnitude)
                except AttributeError:
                    data_.append(T)
        return data_

    def reduce_haber_data(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        This function reduces the size of the arrays for the results section of the
        archive, by removing sections with changeing temperature conditions and
        averaging the values at each steady state.
        """
        if self.instruments[0].name == 'Haber':
            data_dict = {
                'Temp': self.reaction_conditions.set_temperature,
                'Whsv': self.reaction_conditions.weight_hourly_space_velocity,
                'Flow': self.results[0].total_flow_rate,
                'Conv': self.results[0].reactants_conversions[0].conversion,
                'NH3conc': self.reaction_conditions.reagents[0].fraction_in,
                'Rate': self.results[0].rates[0].reaction_rate,
                'Time': self.results[0].time_on_stream,
            }
            data_dict_no_ramps = {}
            for key, value in data_dict.items():
                data_dict_no_ramps[key] = self.remove_ramps_from_data(
                    data_dict['Temp'], value
                )

            # getting the temperature values of each step
            from itertools import groupby

            Temp_program = [key for key, _group in groupby(data_dict_no_ramps['Temp'])]
            # Temp_program = Temp_program.reset_index(drop=True)
            Temp_ = data_dict_no_ramps['Temp']

            Temps = []
            flows = []
            WHSVs = []
            NH3concs = []
            Convs = []
            Rates = []
            Times = []

            for step in range(len(Temp_program)):
                data_dict_single_step = {}
                for key in data_dict_no_ramps:
                    data_dict_single_step[key] = []

                for j in range(len(Temp_) - 1):
                    if Temp_[j] == Temp_program[step] and (
                        step < (len(Temp_program) / 2) and j < (len(Temp_) / 2)
                    ):
                        for key in data_dict_no_ramps:
                            data_dict_single_step[key].append(
                                data_dict_no_ramps[key][j]
                            )

                    elif (
                        step < (len(Temp_program) / 2) and Temp_[j] > Temp_program[step]
                    ):
                        continue
                    elif (
                        step >= (len(Temp_program) / 2)
                        and j > (len(Temp_) / 2)
                        and Temp_[j] == Temp_program[step]
                    ):
                        for key in data_dict_no_ramps:
                            data_dict_single_step[key].append(
                                data_dict_no_ramps[key][j]
                            )
                    elif (
                        step >= (len(Temp_program) / 2)
                        and Temp_[j] < Temp_program[step]
                    ):
                        continue

                Temps.append(np.mean(data_dict_single_step['Temp']))
                flows.append(np.mean(data_dict_single_step['Flow']))
                WHSVs.append(np.mean(data_dict_single_step['Whsv']))
                Convs.append(np.mean(data_dict_single_step['Conv']))
                Rates.append(np.mean(data_dict_single_step['Rate']))
                NH3concs.append(np.mean(data_dict_single_step['NH3conc']))
                Times.append(data_dict_single_step['Time'][-1])

            archive.results.properties.catalytic.reaction.reaction_conditions.weight_hourly_space_velocity = (  # noqa: E501
                WHSVs * ureg.m**3 / ureg.kg / ureg.second
            )  # noqa: E501
            archive.results.properties.catalytic.reaction.reaction_conditions.flow_rate = (  # noqa: E501
                flows * ureg.m**3 / ureg.second
            )
            archive.results.properties.catalytic.reaction.reaction_conditions.temperature = (  # noqa: E501
                Temps * ureg.kelvin
            )
            archive.results.properties.catalytic.reaction.reaction_conditions.time_on_stream = (  # noqa: E501
                Times * ureg.second
            )
            h2_rate = Rate(
                name='molecular hydrogen',
                reaction_rate=Rates * ureg.mmol / ureg.g / ureg.hour,
            )
            rates = []
            rates.append(h2_rate)
            set_nested_attr(
                archive.results.properties.catalytic.reaction,
                'rates',
                rates,
            )
            # archive.results.properties.catalytic.reaction.rate = [h2_rate]

        react = Reactant(name='ammonia', conversion=Convs, mole_fraction_in=NH3concs)

        return react

    def check_react(self, react, threshold_datapoints, archive, logger):
        """
        This function checks if the arrays in the reactant are larger than the number
        stored in "threshold_datapoints" (300). If the arrays are larger, it will reduce
        the size to store in the archive. If it is a haber measurement, it will call the
        function "reduce_haber_data" which averages the values at each steady state. If
        it is not a haber measurement, it will reduce the size of the arrays by taking
        every 100th value.
        Args:
            react (Reactant): the reactant object
            threshold_datapoints (int): the size limit of the arrays above which the
                arrays will be reduced in size.
        return: the reactant object with the reduced arrays.
        """
        for key1 in react:
            if (
                getattr(react, key1) is not None
                and len(getattr(react, key1)) > threshold_datapoints
            ):
                logger.info(
                    f"""Large arrays in {react.name}, reducing to store in the
                    archive."""
                )
                if (
                    self.instruments is not None
                    and self.instruments != []
                    and self.instruments[0].name == 'Haber'
                ):
                    react = self.reduce_haber_data(archive, logger)
                else:
                    for key in react:
                        if key == 'name':
                            continue
                        if getattr(react, key) is not None:
                            if len(getattr(react, key1)) > threshold2_datapoints:
                                setattr(react, key, getattr(react, key)[50::100])
                            else:
                                setattr(react, key, getattr(react, key)[20::10])

                break
        return react

    def return_conversion_results(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> list:
        """
        This function returns the conversion results of the reactants for the results
        section of the archive.
        It checks if the the name of the reactant is not in the list of the inert gases
        and if the name is in the list of the reaction_conditions.reagents, it will try
        to replace the name of the reactant with the IUPAC name of the reagent. If the
        arrays are larger than 300 (threshold_datapoints), it will reduce the size to
        store in the archive.

        return: a list of the reactants with the conversion results.
        """

        conversions_results = []
        for i in self.results[0].reactants_conversions:
            if i.name in ['He', 'helium', 'Ar', 'argon', 'inert']:
                continue
            for j in self.reaction_conditions.reagents:
                if i.name != j.name:
                    continue
                if j.pure_component.iupac_name is not None:
                    iupac_name = j.pure_component.iupac_name
                else:
                    iupac_name = j.name

                if i.fraction_in is None:
                    i.fraction_in = j.fraction_in
                elif not np.allclose(i.fraction_in, j.fraction_in):
                    logger.warning(f"""Gas concentration of '{i.name}' is not
                                the same in reaction_conditions and
                                results.reactants_conversions.""")
                try:
                    if i.conversion[0]<0:
                        react = Reactant(
                            name=iupac_name,
                            mole_fraction_in=i.fraction_in,
                            mole_fraction_out=i.fraction_out,
                        )
                    else:
                        react = Reactant(
                            name=iupac_name,
                            conversion=i.conversion,
                            mole_fraction_in=i.fraction_in,
                            mole_fraction_out=i.fraction_out,
                        )
                except TypeError:
                    react = Reactant(
                        name=iupac_name,
                        conversion=i.conversion,
                        mole_fraction_in=i.fraction_in,
                        mole_fraction_out=i.fraction_out,
                    )
                react = self.check_react(react, threshold_datapoints, archive, logger)

                conversions_results.append(react)
                break
        return conversions_results

    def write_conversion_results(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        """This function writes the conversion results to the archive."""

        if self.results[0].reactants_conversions is None:
            return []

        conversions_results = self.return_conversion_results(archive, logger)

        add_activity(archive)

        set_nested_attr(
            archive.results.properties.catalytic.reaction,
            'reactants',
            conversions_results,
        )

    def write_products_results(
        self, archive: 'EntryArchive', logger: 'BoundLogger'
    ) -> None:
        """This function writes the product results to the archive. If the arrays are
        larger than the number stored in "threshold_datapoints" (300), it will reduce
        the size to store in the archive.
        """
        if self.results[0].products is None:
            return
        product_results = []
        for i in self.results[0].products:
            if i.pure_component is not None and i.pure_component.iupac_name is not None:
                i.name = i.pure_component.iupac_name
            prod = Product(
                name=i.name,
                selectivity=i.selectivity,
                mole_fraction_out=i.fraction_out,
                space_time_yield=i.space_time_yield,
            )
            if i.selectivity is not None and len(i.selectivity) > threshold_datapoints:
                if threshold2_datapoints > len(i.selectivity):
                    prod.selectivity = i.selectivity[20::10]
                else:
                    prod.selectivity = i.selectivity[50::100]
                logger.info(
                    f"""Large arrays in product {i.name}, reducing to store
                    in the archive."""
                )
            if (
                i.fraction_out is not None
                and len(i.fraction_out) > threshold_datapoints
            ):
                if threshold2_datapoints > len(i.fraction_out):
                    prod.mole_fraction_out = i.fraction_out[20::10]
                else:
                    prod.mole_fraction_out = i.fraction_out[50::100]
            if (
                i.space_time_yield is not None
                and len(i.space_time_yield) > threshold_datapoints
            ):
                if threshold2_datapoints > len(i.space_time_yield):
                    prod.space_time_yield = i.space_time_yield[20::10]
                else:
                    prod.space_time_yield = i.space_time_yield[50::100]

            product_results.append(prod)

        add_activity(archive)

        set_nested_attr(
            archive.results.properties.catalytic.reaction,
            'products',
            product_results,
        )
    
    def write_rates_results(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:  # noqa: E501
        '''This function writes the rates results to the archive.'''

        if self.results[0].rates is None:
            return
        rates = []
        for i in self.results[0].rates:    
            rate = Rate(
                name=i.name,
                reaction_rate=i.reaction_rate,
            )
            rates.append(rate)
            set_nested_attr(
                archive.results.properties.catalytic.reaction,
                'rates',
                rates,
            )


    def check_sample(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if not self.samples:
            return
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

        if self.data_file is not None:
            self.check_and_read_data_file(archive, logger)
            logger.info('Data file processed.')

        self.normalize_reaction_conditions(archive, logger)
        if self.pretreatment is not None:
            self.pretreatment.normalize(archive, logger)

        if self.reaction_conditions is not None or self.results is not None:
            self.populate_reactivity_info(archive, logger)
        self.check_sample(archive, logger)

        if self.results is None or self.results == []:
            return

        self.results[0].normalize(archive, logger)
        if len(self.results) > 1:
            logger.warning(
                """Several instances of results found. Only the first result
                is considered for normalization."""
            )
        self.write_conversion_results(archive, logger)
        self.write_products_results(archive, logger)
        self.write_rates_results(archive, logger)

        self.plot_figures(archive, logger)
