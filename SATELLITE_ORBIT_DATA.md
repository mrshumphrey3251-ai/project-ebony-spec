# Satellite Orbit Tracking & Ephemeris Database Specification

This document details the parsing parameters for Two-Line Element (TLE) sets, orbital mechanics propagation routines, and look-angle calculations for satellite communication arrays.

## 1. Local Simplified General Perturbations (SGP4) Execution
* **Offline Vector Calculations:** Runs the SGP4 propagation model natively on edge processors using locally cached TLE datasets to compute exact satellite position vectors without internet dependencies.
* **Look-Angle Determination:** Calculates precise local azimuth, elevation, and range metrics relative to the node's current coordinates to guide active directional antennas.

## 2. Ephemeris Refresh Integrity
* Accepts updated orbital parameter blocks over verified mesh bursts, validating signature structures before replacing the active localized satellite positioning matrix.
