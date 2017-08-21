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
from qgis.PyQt.QtXml import *

import os, time, datetime
from qgis.core import *

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
        QgsProject.instance().writeProject.connect(self.save)
        QgsProject.instance().projectSaved.connect(self.afterSave)
        self.iface.addToolBarIcon(self.actionSave)

    def unload(self):
        self.iface.removeToolBarIcon(self.actionLoad)
        del self.actionLoad
        self.iface.removeToolBarIcon(self.actionSave)
        del self.actionSave

    def afterSave(self):
        #if self.Options['moveBackupQgsFiles'] #ready for options
        thisPath = QgsProject.instance().fileName()
        self.path_absolute = QFileInfo(QgsProject.instance().fileName()) .absolutePath()+'/'
        thisFileName = QFileInfo(QgsProject.instance().fileName()) .fileName()
        if os.path.exists(thisPath+'~'):
            previousModDate = time.strftime('%Y%m%d_%H%M%S',time.localtime(os.path.getmtime(thisPath+'~')))
            os.rename(thisPath+'~', self.path_absolute+'../Backup/'+thisFileName+'.'+previousModDate+'.qgs') #mv files to backup

    def load(self):
        self.path_absolute = QFileInfo(QgsProject.instance().fileName()) .absolutePath()+'/'

        self.qlrs  = []
        self.findAllQlr()
        cnt=self.loopThrough()

        QMessageBox.information(None, u'NestedLayers', u'Loaded Layers: '+format(cnt))

    def save(self, dom):
        self.path_absolute = QFileInfo(QgsProject.instance().fileName()) .absolutePath()+'/'

        # #replace all absolute paths with relative
        # if dom:
        #     QgsMessageLog.logMessage( format(dom.toString()), 'dom')
        #     fixed = dom.toString().replace(self.path_absolute,"./")
        #     QgsMessageLog.logMessage( format(fixed), 'fixed')
        #     dom.setContent(fixed)
        # #commented because it breaks groups - should not be needed anyway!

        self.qlrsRecursive  = []
        self.findAllQlrRecursive()
        cnt=self.loopThroughRecursive()

        QMessageBox.information(None, u'NestedLayers', u'Saved Layers:'+format(cnt))

    def loopThroughRecursive(self):
        savedCount=0

        for thisqlr in self.qlrsRecursive :
            msg = self.path_absolute+thisqlr['layerObj'].name() + ' in: ' + thisqlr['parent'].name()
            QgsMessageLog.logMessage( msg, 'savelyrs')
            thisPath = self.path_absolute+thisqlr['name']+'.qlr'
            newModDate = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            if os.path.exists(thisPath):
                previousModDate = time.strftime('%Y%m%d_%H%M%S',time.localtime(os.path.getmtime(thisPath)))
                os.rename(thisPath, self.path_absolute+'../Backup/'+thisqlr['name']+'.'+previousModDate+'.qlr~') #mv files to backup
            thisqlr['layerObj'].setCustomProperty('LastSaved',newModDate)
            thisqlr['layerObj'].setCustomProperty('TimeTime',round(float(time.time())))
            if QgsLayerDefinition.exportLayerDefinition(thisPath,[thisqlr['layerObj']]):
                savedCount += 1
                # if True: # self.Options.RelativizeQlr:
                #     qlrXmlFile = open(thisPath,'r+')
                #     rel = qlrXmlFile.read().replace(self.path_absolute,"./")
                #     qlrXmlFile.write(rel)
                #     qlrXmlFile.flush()
                #     os.fsync(qlrXmlFile.fileno())
                #     qlrXmlFile.close()
                #     QgsMessageLog.logMessage( rel, 'relqlr')

        return format(savedCount)

    def loopThrough(self):
        loadedCount=0

        for thisqlr in self.qlrs :
            thisPath = self.path_absolute+thisqlr['name']+'.qlr'
            msg = self.path_absolute+thisqlr['layerObj'].name() + ' into: ' + thisqlr['parent'].name()
            QgsMessageLog.logMessage( msg, 'lyrs')
            fileModTime = os.path.getmtime(thisPath)
            nowTime = time.time()
            layerModTime = thisqlr['layerObj'].customProperty('TimeTime')
            if round(float(fileModTime),1) > round(float(layerModTime),1):
                msg = 'Loading:'+thisPath +"\n"+format(fileModTime)+'?>?'+format(round(float(layerModTime),1))
                QgsMessageLog.logMessage( msg, 'Loading')
                if QgsLayerDefinition.loadLayerDefinition(thisPath,thisqlr['parent']):
                    thisqlr['parent'].removeChildNode(thisqlr['layerObj'])
                    loadedCount += 1
            else:
                msg = 'Skipping:'+thisPath +"\n"+format(fileModTime)+'?>?'+format(round(float(layerModTime),1))
                QgsMessageLog.logMessage( msg, 'Loading')

        for thisqlr in self.qlrs :
            #msg = thisqlr['name'] + ' expanded: ' + format(QgsProject.instance().layerTreeRoot().findGroup(thisqlr['name']+'.qlr').isExpanded())
            #QgsMessageLog.logMessage( msg, 'Expanded')
            QgsProject.instance().layerTreeRoot().findGroup(thisqlr['name']+'.qlr').setExpanded(False)

        return loadedCount

    def findAllQlr(self):
        thisLayer = QgsProject.instance().layerTreeRoot()
        for lyr in thisLayer.children():
            lname=lyr.name()
            QgsMessageLog.logMessage(lname, 'lyrext')
            lext=lname[-4:]
            if lext == '.qlr' and lyr.customProperty('embedded') != '1' :
                self.qlrs.append({'name':lname[:-4],'parent':thisLayer,'layerObj':lyr})

    def findAllQlrRecursive(self, thisLayer = QgsProject.instance().layerTreeRoot()):
        for lyr in thisLayer.children():
            lname=lyr.name()
            lext=lname[-4:]
            if lext == '.qlr' and lyr.customProperty('embedded') != '1' :
                self.qlrsRecursive.append({'name':lname[:-4],'parent':thisLayer,'layerObj':lyr})
                self.findAllQlrRecursive(lyr)
