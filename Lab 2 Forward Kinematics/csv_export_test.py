# csv export test 


resultsMatrix = [[0.25, 2.0876822, 2.0675438], [0.5, 2.9670598, 3.0073364], [0.75, 3.2959874, 3.36982768], [1.0, 3.718894, 3.4973716]]
print(resultsMatrix)

# Export resultsMatrix to CSV file
csv_filename = 'Effort_and_Speed_Export.csv'
csv_path = csv_filename  # Save in the same folder

with open(csv_path, 'w') as file:
    # Write header
    file.write("Effort Level,Left Wheel Linear Speed (cm/s),Right Wheel Linear Speed (cm/s)\n")
    for row in resultsMatrix:
        # Convert each value to string and join with commas
        line = ','.join(str(value) for value in row) + '\n'
        file.write(line)