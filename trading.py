
import Queue
import threading
import time

from strategy.testrandom import TestRandomStrategy
from streaming import StreamingForexPrices
from execution import Excution
from oandapyV20 import API

class Client(object):
    ENV = {'practice': {'TOKEN': '1fc6a927c4b0db0503b00bbc073bd0a1-49b477f61767345f977c46a8d442eaaf',
                        'ACCOUNT': '101-004-2941318-001'}, }
    def __init__(self, env):
        self.client = self.build_client(env)
        self.account = Client.ENV.get(env).get('ACCOUNT')

    def build_client(self, env):
        setup = Client.ENV.get(env)
        api = API(access_token=setup.get('TOKEN'), environment=env)
        return api

def trade(events, strategy, execution):
    heartbeat = 0
    while True:
        try:
            event = events.get(False)
        except Queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    strategy.calculate_signals( event )
                elif event.type == 'ORDER':
                    print 'executing an order'
                    execution.execute_order( event )
        time.sleep(heartbeat)

def runner( instrument='GBP_USD', strategy=None ):
    api = Client( 'practice' )
    events = Queue.Queue()
    units = 20

    prices = StreamingForexPrices(api,instrument,events)
    execution = Excution()
    strategy = TestRandomStrategy(instrument, units, events, numofticks=20)

    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution))
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])
    #prices.stream_to_queue()
    # Start both threads
    trade_thread.start()
    price_thread.start()

runner()