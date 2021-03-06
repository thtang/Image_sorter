# -*- coding: utf-8 -*-

# Copyright (c) 2011--2012 Peter Dinges <pdinges@acm.org>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Package imports.
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import cmp_to_key
class MoveListView(QtWidgets.QListView):
    """A specialized QListView that snaps drop events to the closest list item.
       
       Snapping the drop events prevents placing list items in empty space, which
       reorders the items visually without notifying the model. 
    """
    def dropEvent(self, event):
        # The modified behavior only makes sense in icon view mode.
        if self.viewMode() != QtWidgets.QListView.IconMode:
            return QtWidgets.QListView.dropEvent(self, event)
        
        # Compute the number of visible item columns and rows.
        gridCols = self.viewport().width() // (self.gridSize().width() + self.spacing())
        gridRows = self.viewport().height() // (self.gridSize().height() + self.spacing())
        
        # Compute the drop event's column and row (these might be greater than
        # the number of grid columns and rows: there is some empty space next
        # to the items).
        point = event.pos()
        pointCol = min(gridCols, point.x() // (self.gridSize().width() + self.spacing()))
        pointRow = min(gridRows, point.y() // (self.gridSize().height() + self.spacing()))

        # Determine which model row is closest to the drop position; if
        # necessary, adjust it to have items dropped to the right of other
        # items go in between.
        modelIndexRow = min((pointRow * gridCols) + pointCol, self.model().rowCount() - 1)
        if (pointRow >= gridRows or
            pointCol >= gridCols or
            point.x() > (pointCol + 0.5) * (self.gridSize().width() + self.spacing())):
            modelIndexRow += 1

        # Find the model index of the drop target.  Use an empty index
        # to denote the end of the list.
        if modelIndexRow < self.model().rowCount(): 
            modelIndex = self.model().index(modelIndexRow, self.modelColumn())
        else:
            modelIndex = QtCore.QModelIndex()
        
        self.model().dropMimeData(event.mimeData(),
                                  event.possibleActions(),
                                  modelIndexRow,
                                  self.modelColumn(),
                                  modelIndex)
