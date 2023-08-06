"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
import libevt

class Pulse_EVT2(item.item):

    """
    This class (the class with the same name as the module)
    handles the basic functionality of the item. It does
    not deal with GUI stuff.
    """
    
    description = u"Allows setting pins on the EventExchanger-2 (USB) Port"
    
    def reset(self):
        self.var._value = 0
        self.var._duration = 500
        self.var._serialNumber = u'autodetect'
          
    def prepare(self):

        item.item.prepare(self)
  
        dev = self.var._serialNumber
        if dev == u"autodetect":
            dev = None
		# Dynamically create an ee instance
        if not hasattr(self.experiment, "EventExchanger"):
            self.experiment.EventExchanger = libevt.libevt(self.experiment, dev)
            self.python_workspace[u'EventExchanger'] = self.experiment.EventExchanger

    def run(self):

        self.experiment.EventExchanger.PulseLines(self.var._value,self.var._duration)
        
        # Report success
        return True

class qtPulse_EVT2(Pulse_EVT2, qtautoplugin):

    """
    This class (the class named qt[name of module] handles
    the GUI part of the plugin. For more information about
    GUI programming using PyQt4, see:
    <http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/classes.html>
    """

    def __init__(self, name, experiment, string = None):

        """
        Constructor
        """

        # Pass the word on to the parents
        Pulse_EVT2.__init__(self, name, experiment, string)
        qtautoplugin.__init__(self, __file__)

    def init_edit_widget(self):

        """
        This function creates the controls for the edit
        widget.
        """
        #self.add_combobox_control('var','label','options', tooltip='tooltip')
        # Lock the widget until we're doing creating it

        # Pass the word on to the parent
        qtautoplugin.init_edit_widget(self)
        #self.add_combobox_control('var','label','options', tooltip='tooltip')