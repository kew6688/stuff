
import random
import sys
from math import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import turtle
turtle.setup(1200, 800)
turtle.delay (0)
turtle.goto (0, -200)
turtle.begin_poly()
turtle.setheading(150)
turtle.fd (70)
turtle.circle(70 * -3.745, 45)
turtle.circle(70 * -1.431, 165)
turtle.left (120)
turtle.circle(70 * -1.431,165)
turtle.circle(70 * -3.745, 45)
turtle.fd(70)
turtle.end_poly()
angle_coord_list=turtle.get_poly()
turtle.bye()
# angle_coord_list = ((0.00, -200.00), (-86.60 ,-150.00), (-117.49 ,-130.08), (-146.28, -107.24), (-172.69,-81.68), 
#                     (-196.6, -53.65), (-217.38, -23.43), (-235.23,8.69), (-249.85,42.41), (-261.99,77.40), 
#                     (-265.49, 102.74), (-265.28, 128.46), (-260.47, 153.73), (-251.21, 177.73), (-237.81,199.68), 
#                     (-220,69,218.88), (-200.41, 234,70),(-177.63,246.64), (-153.08, 254.31), (-127.55, 257.46), 
#                     (-101.87, 255.99), (-76.87, 249.90), (-53.36, 239.52), (-32.09,225.05), (-13.75, 207.02), 
#                     (1.06,185.99), (15.87, 207.02),(34.21,225.05), (55,48, 239.52), (78.99, 249,96), 
#                     (103.99,255.99), (129.67,257.6), (155.20,254.31), (179.75,246,64),(202.53,234,70), 
#                     (222.81,218.88), (239.93,199.68), (253.33,177.73), (262.59,153.75), (267.40,128.46), 
#                     (267.61, 102.74), (263.21,77.40), (251.97, 42.41), (237.35,8.69), (219.50, -23.43), 
#                     (198.58, -53.65), (174.81, -81.68), (148,40,-107.24), (119.61, -130.08), (88.72, -150.00),
#                     (2.12, -200.00))
new_coord_list = []
# 用旧坐标生成新坐标
for order2, angle_coord in enumerate(angle_coord_list):
    if order2 + 1 < len(angle_coord_list):
        #以0.25为间隔,计算两点之间需要分成多少份
        pointnum_x=int(abs(angle_coord_list[order2+1][0]-angle_coord_list[order2][0])/0.25)
        pointnum_y=int(abs(angle_coord_list[order2+1][1]-angle_coord_list[order2][1])/0.25)
        # 取两值之间大的一个,如果不取,会出现点分布不均匀的情况
        pointnum = max(pointnum_x, pointnum_y)
        # 计算两点之间 横纵左边的最小步距
        step_x=((angle_coord_list[order2+1][0]-angle_coord_list[order2][0])/pointnum)
        step_y=((angle_coord_list[order2+1][1]-angle_coord_list[order2][1])/pointnum)
        # 一次得出新坐标的每个X,Y值
        for i in range (pointnum):
            new_coord = (round(angle_coord_list[order2][0] + (i+1)*step_x,2), 
                         round(angle_coord_list[order2][1]+(i+1)*step_y,2))
            if new_coord not in new_coord_list:
                # 新爱心坐标列表依次获取
                new_coord_list.append(new_coord)

