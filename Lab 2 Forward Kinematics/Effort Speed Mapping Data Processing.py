
# Data Processing

import pandas as pd
import matplotlib.pyplot as plt

resultsMatrix = [[0.25, 6911.5032, 6863.1716], [0.5, 10705.584, 10657.25], [0.75, 12373.043, 12276.379], [1.0, 13581.347, 13194.688]]

rowLabels = ["25%", "50%", "75%", "100%"]
columnLabels = ["Effort Level", "Left Wheel Linear Speed (cm/s)", "Right Wheel Linear Speed (cm/s)"]

# Convert to DataFrame for easy processing
resultsDF = pd.DataFrame(resultsMatrix, rowLabels, columnLabels)
print(resultsDF)

# Plot data and table
plt.figure(0)
plt.plot(resultsDF["Effort Level"], resultsDF["Left Wheel Linear Speed (cm/s)"], marker="o", label = columnLabels[1], color = 'blue') # plot first column Left motor
plt.plot(resultsDF["Effort Level"], resultsDF["Right Wheel Linear Speed (cm/s)"], marker="o", label = columnLabels[2], color = 'red') # plot second column Right motor
plt.xlim([0, 1.25])
plt.xlabel(columnLabels[0])
plt.ylabel("Wheel Linear Speed (cm/s)")
plt.title("Lab 2 Part 1 - XRP PWM Effort vs Linear Speed")
plt.legend()
plt.grid()
plt.show()