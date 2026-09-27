# Hypersphere.dm
# Dimension Language — v0.1

model Hypersphere {

    dimension {
        count: 4
        type: spatial
        coordinates: [x, y, z, w]
    }

    geometry {
        equation:
            x² + y² + z² + w² <= R²

        radius: R
        center: [0, 0, 0, 0]
    }

    topology {
        manifold: S3
        boundary: none
    }

    compactification {
        enabled: false
    }

    field {
        name: density

        definition:
            density(x,y,z,w) = 1
                if x² + y² + z² + w² <= R²
                else 0
    }

    observation {

        source_dimension: 4
        target_dimension: 3

        method: slice

        axis: w

        range: [-R, R]

        equation:
            r(w) = sqrt(R² - w²)
    }

    projection {

        target: 3D

        coordinates: [
            x,
            y,
            z
        ]
    }

    animation {

        parameter: w

        start: -R
        end: R
        steps: 100
    }

    render {

        display: 3D
        show_cross_section: true
        show_axis: w
        show_dimension_label: true
    }
}
