import matplotlib.pyplot as plt
import time
labels = 'x', 'y'
sizes = [100, 50]
colors = ['yellowgreen', 'lightcoral']
explode = (0,0.1)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.show()