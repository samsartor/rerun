# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/archetypes/scalar.fbs".

# You can extend this class by creating a "ScalarExt" class in "scalar_ext.py".

from __future__ import annotations

from typing import Any

import numpy as np
from attrs import define, field

from .. import components, datatypes
from .._baseclasses import (
    Archetype,
    ComponentColumnList,
    DescribedComponentBatch,
)
from ..error_utils import catch_and_log_exceptions

__all__ = ["Scalar"]


@define(str=False, repr=False, init=False)
class Scalar(Archetype):
    """
    **Archetype**: A double-precision scalar, e.g. for use for time-series plots.

    The current timeline value will be used for the time/X-axis, hence scalars
    cannot be static.

    When used to produce a plot, this archetype is used to provide the data that
    is referenced by [`archetypes.SeriesLine`][rerun.archetypes.SeriesLine] or [`archetypes.SeriesPoint`][rerun.archetypes.SeriesPoint]. You can do
    this by logging both archetypes to the same path, or alternatively configuring
    the plot-specific archetypes through the blueprint.

    Examples
    --------
    ### Simple line plot:
    ```python
    import math

    import rerun as rr

    rr.init("rerun_example_scalar", spawn=True)

    # Log the data on a timeline called "step".
    for step in range(0, 64):
        rr.set_time_sequence("step", step)
        rr.log("scalar", rr.Scalar(math.sin(step / 10.0)))
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/1200w.png">
      <img src="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/full.png" width="640">
    </picture>
    </center>

    ### Multiple scalars in a single `send_columns` call:
    ```python
    from __future__ import annotations

    import numpy as np
    import rerun as rr

    rr.init("rerun_example_scalar_send_columns", spawn=True)

    times = np.arange(0, 64)
    scalars = np.sin(times / 10.0)

    rr.send_columns(
        "scalars",
        indexes=[rr.TimeSequenceColumn("step", times)],
        columns=rr.Scalar.columns(scalar=scalars),
    )
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/scalar_send_columns/b4bf172256f521f4851dfec5c2c6e3143f5d6923/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/scalar_send_columns/b4bf172256f521f4851dfec5c2c6e3143f5d6923/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/scalar_send_columns/b4bf172256f521f4851dfec5c2c6e3143f5d6923/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/scalar_send_columns/b4bf172256f521f4851dfec5c2c6e3143f5d6923/1200w.png">
      <img src="https://static.rerun.io/scalar_send_columns/b4bf172256f521f4851dfec5c2c6e3143f5d6923/full.png" width="640">
    </picture>
    </center>

    """

    def __init__(self: Any, scalar: datatypes.Float64Like):
        """
        Create a new instance of the Scalar archetype.

        Parameters
        ----------
        scalar:
            The scalar value to log.

        """

        # You can define your own __init__ function as a member of ScalarExt in scalar_ext.py
        with catch_and_log_exceptions(context=self.__class__.__name__):
            self.__attrs_init__(scalar=scalar)
            return
        self.__attrs_clear__()

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            scalar=None,
        )

    @classmethod
    def _clear(cls) -> Scalar:
        """Produce an empty Scalar, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    @classmethod
    def from_fields(
        cls,
        *,
        clear_unset: bool = False,
        scalar: datatypes.Float64Like | None = None,
    ) -> Scalar:
        """
        Update only some specific fields of a `Scalar`.

        Parameters
        ----------
        clear_unset:
            If true, all unspecified fields will be explicitly cleared.
        scalar:
            The scalar value to log.

        """

        inst = cls.__new__(cls)
        with catch_and_log_exceptions(context=cls.__name__):
            kwargs = {
                "scalar": scalar,
            }

            if clear_unset:
                kwargs = {k: v if v is not None else [] for k, v in kwargs.items()}  # type: ignore[misc]

            inst.__attrs_init__(**kwargs)
            return inst

        inst.__attrs_clear__()
        return inst

    @classmethod
    def cleared(cls) -> Scalar:
        """Clear all the fields of a `Scalar`."""
        return cls.from_fields(clear_unset=True)

    @classmethod
    def columns(
        cls,
        *,
        scalar: datatypes.Float64ArrayLike | None = None,
    ) -> ComponentColumnList:
        """
        Construct a new column-oriented component bundle.

        This makes it possible to use `rr.send_columns` to send columnar data directly into Rerun.

        The returned columns will be partitioned into unit-length sub-batches by default.
        Use `ComponentColumnList.partition` to repartition the data as needed.

        Parameters
        ----------
        scalar:
            The scalar value to log.

        """

        inst = cls.__new__(cls)
        with catch_and_log_exceptions(context=cls.__name__):
            inst.__attrs_init__(
                scalar=scalar,
            )

        batches = [batch for batch in inst.as_component_batches() if isinstance(batch, DescribedComponentBatch)]
        if len(batches) == 0:
            return ComponentColumnList([])

        lengths = np.ones(len(batches[0]._batch.as_arrow_array()))
        columns = [batch.partition(lengths) for batch in batches]

        indicator_batch = DescribedComponentBatch(cls.indicator(), cls.indicator().component_descriptor())
        indicator_column = indicator_batch.partition(np.zeros(len(lengths)))

        return ComponentColumnList([indicator_column] + columns)

    scalar: components.ScalarBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=components.ScalarBatch._converter,  # type: ignore[misc]
    )
    # The scalar value to log.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
