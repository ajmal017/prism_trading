

from events import TickEvent
import oandapyV20.endpoints.pricing as pricing

class StreamingForexPrices(object):
    def __init__(self, client, instruments, events_queue):
        self.client = client
        self.instruments = instruments
        self.events_queue = events_queue
        self.req = self.build_stream()

    def build_stream(self):
        return pricing.PricingStream(accountID=self.client.account, params={'instruments': self.instruments} )

    def stream_to_queue(self):
        '''while loop'''
        self.client.client.request(self.req)
        for line in self.req.response:
            if line.get('type') == 'PRICE':
                instrument = self.instruments
                bid = line.get('bids')[0].get('price')
                ask = line.get('asks')[0].get('price')
                time = line.get('time')
                tev = TickEvent( instrument, time, bid, ask )
                print 'adding tick event', tev
                self.events_queue.put( tev )
