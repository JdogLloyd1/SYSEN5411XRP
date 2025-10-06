# File read/write 101
# store data onboard XRP as text/CSV then pull to laptop via Thonny

import os

# Write a simple text file
with open('hello.txt', 'w') as f:
    f.write('Hello, XRP!\n')

# Append more data
with open('hello.txt', 'a') as f:
    for i in range(3):
        f.write(f'Line {i}\n')

# Read it back
with open('hello.txt', 'r') as f:
    print(f.read())
    
# List files in current directory
print(os.listdir())