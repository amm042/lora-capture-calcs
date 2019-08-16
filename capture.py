# Alan Marchiori 2019
import math
import matplotlib.pyplot as plt
import numpy.random
import numpy
from collections import defaultdict
# randomly select a point in a circle, compute path loss to center
# now pick a new random point (uniformly), is the path loss greater than
# 5 dB? if so, a packet is captured.
# repeat with N simultaneous collisions

def fspl_db(d, f=9.15e8):
    "d is distance in meters"
    #-147.552216778 = 20*log(4*pi/299792458)
    return 20*math.log10(d)+20*math.log10(f)-147.552216778

def cap_test(cap_margin_db=5, N=2, max_d=10e3):
    "N is the number of simultaneous transmissions, max_d is the max distance"
    #d = sorted([max_d*random.random() for i in range(N)])
    #d = sorted([max_d*numpy.random.uniform() for i in range(N)])

    # no sort, this is the probability the first transmitter is caputred
    d = ([max_d*numpy.random.uniform() for i in range(N)])
    fspl = list(map(fspl_db, d))
    margin = [x-fspl[0] for x in fspl]

    # print(d)
    # print(fspl)
    # print(margin)

    capture = True
    # check for any collision
    for m in margin[1:]:
        if m < 5:
            capture = False
    #print(capture)
    return capture

if __name__=="__main__":

    ns = range(2,11)
    rates = []
    #for max_d in [5e3, 10e3, 15e3]:
    max_d = 15e3

    for n in ns:
        res = []
        for trial in range(100):
            tot = 1000
            cap = 0
            for i in range(tot):
                if cap_test(N=n, max_d=max_d):
                    cap += 1
            #print("-"*60)
            #print("N, max_d    :", n, max_d)
            #print("Total trials:", tot)
            #print("Captured    :", cap, "[{:%}]".format(cap/tot))
            res.append(cap/tot)
        rates.append(res)

    for i,n in enumerate(ns):
        print("{}: median: {}".format(
            n,
            numpy.median(rates[i])
        ))

    fig,ax =plt.subplots(figsize=(4,4))
    #for n in ns:
        #ax.plot(ns, rates[d], label='max dist={} km'.format(d/1e3))
    ax.boxplot(rates)
    #ax.boxplot(rates)

    #ax.legend()
    ax.set_ylabel('p(capture)')
    ax.set_ylim((0,0.33))
    ax.set_xlabel('Collision order ($k$)')
    ax.set_xticklabels(ns)
    plt.tight_layout()
    #plt.show()
    plt.savefig("p_cap.pdf")
