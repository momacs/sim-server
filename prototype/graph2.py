import random
from itertools import count
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
from matplotlib.patches import Circle, PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d

# Set the plot type
plt.style.use('fivethirtyeight')

# All of our values
x_values = []
y_values = []
z_values = []
q_values = []
w_values = []

index = count()

# Update the graph even time
# step
def animate(i):
    
    x = next(index)
    x_values.append(x)

    # Fill the graph with random values
    y = random.randint(0, 5)
    z = random.randint(3, 8)
    q = random.randint(0, 10)
    w = random.randint(0, 10)
    y_values.append(y)
    z_values.append(z)
    q_values.append(q)
    w_values.append(w)

    # Add updated arrays
    ax.plot3D(x_values, y_values, z_values, 'blue',linestyle='--')
    ax.plot3D(x_values, q_values, z_values, 'red',linestyle='--')
    ax.plot3D(x_values, w_values, z_values, 'green',linestyle='--')
         
    # Sleep for half of a second
    time.sleep(.5)

fig = plt.figure()
ax = plt.axes(projection='3d')    
ani = FuncAnimation(plt.gcf(), animate, 10)


plt.tight_layout()
plt.show()
