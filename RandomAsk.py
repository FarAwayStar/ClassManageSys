import wx

class RandomAsk(wx.Frame):
    def __init__(self,dbm,zydata):
        super(RandomAsk, self).__init__(parent=None,title='随机提问',size=(260,200))
        self.Center()
        self.dbm=dbm
        panel=wx.Panel(self)
        scoredata=['-2','-1','1','2','3','4','5']

        hbox=wx.BoxSizer(wx.HORIZONTAL)
        cb=wx.ComboBox(panel,-1, choices=zydata,style=wx.CB_SORT | wx.TE_PROCESS_ENTER)
        btn = wx.Button(panel, label='看看谁最幸运')
        hbox.Add(cb,2,flag=wx.ALIGN_LEFT|wx.ALL,border=5)
        hbox.Add(btn, 1, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON,self.suiji,btn)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        cb2 = wx.ComboBox(panel, -1, choices=scoredata, style=wx.CB_SORT | wx.TE_PROCESS_ENTER)
        btn2= wx.Button(panel, label='确认得分')
        hbox2.Add(cb2, 2, flag=wx.ALIGN_LEFT | wx.ALL, border=5)
        hbox2.Add(btn2, 1, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.defen, btn)

        hbox3=wx.BoxSizer(wx.HORIZONTAL)
        self.text=wx.StaticText(panel,label='')
        hbox3.Add(self.text,flag=wx.ALIGN_CENTER)

        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox)
        vbox.Add(hbox2)
        vbox.Add(hbox3)

        panel.SetSizer(vbox)

    def suiji(self,evt):
        pass

    def defen(self,evt):
        pass