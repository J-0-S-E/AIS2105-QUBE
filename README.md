# Quanser QUBE – ROS2 Mini-prosjekt

Styring og visualisering av en Quanser Qube med ROS2, PID-regulator og RViz.

**Gruppemedlemmer:** Arman C. Valseth, Kristian Løkkeberg

## Pakker

| Pakke | Beskrivelse | Viktige filer |
|-------|-------------|---------------|
| `qube_description` | URDF-beskrivelse av Quben med xacro-makro. Svart boks, rød disk, hvit viser. Kan visualiseres alene i RViz. | `urdf/qube.macro.xacro`, `urdf/qube.urdf.xacro`, `launch/view_qube.launch.py` |
| `qube_driver` | Hardware-grensesnitt via ROS2 Control. Håndterer seriellkommunikasjon mot Teensy 4.1 og simulert hardware. | `ros2_control/qube_driver.ros2_control.xacro`, `launch/qube_driver.launch.py` |
| `qube_bringup` | Setter sammen hele systemet i én launch-fil. Starter RViz, robot_state_publisher, controller_manager og velocity_controller. | `urdf/controlled_qube.urdf.xacro`, `launch/bringup.launch.py` |
| `qube_controller` | PID-regulator som leser posisjon fra `/joint_states` og sender pådrag til `/velocity_controller/commands`. Parametere kan justeres i sanntid via `rqt_reconfigure`. | `qube_controller/qube_controller.py` |

Alle pakkene ligger under `src/`.

## Oppsett

Klon repoet inn i ROS2-workspacen din. Vi tar utgangspunkt i at det ligger
under `~/ros2_ws/QUBE`, men du kan kalle mappen hva du vil.

```bash
cd ~/ros2_ws
git clone git@github.com:J-0-S-E/AIS2105-QUBE.git QUBE
cd QUBE
source ~/ros2_ws/install/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Kun visualisering (uten kontroller)

```bash
ros2 launch qube_description view_qube.launch.py
```

## Kjør

```bash
ros2 launch qube_bringup bringup.launch.py simulation:=false device:=/dev/ttyACM0
```

Starter opp RViz, ROS2 Control og kobler til den fysiske Quben. Dropp `simulation:=false device:=/dev/ttyACM0` om du bare vil kjøre simulering.

### Start kontrolleren

I en ny terminal:
```bash
source ~/ros2_ws/QUBE/install/setup.bash
ros2 run qube_controller qube_controller
```

## Justere parametere

Åpne `rqt_reconfigure` i en ny terminal:
```bash
ros2 run rqt_reconfigure rqt_reconfigure
```

Under `qube_controller` kan du endre:

| Parameter | Beskrivelse |
|-----------|-------------|
| `kp` | Proporsjonalforsterkning |
| `ki` | Integralforsterkning |
| `kd` | Derivatforsterkning |
| `target_position` | Referansevinkel i radianer |

Tips: Start med kun P-ledd (`ki=0`, `kd=0`) og juster derfra.

## Topics

Noden abonnerer på `/joint_states` for å lese posisjon og hastighet fra Quben. En PID-regulator beregner et hastighets-pådrag basert på avviket fra ønsket posisjon. Pådraget publiseres til `/velocity_controller/commands` som en `Float64MultiArray`.

| Topic | Type | Retning |
|-------|------|---------|
| `/joint_states` | `sensor_msgs/JointState` | Inn (posisjon og hastighet) |
| `/velocity_controller/commands` | `std_msgs/Float64MultiArray` | Ut (pådrag fra PID) |

## Avhengigheter

```bash
sudo apt install -y ros-jazzy-ros2-control ros-jazzy-ros2-controllers
```
