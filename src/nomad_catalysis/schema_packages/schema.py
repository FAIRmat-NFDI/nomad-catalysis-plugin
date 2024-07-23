from typing import (
    TYPE_CHECKING,
)

import numpy as np
from ase.data import chemical_symbols
from nomad.config import config
from nomad.datamodel.data import ArchiveSection, EntryDataCategory, Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.basesections import (
    CompositeSystem,
    Process,
)
from nomad.datamodel.results import (
    Catalyst,
    CatalyticProperties,
    Material,
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
    pass


configuration = config.get_plugin_entry_point(
    'nomad_catalysis.schema_packages:catalysis'
)

m_package = SchemaPackage()


class CatalysisElnCategory(EntryDataCategory):
    m_def = Category(label='Catalysis', categories=[EntryDataCategory])


def add_catalyst(archive):
    """Adds metainfo structure for catalysis data."""
    if not archive.results:
        archive.results = Results()
    if not archive.results.properties:
        archive.results.properties = Properties()
    if not archive.results.properties.catalytic:
        archive.results.properties.catalytic = CatalyticProperties()
    if not archive.results.properties.catalytic.catalyst:
        archive.results.properties.catalytic.catalyst = Catalyst()


# helper function to retrieve nested attributes
def get_nested_attr(obj, attr_path):
    for attr in attr_path.split('.'):
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    return obj


def set_nested_attr(obj, attr_path, value):
    for attr in attr_path.split('.'):
        obj = getattr(obj, attr, None)
        if obj is None:
            return
    setattr(obj, attr[-1], value)


def populate_catalyst_sample_info_to_results(archive, self, logger, reference=False):
    """
    Copies the catalyst sample information (if reference provided from a reference)
    into the results archive of the measurement.
    """
    if reference:
        sample_obj = self.samples[0].reference
    else:
        sample_obj = self

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
                    archive.results.properties.catalytic.catalyst, catalyst_attr, value
                )
            except ValueError:
                setattr(
                    archive.results.properties.catalytic.catalyst,
                    catalyst_attr,
                    [value],
                )
    if reference:
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


def add_referencing_methods_to_sample_result(self, archive, logger, number):
    if self.lab_id is not None:
        from nomad.search import MetadataPagination, search

        catalyst_sample = self.m_root().metadata.entry_id
        query = {'entry_references.target_entry_id': catalyst_sample}
        search_result = search(
            owner='all',
            query=query,
            pagination=MetadataPagination(page_size=number),
            user_id=archive.metadata.main_author.user_id,
        )

        if search_result.pagination.total > 0:
            methods = []
            for entry in search_result.data:
                if entry['entry_type'] == 'ELNXRayDiffraction':
                    method = 'XRD'
                    methods.append(method)
                elif entry['entry_type'] == 'CatalystCollection':
                    pass
                elif entry['entry_type'] == 'CatalystSampleCollection':
                    pass
                # else:
                #     method = entry['entry_type']
                #     methods.append(method)
            if search_result.pagination.total > number:
                logger.warn(
                    f'Found {search_result.pagination.total} entries with entry_id:'
                    f' "{catalyst_sample}". Will only check the the first '
                    f'"{number}" entries found for XRD method.'
                )
            if methods:
                if (
                    archive.results.properties.catalytic.catalyst.characterization_methods
                ) is None:
                    (
                        archive.results.properties.catalytic.catalyst.characterization_methods
                    ) = []
                (
                    archive.results.properties.catalytic.catalyst.characterization_methods.append(
                        methods[0]
                    )
                )
        else:
            logger.warn(f'Found no entries with reference: "{catalyst_sample}".')


# def populate_reactivity_info(archive, self, logger):
#     """
#     Copies the reaction data
#     into the results archive of the measurement.
#     """
#     add_activity(archive)
#     quantities_results_mapping = {
#         'reaction_conditions.set_temperature': 'reaction_conditions.temperature',
#         'reaction_conditions.set_pressure': 'reaction_conditions.pressure',
#         'reaction_conditions.weight_hourly_space_velocity':
#           'reaction_conditions.weight_hourly_space_velocity',
#         'reaction_conditions.gas_hourly_space_velocity':
#           'reaction_conditions.gas_hourly_space_velocity',
#         'results[0].temperature': 'reaction_conditions.temperature',
#         'results[0].pressure': 'reaction_conditions.pressure',
#         'reaction_name': 'name',
#         'reaction_type': 'type',
#     }

#     # Loop through the mapping and assign the values
#     for ref_attr, reaction_attr in quantities_results_mapping.items():
#         value = get_nested_attr(self, ref_attr)
#         if value is not None:
#             print(value)
#             try:
#                 set_nested_attr(
#                     archive.results.properties.catalytic.reaction, reaction_attr, value
#                 )
#             except ValueError:
#                 set_nested_attr(
#                     archive.results.properties.catalytic.reaction,
#                     reaction_attr,
#                     [value],
#                 )
#             except:
#                 logger.warn(
#                     'Something else went wrong when trying setattr for reaction'
#                 )


class Preparation(ArchiveSection):
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

    preparation_entry_reference = Quantity(
        type=Process,
        shape=[],
        description="""
        A reference to the entry that contains the details of the preparation method.
        """,
        a_eln=dict(component='EntryReference'),
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

    def normalize(self, archive, logger):
        super().normalize(archive, logger)


class SurfaceArea(ArchiveSection):
    m_def = Section(
        label_quantity='method_surface_area_determination',
        a_eln=ELNAnnotation(label='Surface Area'),
    )

    surface_area = Quantity(
        type=np.float64,
        unit=('m**2/g'),
        a_eln=dict(
            component='NumberEditQuantity',
            defaultDisplayUnit='m**2/g',
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
        The dispersion of the catalyst in %.
        """,
        a_eln=dict(component='NumberEditQuantity'),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        if self.method_surface_area_determination is not None:
            add_catalyst(archive)
            (
                archive.results.properties.catalytic.catalyst.characterization_methods.append(
                    self.method_surface_area_determination
                )
            )


class CatalystSample(CompositeSystem, Schema):
    m_def = Section(
        label='Catalyst Sample',
        categories=[CatalysisElnCategory],
    )

    preparation_details = SubSection(
        section_def=Preparation, a_eln=ELNAnnotation(label='Preparation Details')
    )

    surface = SubSection(
        section_def=SurfaceArea, a_eln=ELNAnnotation(label='Surface Area')
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

    def normalize(self, archive, logger):
        populate_catalyst_sample_info_to_results(archive, self, logger)

        from nomad.datamodel.context import ClientContext

        if isinstance(archive.m_context, ClientContext):
            pass
        else:
            super().normalize(archive, logger)
            add_referencing_methods_to_sample_result(self, archive, logger, 10)
