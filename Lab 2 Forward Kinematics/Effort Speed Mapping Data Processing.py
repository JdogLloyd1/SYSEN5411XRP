
# Data Processing

import pandas as pd
import matplotlib.pyplot as plt

rowLabels = ["25%", "50%", "75%", "100%"]
columnLabels = ["Effort Level", "Left Wheel Linear Speed (cm/s)", "Right Wheel Linear Speed (cm/s)"]

csv_filepath = 'C:\Users\jonyl\iCloudDrive\Documents\GitHub\SYSEN5411XRP\Effort_and_Speed_Export.csv'

# Convert to DataFrame for easy processing
resultsDF = pd.read_csv(csv_filepath, header=0)
print(resultsDF)

# Create two subplots: one for the line plot, one for the table
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

# Line plot on the first subplot
ax1.plot(resultsDF["Effort Level"], resultsDF["Left Wheel Linear Speed (cm/s)"], marker="o", label=columnLabels[1], color='blue')
ax1.plot(resultsDF["Effort Level"], resultsDF["Right Wheel Linear Speed (cm/s)"], marker="o", label=columnLabels[2], color='red')
ax1.set_xlim([0, 1.25])
ax1.set_xlabel(columnLabels[0])
ax1.set_ylabel("Wheel Linear Speed (cm/s)")
ax1.set_title("Lab 2 Part 1 - XRP PWM Effort vs Linear Speed")
ax1.legend()
ax1.grid()

# Hide axes for the table subplot
ax2.axis('off')

# Add table to the second subplot
table = ax2.table(cellText=resultsDF.values,
				  rowLabels=rowLabels,
				  colLabels=columnLabels,
				  loc='center',
				  cellLoc='center')

plt.tight_layout()
plt.show()