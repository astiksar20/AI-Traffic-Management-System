# APPLICATIONS OF IMAGE PROCESSING TECHNIQUES IN CYBER-PHYSICAL SYSTEMS
Intelligent Traffic Congestion Analysis and Adaptive Signal Control with YOLOv8


## Overview

This project presents an AI-powered Cyber-Physical Traffic Management System that dynamically adjusts traffic signal timings using Computer Vision and Adaptive Signal Control.

The system utilizes YOLOv8 for vehicle detection, computes multiple traffic parameters, performs congestion analysis, and controls a physical traffic signal prototype through Arduino communication.

The current implementation focuses on a single traffic cross-section as a proof-of-concept prototype.

---

## Key Features

* Dynamic ROI (Region of Interest) Selection
* Real-Time Vehicle Detection using YOLOv8
* Vehicle Count Estimation
* Occupancy Ratio Calculation
* Queue Depth Estimation
* Exponential Smoothing for Stable Measurements
* Weighted Congestion Analysis
* Adaptive Traffic Signal Control
* Serial Communication with Arduino
* Edge Computing-Based Processing

The sample traffic video used during testing is not included in this repository. The system supports dynamic ROI selection and can operate with any compatible traffic video input.
---
## System Workflow

Traffic Video Feed

↓

Dynamic ROI Selection

↓

YOLOv8 Vehicle Detection

↓

Vehicle Count + Occupancy Ratio + Queue Depth

↓

Exponential Smoothing

↓

Congestion Analysis Engine

↓

HIGH / LOW Congestion Classification

↓

Arduino Traffic Signal Controller

↓

Adaptive Traffic Signal Operation

---

## Traffic Parameters

The system computes three major traffic parameters:

### Vehicle Count

Number of vehicles detected within the selected ROI.

### Occupancy Ratio

Ratio of road area occupied by vehicles within the ROI.

### Queue Depth

Estimated queue length based on vehicle distance from the signal reference line.

---

## Congestion Analysis

Congestion is determined using a weighted multi-parameter model:

Congestion Score =

0.40 × Occupancy Ratio

*

0.40 × Queue Depth

*

0.20 × Vehicle Count

This approach provides more reliable congestion estimation than vehicle counting alone.

---

## Signal Control Logic

### Analysis Phase

While ROI selection and traffic analysis are being performed, the traffic signal remains continuously GREEN.

This indicates that the system is actively processing traffic data and no congestion decision has yet been finalized.

### LOW Congestion

* Red Signal = 10 seconds
* Green Signal = 5 seconds
* Yellow Signal = 2 seconds

### HIGH Congestion

* Red Signal = 5 seconds
* Green Signal = 12 seconds
* Yellow Signal = 2 seconds

Once the congestion status is determined, the corresponding signal cycle continues repeatedly until the user presses Q to terminate the execution.

---

## Technologies Used

### Software

* Python
* YOLOv8
* OpenCV
* PySerial
* Arduino IDE

### Hardware

* Arduino Uno
* Traffic Signal LEDs

### Computing Paradigm

* Edge Computing

All traffic analysis, object detection, parameter computation, congestion classification, and decision-making are performed locally on the host machine without relying on cloud services.

---

## Dataset / Input

The sample traffic video used during testing is not included in this repository.

The system supports dynamic ROI selection and can operate with any compatible traffic video input.

---

## Future Scope

* IoT Integration
* Cloud Dashboard
* Multi-Intersection Coordination
* Emergency Vehicle Prioritization
* Predictive Traffic Analytics
* Smart City Deployment

---

## Impact

* Reduced Traffic Congestion
* Improved Traffic Flow
* Reduced Waiting Time
* Better Road Utilization
* Scalable Smart Transportation Infrastructure