# 定义 pyqt5类的类(心累)
class QheartWindow(QMainWindow):
# python类的初始化init--
    def __init__(self):
        # 类的继承
        super(QheartWindow, self).__init__(None)
        # 基础部件
        self.setWindowTitle('QSY')
        self.resize(QDesktopWidget().screenGeometry().width(),QDesktopWidget().screenGeometry().height())
        self.move(1000, 1000)# 位置
        self.setStyleSheet("QMainWindow{background-color:#000000}")# 背景为黑
        # 运行主过程
        self.startTimer(50)# 设置界面刷新时间 1000=1s (电脑算力不够会不流畅)
        self.readlist = 0# 画面显示的第几界面(用10个界面的不规律循环产生心跳效果)
        self.largen = True# 确定心脏是该收缩还是舒展
        self.cen_x=QDesktopWidget().screenGeometry().width()/2#确定心脏的中心点横坐标
        self.cen_y=QDesktopWidget().screenGeometry().height()/2-50#确定心脏的中心点纵坐标
        self.cent = 100# 弥补心脏中心空洞的矩形范围的一半
        self.makecoord()# 生成所有点的坐标及属性

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)


    def makecoord(self):
        #产生主爱心的点--
        self.coord_list1 = []
        # 初始化主心脏的坐标列表
        self.all_coord_list1 = [] # 初始化主心脏跳动起来(每帧)的所有坐标列表
        # 确定受心从外层到内层,各个层级的稠密程度
        # 用圆形'x平方+y平方=100的平方'的公式确定延伸,
        # 因为当x趋近于0时,y不仅值大y变化平缓,正好符合剧中爱心的外密內稀
        #我尝试过高斯分布等,效果都没这个好
        expend_list=[int(9*round(sqrt(10000-(i*i)),4))+200 for i in range(0,105,5)]
        # 用循环读取稠密程度列表
        for order, expend in enumerate(expend_list):
            offset=int((len(expend_list)-sqrt((len(expend_list)**2)-((order+1)**2))+order+2)*0.8)

            for new_coord in new_coord_list:
                if random.randint(1, 8) == 1:
                    # 随机生成点的尺寸,有大有小比较好看
                    size = random.randint(1, 4)
                    #调用上边的稠密程度参数生成内外各个层级的点
                    heart_x = (new_coord[0] * (sqrt(expend) * 0.024))
                    heart_y = (new_coord[1] * (sqrt(expend) * 0.026))
                    # 转换为屏幕中心的点,因为屏幕左上角才为pyqt5的(0, 0)点
                    x = int((heart_x) + self.width() / 2)
                    y = int((-heart_y) + self.height() / 2)
                    # 随机生成偏移量
                    draw_x = x + random.randint(-offset, offset)
                    draw_y = y + random.randint(-offset, offset)
                    # 随机生成颜色(我用PS试的颜色,可以自己调整)
                    colorint = random.randint(1, 7)
                    if colorint == 1:
                        color = QColor(36,140,230, 40)
                    elif colorint == 2:
                        color = QColor(27, 117, 196, 50) # 用白粉 
                    # elif colorint == 3:
                    #     color = QColor(0, 76,153) # 用深红 
                    # elif colorint == 4:
                    #     color = QColor(102, 0, 204) 
                    # elif colorint == 5:
                    #     color = QColor(0, 0, 255) # 红色 # 根据颜色需求调解,比如主爱心白色较多,就在下面又引用了白粉色 
                    else:
                        color = QColor(11, 155, 255, 50)# 用白粉
    #为了省内存,也为了画面更流畅,这里只添加不同坐标、属性的点 
                    if (draw_x, draw_y, size, color) not in self.coord_list1:
                        self.coord_list1.append((draw_x, draw_y, size, color)) # 把初始化的爱心点列表作为画面第1颇 
        self.all_coord_list1.append(self.coord_list1)
# I!重点来了!!!下面做出心脏跳动的效果 
        for su in range(1,10): # 因为我分了10嫩,所以要生成帧的点
            coord_temporary1 = [] # 遍历第1颇所有点 
            for coord in self.coord_list1:
