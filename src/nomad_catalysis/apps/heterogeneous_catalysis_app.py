import yaml

heterogeneous_catalysis_app = yaml.safe_load(
    """
        label: Heterogeneous Catalysis
        path: heterogeneouscatalyst
        category: Use Cases
        description: Search heterogeneous catalysts
        readme: 'This page allows you to search **catalyst and catalysis data**
          within NOMAD. The filter menu on the left and the shown
          default columns are specifically designed for Heterogeneous Catalyst
          exploration. The dashboard directly shows useful
          interactive statistics about the data.'
        # filters:
        #   exclude:
        #   - mainfile
        #   - entry_name
        #   - combine
        # search_quantities:
        #   include:
        #     - '*#nomad_catalysis.schema_packages.catalysis.*'
        filters_locked:
          quantities: results.properties.catalytic
        search_syntaxes:
          exclude:
          - free_text
        columns:
          selected:
          - entry_name
          - results.properties.catalytic.reaction.name
          - results.properties.catalytic.catalyst.catalyst_type
          - results.properties.catalytic.catalyst.preparation_method
          - results.properties.catalytic.catalyst.surface_area
          options:
            results.material.elements: {}
            results.properties.catalytic.catalyst.catalyst_type: {}
            results.properties.catalytic.catalyst.catalyst_name: {}
            results.properties.catalytic.catalyst.preparation_method: {
              label: Preparation}
            results.properties.catalytic.catalyst.surface_area:
              format:
                decimals: 2
                mode: standard
              unit: 'm^2/g'
              label: Surface area
            results.properties.catalytic.reaction.name: {label: Reaction name}
            results.properties.catalytic.reaction.type: {label: Reaction class}
            results.properties.catalytic.reaction.reactants.name: {label: Reactants}
            results.properties.catalytic.reaction.products.name: {label: Products}
            references: {}
            results.material.chemical_formula_hill: {label: Formula}
            results.material.structural_type: {}
            results.eln.lab_ids: {}
            results.eln.sections: {}
            results.eln.methods: {}
            results.eln.tags: {}
            results.eln.instruments: {}
            entry_name: {label: Name}
            entry_type: {}
            mainfile: {}
            upload_create_time: {label: Upload time}
            authors: {}
            comment: {}
            datasets: {}
            published: {label: Access}
        search_quantities:
          include:
            - '*#nomad_catalysis.schema_packages.catalysis.Cat*'
        menu:
          items:
          - type: menu
            title: Heterogeneous Catalysis
          - type: menu
            title: Catalyst Materials
            indentation: 1
          - type: menu
            title: Elements / Formula
            indentation: 2
            size: xxl
            items:
            - type: periodic_table
              search_quantity: results.material.elements
            - type: terms
              search_quantity: results.material.chemical_formula_hill
              width: 6
              options: 0
            - type: terms
              search_quantity: results.material.chemical_formula_iupac
              width: 6
              options: 0
            - type: terms
              search_quantity: results.material.chemical_formula_reduced
              width: 6
              options: 0
            - search_quantity: results.material.chemical_formula_anonymous
              type: terms
              width: 6
              options: 0
            - type: histogram
              x:
                search_quantity: results.material.n_elements
          - type: menu
            title: Catalyst Properties
            indentation: 2
            size: md
            items:
            - search_quantity: results.properties.catalytic.catalyst.catalyst_type
              type: terms
            - search_quantity: results.properties.catalytic.catalyst.preparation_method
              type: terms
            - search_quantity: results.properties.catalytic.catalyst.catalyst_name
              type: terms
            - type: terms
              search_quantity: data.form#nomad_catalysis.schema_packages.catalysis.CatalystSample
            - search_quantity: results.properties.catalytic.catalyst.characterization_methods
              type: terms
            - type: histogram
              x:
                search_quantity: results.properties.catalytic.catalyst.surface_area
                unit: 'm^2/g'
              autorange: false
          - type: menu
            title: Reactions
            size: md
            indentation: 1
            items:
            - search_quantity: data.reaction_type#nomad_catalysis.schema_packages.catalysis.CatalyticReaction
              type: terms
            - search_quantity: results.properties.catalytic.reaction.name
              type: terms
          - type: menu
            title: Reactants
              #path: results.properties.catalytic.reaction.reactants
            indentation: 2
            size: md
            items:
              - search_quantity: results.properties.catalytic.reaction.reactants.name
                type: terms
              - type: histogram
                x:
                  search_quantity: results.properties.catalytic.reaction.reactants.conversion
              - type: histogram
                x:
                  search_quantity: results.properties.catalytic.reaction.reactants.gas_concentration_in
              - type: histogram
                x:
                  search_quantity: results.properties.catalytic.reaction.reactants.gas_concentration_out
          - type: menu
            title: Products
            # path: results.properties.catalytic.reaction.products
            indentation: 2
            size: md
            items:
            - search_quantity: results.properties.catalytic.reaction.products.name
              type: terms
            - type: histogram
              x:
                search_quantity: results.properties.catalytic.reaction.products.selectivity
            - type: histogram
              x:
                search_quantity: results.properties.catalytic.reaction.products.gas_concentration_out
          - type: menu
            title: Reaction Conditions
            indentation: 2
            size: md
            items:
            - type: histogram
              x:
                search_quantity: results.properties.catalytic.reaction.reaction_conditions.temperature
            - type: histogram
              x:
                search_quantity: results.properties.catalytic.reaction.reaction_conditions.pressure
                unit: 'bar'
            - type: histogram
              x:
                search_quantity: results.properties.catalytic.reaction.reaction_conditions.weight_hourly_space_velocity
                unit: 'ml/(g*hr)'
          - type: menu
            title: Author / Dataset
            size: md
            items:
            - search_quantity: authors.name
              type: terms
            - type: histogram
              x:
                search_quantity: upload_create_time
            - type: terms
              search_quantity: datasets.dataset_name
          - type: menu
            title: Electronic Lab Notebook
            size: md
            items:
            - search_quantity: results.eln.sections
              type: terms
            - search_quantity: results.eln.methods
              type: terms
            - search_quantity: results.eln.tags
              type: terms
            - search_quantity: results.eln.instruments
              type: terms
            - search_quantity: results.eln.lab_ids
              type: terms
            # custom_quantities:
            #   label: User Defined Quantities
            #   size: l
            # metadata:
            #   label: Visibility / IDs / Schema
            # optimade:
            #   label: Optimade
            #   size: m
        dashboard:
          widgets:
          - layout:
              lg: {h: 10, minH: 8, minW: 12, w: 16, x: 0, y: 6}
              md: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 5}
              sm: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 4}
              xl: {h: 10, minH: 8, minW: 12, w: 16, x: 0, y: 6}
              xxl: {h: 10, minH: 8, minW: 12, w: 16, x: 0, y: 6}
            quantity: results.material.elements
            scale: linear
            type: periodictable
          - layout:
              lg: {h: 6, minH: 3, minW: 3, w: 8, x: 8, y: 0}
              md: {h: 5, minH: 3, minW: 3, w: 6, x: 6, y: 0}
              sm: {h: 4, minH: 4, minW: 3, w: 4, x: 4, y: 0}
              xl: {h: 6, minH: 3, minW: 3, w: 8, x: 8, y: 0}
              xxl: {h: 6, minH: 3, minW: 3, w: 8, x: 8, y: 0}
            title: 'Reactants'
            quantity: results.properties.catalytic.reaction.reactants.name
            scale: linear
            showinput: true
            type: terms
          - layout:
              lg: {h: 6, minH: 3, minW: 3, w: 8, x: 0, y: 0}
              md: {h: 5, minH: 3, minW: 3, w: 6, x: 0, y: 0}
              sm: {h: 4, minH: 3, minW: 3, w: 4, x: 0, y: 0}
              xl: {h: 6, minH: 3, minW: 3, w: 8, x: 0, y: 0}
              xxl: {h: 6, minH: 3, minW: 3, w: 8, x: 0, y: 0}
            title: 'Reaction Name'
            quantity: results.properties.catalytic.reaction.name
            scale: linear
            showinput: true
            type: terms
          - layout:
              lg: {h: 6, minH: 3, minW: 3, w: 8, x: 16, y: 0}
              md: {h: 5, minH: 3, minW: 3, w: 6, x: 12, y: 0}
              sm: {h: 4, minH: 3, minW: 3, w: 4, x: 8, y: 0}
              xl: {h: 6, minH: 3, minW: 3, w: 8, x: 16, y: 0}
              xxl: {h: 6, minH: 3, minW: 3, w: 8, x: 16, y: 0}
            title: 'Products'
            quantity: results.properties.catalytic.reaction.products.name
            scale: linear
            showinput: true
            type: terms
          - layout:
              lg: {h: 5, minH: 3, minW: 3, w: 8, x: 16, y: 6}
              md: {h: 4, minH: 3, minW: 3, w: 6, x: 12, y: 5}
              sm: {h: 3, minH: 3, minW: 3, w: 6, x: 0, y: 12}
              xl: {h: 5, minH: 3, minW: 3, w: 8, x: 16, y: 6}
              xxl: {h: 5, minH: 3, minW: 3, w: 8, x: 16, y: 6}
            quantity: results.properties.catalytic.catalyst.preparation_method
            scale: linear
            showinput: true
            type: terms
          - layout:
              lg: {h: 5, minH: 3, minW: 3, w: 8, x: 16, y: 11}
              md: {h: 4, minH: 3, minW: 3, w: 6, x: 12, y: 9}
              sm: {h: 3, minH: 3, minW: 3, w: 6, x: 6, y: 12}
              xl: {h: 5, minH: 3, minW: 3, w: 8, x: 16, y: 11}
              xxl: {h: 5, minH: 3, minW: 3, w: 8, x: 16, y: 11}
            quantity: results.properties.catalytic.catalyst.catalyst_type
            scale: linear
            showinput: true
            type: terms
          - autorange: false
            layout:
              lg: {h: 5, minH: 3, minW: 8, w: 12, x: 12, y: 21}
              md: {h: 3, minH: 3, minW: 8, w: 9, x: 9, y: 16}
              sm: {h: 3, minH: 3, minW: 6, w: 6, x: 6, y: 18}
              xl: {h: 4, minH: 3, minW: 8, w: 12, x: 12, y: 20}
              xxl: {h: 4, minH: 3, minW: 8, w: 12, x: 12, y: 20}
            nbins: 30
            x:
              quantity: results.properties.catalytic.reaction.reaction_conditions.weight_hourly_space_velocity
              unit: 'ml/(g*hr)'
            title: 'Weight Hourly Space Velocity'
            scale: linear
            showinput: false
            type: histogram
          - autorange: true
            layout:
              lg: {h: 10, minH: 3, minW: 8, w: 12, x: 0, y: 16}
              md: {h: 6, minH: 3, minW: 8, w: 9, x: 0, y: 13}
              sm: {h: 6, minH: 3, minW: 6, w: 6, x: 0, y: 15}
              xl: {h: 8, minH: 3, minW: 8, w: 12, x: 0, y: 16}
              xxl: {h: 8, minH: 6, minW: 8, w: 12, x: 0, y: 16}
            markers:
              color:
                quantity: results.properties.catalytic.reaction.reactants[*].name
            size: 1000
            x:
              quantity: results.properties.catalytic.reaction.reactants[*].gas_concentration_in
              title: 'gas concentration'
            y:
              quantity: results.properties.catalytic.reaction.reaction_conditions.temperature
            title: 'Reactant feed concentration vs. Temperature'
            type: scatterplot
          - autorange: false
            layout:
              lg: {h: 5, minH: 3, minW: 8, w: 12, x: 12, y: 16}
              md: {h: 3, minH: 3, minW: 8, w: 9, x: 9, y: 13}
              sm: {h: 3, minH: 3, minW: 6, w: 6, x: 6, y: 15}
              xl: {h: 4, minH: 3, minW: 8, w: 12, x: 12, y: 16}
              xxl: {h: 4, minH: 3, minW: 8, w: 12, x: 12, y: 16}
            nbins: 30
            x:
              quantity: results.properties.catalytic.reaction.reaction_conditions.pressure
              unit: 'bar'
            title: 'Reaction Pressure'
            scale: linear
            showinput: false
            type: histogram
          - autorange: true
            layout:
              lg: {h: 8, minH: 3, minW: 3, w: 12, x: 0, y: 26}
              md: {h: 6, minH: 3, minW: 3, w: 9, x: 0, y: 19}
              sm: {h: 5, minH: 3, minW: 3, w: 6, x: 0, y: 21}
              xl: {h: 9, minH: 3, minW: 3, w: 12, x: 0, y: 24}
              xxl: {h: 9, minH: 3, minW: 3, w: 12, x: 0, y: 24}
            markers:
              color:
                quantity: results.properties.catalytic.reaction.reactants[*].name
            size: 1000
            title: 'Temperature vs. Conversion'
            type: scatterplot
            x:
              quantity: results.properties.catalytic.reaction.reaction_conditions.temperature
            y:
              quantity: results.properties.catalytic.reaction.reactants[*].conversion
              title: 'Conversion (%)'
          - autorange: true
            layout:
              lg: {h: 8, minH: 3, minW: 3, w: 12, x: 12, y: 26}
              md: {h: 6, minH: 3, minW: 3, w: 9, x: 9, y: 19}
              sm: {h: 5, minH: 3, minW: 3, w: 6, x: 6, y: 21}
              xl: {h: 9, minH: 3, minW: 3, w: 12, x: 12, y: 24}
              xxl: {h: 9, minH: 3, minW: 3, w: 12, x: 12, y: 24}
            markers:
              color:
                quantity: results.properties.catalytic.reaction.products[*].name
            size: 1000
            title: 'Temperature vs. Selectivity'
            type: scatterplot
            x:
              quantity: results.properties.catalytic.reaction.reaction_conditions.temperature
            y:
              quantity: results.properties.catalytic.reaction.products[*].selectivity
              title: 'Selectivity (%)'
          - autorange: true
            layout:
              lg: {h: 8, minH: 3, minW: 3, w: 12, x: 0, y: 34}
              md: {h: 6, minH: 3, minW: 3, w: 9, x: 0, y: 25}
              sm: {h: 5, minH: 3, minW: 3, w: 6, x: 0, y: 26}
              xl: {h: 9, minH: 3, minW: 3, w: 12, x: 0, y: 33}
              xxl: {h: 9, minH: 3, minW: 3, w: 12, x: 0, y: 33}
            markers:
              color:
                quantity: results.properties.catalytic.reaction.name
            size: 1000
            type: scatterplot
            x:
              quantity: results.properties.catalytic.reaction.reactants[? name=='molecular oxygen'].conversion
              title: 'Oxygen Conversion (%)'
            y:
              quantity: results.properties.catalytic.reaction.products[? name=='acetic acid'].selectivity
              title: 'Acetic Acid Selectivity (%)'
          - autorange: true
            layout:
              lg: {h: 8, minH: 3, minW: 3, w: 12, x: 12, y: 34}
              md: {h: 6, minH: 3, minW: 3, w: 9, x: 9, y: 25}
              sm: {h: 5, minH: 3, minW: 3, w: 6, x: 6, y: 26}
              xl: {h: 9, minH: 3, minW: 3, w: 12, x: 12, y: 33}
              xxl: {h: 9, minH: 3, minW: 3, w: 12, x: 12, y: 33}
            markers:
              color:
                quantity: results.properties.catalytic.catalyst.preparation_method
            size: 1000
            type: scatterplot
            x:
              quantity: results.properties.catalytic.reaction.reactants[? name=='carbon monoxide'].conversion
              title: 'Carbon Monoxide Conversion (%)'
            y:
              quantity: results.properties.catalytic.reaction.products[? name=='ethanol'].selectivity
              title: 'Ethanol Selectivity (%)'
          - autorange: false
            layout:
              lg: {h: 4, minH: 3, minW: 8, w: 12, x: 0, y: 42}
              md: {h: 4, minH: 3, minW: 8, w: 9, x: 0, y: 31}
              sm: {h: 4, minH: 3, minW: 8, w: 8, x: 0, y: 31}
              xl: {h: 4, minH: 3, minW: 8, w: 12, x: 0, y: 42}
              xxl: {h: 4, minH: 3, minW: 8, w: 12, x: 0, y: 42}
            nbins: 30
            x:
              quantity: results.properties.catalytic.catalyst.surface_area
              unit: 'm^2/g'
            title: 'Catalyst Surface Area'
            scale: 1/4
            showinput: false
            type: histogram
          - layout:
              lg: {h: 4, minH: 3, minW: 3, w: 12, x: 12, y: 42}
              md: {h: 4, minH: 3, minW: 3, w: 9, x: 9, y: 31}
              sm: {h: 4, minH: 4, minW: 3, w: 8, x: 8, y: 31}
              xl: {h: 4, minH: 3, minW: 3, w: 12, x: 12, y: 42}
              xxl: {h: 4, minH: 3, minW: 3, w: 12, x: 12, y: 42}
            quantity: results.properties.catalytic.catalyst.characterization_methods
            scale: linear
            showinput: true
            type: terms
"""  # noqa: E501
)
