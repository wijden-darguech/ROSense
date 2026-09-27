# ROSense — Robot mobile différentiel simulé sous ROS2 Jazzy & Gazebo Harmonic

Simulation complète d'un robot mobile à entraînement différentiel, construit avec Xacro, doté d'un LiDAR 2D et d'une centrale inertielle (IMU), piloté au clavier dans Gazebo Harmonic via ROS2 Jazzy.

## Aperçu

Ce projet couvre la chaîne complète de la robotique mobile simulée :

- **Modélisation** du robot en Xacro (châssis, deux roues motrices, roue folle)
- **Propriétés physiques** réalistes (masses, matrices d'inertie calculées analytiquement, collisions)
- **Contrôle différentiel** via le plugin `gz-sim-diff-drive-system`
- **Capteurs simulés** : LiDAR 2D (`gpu_lidar`) et IMU (accéléromètre + gyroscope, avec bruit gaussien et biais)
- **Pont ROS2 ↔ Gazebo** (`ros_gz_bridge`) pour `/cmd_vel`, `/odom`, `/tf`, `/joint_states`, `/scan`, `/imu`, `/clock`
- **Téléopération clavier** via `teleop_twist_keyboard`
- **Visualisation** RViz2 (RobotModel, TF, LaserScan, IMU)

## Stack technique

| Composant | Version / Outil |
|---|---|
| OS | Ubuntu 24.04 LTS |
| ROS2 | Jazzy |
| Simulateur | Gazebo Harmonic (gz-sim 8) |
| Moteur physique | DART (dartsim) |
| Description robot | URDF / Xacro |
| Environnement | Machine virtuelle (VMware) |

## Structure du package

```
xacro_first/
├── urdf/
│   ├── my_robot.urdf.xacro       # Description géométrique et physique du robot
│   └── my_robot.gazebo.xacro     # Plugins Gazebo (diff-drive, capteurs, matériaux)
├── world/
│   └── my_robot.sdf              # Monde de simulation (physique, sol, lumière)
├── parametres/
│   └── parametres.yaml           # Configuration du bridge ROS2 <-> Gazebo
└── launch/
    └── xacro_first_launch_file.launch.py
```

> La visualisation RViz2 (RobotModel, TF, LaserScan, Imu) est configurée manuellement au lancement : Fixed Frame `odom`, puis ajout des displays via **Add**.

## Robot simulé

- Châssis rectangulaire avec 2 roues motrices (contrôle différentiel) + 1 roue folle
- LiDAR 2D 360°, 721 points, portée 0.12–12 m, bruit gaussien
- IMU (gyroscope + accéléromètre 3 axes, bruit + biais)
- Masses et inerties calculées à partir de densités réalistes par matériau

## Lancer la simulation

```bash
cd ~/ros2_ws
colcon build --packages-select xacro_first
source install/setup.bash
ros2 launch xacro_first xacro_first_launch_file.launch.py
```

Dans un second terminal, pour piloter le robot au clavier :

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Pour visualiser les capteurs et le TF tree, lance RViz2 puis configure manuellement : Fixed Frame `odom`, **Add → RobotModel**, **Add → TF**, **Add → LaserScan** (topic `/scan`), **Add → Imu** (topic `/imu`) :

```bash
rviz2
```

## Vérifier les topics

```bash
ros2 topic list
ros2 topic echo /scan
ros2 topic echo /imu
ros2 run tf2_ros tf2_echo odom base_link
```

## Points techniques notables

- **Fusion de liens (link lumping)** : les liens connectés par des joints `fixed` sont fusionnés par le moteur physique. Le LiDAR nécessitant d'exister comme entité de scène distincte pour son pipeline de rendu, son joint est déclaré `revolute` avec des limites verrouillées (`lower="0" upper="0"`) plutôt que `fixed`.
- **Rendu 3D sous VM** : le capteur LiDAR (`gpu_lidar`) nécessite une accélération graphique fonctionnelle (Ogre2). Un environnement avec accélération 3D correctement configurée est requis pour la stabilité du rendu.
- **Synchronisation temporelle** : tous les nœuds ROS2 utilisent `use_sim_time: true` pour rester synchronisés sur l'horloge simulée de Gazebo plutôt que l'horloge système.

## Auteure

Wijden Darguech — étudiante en ingénierie (INSAT, Tunisie), spécialisation Instrumentation et Maintenance Industrielle, orientée GNC / robotique.

[GitHub](https://github.com/wijden-darguech)