#跳动效果公式 # 基本原理是根据各点与中心点的距离远近改变向外放大的程度 #就有了内間变化更剧烈的效果(跳动) 
                flexk=((536-1.11111111111+sqrt(((coord[0] - self.cen_x)**2)+((coord[1] - self.cen_y)**2)))*(0.00006)*su)- (su*0.01+0.017) #保证放大参数为正数 
                if flexk < 0:
                    flexk = 0 #高中学的以特定点为中心放大缩小公式 
                new_x = self.cen_x - (1 + flexk) * (self.cen_x - coord[0]) 
                new_y = self.cen_y - (1 + flexk)*(self.cen_y - coord [1]) # 收集起来
                coord_temporary1.append((new_x, new_y, coord[2], coord[3])) # 保存到下一顿 
            self.all_coord_list1.append(coord_temporary1)


        self.coord_list2 = [] 
        self.all_coord_list2 = []# 这个列表的点为实时无规律变化,不同于主爱心的点有规律 # 注意这里只到90,否则爱心中心不好看 
        expend_list=[int (round(sqrt(10000-(i*i))+100-1,4)) for i in range(0,92,5)] 
        for order, expend in enumerate(expend_list):
            offset=int(len(expend_list)-sqrt((len(expend_list)**2)-((order+1)**2))+2)+10

            for new_coord in new_coord_list:
                if random.randint(1, 7) == 1:
                    size= random.randint(1, 3)
                    heart_x = new_coord[0]*(sqrt(expend) *0.075)
                    heart_y= new_coord[1]* (sqrt(expend) * 0.078)
                    x = int((heart_x) + self.width() / 2)
                    y = int((-heart_y)+self.height() / 2)
                    # 偏移量
                    draw_x = x + random.randint(-offset, offset)
                    draw_y= y + random.randint(-offset, offset)
                    #外围颜色更深,所以布局如下
                    colorint= random.randint(1, 10)
                    if colorint == 1: #粉色
                        color =QColor(77, 43, 190,60)
                    elif colorint == 2:
                        color= QColor(23, 53, 198)
                    elif colorint == 3 or colorint == 5:
                        color= QColor (45, 25, 155) ##
                    elif colorint == 4:
                        color = QColor (51, 51, 232)
                    elif colorint == 7:
                    ###
                        color =QColor(0, 0, 255) #8
                    else:
                        color= QColor (20, 79, 200,60)
                    if (draw_x, draw_y, size, color) not in self.coord_list2: 
                        self.coord_list2.append((draw_x, draw_y, size, color))
                # 爱心中心黑区的点,为了好看地弥补黑区,同上理

        for expendx in range(-self.cent, self.cent):
            for expendy in range(-self.cent, self.cent): 
                if random.randint(1, 100) == 1:
                    size= random.randint(1, 3)
                    heart_x = expendx
                    heart_y = expendy
                    x = int((heart_x) + self.width() / 2) 
                    y = int((-heart_y)+self.height()/2 - 40)
                    # 偏移量
                    offset = 20
                    draw_x = x + random.randint(-offset, offset) 
                    draw_y= y + random.randint(-offset, offset)
                    #颜色
                    colorint =random.randint(1, 10) 
                    if colorint == 1: #粉色
                        color =QColor(77, 43, 190, 60)
                    # elif colorint == 2:
                    #     color= QColor(23, 181, 198)
                    # elif colorint == 3 or colorint == 5:
                    #     color= QColor (45, 25, 155) ##
                    # elif colorint == 4:
                    #     color = QColor (51, 51, 232)
                    # elif colorint == 7:
                    #     color =QColor(0, 0, 255) #8
                    else:
                        color= QColor (20, 79, 200, 60)
                    if (draw_x, draw_y, size, color) not in self.coord_list2:
                        self.coord_list2.append((draw_x, draw_y, size, color))

    def paintEvent(self, event):
        self.painter = QPainter(self) # #974QPainter 
        self.painter.begin(self)
        if self.readlist >= 0:
            # ASERTERS, ITE 
            coord_temporary2 = [] 
            offset = (9 - self.readlist) * 6 
            if offset > 0: 
                for coord in self.coord_list2:
                    new_x = coord[0] + random.randint(-offset, offset) 
                    new_y = coord[1] + random.randint(-offset, offset)
                    coord_temporary2.append((new_x, new_y, coord[2], coord[3])) 
            else:
                coord_temporary2 = self.coord_list2 # # # #, IAR
            self.all_coord_list=self.all_coord_list1[self.readlist]+coord_temporary2 #
                
                
        for coord in self.all_coord_list: 
            if coord[2] <= 3: # RAR+F334@ti
                self.pen = QPen() 
                self.pen.setColor(coord[3]) 
                self.pen.setWidth(coord[2]) 
                self.painter.setPen(self.pen)
                self.painter.drawPoint(int(coord[0]), int(coord[1]),) 
            else: # to R F 3ig2@t
                self.painter.setBrush(coord[3])
                self.painter.drawEllipse(int(coord[0]), int(coord[1]), coord[2] -1, coord[2]-1) 
        self.painter.end()
        
        if self.readlist == 9:
            self.largen = False
        elif self.readlist == 0:
            self.largen = True

        if self.largen:
            self.readlist += 1
        else:
            self.readlist -= 1

    def timerEvent(self, event):
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QheartWindow()
    window.show()
    sys.exit(app.exec_())
