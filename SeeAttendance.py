import wx
import wx.grid
import MyGridTable


class AttendanceFrame(wx.Frame):
    def __init__(self, dbm, zydata):
        super(AttendanceFrame, self).__init__(parent=None, title='查看出勤情况', size=(380, 300))
        self.Center()
        self.panel = wx.Panel(self)
        self.dbm = dbm
        self.stuid = None  # 所选学号
        self.zy = None  # 所选专业
        # self.studata=[] #动态学号列表
        self.col_name = ['学号', '姓名', '出勤时间']  # 列名
        self.data = None  # 内容

        self.ch1 = wx.ComboBox(self.panel, -1, choices=zydata,
                               style=wx.CB_SORT | wx.TE_PROCESS_ENTER)
        btn = wx.Button(self.panel, label='按专业查看')
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox, self.ch1)
        self.Bind(wx.EVT_BUTTON, self.btnlookpro, btn)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.ch1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        hbox1.Add(btn, 1, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        self.ch2 = wx.ComboBox(self.panel, -1, style=wx.CB_SORT | wx.TE_PROCESS_ENTER)
        btn2 = wx.Button(self.panel, label='按学号查看')
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox2, self.ch2)
        self.Bind(wx.EVT_BUTTON, self.btnlookid, btn2)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.ch2, 1, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        hbox2.Add(btn2, 1, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        self.grid = wx.grid.Grid(self.panel)
        self.CreateGridTable()
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.grid, flag=wx.ALIGN_CENTER_HORIZONTAL)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox1, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        vbox.Add(hbox2, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        vbox.Add(hbox3, 5, flag=wx.ALIGN_CENTER)

        self.panel.SetSizer(vbox)

    def on_combobox(self, evt):
        self.zy = self.ch1.GetValue()
        temp = self.dbm.getXuehaoXingming(self.zy)
        xueshengXinxi = []
        for line in temp:
            xueshengXinxi.append(line[0] + ',' + line[1])
        self.ch2.SetItems(xueshengXinxi)
        self.stuid=''

    def btnlookpro(self, evt):
        if not self.zy:
            dlg = wx.MessageDialog(None, u"请选择一个专业", u"很抱歉", wx.YES_DEFAULT | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            return
        sql = "select students.xuehao,students.xingming,dianming.shijian from students,dianming" \
              + " where students.xuehao=dianming.xuehao and students.zhuanye='" + self.zy \
              + "' order by students.xuehao"
        self.data = self.dbm.getDataBySQL(sql)
        self.CreateGridTable()

    def on_combobox2(self, evt):
        self.stuid = str(self.ch2.GetValue()).split(',')[0]
        print(self.stuid)

    def btnlookid(self, evt):
        if not self.stuid:
            dlg = wx.MessageDialog(None, u"请选择一名学生", u"很抱歉", wx.YES_DEFAULT | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            return
        sql = "select students.xuehao,students.xingming,dianming.shijian from students,dianming" \
              + " where students.xuehao=dianming.xuehao and dianming.xuehao='" + self.stuid + "'"
        self.data = self.dbm.getDataBySQL(sql)
        self.CreateGridTable()

    def CreateGridTable(self):
        print(self.data)
        if self.data==None:
            return
        self.gridtable = MyGridTable.MyGridTable(self.col_name, self.data)
        self.grid.SetTable(self.gridtable, True)
        self.grid.AutoSize()  # 设置行和列自定调整
        # 设置文本居中
        for i in range(len(self.data)):
            for j in range(len(self.col_name)):
                self.grid.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.panel.Layout()
