import wx.grid
class MyGridTable(wx.grid.GridTableBase):
    def __init__(self, title, data):
        super().__init__()
        self.colLabels = title
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        if self.data:
            return len(self.data[0])

    def GetValue(self, row, col):
        return self.data[row][col]

    def GetColLabelValue(self, col):
        return self.colLabels[col]