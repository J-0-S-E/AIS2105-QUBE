# qube_controller

En ROS2-pakke som inneholder en PID-regulator for å styre Qube-roboten.

## Innhold

- `qube_controller/qube_controller.py` – ROS2-node som implementerer en PID-regulator for Quben

## Bruk
```bash
ros2 run qube_controller qube_controller
```

## Hvordan det fungerer

Noden abonnerer på `/joint_states` for å lese posisjon og hastighet fra Quben.
En PID-regulator beregner et hastighets-pådrag basert på avviket fra ønsket posisjon.
Pådraget publiseres til `/velocity_controller/commands` som en `Float64MultiArray`.

## Topics

| Topic | Type | Beskrivelse |
|-------|------|-------------|
| `/joint_states` | `sensor_msgs/JointState` | Innkommende posisjon og hastighet |
| `/velocity_controller/commands` | `std_msgs/Float64MultiArray` | Utgående hastighetskommando |

## PID-parametere

PID-parameterne `kp`, `ki` og `kd` kan justeres i koden og i vinduet som dukker opp ved kjøring av programmet.
Anbefaling: Start med kun P-ledd (`ki=0`, `kd=0`) og juster derfra. Man trenger ikke ha høye verdier på parameterne (Prøv <5)
