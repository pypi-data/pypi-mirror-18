import time

from kalliope import BrainLoader
from kalliope.core.EventManager import EventManager

brain_to_test = "brain-test.yml"

bl = BrainLoader(file_path=brain_to_test)
brain = bl.brain

for synapse in brain.synapses:
    print synapse

em = EventManager(brain.synapses)

print "the main"

try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    pass