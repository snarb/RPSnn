from matplotlib import pyplot as plt
import numpy as np

x = list(np.linspace(0, 0.95))

for i in range(20):
    x.append(0.95)

x = np.array(x)
y = x * 3  + 1
t = range(len(x))

plt.scatter(x, y, c=t)
plt.show()

# heatmap, xedges, yedges = np.histogram2d(x, y, bins=5)
# #extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#
# plt.clf()
# plt.imshow(heatmap.T,  origin='lower')
# plt.show()
