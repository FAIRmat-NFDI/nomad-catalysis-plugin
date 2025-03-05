from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Dashboard,
    Layout,
    Menu,
    MenuItemCustomQuantities,
    MenuItemHistogram,
    MenuItemOptimade,
    MenuItemPeriodicTable,
    MenuItemTerms,
    SearchQuantities,
    WidgetPeriodicTable,
    WidgetScatterPlot,
    WidgetTerms,
)

heterogeneous_catalysis_app = App(
    label='Heterogeneous Catalysis',
    path='heterogeneouscatalyst',
    category='Use Cases',
    description='Search heterogeneous catalysts',
    readme="""This page allows you to search **catalyst and catalysis data**
        within NOMAD. The filter menu on the left and the shown
        default columns are specifically designed for Heterogeneous Catalyst
        exploration. The dashboard directly shows useful
        interactive statistics about the data.\n

        In order to generate a custom scatterplot, click on the "+ Scatterplot" button.
        You can then select the x and y quantities by starting to type the property name
        and selecting the appropriate line from the dropdown menus. If the property 
        belongs to
        a repeated quantity, such as e.g. the reactants in a reaction, you can select 
        the either select a specific index, or use the wildcard "*" to select all 
        indices, or
        indicate the specific name of the reactant. If you e.g. want to generate an 
        S-X plot
        for the conversion of the reactant A vs. selectivity to the product B, you can
        select the x-quantity as 
        `results.properties.catalytic.reaction.reactants[? name=="A"].conversion`
        and the y-quantity as 
        `results.properties.catalytic.reaction.products[? name=="B"].selectivity`.
        Be aware that the IUPAC names have to be used for the reactants and products 
        (except for water and ammonia).""",
    filters_locked={'quantities': ['results.properties.catalytic']},
    # search_syntaxes= {
    #     "exclude": ["free_text"]
    # },
    columns=[
        Column(quantity='entry_name', selected=True),
        Column(
            quantity='results.properties.catalytic.reaction.name',
            label='Reaction name',
            selected=True,
        ),
        Column(
            quantity='results.properties.catalytic.catalyst.catalyst_type',
            selected=True,
        ),
        Column(
            quantity='results.properties.catalytic.catalyst.preparation_method',
            label='Preparation',
            selected=True,
        ),
        Column(
            quantity='results.properties.catalytic.catalyst.surface_area',
            format={'decimals': 2, 'mode': 'standard'},
            unit='m^2/g',
            label='Surface area',
        ),
        Column(quantity='results.material.elements'),
        Column(quantity='results.properties.catalytic.catalyst.catalyst_name'),
        Column(
            quantity='results.properties.catalytic.reaction.reactants.name',
            label='Reactants',
        ),
        Column(
            quantity='results.properties.catalytic.reaction.products.name',
            label='Products',
        ),
        Column(
            quantity='results.properties.catalytic.reaction.type',
            label='Reaction type',
        ),
        Column(quantity='references'),
        Column(quantity='results.material.chemical_formula_hill', label='Formula'),
        Column(quantity='results.material.structural_type'),
        Column(quantity='results.eln.lab_ids'),
        Column(quantity='results.eln.sections'),
        Column(quantity='results.eln.methods'),
        Column(quantity='results.eln.tags'),
        Column(quantity='results.eln.instruments'),
        Column(quantity='entry_type'),
        Column(quantity='mainfile'),
        Column(quantity='upload_create_time', label='Upload time'),
        Column(quantity='authors'),
        Column(quantity='comment'),
        Column(quantity='datasets'),
        Column(quantity='published', label='Access'),
        Column(
            quantity='data.datetime#nomad_catalysis.schema_packages.catalysis.CatalystSample',
            label='Sample preparation time',
        ),
        Column(
            quantity='data.datetime#nomad_catalysis.schema_packages.catalysis.CatalyticReaction',
            label='Measurement time',
        ),
    ],
    search_quantities=SearchQuantities(
        include=['*#nomad_catalysis.schema_packages.catalysis.Cat*'],
    ),
    menu=Menu(
        title='Heterogeneous Catalysis',
        items=[
            Menu(
                title='Catalyst Materials',
                indentation=1,
            ),
            Menu(
                title='Elements / Formula',
                indentation=2,
                size='xxl',
                items=[
                    MenuItemPeriodicTable(search_quantity='results.material.elements'),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_hill',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_iupac',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_reduced',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_anonymous',
                        width=6,
                        options=0,
                    ),
                    MenuItemHistogram(
                        x={'search_quantity': 'results.material.n_elements'}
                    ),
                ],
            ),
            Menu(
                title='Catalyst Properties',
                indentation=2,
                size='md',
                items=[
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.catalyst.catalyst_type'
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.catalyst.support'
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.catalyst.preparation_method'
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.catalyst.catalyst_name'
                    ),
                    MenuItemTerms(
                        search_quantity='data.form#nomad_catalysis.schema_packages.catalysis.CatalystSample'
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.catalyst.characterization_methods'
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.catalyst.surface_area',
                            'unit': 'm^2/g',
                        },
                        autorange=False,
                    ),
                ],
            ),
            Menu(
                title='Reactions',
                size='md',
                indentation=1,
                items=[
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.reaction.type'
                    ),
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.reaction.name'
                    ),
                ],
            ),
            Menu(
                title='Reactants',
                indentation=2,
                size='md',
                items=[
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.reaction.reactants.name'
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.reactants.conversion'
                        }
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.reactants.mole_fraction_in'
                        }
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.reactants.mole_fraction_out'
                        }
                    ),
                ],
            ),
            Menu(
                title='Products',
                indentation=2,
                size='md',
                items=[
                    MenuItemTerms(
                        search_quantity='results.properties.catalytic.reaction.products.name'
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.products.selectivity'
                        }
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.products.mole_fraction_out'
                        }
                    ),
                ],
            ),
            Menu(
                title='Reaction Conditions',
                indentation=2,
                size='md',
                items=[
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.reaction_conditions.temperature'
                        }
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.reaction_conditions.pressure',
                            'unit': 'bar',
                        }
                    ),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'results.properties.catalytic.reaction.reaction_conditions.weight_hourly_space_velocity', # noqa: E501
                            'unit': 'ml/(g*hr)',
                        }
                    ),
                ],
            ),
            Menu(
                title='Author / Dataset',
                size='md',
                items=[
                    MenuItemTerms(search_quantity='authors.name'),
                    MenuItemHistogram(x={'search_quantity': 'upload_create_time'}),
                    MenuItemTerms(search_quantity='datasets.dataset_name'),
                ],
            ),
            Menu(
                title='Electronic Lab Notebook',
                size='md',
                items=[
                    MenuItemTerms(search_quantity='results.eln.sections'),
                    MenuItemTerms(search_quantity='results.eln.methods'),
                    MenuItemHistogram(
                        x={
                            'search_quantity': 
                            'data.datetime#nomad_catalysis.schema_packages.catalysis.CatalyticReaction'
                        },
                        title='Date of the catalytic reaction test',
                    ),
                    MenuItemTerms(search_quantity='results.eln.tags'),
                    MenuItemTerms(search_quantity='results.eln.instruments'),
                    MenuItemTerms(search_quantity='results.eln.lab_ids'),
                ],
            ),
            Menu(
                title='User Defined Quantities',
                size='xl',
                items=[
                    MenuItemCustomQuantities(),
                ],
            ),
            Menu(
                title='Optimade',
                size='lg',
                items=[
                    MenuItemOptimade(),
                ],
            ),
        ],
    ),
    dashboard=Dashboard(
        widgets=[
            WidgetPeriodicTable(
                layout={
                    'lg': Layout(h= 8, minH= 8, minW= 12, w= 12, x= 0, y= 0),
                    'md': Layout(h= 8, minH= 6, minW= 8, w= 10, x= 0, y= 0),
                    'sm': Layout(h= 8, minH= 8, minW= 12, w= 12, x= 0, y= 0),
                    'xl': {'h': 10, 'minH': 8, 'minW': 12, 'w': 12, 'x': 0, 'y': 0},
                    'xxl': {'h': 10, 'minH': 8, 'minW': 12, 'w': 16, 'x': 0, 'y': 0},
                },
                search_quantity='results.material.elements',
                scale='linear',
                title='Elements of the catalyst material',
            ),
            WidgetTerms(
                title='Reaction name',
                layout={
                    'lg': Layout(h=8, minH=3, minW=3, w=6, x=12, y=0),
                    'md': Layout(h=8, minH=3, minW=3, w=4, x=10, y=0),
                    'sm': Layout(h=4, minH=3, minW=3, w=4, x=0, y=8),
                    'xl': Layout(h=10, minH=3, minW=3, w=6, x=12, y=0),
                    'xxl': Layout(h=10, minH=3, minW=3, w=6, x=16, y=0),
                },
                search_quantity='results.properties.catalytic.reaction.name',
            ),
            WidgetTerms(
                title='Reactants',
                layout={
                    'lg': Layout(h=4, minH=3, minW=3, w=6, x=18, y=0),
                    'md': Layout(h=4, minH=3, minW=3, w=4, x=14, y=0),
                    'sm': Layout(h=4, minH=4, minW=3, w=4, x=4, y=8),
                    'xl': Layout(h=5, minH=3, minW=3, w=6, x=18, y=0),
                    'xxl': Layout(h=10, minH=3, minW=3, w=6, x=22, y=0),
                },
                search_quantity='results.properties.catalytic.reaction.reactants.name',
                showinput=True,
                scale='linear',
            ),
            WidgetTerms(
                title='Products',
                layout={
                    'lg': Layout(h=4, minH=3, minW=3, w=6, x=18, y=4),
                    'md': Layout(h=4, minH=3, minW=3, w=4, x=14, y=4),
                    'sm': Layout(h=4, minH=4, minW=3, w=4, x=8, y=8),
                    'xl': Layout(h=5, minH=3, minW=3, w=6, x=18, y=5),
                    'xxl': Layout(h=10, minH=3, minW=3, w=6, x=28, y=0),
                },
                search_quantity='results.properties.catalytic.reaction.products.name',
                showinput=True,
                scale='linear',
            ),
            WidgetScatterPlot(
                title='Feed composition vs. Temperature',
                autorange=True,
                layout={
                    'lg': Layout(h=10, minH=3, minW=8, w=12, x=0, y=8),
                    'md': Layout(h=6, minH=3, minW=8, w=9, x=0, y=8),
                    'sm': Layout(h=6, minH=3, minW=6, w=6, x=0, y=12),
                    'xl': Layout(h=8, minH=3, minW=8, w=12, x=0, y=10),
                    'xxl': Layout(h=8, minH=6, minW=8, w=12, x=0, y=10),
                },
                x=Axis(
                    search_quantity='results.properties.catalytic.reaction.reactants[*].mole_fraction_in',
                    title='Feed composition',
                ),
                y=Axis(
                    search_quantity='results.properties.catalytic.reaction.reaction_conditions.temperature'
                ),
                color='results.properties.catalytic.reaction.reactants[*].name',
                size=1000,
            ),
            WidgetScatterPlot(
                title='Temperature vs. Conversion',
                autorange=True,
                layout={
                    'lg': Layout(h=10, minH=3, minW=3, w=12, x=12, y=8),
                    'md': Layout(h=6, minH=3, minW=3, w=9, x=9, y=8),
                    'sm': Layout(h=6, minH=3, minW=3, w=6, x=6, y=12),
                    'xl': Layout(h=8, minH=3, minW=3, w=12, x=12, y=10),
                    'xxl': Layout(h=8, minH=3, minW=3, w=12, x=12, y=10),
                },
                x=Axis(
                    search_quantity='results.properties.catalytic.reaction.reaction_conditions.temperature'
                ),
                y=Axis(
                    search_quantity='results.properties.catalytic.reaction.reactants[*].conversion',
                    title='Conversion (%)',
                ),
                color='results.properties.catalytic.reaction.reactants[*].name',
                size=1000,
            ),
        ]
    ),
)
