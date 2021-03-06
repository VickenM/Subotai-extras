from PySide2 import QtCore
from PySide2.QtCore import Slot

from eventnodes.base import ComputeNode
from eventnodes.params import StringParam, ListParam, IntParam, EnumParam, PARAM
from eventnodes.signal import Signal, INPUT_PLUG, OUTPUT_PLUG

class WickedNode(ComputeNode):
    type = 'Wicked'
    categories = ['Flow Control']
    description = \
        """this is a test node
"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.signals.append(Signal(node=self, name='event', pluggable=INPUT_PLUG))
        self.signals.append(Signal(node=self, name='reset', pluggable=INPUT_PLUG))
        self.signals.append(Signal(node=self, name='event', pluggable=OUTPUT_PLUG))

        self.params.append(IntParam(name='initial', value=0, pluggable=PARAM | INPUT_PLUG))
        self.params.append(IntParam(name='increment', value=1, pluggable=PARAM | INPUT_PLUG))
        self.params.append(IntParam(name='value', value=0, pluggable=OUTPUT_PLUG))

    def map_signal(self, signal):
        if signal == 'reset':
            return self.reset
        elif signal == 'event':
            return self.trigger

    @Slot()
    def trigger(self):
        self.compute()

    @Slot()
    def reset(self):
        item = self.get_first_param('value')
        initial = self.get_first_param('initial')
        item.value = initial.value

    @ComputeNode.Decorators.show_ui_computation
    @Slot()
    def compute(self):
        QtCore.QCoreApplication.processEvents()
        self.start_spinner_signal.emit()
        event = self.get_first_signal('event', pluggable=OUTPUT_PLUG)
        increment = self.get_first_param('increment')
        item = self.get_first_param('value')
        item.value += increment.value
        self.stop_spinner_signal.emit()
        event.emit_event()
