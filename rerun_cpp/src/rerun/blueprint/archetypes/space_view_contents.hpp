// DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/cpp/mod.rs
// Based on "crates/re_types/definitions/rerun/blueprint/archetypes/space_view_contents.fbs".

#pragma once

#include "../../blueprint/components/query_expression.hpp"
#include "../../collection.hpp"
#include "../../data_cell.hpp"
#include "../../indicator_component.hpp"
#include "../../result.hpp"

#include <cstdint>
#include <utility>
#include <vector>

namespace rerun::blueprint::archetypes {
    /// **Archetype**: The contents of a `SpaceView`.
    struct SpaceViewContents {
        /// The `QueryExpression` that populates the contents for the `SpaceView`.
        ///
        /// They determine which entities are part of the spaceview.
        rerun::blueprint::components::QueryExpression query;

      public:
        static constexpr const char IndicatorComponentName[] =
            "rerun.blueprint.components.SpaceViewContentsIndicator";

        /// Indicator component, used to identify the archetype when converting to a list of components.
        using IndicatorComponent = rerun::components::IndicatorComponent<IndicatorComponentName>;

      public:
        SpaceViewContents() = default;
        SpaceViewContents(SpaceViewContents&& other) = default;

        explicit SpaceViewContents(rerun::blueprint::components::QueryExpression _query)
            : query(std::move(_query)) {}

        /// Returns the number of primary instances of this archetype.
        size_t num_instances() const {
            return 1;
        }
    };

} // namespace rerun::blueprint::archetypes

namespace rerun {
    /// \private
    template <typename T>
    struct AsComponents;

    /// \private
    template <>
    struct AsComponents<blueprint::archetypes::SpaceViewContents> {
        /// Serialize all set component batches.
        static Result<std::vector<DataCell>> serialize(
            const blueprint::archetypes::SpaceViewContents& archetype
        );
    };
} // namespace rerun
