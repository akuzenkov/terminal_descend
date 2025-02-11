import heapq
from time import time

from pynput.keyboard import Listener


PRESSED_KEYS = {}
KEY_HEAP = []


def on_press(key):
    if not hasattr(key, "char"):
        return
    
    PRESSED_KEYS[key.char] = [key, time()]
    heapq.heappush(KEY_HEAP, (time() * -1, key))
    

def on_release(key):
    if not hasattr(key, "char"):
        return
    
    del PRESSED_KEYS[key.char]


def get_key():
    while KEY_HEAP:
        _, key = heapq.heappop(KEY_HEAP)
        KEY_HEAP.clear()
        return key
    return

