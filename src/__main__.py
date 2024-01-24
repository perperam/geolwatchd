from main import Processor, Handler
from sensor import Simulator
from blacklist import Blacklist
from subscriber import Subscriber


if __name__ == "__main__":
    simulator = Simulator(
            [[1.0, 1.0], [1.5, 1.5], [2.0, 2.0], [2.5, 2.5], [3.0, 3.0], [3.5, 3.5], [4.0, 4.0], [4.5, 4.5], None, [5.0, 5.0], [5.5, 5.5]],
            interval=5
        )

    blacklist = Blacklist("../blacklist.json")
    handler = Handler()

    sub1 = Subscriber('localhost', 12345)
    handler.add_subscriber(sub1)

    processor = Processor(simulator, blacklist, handler)
    processor.run()
