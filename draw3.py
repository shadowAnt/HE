import matplotlib.pyplot as plt
import prettyplotlib as ppl
from pylab import mpl
import numpy as np

font_size = 12
fig_size = (8, 6)
# 更新字体大小
mpl.rcParams['font.size'] = font_size
# 更新图表大小
mpl.rcParams['figure.figsize'] = fig_size
mpl.rcParams['font.sans-serif'] = ['SimHei']


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%.6s' % float(height))

x = ['sever.setup()', 'user.setup()', 'sever.transmit()', 'user.receive()']
y = [147.623+3.911, 74.29862022399902, 1481.8323993682861, 6.84356689453125]

width = 0.5
a = plt.bar(range(len(y)), y, width, color=['b', 'r', 'yellow', 'black'], tick_label=x)
autolabel(a)
plt.grid(axis= 'y')
# plt.xlabel(u"各个阶段")
plt.ylabel('具体所用时间 /ms')
plt.show()
