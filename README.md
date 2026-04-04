# Quanser QUBE – ROS2 Mini-prosjekt

Styring og visualisering av en Quanser Qube med ROS2, PID-regulator og RViz.

**Gruppemedlemmer:** Arman C. Valseth, Kristian Løkkeberg

## Pakker

| Pakke | Beskrivelse | Viktige filer |
|-------|-------------|---------------|
| `qube_description` | URDF-beskrivelse av Quben | `urdf/qube.macro.xacro`, `urdf/qube.urdf.xacro`, `launch/view_qube.launch.py` |
| `qube_driver` | Hardware-grensesnitt (ROS2 Control) | `ros2_control/qube_driver.ros2_control.xacro`, `launch/qube_driver.launch.py` |
| `qube_bringup` | Launch-filer som setter alt sammen | `urdf/controlled_qube.urdf.xacro`, `launch/bringup.launch.py` |
| `qube_controller` | PID-regulator | `qube_controller/qube_controller.py` |

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

Starter opp RViz, ROS2 Control og kobler til den fysiske Quben. Ta bort `simulation:=false device:=/dev/ttyACM0` om du bare vil kjøre simulering.

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

## Avhengigheter

```bash
sudo apt install -y ros-jazzy-ros2-control ros-jazzy-ros2-controllers
```
