import wx
import socket
import re
import os
import os.path
import sys
import struct
import threading
import time
import ctypes
import psutil
from PIL import ImageGrab, Image, ImageTk
import DBManger

class MyFrame(wx.Frame):
    #初始化部分数据
    def init(self):
        self.serverIP='127.0.0.1'
        self.int_searchServer=1
        thread_findServer = threading.Thread(target=self.findServer)
        thread_findServer.start()

    def __init__(self):
        super(MyFrame, self).__init__(parent=None, title="学生端程序-俞立栋", size=(320, 260))
        self.Center()
        panel=wx.Panel(self)
        self.init()
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='学号：')
        self.tc1 = wx.TextCtrl(panel)
        h1.Add(st1, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h1.Add(self.tc1, 2, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        h2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='姓名：')
        self.tc2 = wx.TextCtrl(panel)
        h2.Add(st2, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h2.Add(self.tc2, 2, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        h3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(panel, label='服务器IP地址：')
        self.tc3 = wx.TextCtrl(panel)
        self.tc3.SetValue(self.serverIP)
        h3.Add(st3, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h3.Add(self.tc3, 2, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

        h4 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='报道')
        btn2 = wx.Button(panel,label='全屏截图交作业')
        btn3 = wx.Button(panel, label='提问')
        h4.Add(btn1, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h4.Add(btn2, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h4.Add(btn3, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON,self.baodao,btn1)
        self.Bind(wx.EVT_BUTTON, self.uppic, btn2)
        self.Bind(wx.EVT_BUTTON, self.ask, btn3)

        h5 = wx.BoxSizer(wx.HORIZONTAL)
        btn4 = wx.Button(panel, label='自我测试')
        btn5 = wx.Button(panel, label='上传文件交作业')
        btn6 = wx.Button(panel, label='考试')
        h5.Add(btn4, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h5.Add(btn5, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h5.Add(btn6, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.test, btn4)
        self.Bind(wx.EVT_BUTTON, self.upfile, btn5)
        self.Bind(wx.EVT_BUTTON, self.test2, btn6)

        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(h1,flag=wx.EXPAND|wx.ALIGN_CENTER)
        vbox.Add(h2, flag=wx.EXPAND | wx.ALIGN_CENTER)
        vbox.Add(h3, flag=wx.EXPAND | wx.ALIGN_CENTER)
        vbox.Add(h4, flag=wx.EXPAND | wx.ALIGN_CENTER)
        vbox.Add(h5, flag=wx.EXPAND | wx.ALIGN_CENTER)

        panel.SetSizer(vbox)

    #接受广播线程体
    def findServer(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket对象
        sock.bind(('', 5109))  # 绑定socket
        try:
            while self.int_searchServer == 1:
                data, addr = sock.recvfrom(1024)  # 接收信息
                if data.decode() == 'ServerIP':  # 输出收到的信息
                    self.serverIP=addr[0]
                time.sleep(3)
        except:
            pass
    #报道
    def baodao(self,evt):  # 登录按钮事件处理函数
        xuehao = self.tc1.GetValue()  # 获取学号
        xingming = self.tc2.GetValue()  # 获取姓名
        serverIP = self.tc3.GetValue()
        if not re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', serverIP):
            dlg=wx.MessageDialog(None,'服务器IP地址不合法','很抱歉', wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((serverIP, 16109))
        except Exception as e:
            dlg = wx.MessageDialog(None, '现在不是点名时间', '很抱歉', wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()
            return

        # 获取客户端MAC地址，使用MAC+IP保证每台计算机每节课只能点名一次
        import uuid
        node = uuid.getnode()
        macHex = uuid.UUID(int=node).hex[-12:]
        mac = []
        for i in range(len(macHex))[::2]:
            mac.append(macHex[i:i + 2])
        mac = ''.join(mac)

        sock.sendall(','.join((xuehao, xingming, mac)).encode())

        data = sock.recv(1024).decode()
        if data.lower() == 'ok':
            # 点名成功
            sock.close()

            # 保存学号、姓名和服务器IP地址，方便下次自动填写信息
            path = os.getenv('temp')
            filename = path + '\\' + 'info.txt'
            with open(filename, 'w') as fp:
                fp.write(','.join((xuehao, xingming, serverIP)))
            dlg = wx.MessageDialog(None, xuehao + ',' + xingming + '  报到点名成功', '恭喜', wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()
            return
        elif data.lower() == 'repeat':
            sock.close()
            dlg = wx.MessageDialog(None, xuehao + '不允许重复报到', '很抱歉', wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()
            return
        elif data.lower() == 'notmatch':
            sock.close()
            dlg = wx.MessageDialog(None, xuehao + '学号与姓名不匹配', '很抱歉', wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()
            return
        elif data.lower() == 'daidianming':
            sock.close()
            dlg = wx.MessageDialog(None, xuehao + '不允许替别人点名，警告一次', '很抱歉', wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()
            return

    #全屏截图交作业
    def uppic(self,evt):
        pass

    # 提问
    def ask(self,evt):
        pass

    # 自我测试
    def test(self,evt):
        pass

    # 上传文件交作业
    def upfile(self,evt):
        pass

    # 考试
    def test2(self,evt):
        pass


class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        frame = MyFrame()
        frame.Show()
        return True

    def OnExit(self):
        print("应用程序退出")
        return 0


if __name__ == '__main__':
    app = App()
    app.MainLoop()