import asyncio
import concurrent
import logging
import threading

logger = logging.getLogger("octoprint.plugins.octoprint_gopro.manager")


class WorkerManager:
    """
    Manages an asynio event loop running in a separate ThreadPool
    """

    def __init__(self, plugin):

        self.event_loop_thread = threading.Thread(target=self._event_loop_worker)
        self.event_loop_thread.daemon = True
        self.event_loop_thread.start()
        self.plugin = plugin

    def _event_loop_worker(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
        self.loop = loop
        return loop.run_forever()
