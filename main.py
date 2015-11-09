import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('image.jpg',0)
kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(img,-1,kernel)
edges = cv2.Canny(dst,100,200)

ret,thresh = cv2.threshold(dst,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(dst,contours,-1,(0,255,0),-1)

ax1 = plt.subplot2grid((3,3), (0,0))
ax2 = plt.subplot2grid((3,3), (0,1))
ax3 = plt.subplot2grid((3,3), (0,2))

ax1.set_title('initial image')
ax2.set_title('edges')
ax3.set_title('contours')

plt.sca(ax1)
plt.imshow(img, cmap='gray')

plt.sca(ax2)
plt.imshow(edges, cmap='gray')

plt.sca(ax3)
plt.imshow(dst)
plt.show()