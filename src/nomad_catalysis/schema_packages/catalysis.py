from typing import (
    TYPE_CHECKING,
)

import numpy as np
from nomad.config import config
from nomad.datamodel.data import ArchiveSection, EntryDataCategory, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.basesections import (
    CompositeSystem,
)
from nomad.datamodel.results import (
    Catalyst,
    CatalyticProperties,
    Properties,
    Results,
)
from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
)
from nomad.metainfo.metainfo import Category

# from .catalyst_measurement import (
#     CatalyticReactionData,
#     CatalyticReactionData_core,
#     Rates,
#     ReactionConditions,
#     ReactionConditionsSimple,
#     ReactorSetup,
#     add_activity,
# )
# from .catalyst_measurement import Product as Product_data
# from .catalyst_measurement import Reactant as Reactant_data
# from .catalyst_measurement import Reagent as Reagent_data

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
            return
    setattr(obj, attr[-1], value)


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
