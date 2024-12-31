# Simple Patrolling Behavior

## Overview
This project implements a **Simple Patrolling Behavior** using ROS2. Robots navigate autonomously between predefined waypoints(environment) while avoiding obstacles, showcasing efficient path planning and navigation.

## Features
- Autonomous patrolling between waypoints.
- Obstacle avoidance using sensor data of Lazer Scan.
- Simulation tested in Gazebo with TurtleBot3.

## Project Structure
- **notebook_ws/**: Contains Jupyter notebooks for analysis and visualization.
    -   *Note* : this Mateirial is from https://app.theconstruct.ai/
- **ros2_ws/**: ROS2 workspace with the main source code.
- **simulation_ws/**: Simulation files and configurations for Gazebo.
- **webpage_ws/**: Optional web interface for monitoring robot status.

## Requirements
- **ROS2 Humble/Foxy**
- **Gazebo Simulator**
- **TurtleBot3 Packages**

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Simple-Patrolling-Behavior.git
   cd Simple-Patrolling-Behavior

## Test your program in the simulation
```bash
    ros2 launch patrol_behavior start_patrolling.launch.py
