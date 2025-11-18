# Lab 8 - 1D Kalman Filter
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: November 8, 2025

# Goal:
# Analyze & Plot Wall Follow Data with a 1D Kalman Filter

import matplotlib.pyplot as plt
import csv
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

########################################################
# Data collection and preprocessing
########################################################

# List to store sensor data

time_stamps = []
left_encoders = []
right_encoders = []
rangefinder_distances = []
# Read data from data.csv
with open('Lab 8 Kalman Filtering\\data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 4:
            continue # skip if row is malformed
        
        t = float(row[0])
        left = float(row[1])
        right = float(row[2])
        rangefinder = float(row[3])

        # Append data to lists
        time_stamps.append(t)
        left_encoders.append(left)
        right_encoders.append(right)
        rangefinder_distances.append(rangefinder)

# Compute average encoder position 
avg_encoders = [(l + r) / 2 for l, r in zip(left_encoders,
right_encoders)]
# Adjust rangefinder distances to be relative to the starting position
rangefinder_distances = [d - rangefinder_distances[0] for d in
rangefinder_distances]


########################################################
# Estimate sensor noise and process noise
########################################################

# Simple 1D Kalman Filter (scalar form)
# State is position along the line; prediction uses last estimate +
# encoder step change, measurement uses rangefinder_distances

# Lists to store filtered positions, Kalman gains, and estimate noises
filtered_positions = []
kalman_gains = []

# Global, tunable noise parameters (students can tweak these)
PROCESS_NOISE_Q = 1e-1 # process noise
SENSOR_NOISE_R = 1 # measurement noise

# Enable dynamic adjustment of sensor noise (optional feature)
# Dynamic sensor noise is when the sensor noise is adjusted based on the
# difference between the measurement and the previous filter estimate
# Try running the filter with dynamic_sensor_noise set to False to see
# the difference
dynamic_sensor_noise = True

# Precompute a list of process noise values (same value for all time
# steps here)
process_noises = [PROCESS_NOISE_Q]*len(time_stamps)

# Dynamically adjust sensor noise for each time step (if enabled)
# If the difference between measurement and previous filter estimate is
# large, distrust measurement
# and increase measurement noise (trust prediction more).
sensor_noises = [SENSOR_NOISE_R]*len(time_stamps)
for i in range(len(time_stamps)):
    # If the difference between measurement and previous filter estimate
    # is large, distrust measurement
    # and increase measurement noise (trust prediction more).
    if i > 0:
        if dynamic_sensor_noise and abs(rangefinder_distances[i] -
                                         rangefinder_distances[i-1]) > 3:
            sensor_noises[i] = SENSOR_NOISE_R * 10
        else:
            sensor_noises[i] = SENSOR_NOISE_R
    else:
        sensor_noises[i] = SENSOR_NOISE_R
# List to store estimate variances. This is the variance of the estimate
# of the position produced by the Kalman filter.
estimate_noises = []


########################################################
# Kalman Filter Implementation
########################################################

# Initialize estimate with the first encoder value (could also use first
# measurement) and variance
x_est = avg_encoders[0]
P = 1.0

# Append initial estimate to filtered positions list.
filtered_positions.append(x_est)

# Append initial estimate variance to estimate noises list
estimate_noises.append(P)

# Loop from the second sample onward
for i in range(1, len(time_stamps)):
    # Predict step: last estimate + step change in encoder readings
    delta_encoder = avg_encoders[i] - avg_encoders[i-1]
    # Use the delta encoder to predict the prior estimate
    x_prior = x_est + delta_encoder
    # Add the process noise to the prior estimate variance
    P = P + process_noises[i]
    # Update step with rangefinder measurement
    z = rangefinder_distances[i]
    # Calculate the Kalman gain
    K = P / (P + sensor_noises[i])
    # Update the estimate with the Kalman gain
    x_est = x_prior + K * (z - x_prior)
    # Update the estimate variance with the Kalman gain
    P = (1 - K) * P

    filtered_positions.append(x_est)
    kalman_gains.append(K)
    estimate_noises.append(P)


########################################################
# Plotting Matplotlib
########################################################
# Plot average encoder position and rangefinder distance vs. time
plt.figure(figsize=(10, 6))
plt.plot(time_stamps, avg_encoders, label="Average Encoder Position")
plt.plot(time_stamps, rangefinder_distances, label="Rangefinder Distance")
if filtered_positions:
    plt.plot(time_stamps, filtered_positions, label="Kalman Filtered Position")
plt.xlabel("Time (s)")
plt.legend()
plt.title("Average Encoder Position and Rangefinder Distance vs. Time")

# plt.savefig('data_plot_matplotlib.png')
# Uncomment this to show the plot in a new window
plt.show()


########################################################
# Plotting Plotly
########################################################

# Set renderer to browser
pio.renderers.default = "browser"

fig = go.Figure()

# Error band for avg_encoders: process_noises (using variance)
avg_encoders_upper = np.array(avg_encoders) + process_noises
avg_encoders_lower = np.array(avg_encoders) - process_noises
fig.add_trace(go.Scatter(
    x=time_stamps + time_stamps[::-1],
    y=np.concatenate([avg_encoders_upper, avg_encoders_lower[::-1]]),
    fill='toself',
    fillcolor='rgba(0, 65, 255, 0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name="Encoder ±variance (process noise)"
))
fig.add_trace(go.Scatter(
    x=time_stamps, y=avg_encoders, mode='lines', name="Average Encoder Position",
    line=dict(color="rgb(0, 65, 255)")
))

# Error band for rangefinder: sensor_noises (using variance)
rangefinder_upper = np.array(rangefinder_distances) + sensor_noises
rangefinder_lower = np.array(rangefinder_distances) - sensor_noises
fig.add_trace(go.Scatter(
    x=time_stamps + time_stamps[::-1],
    y=np.concatenate([rangefinder_upper, rangefinder_lower[::-1]]),
    fill='toself',
    fillcolor='rgba(255, 0, 0, 0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name="Rangefinder ±variance (sensor noise)"
))
fig.add_trace(go.Scatter(
    x=time_stamps, y=rangefinder_distances, mode='lines', name="Rangefinder Distance",
    line=dict(color="rgb(255, 127, 14)")
))

# Error band for Kalman filtered: estimate_noises (using variance)
if filtered_positions and len(filtered_positions) == len(estimate_noises):
    filtered_upper = np.array(filtered_positions) + estimate_noises
    filtered_lower = np.array(filtered_positions) - estimate_noises
    fig.add_trace(go.Scatter(
        x=time_stamps + time_stamps[::-1],
        y=np.concatenate([filtered_upper, filtered_lower[::-1]]),
        fillcolor='rgba(44, 160, 44, 0.14)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name="Kalman ±variance (estimate noise)"
    ))
    fig.add_trace(go.Scatter(
        x=time_stamps, y=filtered_positions, mode='lines', name="Kalman Filtered Position",
        line=dict(color="rgb(44, 160, 44)")
    ))
elif filtered_positions:
    fig.add_trace(go.Scatter(
        x=time_stamps, y=filtered_positions, mode='lines', name="Kalman Filtered Position"
    ))

fig.update_layout(
    title="Average Encoder Position and Rangefinder Distance vs. Time",
    xaxis_title="Time (s)",
    yaxis_title="Value",
    legend=dict(x=1, y=0, xanchor='right', yanchor='bottom')
)

fig.show()