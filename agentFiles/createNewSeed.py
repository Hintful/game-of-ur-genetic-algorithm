import sys
import random

minRange = float(sys.argv[1])
maxRange = float(sys.argv[2])

for agentIndex in range(1, 12):
    with open("a" + f'{agentIndex:02}', 'w') as f:
        for gene in range(0, 10):
            f.write(str(round(random.uniform(minRange, maxRange), 2)) + '\n')
        f.close()
