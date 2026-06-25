# Inertial Navigation & Dead-Reckoning Specification

This file outlines the sensor fusion algorithms, error bias compensations, and coordinate propagation tracks when primary GNSS signals are unavailable.

## 1. Kalman Filter Sensor Fusion
* **High-Rate IMU Ingestion:** Samples raw 9-axis accelerometer, gyroscope, and magnetometer arrays continuously at high frequencies via local SPI buses.
* **Error State Covariance:** Runs localized error-state Kalman filtering (ESKF) to dynamically track and nullify sensor bias drift over extended operational durations.

## 2. Dead-Reckoning Odometry
* Fuses wheel encoder metrics or visual odometry vectors with inertial states to maintain precise vehicle positioning coordinates across contested or underground terrain.
