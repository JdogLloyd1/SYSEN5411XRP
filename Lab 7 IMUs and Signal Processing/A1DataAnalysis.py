# Lab 7 - IMU and Signal Processing 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 27, 2025

# Goal:
# Task A1 - plot accelerometer data

import time
import math
import os
import pandas as pd
import matplotlib.pyplot as plt

# Read A1_accel_log.csv into a pandas DataFrame
csv_path = "A1_accel_log.csv"
if not os.path.exists(csv_path):
    # try relative to this script's directory
    script_dir = os.path.dirname(__file__)
    alt_path = os.path.join(script_dir, csv_path)
    if os.path.exists(alt_path):
        csv_path = alt_path
    else:
        raise FileNotFoundError(f"{csv_path} not found in {os.getcwd()} or {script_dir}")

df = pd.read_csv(csv_path)

# Ensure numeric types for expected columns and drop malformed rows
expected_cols = ['t_ms', 'ax_mg', 'ay_mg', 'az_mg', 'roll_acc_deg', 'pitch_acc_deg']
for col in expected_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['t_ms']).reset_index(drop=True)
df['t_s'] = df['t_ms'] / 1000.0

# Convert accelerations from mg to g for plotting (if present)
if 'ax_mg' in df.columns:
    df['ax_g'] = df['ax_mg'] / 1000.0
if 'ay_mg' in df.columns:
    df['ay_g'] = df['ay_mg'] / 1000.0
if 'az_mg' in df.columns:
    df['az_g'] = df['az_mg'] / 1000.0

# Create figures first, then call a single plt.show() so both windows open at once
fig1 = None
fig2 = None
if 'ax_g' in df.columns or 'ay_g' in df.columns or 'az_g' in df.columns:
    fig1 = plt.figure(figsize=(10, 6))
    if 'ax_g' in df.columns:
        plt.plot(df['t_s'], df['ax_g'], label='ax (g)', linewidth=0.8)
    if 'ay_g' in df.columns:
        plt.plot(df['t_s'], df['ay_g'], label='ay (g)', linewidth=0.8)
    if 'az_g' in df.columns:
        plt.plot(df['t_s'], df['az_g'], label='az (g)', linewidth=0.8)
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.title('A1 Accelerometer - ax / ay / az (g)')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()

if 'roll_acc_deg' in df.columns and 'pitch_acc_deg' in df.columns:
    fig2 = plt.figure(figsize=(10, 4))
    plt.plot(df['t_s'], df['roll_acc_deg'], label='roll (deg)')
    plt.plot(df['t_s'], df['pitch_acc_deg'], label='pitch (deg)')
    plt.xlabel('Time (s)')
    plt.ylabel('Degrees')
    plt.title('A1 Accelerometer-based Roll / Pitch')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

# Show all created figures at once (non-blocking depends on backend); calling once opens all figures together
plt.show()

