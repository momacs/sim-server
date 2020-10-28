import time
import psutil
import matplotlib.pyplot as plt

# Set the positon of the subplot
fig = plt.figure()
ax = fig.add_subplot(111) 

# Arrays that will be used for our x and y 
# values
i = 0
x, y = [], []

# Let's graph the CPU usage
while True:
    # Get a CPU usage % each iteration
    x.append(i)
    y.append(psutil.cpu_percent())
    
    # use the updated arrays
    ax.plot(x, y, color='b')

    # draw the graph
    fig.canvas.draw()
    
    # Make sure the graph doesn't go
    # off the screen
    ax.set_xlim(left=max(0, i - 50), right=i + 50)
    fig.show()
    plt.pause(0.01)
    i += 1
