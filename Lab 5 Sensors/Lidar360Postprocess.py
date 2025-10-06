# Lab 5 - Sensors TST 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 5, 2025

# Goal:
# Postprocess lidar csv data to create a polar plot

import pandas as pd
import matplotlib.pyplot as plt

# Read in csv data
df = pd.read_csv('Lab 5 Sensors\scan.csv')

# Create polar plot (scatter plot without lines)
plt.polar(df['Degree'], df['Range'], marker='o', linestyle='None')
plt.title('Lidar Scan')
plt.xlabel('Degree')
plt.ylabel('Range')
plt.show()

# Save plot to png
plt.savefig('lidar_scan_polar_plot.png')