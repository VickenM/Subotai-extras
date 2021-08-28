from PySide2 import QtCore
from PySide2.QtCore import Slot

from eventnodes.base import ComputeNode
from eventnodes.params import StringParam, ListParam, IntParam, EnumParam, PARAM
from eventnodes.signal import Signal, INPUT_PLUG, OUTPUT_PLUG


class MyNode(ComputeNode):
    type = 'MyNode'
    categories = ['examples']
    description = """A simple node for demonstration purposes"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.signals.append(Signal(node=self, name='event', pluggable=INPUT_PLUG))
        self.signals.append(Signal(node=self, name='event', pluggable=OUTPUT_PLUG))

        self.params.append(StringParam(name='name', value='', pluggable=PARAM | INPUT_PLUG))
        self.params.append(StringParam(name='output', value='', pluggable=OUTPUT_PLUG))

    @ComputeNode.Decorators.show_ui_computation
    @Slot()
    def compute(self):
        event = self.get_first_signal('event', pluggable=OUTPUT_PLUG)
        name = self.get_first_param('name')
        output = self.get_first_param('output')

        output.value = 'Hello {}. I am Subotai! Thief and archer. I am Hyrkanian. The Great Order of Kurlit.'.format(
            name.value)

        event.emit_event()
