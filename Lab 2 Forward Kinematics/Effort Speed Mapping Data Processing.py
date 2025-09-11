
# Data Processing

import pandas as pd
import matplotlib.pyplot as plt

resultsMatrix = [[0.25, 6911.5032, 6863.1716], [0.5, 10705.584, 10657.25], [0.75, 12373.043, 12276.379], [1.0, 13581.347, 13194.688]]

rowLabels = ["25%", "50%", "75%", "100%"]
columnLabels = ["Effort Level", "Left Wheel Linear Speed (cm/s)", "Right Wheel Linear Speed (cm/s)"]

# Convert to DataFrame for easy processing
resultsDF = pd.DataFrame(resultsMatrix, rowLabels, columnLabels)
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
table = ax2.table(cellText=resultsMatrix,
				  rowLabels=rowLabels,
				  colLabels=columnLabels,
				  loc='center',
				  cellLoc='center')

plt.tight_layout()
plt.show()