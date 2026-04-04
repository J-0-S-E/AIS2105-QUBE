# qube_bringup

En ROS2-pakke som inneholder launch- og konfigurasjonsfiler for å sette sammen hele Qube-systemet.

## Innhold

- `urdf/controlled_qube.urdf.xacro` – Scenefil som beskriver Quben med ros2_control-integrasjon
- `launch/bringup.launch.py` – Launch-fil som starter opp hele Qube-systemet

## Bruk
```bash
ros2 launch qube_bringup bringup.launch.py
```

Argumenter kan overstyres fra terminalen:
```bash
ros2 launch qube_bringup bringup.launch.py simulation:=false device:=/dev/ttyACM0
```

## Hva som startes opp

- **robot_state_publisher** – holder orden på robotens tilstand ved å publisere transformasjoner basert på URDF-en
- **controller_manager** – håndterer samhandlingen mellom controller-delen og hardware-delen i qube_driver
- **joint_state_broadcaster** – leser verdier fra hardware og publiserer posisjon og hastighet på `/joint_states`
- **velocity_controller** – tar imot hastighetskommandoer og sender de videre til hardware-delen
- **RViz** – visualisering av Quben

## Avhengigheter

- `qube_description`
- `qube_driver`
- `robot_state_publisher`
- `ros2_controllers`
- `rviz2`
