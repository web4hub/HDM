dm 0.1

model SpaceCapture {

    dimension 6

    axes [x,y,z,vx,vy,vz]

    target {
        type: orbital_object
        identifier: target_001

        state {
            position: [x,y,z]
            velocity: [vx,vy,vz]
        }

        physical {
            mass: 120.0
            radius: 0.85
            cooperative: true
        }
    }

    sensors {

        camera {
            enabled: true
            mode: optical_tracking
        }

        lidar {
            enabled: true
            range: 500.0
        }

        radar {
            enabled: true
            mode: relative_tracking
        }
    }

    tracking {
        method: state_estimation
        update_rate: 20
        coordinate_system: spacecraft_relative
    }

    capture {
        method: docking
        safety_radius: 5.0
        capture_radius: 1.0
        relative_speed_limit: 0.10
    }

    mission {

        phase search
        phase identify
        phase track
        phase approach
        phase capture
        phase verify

        transition {
            search -> identify
            identify -> track
            track -> approach
            approach -> capture
            capture -> verify
        }
    }

    observation {
        target: 3D
        method: projection
    }

    render {
        mode: orbital_scene
        interactive: true
    }
}
