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
          interactive statistics about the data.\n

          In order to generate a custom scatterplot, click on the "+ Scatterplot" button.
          You can then select the x and y quantities by starting to type the property name
          and selecting the appropriate line from the dropdown menus. If the property belongs to
          a repeated quantity, such as e.g. the reactants in a reaction, you can select the
          either select a specific index, or use the wildcard "*" to select all indices, or
          indicate the specific name of the reactant. If you e.g. want to generate an S-X plot
          for the conversion of the reactant A vs. selectivity to the product B, you can
          select the x-quantity as `results.properties.catalytic.reaction.reactants[? name=="A"].conversion`
          and the y-quantity as `results.properties.catalytic.reaction.products[? name=="B"].selectivity`.
          Be aware that the IUPAC names have to be used for the reactants and products (except for water and
          ammonia).'
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
            results.properties.catalytic.reaction.type: {label: Reaction type}
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
            data.datetime#nomad_catalysis.schema_packages.catalysis.CatalyticReaction: {label: Measurement time}
            data.datetime#nomad_catalysis.schema_packages.catalysis.CatalystSample: {label: Sample preparation time}
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
            - search_quantity: results.properties.catalytic.catalyst.support
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
            - search_quantity: results.properties.catalytic.reaction.type
              type: terms
            - search_quantity: results.properties.catalytic.reaction.name
              type: terms
          - type: menu
            title: Reactants
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
                  search_quantity: results.properties.catalytic.reaction.reactants.mole_fraction_in
              - type: histogram
                x:
                  search_quantity: results.properties.catalytic.reaction.reactants.mole_fraction_out
          - type: menu
            title: Products
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
                search_quantity: results.properties.catalytic.reaction.products.mole_fraction_out
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
            - type: histogram
              x:
                search_quantity: data.datetime#nomad_catalysis.schema_packages.catalysis.CatalyticReaction
            - search_quantity: results.eln.tags
              type: terms
            - search_quantity: results.eln.instruments
              type: terms
            - search_quantity: results.eln.lab_ids
              type: terms
          - type: menu
            title: User Defined Quantities
            size: xl
            items:
            - type: custom_quantities
          - type: menu
            title: Optimade
            size: lg
            items:
            - type: optimade
        dashboard:
          widgets:
          - layout:
              lg: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 0}
              md: {h: 8, minH: 6, minW: 8, w: 10, x: 0, y: 0}
              sm: {h: 8, minH: 8, minW: 12, w: 12, x: 0, y: 0}
              xl: {h: 10, minH: 8, minW: 12, w: 12, x: 0, y: 0}
              xxl: {h: 10, minH: 8, minW: 12, w: 16, x: 0, y: 0}
            quantity: results.material.elements
            scale: linear
            type: periodictable
            title: 'Elements of the catalyst material'
          - layout:
              lg: {h: 4, minH: 3, minW: 3, w: 6, x: 18, y: 0}
              md: {h: 4, minH: 3, minW: 3, w: 4, x: 14, y: 0}
              sm: {h: 4, minH: 4, minW: 3, w: 4, x: 4, y: 8}
              xl: {h: 5, minH: 3, minW: 3, w: 6, x: 18, y: 0}
              xxl: {h: 10, minH: 3, minW: 3, w: 6, x: 22, y: 0}
            title: 'Reactants'
            quantity: results.properties.catalytic.reaction.reactants.name
            scale: linear
            showinput: true
            type: terms
          - layout:
              lg: {h: 8, minH: 3, minW: 3, w: 6, x: 12, y: 0}
              md: {h: 8, minH: 3, minW: 3, w: 4, x: 10, y: 0}
              sm: {h: 4, minH: 3, minW: 3, w: 4, x: 0, y: 8}
              xl: {h: 10, minH: 3, minW: 3, w: 6, x: 12, y: 0}
              xxl: {h: 10, minH: 3, minW: 3, w: 6, x: 16, y: 0}
            title: 'Reaction Name'
            quantity: results.properties.catalytic.reaction.name
            scale: linear
            showinput: true
            type: terms
          - layout:
              lg: {h: 4, minH: 3, minW: 3, w: 6, x: 18, y: 4}
              md: {h: 4, minH: 3, minW: 3, w: 4, x: 14, y: 4}
              sm: {h: 4, minH: 3, minW: 3, w: 4, x: 8, y: 8}
              xl: {h: 5, minH: 3, minW: 3, w: 6, x: 18, y: 5}
              xxl: {h: 10, minH: 3, minW: 3, w: 6, x: 28, y: 0}
            title: 'Products'
            quantity: results.properties.catalytic.reaction.products.name
            scale: linear
            showinput: true
            type: terms
          - autorange: true
            layout:
              lg: {h: 10, minH: 3, minW: 8, w: 12, x: 0, y: 8}
              md: {h: 6, minH: 3, minW: 8, w: 9, x: 0, y: 8}
              sm: {h: 6, minH: 3, minW: 6, w: 6, x: 0, y: 12}
              xl: {h: 8, minH: 3, minW: 8, w: 12, x: 0, y: 10}
              xxl: {h: 8, minH: 6, minW: 8, w: 12, x: 0, y: 10}
            markers:
              color:
                quantity: results.properties.catalytic.reaction.reactants[*].name
            size: 1000
            x:
              quantity: results.properties.catalytic.reaction.reactants[*].mole_fraction_in
              title: 'Feed composition'
            y:
              quantity: results.properties.catalytic.reaction.reaction_conditions.temperature
            title: 'Feed composition vs. Temperature'
            type: scatterplot
          - autorange: true
            layout:
              lg: {h: 10, minH: 3, minW: 3, w: 12, x: 12, y: 8}
              md: {h: 6, minH: 3, minW: 3, w: 9, x: 9, y: 8}
              sm: {h: 6, minH: 3, minW: 3, w: 6, x: 6, y: 12}
              xl: {h: 8, minH: 3, minW: 3, w: 12, x: 12, y: 10}
              xxl: {h: 8, minH: 3, minW: 3, w: 12, x: 12, y: 10}
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
"""  # noqa: E501
)
