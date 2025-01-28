# DO NOT EDIT! This file was auto-generated by crates/build/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/store/re_types/definitions/rerun/archetypes/segmentation_image.fbs".

# You can extend this class by creating a "SegmentationImageExt" class in "segmentation_image_ext.py".

from __future__ import annotations

import numpy as np
from attrs import define, field

from .. import components, datatypes
from .._baseclasses import (
    Archetype,
    ComponentColumnList,
    DescribedComponentBatch,
)
from ..error_utils import catch_and_log_exceptions
from .segmentation_image_ext import SegmentationImageExt

__all__ = ["SegmentationImage"]


@define(str=False, repr=False, init=False)
class SegmentationImage(SegmentationImageExt, Archetype):
    """
    **Archetype**: An image made up of integer [`components.ClassId`][rerun.components.ClassId]s.

    Each pixel corresponds to a [`components.ClassId`][rerun.components.ClassId] that will be mapped to a color based on annotation context.

    In the case of floating point images, the label will be looked up based on rounding to the nearest
    integer value.

    See also [`archetypes.AnnotationContext`][rerun.archetypes.AnnotationContext] to associate each class with a color and a label.

    Example
    -------
    ### Simple segmentation image:
    ```python
    import numpy as np
    import rerun as rr

    # Create a segmentation image
    image = np.zeros((8, 12), dtype=np.uint8)
    image[0:4, 0:6] = 1
    image[4:8, 6:12] = 2

    rr.init("rerun_example_segmentation_image", spawn=True)

    # Assign a label and color to each class
    rr.log("/", rr.AnnotationContext([(1, "red", (255, 0, 0)), (2, "green", (0, 255, 0))]), static=True)

    rr.log("image", rr.SegmentationImage(image))
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/1200w.png">
      <img src="https://static.rerun.io/segmentation_image_simple/f8aac62abcf4c59c5d62f9ebc2d86fd0285c1736/full.png" width="640">
    </picture>
    </center>

    """

    # __init__ can be found in segmentation_image_ext.py

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            buffer=None,
            format=None,
            opacity=None,
            draw_order=None,
        )

    @classmethod
    def _clear(cls) -> SegmentationImage:
        """Produce an empty SegmentationImage, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    @classmethod
    def from_fields(
        cls,
        *,
        clear_unset: bool = False,
        buffer: datatypes.BlobLike | None = None,
        format: datatypes.ImageFormatLike | None = None,
        opacity: datatypes.Float32Like | None = None,
        draw_order: datatypes.Float32Like | None = None,
    ) -> SegmentationImage:
        """
        Update only some specific fields of a `SegmentationImage`.

        Parameters
        ----------
        clear_unset:
            If true, all unspecified fields will be explicitly cleared.
        buffer:
            The raw image data.
        format:
            The format of the image.
        opacity:
            Opacity of the image, useful for layering the segmentation image on top of another image.

            Defaults to 0.5 if there's any other images in the scene, otherwise 1.0.
        draw_order:
            An optional floating point value that specifies the 2D drawing order.

            Objects with higher values are drawn on top of those with lower values.

        """

        inst = cls.__new__(cls)
        with catch_and_log_exceptions(context=cls.__name__):
            kwargs = {
                "buffer": buffer,
                "format": format,
                "opacity": opacity,
                "draw_order": draw_order,
            }

            if clear_unset:
                kwargs = {k: v if v is not None else [] for k, v in kwargs.items()}  # type: ignore[misc]

            inst.__attrs_init__(**kwargs)
            return inst

        inst.__attrs_clear__()
        return inst

    @classmethod
    def cleared(cls) -> SegmentationImage:
        """Clear all the fields of a `SegmentationImage`."""
        return cls.from_fields(clear_unset=True)

    @classmethod
    def columns(
        cls,
        *,
        buffer: datatypes.BlobArrayLike | None = None,
        format: datatypes.ImageFormatArrayLike | None = None,
        opacity: datatypes.Float32ArrayLike | None = None,
        draw_order: datatypes.Float32ArrayLike | None = None,
    ) -> ComponentColumnList:
        """
        Construct a new column-oriented component bundle.

        This makes it possible to use `rr.send_columns` to send columnar data directly into Rerun.

        The returned columns will be partitioned into unit-length sub-batches by default.
        Use `ComponentColumnList.partition` to repartition the data as needed.

        Parameters
        ----------
        buffer:
            The raw image data.
        format:
            The format of the image.
        opacity:
            Opacity of the image, useful for layering the segmentation image on top of another image.

            Defaults to 0.5 if there's any other images in the scene, otherwise 1.0.
        draw_order:
            An optional floating point value that specifies the 2D drawing order.

            Objects with higher values are drawn on top of those with lower values.

        """

        inst = cls.__new__(cls)
        with catch_and_log_exceptions(context=cls.__name__):
            inst.__attrs_init__(
                buffer=buffer,
                format=format,
                opacity=opacity,
                draw_order=draw_order,
            )

        batches = [batch for batch in inst.as_component_batches() if isinstance(batch, DescribedComponentBatch)]
        if len(batches) == 0:
            return ComponentColumnList([])

        lengths = np.ones(len(batches[0]._batch.as_arrow_array()))
        columns = [batch.partition(lengths) for batch in batches]

        indicator_batch = DescribedComponentBatch(cls.indicator(), cls.indicator().component_descriptor())
        indicator_column = indicator_batch.partition(np.zeros(len(lengths)))

        return ComponentColumnList([indicator_column] + columns)

    buffer: components.ImageBufferBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=components.ImageBufferBatch._converter,  # type: ignore[misc]
    )
    # The raw image data.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    format: components.ImageFormatBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=components.ImageFormatBatch._converter,  # type: ignore[misc]
    )
    # The format of the image.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    opacity: components.OpacityBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=components.OpacityBatch._converter,  # type: ignore[misc]
    )
    # Opacity of the image, useful for layering the segmentation image on top of another image.
    #
    # Defaults to 0.5 if there's any other images in the scene, otherwise 1.0.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    draw_order: components.DrawOrderBatch | None = field(
        metadata={"component": True},
        default=None,
        converter=components.DrawOrderBatch._converter,  # type: ignore[misc]
    )
    # An optional floating point value that specifies the 2D drawing order.
    #
    # Objects with higher values are drawn on top of those with lower values.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]
