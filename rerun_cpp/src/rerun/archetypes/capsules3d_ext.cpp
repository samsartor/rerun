#if 0

#include "capsules3d.hpp"

namespace rerun::archetypes {
    // <CODEGEN_COPY_TO_HEADER>

    /// Creates a new `Capsules3D` with the given axis-aligned lengths and radii.
    ///
    /// For multiple capsules, you should generally follow this with
    /// `Capsules3D::with_translations()` and one of the rotation methods, in order to move them
    /// apart from each other.
    //
    // TODO(andreas): This should not take an std::vector.
    static Capsules3D from_lengths_and_radii(
        const std::vector<float>& lengths, const std::vector<float>& radii
    ) {
        return Capsules3D().with_lengths(std::move(lengths)).with_radii(std::move(radii));
    }

    /* TODO(kpreid): This should exist for parity with Rust, but actually implementing this
           needs a bit of quaternion math.

        /// Creates a new `Capsules3D` where each capsule extends between the given pairs of points.
        //
        // TODO(andreas): This should not take an std::vector.
        //
        static Capsules3D from_endpoints_and_radii(
            const std::vector<datatypes::Vec3D>& start_points,
            const std::vector<datatypes::Vec3D>& end_points,
            const std::vector<float>& radii
        );
        */

    // </CODEGEN_COPY_TO_HEADER>
} // namespace rerun::archetypes

#endif
