# encoding: utf-8
#-----------------------------------------------------------
# Forked from NestedLayers (C) 2015 Martin Dobias (GNU GPL 2)
#-----------------------------------------------------------
# NestedLayers (C) 2017 Joshua Gottdenker (GNU GPL 2)
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

from PyQt4.QtGui import *
from PyQt4.QtCore import *

def classFactory(iface):
    return NestedLayers(iface)


class NestedLayers:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction(u'Go!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        QMessageBox.information(None, u'Minimal plugin', u'Do something useful here')
