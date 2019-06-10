import datetime
import socket
import random
import threading
import time
import struct
import os
import sys
import string
import re
import docx
import openpyxl
import wx
import xlrd
import DBManger
import SeeStu
import SeeAttendance
import RandomAsk
from PIL import ImageGrab


class MyFrame(wx.Frame):
    #初始化全局变量
    def init(self):
        self.sip = self.getIP()
        self.dbm = DBManger.DBM()
        self.dianming=0;
        self.shoupic=0;
        self.shouquestion=0;
        self.shoufile=0;

    def __init__(self):
        super(MyFrame, self).__init__(parent=None, title="教师端程序-俞立栋", size=(380, 530))
        self.Center()
        self.init()
        panel = wx.Panel(self)

        h1 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='导入学生名单', size=(110, 30))
        btn2 = wx.Button(panel, label='查看学生信息', size=(110, 30))
        btn3 = wx.Button(panel, label='查看本机IP地址', size=(110, 30))
        h1.Add(btn1, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h1.Add(btn2, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h1.Add(btn3, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn1)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn2)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn3)

        h2 = wx.BoxSizer(wx.HORIZONTAL)
        btn4 = wx.Button(panel, label='开始点名', size=(110, 30))
        btn5 = wx.Button(panel, label='结束点名', size=(110, 30))
        btn6 = wx.Button(panel, label='查看出勤情况', size=(110, 30))
        h2.Add(btn4, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h2.Add(btn5, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h2.Add(btn6, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.startName, btn4)
        self.Bind(wx.EVT_BUTTON, self.endName, btn5)
        self.Bind(wx.EVT_BUTTON, self.seeName, btn6)

        h3 = wx.BoxSizer(wx.HORIZONTAL)
        btn7 = wx.Button(panel, label='随机提问', size=(110, 30))
        btn8 = wx.Button(panel, label='查看提问情况', size=(110, 30))
        btn9 = wx.Button(panel, label='查看出勤情况', size=(110, 30))
        h3.Add(btn7, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h3.Add(btn8, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h3.Add(btn9, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.ranask, btn7)
        self.Bind(wx.EVT_BUTTON, self.seeQuestion, btn8)
        self.Bind(wx.EVT_BUTTON, self.seeAll, btn9)

        h4 = wx.BoxSizer(wx.HORIZONTAL)
        btn10 = wx.Button(panel, label='开始收截图作业', size=(110, 30))
        btn11 = wx.Button(panel, label='结束收截图作业', size=(110, 30))
        btn12 = wx.Button(panel, label='练习作者', size=(110, 30))
        h4.Add(btn10, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h4.Add(btn11, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h4.Add(btn12, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn10)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn11)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn12)

        h5 = wx.BoxSizer(wx.HORIZONTAL)
        btn13 = wx.Button(panel, label='开始接受提问', size=(110, 30))
        btn14 = wx.Button(panel, label='停止接受提问', size=(110, 30))
        btn15 = wx.Button(panel, label='学生主动提问情况', size=(110, 30))
        h5.Add(btn13, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h5.Add(btn14, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h5.Add(btn15, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn13)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn14)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn15)

        h6 = wx.BoxSizer(wx.HORIZONTAL)
        btn16 = wx.Button(panel, label='开始收文件作业', size=(110, 30))
        btn17 = wx.Button(panel, label='结束收文件作业', size=(110, 30))
        btn18 = wx.Button(panel, label='数据导出', size=(110, 30))
        h6.Add(btn16, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h6.Add(btn17, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h6.Add(btn18, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn16)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn17)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn18)

        h7 = wx.BoxSizer(wx.HORIZONTAL)
        btn19 = wx.Button(panel, label='生成word试卷', size=(110, 30))
        btn20 = wx.Button(panel, label='合并数据库', size=(110, 30))
        btn21 = wx.Button(panel, label='关闭所有学生机器', size=(110, 30))
        h7.Add(btn19, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h7.Add(btn20, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h7.Add(btn21, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn19)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn20)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn21)

        h8 = wx.BoxSizer(wx.HORIZONTAL)
        btn22 = wx.Button(panel, label='导入题库', size=(110, 30))
        btn23 = wx.Button(panel, label='开始学生自测', size=(110, 30))
        btn24 = wx.Button(panel, label='停止学生自测', size=(110, 30))
        h8.Add(btn22, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h8.Add(btn23, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h8.Add(btn24, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn22)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn23)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn24)

        h9 = wx.BoxSizer(wx.HORIZONTAL)
        btn25 = wx.Button(panel, label='开始考试', size=(110, 30))
        btn26 = wx.Button(panel, label='结束考试', size=(110, 30))
        btn27 = wx.Button(panel, label='删除考试数据', size=(110, 30))
        h9.Add(btn25, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h9.Add(btn26, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h9.Add(btn27, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn25)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn26)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn27)

        h10 = wx.BoxSizer(wx.HORIZONTAL)
        btn28 = wx.Button(panel, label='开始屏幕广播', size=(110, 30))
        btn29 = wx.Button(panel, label='结束屏幕广播', size=(110, 30))
        btn30 = wx.Button(panel, label='useless', size=(110, 30))
        h10.Add(btn28, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h10.Add(btn29, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        h10.Add(btn30, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.impStuMess, btn28)
        self.Bind(wx.EVT_BUTTON, self.seeStu, btn29)
        self.Bind(wx.EVT_BUTTON, self.bt_ip, btn30)

        v = wx.BoxSizer(wx.VERTICAL)
        v.Add(h1,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h2,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h3,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h4,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h5,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h6,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h7,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h8,1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h9, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        v.Add(h10, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=5)
        panel.SetSizer(v)

    #导入学生信息
    def impStuMess(self,event):
        dlg = wx.FileDialog(self,message='请选择Excel文件',wildcard="*.xls",style=wx.FD_OPEN)
        if dlg.ShowModal()==wx.ID_OK:
            filename=dlg.GetPath()
            print(filename)
            dlg.Destroy()
            if filename:
                # 读取数据并导入数据库
                workbook = xlrd.open_workbook(filename=filename)
                sheet1 = workbook.sheet_by_index(0)
                # Excel文件必须包含4列，分别为学号、姓名、专业年级、课程名称
                if sheet1.ncols != 4:
                    dlg2=wx.MessageDialog(None, u"Excel文件格式不对", u"很抱歉", wx.YES_DEFAULT | wx.ICON_QUESTION)
                    if dlg2.ShowModal() == wx.ID_YES:
                        self.Close(True)
                    dlg2.Destroy()
                    return
                # 遍历Excel文件每一行
                for rowIndex in range(1, sheet1.nrows):
                    row = sheet1.row(rowIndex)
                    sql = "insert into students(xuehao,xingming,zhuanye,kecheng) values('" \
                          + "','".join(map(lambda item: str(item.value).strip(), row)) + "')"
                    self.dbm.doSQL(sql)
                dlg3= wx.MessageDialog(None, u"导入成功", u"恭喜", wx.YES_DEFAULT | wx.ICON_QUESTION)
                if dlg3.ShowModal() == wx.ID_YES:
                    self.Close(True)
                dlg3.Destroy()

    #查看学生信息
    def seeStu(self,event):
        xueshengZhuanye = self.dbm.getZhuanye()
        SeeStuDlg=SeeStu.SeeStu(self.dbm,zydata=xueshengZhuanye)
        SeeStuDlg.Show()

    # 获取本机IP
    def getIP(self):
        # 获取本机IP
        serverIP = socket.gethostbyname(socket.gethostname())
        if serverIP.startswith('127.0.'):
            addrs = socket.getaddrinfo(socket.gethostname(), None, 0, socket.SOCK_STREAM)
            addrs = [x[4][0] for x in addrs]
            serverIP = [x for x in addrs if ':' not in x][0]
        return serverIP

    # 查看本机IP
    def bt_ip(self,evt):
        dlg3 = wx.MessageDialog(None, self.getIP(), u"本机IP地址", wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dlg3.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg3.Destroy()

    # 开始点名
    def startName(self,evt):
        if self.dianming == 1:
            dlg=wx.MessageDialog(None,'现在正在点名','很抱歉',wx.YES_DEFAULT)
            if dlg.ShowModal()==wx.ID_YES:
                self.Close()
            return
        dlg = wx.MessageDialog(None, '现在开始点名', '提示', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close()
        # 开始点名
        self.dianming=1
        global tDianming_id
        t = threading.Thread(target=self.thread_Dianming)
        t.start()
        tDianming_id = t.ident

    # 结束点名
    def endName(self,evt):
        if self.dianming == 0:
            dlg = wx.MessageDialog(None, '还没开始点名', '很抱歉', wx.YES_DEFAULT)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close()
            return

        # 停止点名
        self.dianming=0
        sockDianming.close()
        time.sleep(0.1)
        sql = 'select zhuanye from students where xuehao=(select xuehao from dianming where shijian<="' \
              + self.dbm.getCurrentDateTime() + '"  order by shijian desc limit 1)'
        currentZhuanye = self.dbm.getDataBySQL(sql)[0][0]
        sql = 'select count(zhuanye) from students where zhuanye="' + currentZhuanye + '"'
        totalRenshu = self.dbm.getDataBySQL(sql)[0][0]

        sql = 'select count(xuehao) from dianming where shijian<="' + self.dbm.getCurrentDateTime() \
              + '" and shijian>="' + self.dbm.getStartDateTime() + '"'
        totalShidao = self.dbm.getDataBySQL(sql)[0][0]

        message = '设置成功，现在停止点名!\n当前点名专业：' + currentZhuanye \
                  + '\n应到人数：' + str(totalRenshu) + '\n实到人数：' + str(totalShidao)
        dlg = wx.MessageDialog(None, '结束点名', '提示', wx.YES_DEFAULT)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close()

    # 开始点名
    def thread_Dianming(self):
        # 开始监听
        global sockDianming
        sockDianming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockDianming.bind(('', 16109))
        sockDianming.listen(200)
        while self.dianming == 1:
            try:
                # 接受一个客户端连接
                conn, addr = sockDianming.accept()
            except:
                continue
            data = conn.recv(1024).decode()
            try:
                # 客户端发来的消息格式为：学号,姓名,MAC地址
                xuehao, xingming, mac = data.split(',')
            except:
                conn.sendall('notmatch'.encode())
                conn.close()
                continue
            # 防SQL注入
            xuehao = re.sub(r'[;"\'=]', '', xuehao)
            xingming = re.sub(r'[;"\'=]', '', xingming)
            # 首先检查学号与姓名是否匹配，并且与数据库中的学生信息一致
            sqlIfMatch = "select count(xuehao) from students where xuehao='" + xuehao + "' and xingming='" + xingming + "'"
            if self.dbm.getDataBySQL(sqlIfMatch)[0][0] != 1:
                conn.sendall('notmatch'.encode())
                conn.close()
            else:
                # 记录该学生点名信息：学号，姓名，时间，并反馈给客户端点名成功，然后客户端关闭连接
                currentTime = self.dbm.getCurrentDateTime()
                # 获取一个半小时之前的时间
                startTime = self.dbm.getStartDateTime()
                # 查看是否已经点名过，避免一个半小时内重复点名
                sqlShifouChongfuDianming = "select count(xuehao) from dianming where xuehao='" \
                                           + xuehao + "' and shijian >='" + startTime + "'"

                if self.dbm.getDataBySQL(sqlShifouChongfuDianming)[0][0] != 0:
                    conn.sendall('repeat'.encode())
                    conn.close()
                else:
                    # 检查是否代替点名，根据学生端IP地址识别
                    sqlShifouDaiDianming = "select count(ip) from dianming where ip='" \
                                           + addr[0] + "' and shijian >='" + startTime + "'"
                    sqlMacShifouChongfu = "select count(mac) from dianming where mac='" \
                                          + mac + "' and shijian>='" + startTime + "'"

                    if self.dbm.getDataBySQL(sqlShifouDaiDianming)[0][0] != 0 \
                            or self.dbm.getDataBySQL(sqlMacShifouChongfu)[0][0] != 0:
                        conn.sendall('daidianming'.encode())
                        conn.close()
                    else:
                        # 点名
                        sqlDianming = "insert into dianming(xuehao,shijian,ip,mac) values('" \
                                      + xuehao + "','" + currentTime + "','" + addr[0] + "','" + mac + "')"
                        self.dbm.doSQL(sqlDianming)
                        conn.sendall('ok'.encode())
                        conn.close()
        sockDianming.close()
        sockDianming = None

    def seeName(self,evt):
        xueshengZhuanye = self.dbm.getZhuanye()
        SeeADlg = SeeAttendance.AttendanceFrame(self.dbm, zydata=xueshengZhuanye)
        SeeADlg.Show()

    def ranask(self,evt):
        xueshengZhuanye = self.dbm.getZhuanye()
        RandomDlg=RandomAsk.RandomAsk(self.dbm,zydata=xueshengZhuanye)
        RandomDlg.Show()

    def seeQuestion(self,evt):
        pass

    def seeAll(self,evt):
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
