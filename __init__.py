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
import os
from qgis.core import QgsProject
from qgis.core import QgsMessageLog
from qgis.core import QgsLayerDefinition

def classFactory(iface):
    return NestedLayers(iface)

class NestedLayers:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.actionLoad = QAction(u'Load QLRs', self.iface.mainWindow())
        self.actionLoad.triggered.connect(self.load)
        self.iface.addToolBarIcon(self.actionLoad)

        self.actionSave = QAction(u'Save QLRs', self.iface.mainWindow())
        self.actionSave.triggered.connect(self.save)
        self.iface.addToolBarIcon(self.actionSave)

    def unload(self):
        self.iface.removeToolBarIcon(self.actionLoad)
        del self.actionLoad
        self.iface.removeToolBarIcon(self.actionSave)
        del self.actionSave

    def load(self):
        self.qlrs  = []
        self.findAllQlr()
        cnt=self.loopThrough()

        QMessageBox.information(None, u'NestedLayers', u'Loaded Layers: '+format(cnt))

    def save(self):
        self.qlrsRecursive  = []
        #self.findAllQlr()
        #cnt=self.loopThrough()

        QMessageBox.information(None, u'NestedLayers', u'Placeholder for Saving')

    def loopThrough(self):

        loadedCount=0
        path_absolute = QgsProject.instance().readPath("./")+'/'
        for thisqlr in self.qlrs :
            msg = path_absolute+thisqlr['layerObj'].name() + ' into: ' + thisqlr['parent'].name()
            QgsMessageLog.logMessage( msg, 'lyrs')
            if QgsLayerDefinition.loadLayerDefinition(path_absolute+thisqlr['name']+'.qlr',thisqlr['parent']):
                thisqlr['parent'].removeChildNode(thisqlr['layerObj'])
                loadedCount += 1
        for thisqlr in self.qlrs :
            msg = thisqlr['name'] + ' expanded: ' + format(QgsProject.instance().layerTreeRoot().findGroup(thisqlr['name']+'.qlr').isExpanded())
            QgsMessageLog.logMessage( msg, 'Expanded')
            QgsProject.instance().layerTreeRoot().findGroup(thisqlr['name']+'.qlr').setExpanded(False)
        for thisqlr in self.qlrs :
            msg = thisqlr['name'] + ' expanded: ' + format(QgsProject.instance().layerTreeRoot().findGroup(thisqlr['name']+'.qlr').isExpanded())
            QgsMessageLog.logMessage( msg, 'Expanded')
        return loadedCount

    def findAllQlr(self):
        thisLayer = QgsProject.instance().layerTreeRoot()
        for lyr in thisLayer.children():
            lname=lyr.name()
            QgsMessageLog.logMessage(lname, 'lyrext')
            lext=lname[-4:]
            if lext == '.qlr':
                self.qlrs .append({'name':lname[:-4],'parent':thisLayer,'layerObj':lyr})
