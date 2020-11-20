# Labelimg改进版本

本项目是Labelimg若干功能的改进版本，主要是为了让标注过程更方便，改进原来某些设计的不合理的地方。

原始代码是下载的`1.8.4 (2020-11-04)`版本，参考[HISTORY.rst](https://github.com/tzutalin/labelImg/blob/master/HISTORY.rst)

# 打开方法

```shell
# 1.安装requirements\requirements-linux-python3.txt中的依赖
# 2.对于qt5py3（其它的qt或python版本参考Makefile中具体的命令）
pyrcc5 -o libs/resources.py resources.qrc
# 3.修改data\predefined_classes.txt中的预定义label
# 4.打开软件
python labelImg.py
```

# 功能改进点

## 鼠标划入label清单时高亮提示

![](demo\label_list_highlight.gif)

## 拖拽鼠标右键快速调整矩形框

原始的软件必须要先选中一个顶点然后拖拽修改，当长时间标注数据时，每次先寻找顶点的过程很耗费精力。而右键拖拽时无需先选中某个顶点按钮，直接会将距离鼠标当前位置最近的一个顶点吸附到鼠标。
![](demo\drag_rect.gif)

目标框叠加在一起时：如果没有选中任何目标框，默认会选择最顶层的目标框激活并吸附最近的顶点。
![](demo\drag_rect1.gif)

目标框叠加在一起时：如果预先选中了一个特定的目标框，会自动选择被选中的目标框，吸附其最近的顶点，不管其它的目标框。如果遇到一个小框被大框覆盖的情况，只能将大框移开，然后修改小框。通过这个右键拖拽功能，可以先通过高亮提示选中小框，然后直接右键拖拽编辑。
![](demo\drag_rect2.gif)

## 复制label功能

快捷键：C
如果目前没有选中任何的label，直接复制当前图片的所有label到下一张图片。
![](demo\copy_all.gif)

如果目前存在一个选中的label，只会复制这个label到下一张图片，并且继续设置该label为选中状态，以实现连续"C"。
![](demo\copy_one.gif)

注意，如果前后图片的尺寸不一样，超出图片范围的框的长和宽会被压缩为0。坐标以图片左上角为原点。

## 修改label的弹窗改进

原来的修改label的弹窗不是很方便，做了一点改进：
快捷键：E  （选中目标框并按下后弹出设置窗口）

对于原来的弹窗，如果鼠标位于软件窗口的右侧或下侧，弹窗总会超出软件边界，需要拖拽进来再选择label。现在弹窗的区域直接限制在了整个软件范围之内。
![](demo\label_edit_area.gif)

对于原来的弹窗，必须按下其中的按钮才可以关闭，弹窗打开时，点击其它区域都无响应。现在点击弹窗外的其他区域会自动关闭弹窗，并且不会进行修改label的操作。
![](demo\label_edit_auto_close.gif)

## 快捷键改变

- X：删除当前选中的目标框

## 删除的功能

- 删除了右键菜单功能，因为可能与第二章的右键拖拽功能冲突导致BUG，同时其中的功能都已经设置了快捷键进行实现，见上文。原始的右键菜单如图：
![](demo\menu_original.png)
