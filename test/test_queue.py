from hauhau.camera import LifoQueue

def test_queue():
    queue = LifoQueue(3)

    queue.put('a')
    queue.put('b')
    queue.put('c')
    queue.put('d')

    assert 'a' not in queue.queue and 'd' in queue.queue