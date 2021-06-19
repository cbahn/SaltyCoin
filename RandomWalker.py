#!/usr/bin/env python3

import json
import numpy as np
# import os.path
# from os import path

class RandomWalker:
    data = []
    value = 0
    
    initialValue = 10
    initialDatapoints = 100

    skew = 0
    volitility = 0.01
    minimum = 0.01

    ### CORE

    def __init__(self):
        self.value = self.initialValue
        for _ in range(self.initialDatapoints):
            self.next()

    """Step the random walk forward by one."""
    def next(self):
        # Value changes are based on a multiplier.
        multiplier = 1 + np.random.normal(self.skew, self.volitility)

        # Sanity check: max value change up or down is 90%.
        # This is to prevent the value from going negative.
        multiplier = max(0.1, multiplier)
        multiplier = min(multiplier, 1.9)

        # Update the value and enforce the minimum
        self.value = max(self.minimum, self.value * multiplier)

        self.data.append(self.value)
        return self.value

    def changePrice(self,percentChange): # TODO this doesn't enforce the minimun change or minimum value. I should reconsider how this is done
        self.value *= 1 + 0.01 * percentChange

    ### EXPORTERS

    def exportRecentValuesAsJson(self,numValues):
        return json.dumps(self.data[-numValues:])



market = RandomWalker()
print(market.exportRecentValuesAsJson(30))
