import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 5, 11)
y = x ** 2

#subplot performs axes operation of figure class automatically

#fig,axes = plt.subplots(nrows = 3, ncols = 3)
#plt.tight_layout()#finx overlapping of canvas

fig,axes = plt.subplots(nrows = 1, ncols = 2)

#iterat axes
#for curr in axes:
#    curr.plot()

axes[0].plot(x,y)
axes[0].set_title('1st')
axes[1].plot(y,x,'r')

plt.tight_layout()
plt.show()