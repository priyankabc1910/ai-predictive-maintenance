# AI-Powered Predictive Maintenance & Reliability Intelligence Platform

An AI-powered predictive maintenance system that analyzes industrial
equipment sensor data to estimate Remaining Useful Life (RUL), identify
abnormal operating behavior, and provide evidence-grounded reliability
insights using maintenance knowledge retrieval.

The system combines machine learning, time-series feature engineering,
anomaly detection, retrieval-augmented generation (RAG), and an
interactive reliability dashboard into a unified decision-support platform.

---

## Problem Statement

Unexpected equipment failures can result in production downtime, expensive
repairs, and reduced operational reliability.

Traditional maintenance strategies often rely on fixed schedules or
reactive inspection after a failure occurs. Predictive maintenance instead
uses equipment condition data to identify degradation early and estimate
when maintenance may be required.

This project addresses the following question:

> **Given an equipment asset's operating history and sensor measurements,
> can we estimate its remaining useful life, detect abnormal behavior, and
> provide evidence-based reliability insights to an engineer?**

---

## Solution Overview

The platform processes time-series sensor measurements from equipment and
passes them through several intelligence layers:

**Sensor Data**
→ **Data Processing & Feature Engineering**
→ **RUL Prediction**
→ **Anomaly Detection**
→ **Reliability Intelligence**
→ **Maintenance Knowledge Retrieval**
→ **AI Reliability Copilot**
→ **Engineer Dashboard**

The machine-learning components provide quantitative predictions, while the
knowledge-retrieval layer provides supporting evidence for the resulting
insights.

---

## Key Capabilities

### Remaining Useful Life Prediction

Estimate the number of operating cycles remaining before the end of the
observed useful life of an equipment asset.

### Sensor-Based Degradation Analysis

Analyze temporal patterns in equipment sensor measurements to identify
signals associated with degradation.

### Anomaly Detection

Identify operating conditions that deviate significantly from expected
equipment behavior.

### Maintenance Knowledge Retrieval

Retrieve relevant information from maintenance documentation, historical
incidents, and equipment-related knowledge sources.

### AI Reliability Copilot

Combine model predictions, detected anomalies, historical information, and
retrieved documentation to generate evidence-grounded reliability insights.

### Reliability Dashboard

Provide engineers with an interface for monitoring:

- Equipment health
- RUL estimates
- Sensor trends
- Anomaly scores
- Degradation patterns
- Risk indicators
- Retrieved evidence
- AI-generated explanations

---

## Dataset

The initial implementation uses the **NASA C-MAPSS FD001 turbofan engine
degradation dataset**.

The dataset contains multivariate time-series observations from simulated
turbofan engine units operating until failure.

FD001 contains:

- 100 engine units
- 20,631 training observations
- 3 operational settings
- 21 sensor measurements
- 26 columns in total
- No missing values in the training data

The engine trajectories have different operating lifetimes, making the
dataset suitable for studying degradation and Remaining Useful Life
prediction.

> **Important:** C-MAPSS is a simulated research dataset. This project is a
> predictive-maintenance prototype and does not represent a deployed system
> operating on real aircraft or live industrial equipment.

---

## Machine Learning Problem

The primary prediction task is **Remaining Useful Life (RUL) estimation**.

For the training trajectories, RUL is derived from the observed degradation
history:

```text
RUL = Maximum observed cycle for the engine - Current cycle