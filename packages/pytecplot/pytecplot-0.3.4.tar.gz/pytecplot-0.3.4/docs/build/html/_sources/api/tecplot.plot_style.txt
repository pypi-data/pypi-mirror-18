Plot Style
==========

..  contents::
    :local:
    :depth: 2


Scatter Plots
-------------

.. py:currentmodule:: tecplot.plot

Scatter
^^^^^^^

.. autoclass:: Scatter

    **Attributes**

    .. autosummary::
        :nosignatures:

        variable
        variable_index

.. autoattribute:: Scatter.variable
.. autoattribute:: Scatter.variable_index

Vector Plots
------------

..  contents::
    :local:
    :depth: 1

.. py:currentmodule:: tecplot.plot

Vector2D
^^^^^^^^

.. autoclass:: Vector2D

    **Attributes**

    .. autosummary::
        :nosignatures:

        u_variable
        u_variable_index
        v_variable
        v_variable_index

.. autoattribute:: Vector2D.u_variable
.. autoattribute:: Vector2D.u_variable_index
.. autoattribute:: Vector2D.v_variable
.. autoattribute:: Vector2D.v_variable_index

.. py:currentmodule:: tecplot.plot

Vector3D
^^^^^^^^

.. autoclass:: Vector3D

    **Attributes**

    .. autosummary::
        :nosignatures:

        u_variable
        u_variable_index
        v_variable
        v_variable_index
        w_variable
        w_variable_index

.. autoattribute:: Vector3D.u_variable
.. autoattribute:: Vector3D.u_variable_index
.. autoattribute:: Vector3D.v_variable
.. autoattribute:: Vector3D.v_variable_index
.. autoattribute:: Vector3D.w_variable
.. autoattribute:: Vector3D.w_variable_index

Contours
--------

..  contents::
    :local:
    :depth: 1

.. py:currentmodule:: tecplot.plot

ContourGroup
^^^^^^^^^^^^

.. autoclass:: ContourGroup

    **Attributes**

    .. autosummary::
        :nosignatures:

        color_cutoff
        colormap_filter
        colormap_name
        default_num_levels
        labels
        legend
        levels
        lines
        variable
        variable_index

.. autoattribute:: ContourGroup.color_cutoff
.. autoattribute:: ContourGroup.colormap_filter
.. autoattribute:: ContourGroup.colormap_name
.. autoattribute:: ContourGroup.default_num_levels
.. autoattribute:: ContourGroup.labels
.. autoattribute:: ContourGroup.legend
.. autoattribute:: ContourGroup.levels
.. autoattribute:: ContourGroup.lines
.. autoattribute:: ContourGroup.variable
.. autoattribute:: ContourGroup.variable_index

.. py:currentmodule:: tecplot.plot

ContourColorCutoff
^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColorCutoff

    **Attributes**

    .. autosummary::
        :nosignatures:

        inverted
        max
        min

.. autoattribute:: ContourColorCutoff.inverted
.. autoattribute:: ContourColorCutoff.max
.. autoattribute:: ContourColorCutoff.min

.. py:currentmodule:: tecplot.plot

ContourColormapFilter
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColormapFilter

    **Attributes**

    .. autosummary::
        :nosignatures:

        distribution
        fast_continuous_flood
        num_cycles
        reversed
        show_overrides
        zebra_shade

    **Methods**

    .. autosummary::

        override

.. autoattribute:: ContourColormapFilter.distribution
.. autoattribute:: ContourColormapFilter.fast_continuous_flood
.. autoattribute:: ContourColormapFilter.num_cycles
.. automethod:: ContourColormapFilter.override
.. autoattribute:: ContourColormapFilter.reversed
.. autoattribute:: ContourColormapFilter.show_overrides
.. autoattribute:: ContourColormapFilter.zebra_shade

.. py:currentmodule:: tecplot.plot

ContourColormapOverride
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColormapOverride

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        end_level
        show
        start_level

.. autoattribute:: ContourColormapOverride.color
.. autoattribute:: ContourColormapOverride.end_level
.. autoattribute:: ContourColormapOverride.show
.. autoattribute:: ContourColormapOverride.start_level

.. py:currentmodule:: tecplot.plot

ContourColormapZebraShade
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ContourColormapZebraShade

    **Attributes**

    .. autosummary::
        :nosignatures:

        color
        show

.. autoattribute:: ContourColormapZebraShade.color
.. autoattribute:: ContourColormapZebraShade.show

.. py:currentmodule:: tecplot.plot

ContourLabels
^^^^^^^^^^^^^

.. autoclass:: ContourLabels

    **Attributes**

    .. autosummary::
        :nosignatures:

        auto_align
        auto_generate
        background_color
        color
        font
        label_by_level
        margin
        show
        spacing
        step

