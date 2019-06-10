import wx
import wx.grid
import MyGridTable
import DBManger


# 查看学生信息类
class SeeStu(wx.Frame):
    def __init__(self, dbm, zydata=None):
        super(SeeStu, self).__init__(parent=None, title='查看学生信息', size=(380, 400))
        self.dbm = dbm
        self.zy = None  # 所选专业
        self.col_name = ['学号', '姓名']  # 列名
        self.click = None  # 点击的学号
        self.data = None  # 内容
        self.Center()
        self.panel = wx.Panel(self)
        self.ch1 = wx.ComboBox(self.panel, -1, choices=zydata,
                               style=wx.CB_SORT | wx.TE_PROCESS_ENTER)
        btn = wx.Button(self.panel, label='查看')
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox, self.ch1)
        self.Bind(wx.EVT_BUTTON, self.btnlook, btn)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.ch1, 1, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        hbox1.Add(btn, 1, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        self.grid = wx.grid.Grid(self.panel)
        self.CreateGridTable()
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnClickItem)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnClickItem)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.grid)

        btnjia = wx.Button(self.panel, label='认真听课加分')
        btnjian = wx.Button(self.panel, label='不认真听课减分')
        btnbu = wx.Button(self.panel, label='离线点名')
        self.Bind(wx.EVT_BUTTON, self.lixian, btnbu)
        self.Bind(wx.EVT_BUTTON, self.jiafen, btnjia)
        self.Bind(wx.EVT_BUTTON, self.jianfen, btnjian)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(btnjia, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        hbox3.Add(btnjian, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        hbox3.Add(btnbu, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, 0, flag=wx.EXPAND | wx.ALIGN_CENTER)
        vbox.Add(hbox2, 1, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox3, 0, flag=wx.EXPAND | wx.ALIGN_CENTER)
        self.panel.SetSizer(vbox)

    def on_combobox(self, event):
        self.zy = self.ch1.GetValue()

    def btnlook(self, event):
        if not self.zy:
            dlg = wx.MessageDialog(None, u"请选择一个专业", u"很抱歉", wx.YES_DEFAULT | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            return
        # print(self.zy)
        self.data = self.dbm.getXuehaoXingming(self.zy)
        print(self.data)
        self.CreateGridTable()

    def CreateGridTable(self):
        if self.data == None:
            return
        print(self.data)
        self.gridtable = MyGridTable.MyGridTable(self.col_name, self.data)
        self.grid.SetTable(self.gridtable, True)
        self.grid.AutoSize()  # 设置行和列自定调整
        # 设置文本居中
        for i in range(len(self.data)):
            for j in range(len(self.col_name)):
                self.grid.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.panel.Layout()

    def OnClickItem(self, evt):
        row = int(evt.GetRow())
        self.click = self.data[row][0]
        print(self.click)
        evt.Skip()

    def noStuSelect(self):
        dlg = wx.MessageDialog(None, u"请选择一名学生", u"很抱歉", wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()

    def lixian(self, event):
        if not self.click:
            self.noStuSelect()
            return
        currentTime = self.dbm.getCurrentDateTime()
        # 获取一个半小时之前的时间
        startTime = self.dbm.getStartDateTime()
        # 查看是否已经点名过，避免一个半小时内重复点名
        sqlShifouChongfuDianming = "select count(xuehao) from dianming where xuehao=%s and shijian >=%s"
        parm = [self.click, startTime]
        if self.dbm.getDataBySQL(sqlShifouChongfuDianming, parm)[0][0] != 0:
            dlg = wx.MessageDialog(None, self.click + "号同学重复点名", u"很抱歉", wx.YES_DEFAULT | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            return
        # 点名
        sqlDianming = "insert into dianming(xuehao,shijian) values('" + self.click + "','" + currentTime + "')"
        self.dbm.doSQL(sqlDianming)
        dlg = wx.MessageDialog(None, self.click + "号同学离线点名成功", u"恭喜", wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()

    def jiafen(self, event):
        if not self.click:
            self.noStuSelect()
            return
        sqlJiafen = "insert into tiwen(xuehao,shijian,defen) values('" \
                    + self.click + "','" + self.dbm.getCurrentDateTime() + "'," + str(5) + ")"
        self.dbm.doSQL(sqlJiafen)
        dlg = wx.MessageDialog(None, self.click + "号同学加分成功", u"恭喜", wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()

    def jianfen(self, event):
        if not self.click:
            self.noStuSelect()
            return
        sqlJiafen = "insert into tiwen(xuehao,shijian,defen) values('" \
                    + self.click + "','" + self.dbm.getCurrentDateTime() + "'," + str(-5) + ")"
        self.dbm.doSQL(sqlJiafen)
        dlg = wx.MessageDialog(None, self.click + "号同学减分成功", u"恭喜", wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()
