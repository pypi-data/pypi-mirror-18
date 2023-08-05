Data
====

..  contents::
    :local:
    :depth: 2

.. automodule:: tecplot.data

Loading Data
------------

.. autofunction:: tecplot.data.load_tecplot
.. autofunction:: tecplot.data.load_cgns
.. autofunction:: tecplot.data.load_fluent
.. autofunction:: tecplot.data.load_plot3d

Saving Data
-----------

.. autofunction:: tecplot.data.save_tecplot_binary
.. autofunction:: tecplot.data.save_tecplot_ascii

Data Queries
------------

.. autofunction:: tecplot.data.query.probe_at_position

Data Operations
---------------

.. autofunction:: tecplot.data.operate.Range
.. autofunction:: tecplot.data.operate.execute_equation

Data Access
-----------

.. py:currentmodule:: tecplot.data

Dataset
^^^^^^^

.. autoclass:: Dataset

    **Attributes**

    .. autosummary::
        :nosignatures:

        VariablesNamedTuple
        num_variables
        num_zones
        title

    **Methods**

    .. autosummary::

        add_fe_zone
        add_ordered_zone
        add_poly_zone
        add_variable
        add_zone
        copy_zones
        delete_variables
        delete_zones
        variable
        variables
        zone
        zones

.. autoattribute:: Dataset.VariablesNamedTuple
.. automethod:: Dataset.add_fe_zone
.. automethod:: Dataset.add_ordered_zone
.. automethod:: Dataset.add_poly_zone
.. automethod:: Dataset.add_variable
.. automethod:: Dataset.add_zone
.. automethod:: Dataset.copy_zones
.. automethod:: Dataset.delete_variables
.. automethod:: Dataset.delete_zones
.. autoattribute:: Dataset.num_variables
.. autoattribute:: Dataset.num_zones
.. autoattribute:: Dataset.title
.. automethod:: Dataset.variable
.. automethod:: Dataset.variables
.. automethod:: Dataset.zone
.. automethod:: Dataset.zones

.. py:currentmodule:: tecplot.data

Variable
^^^^^^^^

.. autoclass:: Variable

    **Attributes**

    .. autosummary::
        :nosignatures:

        index
        name
        num_zones

    **Methods**

    .. autosummary::

        zone
        zones

.. autoattribute:: Variable.index
.. autoattribute:: Variable.name
.. autoattribute:: Variable.num_zones
.. automethod:: Variable.zone
.. automethod:: Variable.zones

.. py:currentmodule:: tecplot.data

Zone
^^^^

.. autoclass:: Zone

    **Attributes**

    .. autosummary::
        :nosignatures:

        index
        name
        num_points
        num_variables
        shape
        solution_time
        strand
        type

    **Methods**

    .. autosummary::

        copy
        variable
        variables

.. automethod:: Zone.copy
.. autoattribute:: Zone.index
.. autoattribute:: Zone.name
.. autoattribute:: Zone.num_points
.. autoattribute:: Zone.num_variables
.. autoattribute:: Zone.shape
.. autoattribute:: Zone.solution_time
.. autoattribute:: Zone.strand
.. autoattribute:: Zone.type
.. automethod:: Zone.variable
.. automethod:: Zone.variables

.. py:currentmodule:: tecplot.data

Array
^^^^^

.. autoclass:: Array

    **Attributes**

    .. autosummary::
        :nosignatures:

        c_type
        data
        data_type
        minmax
        shape
        size
        value

    **Methods**

    .. autosummary::

        as_numpy_array
        copy
        max
        min

.. automethod:: Array.as_numpy_array
.. autoattribute:: Array.c_type
.. automethod:: Array.copy
.. autoattribute:: Array.data
.. autoattribute:: Array.data_type
.. automethod:: Array.max
.. automethod:: Array.min
.. autoattribute:: Array.minmax
.. autoattribute:: Array.shape
.. autoattribute:: Array.size
.. autoattribute:: Array.value

Auxiliary Data
--------------

.. py:currentmodule:: tecplot.data

AuxData
^^^^^^^

.. autoclass:: AuxData

    **Methods**

    .. autosummary::

        item

.. automethod:: AuxData.item
