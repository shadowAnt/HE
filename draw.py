
import matplotlib.pyplot as plt
import prettyplotlib as ppl
from pylab import mpl
import numpy as np

font_size = 17
fig_size = (10, 6)
# 更新字体大小
mpl.rcParams['font.size'] = font_size
# 更新图表大小
mpl.rcParams['figure.figsize'] = fig_size
mpl.rcParams['font.sans-serif'] = ['SimHei']
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%.6s' % float(height))

# x = ['sever.setup()', 'user.setup()', 'sever.transmit()', 'user.receive()']
# y = [147.623+3.911, 74.29862022399902, 1841.8323993682861, 6.84356689453125]
#
# a = plt.bar(range(len(y)), y, color=['c', 'y', 'tan', 'r'], tick_label=x)
# autolabel(a)
# plt.xlabel(u"各个阶段")
# plt.ylabel('具体所用时间')
# plt.show()

# x = ['阶段1', '阶段2', '阶段3']
# y = [235, 6918.98, 262.43]
#
# a = plt.bar(range(len(y)), y, color=['c', 'y', 'tan', 'r'], tick_label=x)
# autolabel(a)
# plt.xlabel(u"各个阶段")
# plt.ylabel('具体所用时间')
# plt.show()

# plt.ylim=(10, 40000)
qNum = ['1', '500', '1000', '1500','2000']
stage1 = [8166, 7969, 8322, 8181, 8489 ]
stage2 = [16, 8494, 17236, 25993, 34572]
stage3 = [262, 123210, 243509, 364005, 493439]

x = np.arange(len(qNum))
width = 0.25
fig, ax = plt.subplots()

b1 = ax.bar(x-width, stage1, width, label='步骤1', color= 'r')
b2 = ax.bar(x, stage2, width, label='步骤2', color= 'b', tick_label= qNum)
b3 = ax.bar(x+width, stage3, width, label='步骤3', color= 'yellow')

for rect in b1+b2+b3:
    h = rect.get_height()
    ax.text(rect.get_x()+rect.get_width()/2, h, '%d' % int(h), ha='center', va='bottom')
plt.grid(axis= 'y')
plt.xlabel('单个用户连续发送请求的数量')
plt.ylabel('所用的时间 /ms')
# plt.title('不同请求数量各阶段所用时间')
plt.legend()
plt.show()