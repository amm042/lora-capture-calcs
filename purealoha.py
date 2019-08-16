# Alan Marchiori 2019
# plot pure aloha efficency
# assume N=100 nodes (scale p accordingly)
# p is the probability of a node transmitting
# assume time units are aligned with packet lengths

import math
import matplotlib.pyplot as plt
import numpy.random
import numpy as np

def tx_aloha(N=100, p=0.1):
    pr = N*p*(1-p)**(2*(N-1))
    return numpy.random.rand() < pr

def tx_capture(N=100, p=0.1):
    # output from capture program
    # first two are padding
    cap_pr=[0, 0, 0.2835, 0.187, 0.1405, 0.113, 0.093, 0.08, 0.071, 0.064, 0.056]

    # aloha pr one transmitter, no capture needed.
    pr = N*p*(1-p)**(2*(N-1))

    # more than one transmitter has computed capture probability
    for txes, cpr in enumerate(cap_pr):
        if txes > 1:
            # exactly txes nodes transmit AND capture was successful
            pr += (N*cpr*p**txes*(1-p)**(2*(N-txes)))

    return numpy.random.rand() < pr

attempts = 1000
trials = 100
N = 100
ps = np.linspace(0, 4/N, num=15)
print(ps)

def ef(tx_func):
    efficency = []
    for p in ps:
        result = []
        for trial in range(trials):
            count = 0
            for attempt in range(attempts):
                if tx_func(N=N, p=p):
                    count+=1
            result.append(count/attempts)
        print("p: {:0.4f}, eff: {:0.4f}".format(
            p, np.median(result)
        ))
        efficency.append(result)
    return efficency

print("-- ALOHA --")
aloha_efficency = ef(tx_aloha)
print("--caputre--")
cap_efficency = ef(tx_capture)

fig,ax =plt.subplots(figsize=(4,4))
#for n in ns:
    #ax.plot(ns, rates[d], label='max dist={} km'.format(d/1e3))
#ax.boxplot(efficency)
ax.plot(range(1,len(ps)+1), [100*np.median(x) for x in aloha_efficency],
        color='blue', alpha=0.2, lw=2, ls='dashed', label='pure ALOHA')
ax.plot(range(1,len(ps)+1), [100*np.median(x) for x in cap_efficency],
        color='red', alpha=0.6, lw=2, ls='solid', label='ALOHA w/ 5 dB capture')
#ax.boxplot(rates)

ax.legend()
ax.set_ylabel('efficency (%)')
#ax.set_ylim((0,0.33))
ax.set_xlabel('$p$ (%)')
ax.set_xticks(numpy.arange(1, len(ps) + 1))
ax.set_xticklabels(["{:0.1f}".format(100*x) for x in ps],rotation=90)
plt.tight_layout()
plt.savefig("capeff.pdf")
