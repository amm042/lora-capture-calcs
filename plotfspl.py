# Alan Marchiori 2019
import math
import matplotlib.pyplot as plt
import numpy.random
import numpy as np
from collections import defaultdict
def fspl_db(d, f=9.15e8):
    "d is distance in meters"
    #-147.552216778 = 20*log(4*pi/299792458)
    if d == 0:
        return 0.0
    return 20*math.log10(d)+20*math.log10(f)-147.552216778


fig,ax =plt.subplots(figsize=(4,4))

pts = np.linspace(0, 15000, num=100)
ax.plot([x/1000 for x in pts], map(fspl_db, pts))


#ax.legend()
ax.set_ylabel('Free-space path loss (dB)')
#ax.set_ylim((0,0.33))
ax.set_xlabel('Distance (km)')
#ax.set_xticklabels(ns)
plt.tight_layout()

plt.savefig("lorafspl.pdf")

plt.show()
