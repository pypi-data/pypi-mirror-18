#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg


class PlotWidget(pg.PlotWidget):
    exportSignal = QtCore.pyqtSignal(str)
    watchMouseSignal = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None, background='default', **kargs):
        super(PlotWidget, self).__init__(parent, background, **kargs)
        self.plotItem.vb.menu.addSeparator()
        self.exportAction = self.plotItem.vb.menu.addAction('Export data...')
        self.plotItem.vb.menu.addSeparator()
        self.exportAction.triggered.connect(self.exportData)
        self.proxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def mouseMoved(self, evt):
        pos = evt[0]
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)
            self.watchMouseSignal.emit(mousePoint.x(), mousePoint.y())

    def exportData(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save data into file')[0]
        if filename:
            self.exportSignal.emit(filename)
