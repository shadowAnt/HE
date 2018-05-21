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

qNum = ['步骤1', '步骤2', '步骤3', '步骤4']
npp = [1457, 98.35, 40335, 762 ]
pp = [1601, 97.26, 55687, 765]

x = np.arange(len(qNum))
width = 0.4
fig, ax = plt.subplots()

b1 = ax.bar(x, npp, width, label='NPP', color= 'b')
b2 = ax.bar(x+width, pp, width, label='PP', color= 'yellow')
plt.xticks(x + width/2, qNum)
plt.grid(axis= 'y')

for rect in b1+b2:
    h = rect.get_height()
    ax.text(rect.get_x()+rect.get_width()/2, h, '%d' % int(h), ha='center', va='bottom')

# plt.xlabel('各步骤')
plt.ylabel('所用的时间 /ms')
# plt.title('方案3.1各阶段所用时间')
plt.legend()
plt.show()