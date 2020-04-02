import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 5, 11)
y = x ** 2

fig = plt.figure()

# Add set of axes to figure
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)

# Plot on that set of axes
axes.plot(x, y, 'b')
axes.set_xlabel('Set X Label') # Notice the use of set_ to begin methods
axes.set_ylabel('Set y Label')
axes.set_title('Set Title')

#Inner plot
fig1 = plt.figure()
axes1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
axes2 = fig1.add_axes([0.35, 0.15, 0.5, 0.4])

axes1.plot(x,y,'r')
axes1.set_title('large Canvas')
axes2.plot(y,x,'b')
axes2.set_title('Small Canvas')
plt.show()