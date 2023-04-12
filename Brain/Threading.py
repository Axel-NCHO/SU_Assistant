from threading import Thread
from abc import ABC


class Threading(ABC):
    
    @staticmethod
    def start_thread(target, args=None, name=None, daemon=False):
        if not args:
            args = []
        t = Thread(name=name, target=target, args=args, daemon=daemon)
        t.start()
        return t

    @staticmethod
    def stop_thread(thread: Thread, timeout=None):
        thread.join(timeout)
