

import random
from events import OrderEvent

class TestRandomStrategy(object):
    def __init__(self, instrument, units, events, numofticks=5):
        self.instrument = instrument
        self.units = units
        self.events = events
        self.ticks = 0
        self.numofticks = numofticks

    def calculate_signals(self, event ):
        ''' a simple strategy that place an order every five ticks '''
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks % self.numofticks == 0:
                side = random.choice(['buy', 'sell'])
                order = OrderEvent(self.instrument, self.units, 'market', side)
                self.events.put( order )

