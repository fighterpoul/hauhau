from hauhau.detector import is_detected

def test_valid_subset():
    detections = ['cat', 'dog', 'cell phone']
    musts = ['cat', 'cell phone']
    assert is_detected(detections=detections, musts=musts)

def test_empty_musts():
    detections = ['cat', 'dog', 'cell phone']
    musts = []
    assert is_detected(detections=detections, musts=musts)

def test_must_nots_only():
    detections = ['cat', 'dog', 'cell phone']
    must_nots = ['person']
    assert is_detected(detections=detections, musts=[], must_nots=must_nots)

# Test case for an invalid subset
def test_invalid_subset():
    detections = ['cat', 'dog', 'cell phone']
    musts = ['cat', 'frog']
    assert not is_detected(detections=detections, musts=musts)
