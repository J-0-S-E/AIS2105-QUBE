# qube_description

En ROS2-pakke som inneholder URDF-beskrivelsen av Qube-roboten.

## Innhold

- `urdf/qube.macro.xacro` – Gjenbrukbar xacro-makro som beskriver Quben (svart boks, rød spinnende disk, hvit viser)
- `urdf/qube.urdf.xacro` – Enkel scenefil som plasserer Quben i origo, beregnet for visualisering
- `launch/view_qube.launch.py` – Launch-fil som starter robot_state_publisher og RViz for å visualisere Quben

## Bruk
```bash
ros2 launch qube_description view_qube.launch.py
```
