import datetime

import pymysql


class DBM():
    def __init__(self):
        self.conn = pymysql.connect("localhost", 'root', 'root', 'yld_pysql')

    def __del__(self):
        self.conn.close()

    # 查询数据库，获取学生专业列表
    def getZhuanye(self):
        cursor = self.conn.cursor()
        cursor.execute('select distinct(zhuanye) from students')
        temp = cursor.fetchall()
        xueshengZhuanye = []
        for line in temp:
            xueshengZhuanye.append(line[0])
        return xueshengZhuanye

    # 获取指定专业的学生名单
    def getXuehaoXingming(self, name):
        # print(name)
        if name is None:
            return
        sql = 'select xuehao,xingming from students where zhuanye = %s order by xuehao'
        param = [name]
        cursor = self.conn.cursor()
        cursor.execute(sql, param)
        temp = cursor.fetchall()
        print('按照专业查询结果：', temp)
        cursor.close()
        # xueshengXinxi = []
        # for line in temp:
        #     xueshengXinxi.append(line[0] + ',' + line[1])
        return temp

    # 获取指定学号的出勤次数
    def getChuqinCishu(self, xuehao):
        cursor = self.conn.cursor()
        cursor.execute("select count(xuehao) from dianming where xuehao=%s", [xuehao])
        temp = cursor.fetchall()
        cursor.close()
        return temp[0][0]

    # 获取指定学号的学生提问总得分
    def getTiwenDefen(self, xuehao):
        cursor = self.conn.cursor()
        cursor.execute("select sum(defen) from tiwen where xuehao=%s", [xuehao])
        temp = cursor.fetchall()
        cursor.close()
        return temp[0][0]

    # 获取指定学号的学生主动提问次数
    def getZhudongTiwenCishu(self, xuehao):
        cursor = self.conn.cursor()
        cursor.execute(
            "select count(xuehao) from xueshengtiwen where xuehao=%s and wenti not like '老师回复%'", [xuehao])
        temp = cursor.fetchall()
        cursor.close()
        return temp[0][0]

    # 查看学生在线考试得分
    def getKaoshiDefen(self, xuehao):
        cursor = self.conn.cursor()
        cursor.execute("select count(xuehao) from kaoshi where xuehao=%s and shifouzhengque='Y'", [xuehao])
        temp = cursor.fetchall()
        cursor.close()
        return temp[0][0]

    # 获取指定SQL语句查询结果
    def getDataBySQL(self, sql, lst=None):
        cursor = self.conn.cursor()
        if lst == None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, lst)
        result = cursor.fetchall()
        cursor.close()
        return result

    # 执行SQL语句
    def doSQL(self, sql, lst=None):
        cursor = self.conn.cursor()
        if lst == None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, lst)
        self.conn.commit()
        cursor.close()

    # 当前日期时间，格式为“年-月-日 时:分:秒”
    def getCurrentDateTime(self):
        return str(datetime.datetime.now())[:19]

    # 当前日期时间之前一个半小时前的时间，主要用来避免重复点名
    def getStartDateTime(self):
        now = datetime.datetime.now()
        now = now + datetime.timedelta(minutes=-90)
        return str(now)[:19]