.. autoattribute:: ContourLabels.auto_align
.. autoattribute:: ContourLabels.auto_generate
.. autoattribute:: ContourLabels.background_color
.. autoattribute:: ContourLabels.color
.. autoattribute:: ContourLabels.font
.. autoattribute:: ContourLabels.label_by_level
.. autoattribute:: ContourLabels.margin
.. autoattribute:: ContourLabels.show
.. autoattribute:: ContourLabels.spacing
.. autoattribute:: ContourLabels.step

.. py:currentmodule:: tecplot.plot

ContourLevels
^^^^^^^^^^^^^

.. autoclass:: ContourLevels

    **Methods**

    .. autosummary::

        add
        delete_nearest
        delete_range
        reset
        reset_levels
        reset_to_nice

.. automethod:: ContourLevels.add
.. automethod:: ContourLevels.delete_nearest
.. automethod:: ContourLevels.delete_range
.. automethod:: ContourLevels.reset
.. automethod:: ContourLevels.reset_levels
.. automethod:: ContourLevels.reset_to_nice

.. py:currentmodule:: tecplot.plot

ContourLines
^^^^^^^^^^^^

.. autoclass:: ContourLines

    **Attributes**

    .. autosummary::
        :nosignatures:

        mode
        pattern_length
        step

.. autoattribute:: ContourLines.mode
.. autoattribute:: ContourLines.pattern_length
.. autoattribute:: ContourLines.step

Streamtraces
------------

..  contents::
    :local:
    :depth: 1

.. py:currentmodule:: tecplot.plot

Streamtrace
^^^^^^^^^^^

.. autoclass:: Streamtrace


.. py:currentmodule:: tecplot.plot

StreamtraceRibbon
^^^^^^^^^^^^^^^^^

.. autoclass:: StreamtraceRibbon


Viewport
--------

..  contents::
    :local:
    :depth: 1

.. py:currentmodule:: tecplot.plot

ReadOnlyViewport
^^^^^^^^^^^^^^^^

.. autoclass:: ReadOnlyViewport

    **Attributes**

    .. autosummary::
        :nosignatures:

        bottom
        left
        right
        top

.. autoattribute:: ReadOnlyViewport.bottom
.. autoattribute:: ReadOnlyViewport.left
.. autoattribute:: ReadOnlyViewport.right
.. autoattribute:: ReadOnlyViewport.top

.. py:currentmodule:: tecplot.plot

Viewport
^^^^^^^^

.. autoclass:: Viewport

    **Attributes**

    .. autosummary::
        :nosignatures:

        bottom
        left
        right
        top

.. autoattribute:: Viewport.bottom
.. autoattribute:: Viewport.left
.. autoattribute:: Viewport.right
.. autoattribute:: Viewport.top

.. py:currentmodule:: tecplot.plot

Cartesian2DViewport
^^^^^^^^^^^^^^^^^^^

.. autoclass:: Cartesian2DViewport

    **Attributes**

    .. autosummary::
        :nosignatures:

        bottom
        left
        nice_fit_buffer
        right
        top
        top_snap_target
        top_snap_tolerance

.. autoattribute:: Cartesian2DViewport.bottom
.. autoattribute:: Cartesian2DViewport.left
.. autoattribute:: Cartesian2DViewport.nice_fit_buffer
.. autoattribute:: Cartesian2DViewport.right
.. autoattribute:: Cartesian2DViewport.top
.. autoattribute:: Cartesian2DViewport.top_snap_target
.. autoattribute:: Cartesian2DViewport.top_snap_tolerance

.. py:currentmodule:: tecplot.plot

PolarViewport
^^^^^^^^^^^^^

.. autoclass:: PolarViewport

    **Attributes**

    .. autosummary::
        :nosignatures:

        border_thickness
        bottom
        fill_color
        left
        right
        show_border
        top

.. autoattribute:: PolarViewport.border_thickness
.. autoattribute:: PolarViewport.bottom
.. autoattribute:: PolarViewport.fill_color
.. autoattribute:: PolarViewport.left
.. autoattribute:: PolarViewport.right
.. autoattribute:: PolarViewport.show_border
.. autoattribute:: PolarViewport.top

View
----

..  contents::
    :local:
    :depth: 1

.. py:currentmodule:: tecplot.plot

Cartesian2DView
^^^^^^^^^^^^^^^

.. autoclass:: Cartesian2DView

    **Methods**

    .. autosummary::

        fit

.. automethod:: Cartesian2DView.fit

.. py:currentmodule:: tecplot.plot

Cartesian3DView
^^^^^^^^^^^^^^^

.. autoclass:: Cartesian3DView

    **Methods**

    .. autosummary::

        fit

.. automethod:: Cartesian3DView.fit

.. py:currentmodule:: tecplot.plot

LineView
^^^^^^^^

.. autoclass:: LineView

    **Methods**

    .. autosummary::

        fit

.. automethod:: LineView.fit

.. py:currentmodule:: tecplot.plot

PolarView
^^^^^^^^^

.. autoclass:: PolarView

    **Methods**

    .. autosummary::

        fit

.. automethod:: PolarView.fit
