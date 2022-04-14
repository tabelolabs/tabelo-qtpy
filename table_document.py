# This Python file uses the following encoding: utf-8
#
# Copyright 2022 naracanto <https://naracanto.github.io>.
#
# This file is part of PyTabelo <https://github.com/cutelabs/pytabelo>.
#
# PyTabelo is an open source table editor written in Python using
# the Python bindings for the Qt framework.
#
# PyTabelo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# PyTabelo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTabelo.  If not, see <https://www.gnu.org/licenses/>.
#

from PySide2.QtCore import Property, Signal, Qt
from PySide2.QtWidgets import QTabWidget, QVBoxLayout, QWidget


class TableDocument(QWidget):

    documentCountChanged = Signal(int)

    tabPositionChanged = Signal(QTabWidget.TabPosition)
    tabBarAutoHideChanged = Signal(bool)


    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._tabPosition = QTabWidget.South
        self._tabBarAutoHide = True

        self._tabBox = QTabWidget()
        self._tabBox.setDocumentMode(True)
        self._tabBox.setMovable(True)
        self._tabBox.setTabBarAutoHide(self._tabBarAutoHide)
        self._tabBox.setTabPosition(self._tabPosition)
        self._tabBox.setTabsClosable(True)
        self._tabBox.tabCloseRequested.connect(self._closeTab)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._tabBox)
        self.setLayout(mainLayout)

        self.documentCountChanged.connect(self._addTab)


    def getTabPosition(self):

        return self._tabBox.tabPosition()


    def setTabPosition(self, position):

        if position != self._tabBox.tabPosition():
            self._tabBox.setTabPosition(position)
            self.tabPositionChanged.emit(position)


    tabPosition = Property(QTabWidget.TabPosition, getTabPosition, setTabPosition, notify=tabPositionChanged)


    def initTabPosition(self):

        self._tabBox.setTabPosition(self._tabPosition)
        self.tabPositionChanged.emit(self._tabPosition)


    def getTabBarAutoHide(self):

        return self._tabBox.tabBarAutoHide()


    def setTabBarAutoHide(self, hide):

        if hide != self._tabBox.tabBarAutoHide():
            self._tabBox.setTabBarAutoHide(hide)
            self.tabBarAutoHideChanged.emit(hide)


    tabBarAutoHide = Property(bool, getTabBarAutoHide, setTabBarAutoHide, notify=tabBarAutoHideChanged)


    def initTabBarAutoHide(self):

        self._tabBox.setTabBarAutoHide(self._tabBarAutoHide)
        self.tabBarAutoHideChanged.emit(self._tabBarAutoHide)


    def _addTab(self, count):

        if not self._tabBox.count():
            for i in range(1, count+1):
                widget = QWidget()
                widget.setAttribute(Qt.WA_DeleteOnClose)
                self._tabBox.addTab(widget, self.tr("Sheet {0}").format(i))


    def _closeTab(self, index):

        widget = self._tabBox.widget(index)
        if widget is not None:
            widget.close()

        self._tabBox.removeTab(index)
