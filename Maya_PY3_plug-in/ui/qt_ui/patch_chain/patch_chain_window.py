# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
import inspect
import math

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
maya_version_int = int(maya_version)
for i in range(30):
    test_version = maya_version_int - i
    maya_version = str(test_version)
    library_path = root_path + '\\' + maya_version
    if os.path.isdir(library_path):
        sys.path.append(library_path)
        maya_version_int = test_version
        break

import general_settings
from general_settings import *
importlib.reload(general_settings)

import ui_edit
importlib.reload(ui_edit)
from ui_edit import *

import maya_common
importlib.reload(maya_common)
from maya_common import *


# 三次贝塞尔：控制点 (x1,y1)、(x2,y2)，端点 (0,0)->(1,1)
def _bezier_poly(t, c1, c2):
    a = 1.0 - t
    return 3.0 * a * a * t * c1 + 3.0 * a * t * t * c2 + t * t * t


def bezier_x(t, x1, x2):
    return _bezier_poly(t, x1, x2)


def bezier_y(t, y1, y2):
    return _bezier_poly(t, y1, y2)


# 权重缓动：给定 u∈[0,1]，求解 t 使 X(t)=u，返回 Y(t)
def bezier_weight(u, x1, y1, x2, y2):
    u = max(0.0, min(1.0, u))
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) * 0.5
        if bezier_x(mid, x1, x2) < u:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) * 0.5
    return bezier_y(t, y1, y2)


# 贝塞尔预设方案：(x1, y1, x2, y2)
BEZIER_PRESETS = {
    '线性过渡': (1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0),
    '平滑过渡': (1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0),
    '缓入': (1.0 / 3.0, 0.0, 2.0 / 3.0, 0.0),
    '缓出': (1.0 / 3.0, 1.0, 2.0 / 3.0, 1.0),
}


# 在「权重=1」的硬归属基础上沿离散环方向做贝塞尔核扩散（纯算法，不依赖 Maya 平滑命令）
# owner_at(k)：返回第 k 个离散环的硬归属 [(标识, 源权重), ...]（中点双归属时两个 0.5）
# q：当前顶点所在环索引；radius_up/down：向上/下游扩散半径（环数）；periodic：环形
def diffuse_along_rings(owner_at, q, total, radius_up, radius_down, bez, periodic=False):
    x1, y1, x2, y2 = bez
    radius_up = max(0, int(radius_up))
    radius_down = max(0, int(radius_down))
    raw = {}
    for dk in range(-radius_up, radius_down + 1):
        if periodic:
            k = (q + dk) % total
            radius = radius_up if dk <= 0 else radius_down
        else:
            k = q + dk
            if k < 0 or k >= total:
                continue
            radius = radius_up if dk <= 0 else radius_down
        if abs(dk) > radius:
            continue
        if dk == 0 or radius == 0:
            falloff = 1.0
        else:
            falloff = 1.0 - bezier_weight(abs(dk) / float(radius), x1, y1, x2, y2)
        owners = owner_at(k)
        if owners:
            for oid, src_w in owners:
                raw[oid] = raw.get(oid, 0.0) + falloff * src_w
    total_w = sum(raw.values()) or 1.0
    return dict((oid, v / total_w) for oid, v in raw.items())


# 环 k（每段 seg 个环）在三种锚点下的硬归属索引（相对段起点 b）
# 返回段内归属索引列表 [(相对索引, 源权重)]，相对索引可能为 -1（上一根）或 0/1
def ring_owner_offsets(k, seg, anchor, periodic=False):
    b = k // seg
    u = (k % seg) / float(seg)
    if anchor == '上一根骨骼权重=1':
        if u == 0.0 and (b > 0 or periodic):
            # 根部特殊处理：b==1（第一根骨骼位置）时不再把权重归给根骨骼，
            # 而是归当前骨骼，避免根骨骼在环0和环seg两处都是1造成的不自然平台
            if b == 1 and not periodic:
                return [(0, 1.0)]
            return [(-1, 1.0)]
        return [(0, 1.0)]
    if anchor == '就近骨骼权重=1':
        if u < 0.5:
            return [(0, 1.0)]
        if u > 0.5:
            return [(1, 1.0)]
        return [(0, 0.5), (1, 0.5)]
    # 自身骨骼权重=1：整段 [b, b+1) 归 b（末环 u=0 归当根）
    return [(0, 1.0)]


# 贝塞尔曲线可视化 / 拖拽编辑控件
class BezierCanvas(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float, float, float, float)  # x1, y1, x2, y2
    GRID = 0.25

    def __init__(self, parent=None):
        super(BezierCanvas, self).__init__(parent)
        self.x1 = 1.0 / 3.0
        self.y1 = 0.0
        self.x2 = 2.0 / 3.0
        self.y2 = 1.0
        self._dragging = None  # 1 或 2
        self._snap = False
        self.setMinimumHeight(180)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def sizeHint(self):
        return QtCore.QSize(400, 200)

    def minimumSizeHint(self):
        return QtCore.QSize(320, 180)

    def set_values(self, x1, y1, x2, y2):
        self.x1 = max(0.0, min(1.0, x1))
        self.y1 = max(0.0, min(1.0, y1))
        self.x2 = max(0.0, min(1.0, x2))
        self.y2 = max(0.0, min(1.0, y2))
        self.update()

    def _pad(self):
        return 26

    def _to_widget(self, x, y):
        pad = self._pad()
        w = self.width() - 2 * pad
        h = self.height() - 2 * pad
        px = pad + x * w
        py = self.height() - pad - y * h
        return px, py

    def _to_norm(self, px, py):
        pad = self._pad()
        w = self.width() - 2 * pad
        h = self.height() - 2 * pad
        x = (px - pad) / w
        y = (self.height() - pad - py) / h
        return max(0.0, min(1.0, x)), max(0.0, min(1.0, y))

    def _handle_pos(self, idx):
        if idx == 1:
            return self._to_widget(self.x1, self.y1)
        return self._to_widget(self.x2, self.y2)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pad = self._pad()
        w = self.width()
        h = self.height()

        # 背景
        painter.fillRect(self.rect(), QtGui.QColor(35, 35, 38))

        # 网格
        painter.setPen(QtGui.QPen(QtGui.QColor(60, 60, 65), 1))
        for i in range(1, 4):
            x = pad + (w - 2 * pad) * i / 4.0
            y = pad + (h - 2 * pad) * i / 4.0
            painter.drawLine(int(x), pad, int(x), h - pad)
            painter.drawLine(pad, int(y), w - pad, int(y))

        # 边框
        painter.setPen(QtGui.QPen(QtGui.QColor(120, 120, 125), 1))
        painter.drawRect(pad, pad, w - 2 * pad, h - 2 * pad)

        # 控制折线（虚线）
        p0 = self._to_widget(0.0, 0.0)
        p1 = self._handle_pos(1)
        p2 = self._handle_pos(2)
        p3 = self._to_widget(1.0, 1.0)
        pen = QtGui.QPen(QtGui.QColor(140, 140, 145), 1)
        pen.setStyle(QtCore.Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(int(p0[0]), int(p0[1]), int(p1[0]), int(p1[1]))
        painter.drawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))
        painter.drawLine(int(p2[0]), int(p2[1]), int(p3[0]), int(p3[1]))

        # 曲线
        painter.setPen(QtGui.QPen(QtGui.QColor(90, 180, 255), 2))
        last = None
        for i in range(101):
            t = i / 100.0
            u = bezier_x(t, self.x1, self.x2)
            v = bezier_y(t, self.y1, self.y2)
            pt = self._to_widget(u, v)
            if last is not None:
                painter.drawLine(int(last[0]), int(last[1]), int(pt[0]), int(pt[1]))
            last = pt

        # 端点
        painter.setBrush(QtGui.QColor(200, 200, 200))
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        for pt in (p0, p3):
            painter.drawEllipse(int(pt[0]) - 4, int(pt[1]) - 4, 8, 8)

        # 控制手柄
        for idx, pt in ((1, p1), (2, p2)):
            painter.setBrush(QtGui.QColor(255, 180, 60))
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
            painter.drawEllipse(int(pt[0]) - 6, int(pt[1]) - 6, 12, 12)

        painter.end()

    def _hit_handle(self, px, py):
        for idx in (1, 2):
            hx, hy = self._handle_pos(idx)
            if (px - hx) ** 2 + (py - hy) ** 2 <= 15 ** 2:
                return idx
        return None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._dragging = self._hit_handle(event.x(), event.y())

    def mouseMoveEvent(self, event):
        if self._dragging is None:
            return
        x, y = self._to_norm(event.x(), event.y())
        if self._snap:
            x = round(round(x / self.GRID) * self.GRID, 4)
            y = round(round(y / self.GRID) * self.GRID, 4)
        if self._dragging == 1:
            self.x1, self.y1 = x, y
        else:
            self.x2, self.y2 = x, y
        self.update()
        self.valueChanged.emit(self.x1, self.y1, self.x2, self.y2)

    def mouseReleaseEvent(self, event):
        self._dragging = None

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_X:
            self._snap = True
        super(BezierCanvas, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_X:
            self._snap = False
        super(BezierCanvas, self).keyReleaseEvent(event)


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=wrapInstance(int(Omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        try:
            window.close()
            window.deleteLater()
        except:
            pass
        super(Window, self).__init__(parent)

        self.maya_version = cmds.about(version=True)
        self.setWindowTitle('面片链(Maya' + self.maya_version + ')')
        self.setFixedWidth(420)

        self.ui_edit = UiEdit()
        self.maya_common = MayaCommon()

        self.file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
        self.root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
        self.library_path = self.root_path + '\\' + maya_version

        # 已生成的网格信息：key(根骨骼短名 或 '_sheet') -> {'mesh','mode','chains','wrap'}
        self.generated = {}
        # 应用模板中（阻断中间态实时刷新）
        self._applying = False
        # 设置模板（持久化到 json）
        self.presets = self._load_presets()

        self.create_widgets()
        self.create_layouts()
        self.create_connect()
        self._refresh_preset_combo()

    def create_widgets(self):
        # 骨骼链（支持逗号分隔的多个根骨骼）
        self.button_1 = QtWidgets.QPushButton('选择骨骼链根骨骼')
        self.line_edit_1 = QtWidgets.QLineEdit('')
        self.button_2 = QtWidgets.QPushButton('加载')

        # 生成模式：条状面片 / 连续面片
        self.label_mode = QtWidgets.QLabel('生成模式:')
        self.combo_mode = QtWidgets.QComboBox()
        self.combo_mode.addItems(['条状面片', '连续面片'])
        self.chk_wrap = QtWidgets.QCheckBox('链接末端(首尾链相连)')
        self.chk_wrap.setChecked(False)
        self.chk_wrap.setEnabled(False)

        # 设置模板（保存/应用当前所有设置）
        self.label_preset = QtWidgets.QLabel('设置模板:')
        self.combo_preset = QtWidgets.QComboBox()
        self.combo_preset.setEditable(True)
        self.button_save_preset = QtWidgets.QPushButton('存为模板')
        self.button_del_preset = QtWidgets.QPushButton('删除模板')

        # 分段数（沿骨骼方向）
        self.label_seg = QtWidgets.QLabel('分段数:')
        self.slider_seg = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_seg.setMinimum(1)
        self.slider_seg.setMaximum(20)
        self.slider_seg.setValue(4)
        self.label_seg_val = QtWidgets.QLabel('4')

        # 面片宽度（条状面片）
        self.label_width = QtWidgets.QLabel('面片宽度:')
        self.spin_width = QtWidgets.QDoubleSpinBox()
        self.spin_width.setRange(0.1, 100.0)
        self.spin_width.setValue(2.0)
        self.spin_width.setSingleStep(0.1)
        self.spin_width.setDecimals(2)

        # 绕骨骼旋转角度（滑块 + 可填写）
        self.label_rot = QtWidgets.QLabel('旋转角度:')
        self.slider_rot = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_rot.setMinimum(-180)
        self.slider_rot.setMaximum(180)
        self.slider_rot.setValue(0)
        self.spin_rot = QtWidgets.QSpinBox()
        self.spin_rot.setRange(-180, 180)
        self.spin_rot.setSuffix('°')

        self.splitter_1 = QtWidgets.QSplitter()
        self.splitter_1.setFixedHeight(1)
        self.splitter_1.setFrameStyle(1)

        # ---- 骨骼方向权重（沿用现有编辑方式）----
        # 权重锚点
        self.label_anchor = QtWidgets.QLabel('骨骼位置权重:')
        self.combo_anchor = QtWidgets.QComboBox()
        self.combo_anchor.addItems(['自身骨骼权重=1', '上一根骨骼权重=1', '就近骨骼权重=1'])

        # 权重过渡
        self.label_falloff = QtWidgets.QLabel('分段之间权重:')
        self.combo_falloff = QtWidgets.QComboBox()
        self.combo_falloff.addItems(['保持权重为1', '平滑'])

        # 跨越骨骼数（平滑时影响范围加宽，可越过下根骨骼；0=不跨越）
        self.label_span = QtWidgets.QLabel('跨越骨骼数:')
        self.spin_span = QtWidgets.QSpinBox()
        self.spin_span.setRange(0, 5)
        self.spin_span.setValue(0)

        # 收缩权重扩散环边（数值越大，向该方向扩散范围越小，影响骨骼越少；0=不收缩）
        self.label_shrink_up = QtWidgets.QLabel('向上收缩环边:')
        self.spin_shrink_up = QtWidgets.QSpinBox()
        self.spin_shrink_up.setRange(0, 64)
        self.spin_shrink_up.setValue(0)
        self.label_shrink_down = QtWidgets.QLabel('向下收缩环边:')
        self.spin_shrink_down = QtWidgets.QSpinBox()
        self.spin_shrink_down.setRange(0, 64)
        self.spin_shrink_down.setValue(0)

        # 算法平滑（纯算法模拟 Maya 后期笔刷平滑：拓扑邻居迭代平均），0=不做
        self.label_smooth_iter = QtWidgets.QLabel('算法平滑次数:')
        self.spin_smooth_iter = QtWidgets.QSpinBox()
        self.spin_smooth_iter.setRange(0, 20)
        self.spin_smooth_iter.setValue(0)

        # 锁定根/末端骨骼位置的边权重为 1（平滑模式下过渡自动重排，不是硬夹边）
        self.chk_lock_root = QtWidgets.QCheckBox('锁住根骨骼边权重=1')
        self.chk_lock_root.setChecked(False)
        self.chk_lock_end = QtWidgets.QCheckBox('锁住末端骨骼边权重=1')
        self.chk_lock_end.setChecked(False)

        # 贝塞尔页面
        self.label_bezier = QtWidgets.QLabel('贝塞尔方案:')
        self.combo_bezier = QtWidgets.QComboBox()
        self.combo_bezier.addItems(['平滑过渡', '线性过渡', '缓入', '缓出'])

        self.canvas_bezier = BezierCanvas()
        self.canvas_bezier.set_values(*BEZIER_PRESETS['平滑过渡'])

        self.label_x1 = QtWidgets.QLabel('控制点1(X):')
        self.spin_x1 = QtWidgets.QDoubleSpinBox()
        self.spin_x1.setRange(0.0, 1.0)
        self.spin_x1.setSingleStep(0.01)
        self.spin_x1.setDecimals(2)
        self.spin_x1.setValue(BEZIER_PRESETS['平滑过渡'][0])

        self.label_y1 = QtWidgets.QLabel('控制点1(Y):')
        self.spin_y1 = QtWidgets.QDoubleSpinBox()
        self.spin_y1.setRange(0.0, 1.0)
        self.spin_y1.setSingleStep(0.01)
        self.spin_y1.setDecimals(2)
        self.spin_y1.setValue(BEZIER_PRESETS['平滑过渡'][1])

        self.label_x2 = QtWidgets.QLabel('控制点2(X):')
        self.spin_x2 = QtWidgets.QDoubleSpinBox()
        self.spin_x2.setRange(0.0, 1.0)
        self.spin_x2.setSingleStep(0.01)
        self.spin_x2.setDecimals(2)
        self.spin_x2.setValue(BEZIER_PRESETS['平滑过渡'][2])

        self.label_y2 = QtWidgets.QLabel('控制点2(Y):')
        self.spin_y2 = QtWidgets.QDoubleSpinBox()
        self.spin_y2.setRange(0.0, 1.0)
        self.spin_y2.setSingleStep(0.01)
        self.spin_y2.setDecimals(2)
        self.spin_y2.setValue(BEZIER_PRESETS['平滑过渡'][3])

        # ---- 侧向权重（连续面片跨骨骼链方向，独立编辑）----
        self.label_lat_anchor = QtWidgets.QLabel('骨骼位置权重:')
        self.combo_lat_anchor = QtWidgets.QComboBox()
        self.combo_lat_anchor.addItems(['自身骨骼权重=1', '上一根骨骼权重=1', '就近骨骼权重=1'])

        self.label_lat_seg = QtWidgets.QLabel('侧向分段数:')
        self.spin_lat_seg = QtWidgets.QSpinBox()
        self.spin_lat_seg.setRange(1, 10)
        self.spin_lat_seg.setValue(2)

        self.label_lat_falloff = QtWidgets.QLabel('侧向分段权重:')
        self.combo_lat_falloff = QtWidgets.QComboBox()
        self.combo_lat_falloff.addItems(['保持权重为1', '平滑'])

        # 侧向跨越骨骼数（同沿骨骼方向，独立编辑）
        self.label_lat_span = QtWidgets.QLabel('跨越骨骼数:')
        self.spin_lat_span = QtWidgets.QSpinBox()
        self.spin_lat_span.setRange(0, 5)
        self.spin_lat_span.setValue(0)

        # 侧向收缩权重扩散环边（向上一根链 / 下一根链方向）
        self.label_lat_shrink_up = QtWidgets.QLabel('向上收缩环边:')
        self.spin_lat_shrink_up = QtWidgets.QSpinBox()
        self.spin_lat_shrink_up.setRange(0, 64)
        self.spin_lat_shrink_up.setValue(0)
        self.label_lat_shrink_down = QtWidgets.QLabel('向下收缩环边:')
        self.spin_lat_shrink_down = QtWidgets.QSpinBox()
        self.spin_lat_shrink_down.setRange(0, 64)
        self.spin_lat_shrink_down.setValue(0)

        self.label_lat_bezier = QtWidgets.QLabel('贝塞尔方案:')
        self.combo_lat_bezier = QtWidgets.QComboBox()
        self.combo_lat_bezier.addItems(['平滑过渡', '线性过渡', '缓入', '缓出'])

        self.canvas_lat_bezier = BezierCanvas()
        self.canvas_lat_bezier.set_values(*BEZIER_PRESETS['平滑过渡'])

        self.label_lat_x1 = QtWidgets.QLabel('控制点1(X):')
        self.spin_lat_x1 = QtWidgets.QDoubleSpinBox()
        self.spin_lat_x1.setRange(0.0, 1.0)
        self.spin_lat_x1.setSingleStep(0.01)
        self.spin_lat_x1.setDecimals(2)
        self.spin_lat_x1.setValue(BEZIER_PRESETS['平滑过渡'][0])

        self.label_lat_y1 = QtWidgets.QLabel('控制点1(Y):')
        self.spin_lat_y1 = QtWidgets.QDoubleSpinBox()
        self.spin_lat_y1.setRange(0.0, 1.0)
        self.spin_lat_y1.setSingleStep(0.01)
        self.spin_lat_y1.setDecimals(2)
        self.spin_lat_y1.setValue(BEZIER_PRESETS['平滑过渡'][1])

        self.label_lat_x2 = QtWidgets.QLabel('控制点2(X):')
        self.spin_lat_x2 = QtWidgets.QDoubleSpinBox()
        self.spin_lat_x2.setRange(0.0, 1.0)
        self.spin_lat_x2.setSingleStep(0.01)
        self.spin_lat_x2.setDecimals(2)
        self.spin_lat_x2.setValue(BEZIER_PRESETS['平滑过渡'][2])

        self.label_lat_y2 = QtWidgets.QLabel('控制点2(Y):')
        self.spin_lat_y2 = QtWidgets.QDoubleSpinBox()
        self.spin_lat_y2.setRange(0.0, 1.0)
        self.spin_lat_y2.setSingleStep(0.01)
        self.spin_lat_y2.setDecimals(2)
        self.spin_lat_y2.setValue(BEZIER_PRESETS['平滑过渡'][3])

        # 实时计算权重
        self.chk_realtime = QtWidgets.QCheckBox('实时计算权重')
        self.chk_realtime.setChecked(False)

        # 生成完成后自动勾选实时计算（进入交互式权重调整）
        self.chk_auto_switch = QtWidgets.QCheckBox('完成后切换为交互式权重')
        self.chk_auto_switch.setChecked(True)

        # 小权重清理阈值（低于该值清为 0 后归一化；0=不清理）
        self.label_prune = QtWidgets.QLabel('清理过小权重:')
        self.spin_prune = QtWidgets.QDoubleSpinBox()
        self.spin_prune.setRange(0.0, 0.5)
        self.spin_prune.setSingleStep(0.001)
        self.spin_prune.setDecimals(3)
        self.spin_prune.setValue(0.01)

        # 生成 / 删除
        self.button_5 = QtWidgets.QPushButton('生成面片链')
        self.button_5.setStyleSheet('color:rgb(0,0,0);background:rgb(255,102,102)')
        self.button_6 = QtWidgets.QPushButton('删除面片链')
        self.button_6.setStyleSheet('color:rgb(0,0,0);background:rgb(80,80,80)')

        self.label_2 = QtWidgets.QLabel('说明: 框选多个根骨骼点"加载"（逗号分隔），再点"生成面片链"。条状面片为每根骨骼链生成一条带子；连续面片把多根骨骼链横向连成一张面片，可选链接末端闭合成筒。勾选实时计算后分段/旋转/宽度即时生效；权重编辑以蒙皮中的骨骼为准；骨骼方向与侧向权重在两个页面中分别编辑。')
        self.label_2.setWordWrap(True)

    def create_layouts(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(2)

        h1 = QtWidgets.QHBoxLayout()
        h1.addWidget(self.button_1)
        h1.addWidget(self.line_edit_1)
        h1.addWidget(self.button_2)
        h1.setSpacing(1)
        main_layout.addLayout(h1)

        h_mode = QtWidgets.QHBoxLayout()
        h_mode.addWidget(self.label_mode)
        h_mode.addWidget(self.combo_mode)
        h_mode.addWidget(self.chk_wrap)
        main_layout.addLayout(h_mode)

        h_preset = QtWidgets.QHBoxLayout()
        h_preset.addWidget(self.label_preset)
        h_preset.addWidget(self.combo_preset)
        h_preset.addWidget(self.button_save_preset)
        h_preset.addWidget(self.button_del_preset)
        main_layout.addLayout(h_preset)

        h2 = QtWidgets.QHBoxLayout()
        h2.addWidget(self.label_seg)
        h2.addWidget(self.slider_seg)
        h2.addWidget(self.label_seg_val)
        h2.setSpacing(2)
        main_layout.addLayout(h2)

        h3 = QtWidgets.QHBoxLayout()
        h3.addWidget(self.label_width)
        h3.addWidget(self.spin_width)
        h3.addStretch(1)
        main_layout.addLayout(h3)

        h3b = QtWidgets.QHBoxLayout()
        h3b.addWidget(self.label_rot)
        h3b.addWidget(self.slider_rot)
        h3b.addWidget(self.spin_rot)
        h3b.setSpacing(2)
        main_layout.addLayout(h3b)

        main_layout.addWidget(self.splitter_1)

        # 选项卡：骨骼方向权重 / 侧向权重
        self.tab_weights = QtWidgets.QTabWidget()

        tab_along = QtWidgets.QWidget()
        lay_along = QtWidgets.QVBoxLayout(tab_along)
        lay_along.setContentsMargins(2, 2, 2, 2)
        lay_along.setSpacing(2)
        h4 = QtWidgets.QHBoxLayout()
        h4.addWidget(self.label_anchor)
        h4.addWidget(self.combo_anchor)
        lay_along.addLayout(h4)
        h5 = QtWidgets.QHBoxLayout()
        h5.addWidget(self.label_falloff)
        h5.addWidget(self.combo_falloff)
        lay_along.addLayout(h5)
        h5b = QtWidgets.QHBoxLayout()
        h5b.addWidget(self.label_span)
        h5b.addWidget(self.spin_span)
        h5b.addStretch(1)
        lay_along.addLayout(h5b)
        h5sh = QtWidgets.QHBoxLayout()
        h5sh.addWidget(self.label_shrink_up)
        h5sh.addWidget(self.spin_shrink_up)
        h5sh.addWidget(self.label_shrink_down)
        h5sh.addWidget(self.spin_shrink_down)
        h5sh.addStretch(1)
        lay_along.addLayout(h5sh)
        h5si = QtWidgets.QHBoxLayout()
        h5si.addWidget(self.label_smooth_iter)
        h5si.addWidget(self.spin_smooth_iter)
        h5si.addStretch(1)
        lay_along.addLayout(h5si)
        h5c = QtWidgets.QHBoxLayout()
        h5c.addWidget(self.chk_lock_root)
        h5c.addWidget(self.chk_lock_end)
        h5c.addStretch(1)
        lay_along.addLayout(h5c)
        h6 = QtWidgets.QHBoxLayout()
        h6.addWidget(self.label_bezier)
        h6.addWidget(self.combo_bezier)
        lay_along.addLayout(h6)
        lay_along.addWidget(self.canvas_bezier)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.label_x1, 0, 0)
        grid.addWidget(self.spin_x1, 0, 1)
        grid.addWidget(self.label_y1, 0, 2)
        grid.addWidget(self.spin_y1, 0, 3)
        grid.addWidget(self.label_x2, 1, 0)
        grid.addWidget(self.spin_x2, 1, 1)
        grid.addWidget(self.label_y2, 1, 2)
        grid.addWidget(self.spin_y2, 1, 3)
        lay_along.addLayout(grid)
        self.tab_weights.addTab(tab_along, '骨骼方向权重')

        tab_lat = QtWidgets.QWidget()
        lay_lat = QtWidgets.QVBoxLayout(tab_lat)
        lay_lat.setContentsMargins(2, 2, 2, 2)
        lay_lat.setSpacing(2)
        hl0 = QtWidgets.QHBoxLayout()
        hl0.addWidget(self.label_lat_anchor)
        hl0.addWidget(self.combo_lat_anchor)
        lay_lat.addLayout(hl0)
        hl1 = QtWidgets.QHBoxLayout()
        hl1.addWidget(self.label_lat_seg)
        hl1.addWidget(self.spin_lat_seg)
        hl1.addStretch(1)
        lay_lat.addLayout(hl1)
        hl2 = QtWidgets.QHBoxLayout()
        hl2.addWidget(self.label_lat_falloff)
        hl2.addWidget(self.combo_lat_falloff)
        lay_lat.addLayout(hl2)
        hl2b = QtWidgets.QHBoxLayout()
        hl2b.addWidget(self.label_lat_span)
        hl2b.addWidget(self.spin_lat_span)
        hl2b.addStretch(1)
        lay_lat.addLayout(hl2b)
        hl2sh = QtWidgets.QHBoxLayout()
        hl2sh.addWidget(self.label_lat_shrink_up)
        hl2sh.addWidget(self.spin_lat_shrink_up)
        hl2sh.addWidget(self.label_lat_shrink_down)
        hl2sh.addWidget(self.spin_lat_shrink_down)
        hl2sh.addStretch(1)
        lay_lat.addLayout(hl2sh)
        hl3 = QtWidgets.QHBoxLayout()
        hl3.addWidget(self.label_lat_bezier)
        hl3.addWidget(self.combo_lat_bezier)
        lay_lat.addLayout(hl3)
        lay_lat.addWidget(self.canvas_lat_bezier)
        grid_lat = QtWidgets.QGridLayout()
        grid_lat.addWidget(self.label_lat_x1, 0, 0)
        grid_lat.addWidget(self.spin_lat_x1, 0, 1)
        grid_lat.addWidget(self.label_lat_y1, 0, 2)
        grid_lat.addWidget(self.spin_lat_y1, 0, 3)
        grid_lat.addWidget(self.label_lat_x2, 1, 0)
        grid_lat.addWidget(self.spin_lat_x2, 1, 1)
        grid_lat.addWidget(self.label_lat_y2, 1, 2)
        grid_lat.addWidget(self.spin_lat_y2, 1, 3)
        lay_lat.addLayout(grid_lat)
        self.tab_weights.addTab(tab_lat, '侧向权重')
        self.tab_weights.setTabEnabled(1, False)

        main_layout.addWidget(self.tab_weights)

        h_realtime = QtWidgets.QHBoxLayout()
        h_realtime.addWidget(self.chk_realtime)
        h_realtime.addWidget(self.chk_auto_switch)
        h_realtime.addStretch(1)
        main_layout.addLayout(h_realtime)

        h_prune = QtWidgets.QHBoxLayout()
        h_prune.addWidget(self.label_prune)
        h_prune.addWidget(self.spin_prune)
        h_prune.addStretch(1)
        main_layout.addLayout(h_prune)

        main_layout.addWidget(self.button_5)
        main_layout.addWidget(self.button_6)
        main_layout.addWidget(self.label_2)

        main_layout.addStretch(1)

        # 限制窗口最小高度，防止缩小窗口时控件被压缩重叠
        self.setMinimumHeight(main_layout.minimumSize().height())

    def create_connect(self):
        self.button_1.clicked.connect(lambda: self.maya_common.select_text_target(self.line_edit_1, ['QLineEdit']))
        self.button_2.clicked.connect(lambda: self.ui_edit.load_select_for_ui_text(self.line_edit_1, ['QLineEdit']))

        self.button_save_preset.clicked.connect(self.save_preset)
        self.button_del_preset.clicked.connect(self.delete_preset)
        self.combo_preset.activated[int].connect(self.apply_preset_by_index)

        self.slider_seg.valueChanged.connect(self.on_seg_changed)
        self.spin_width.valueChanged.connect(self.on_width_changed)
        self.slider_rot.valueChanged.connect(self.on_rot_changed)
        self.spin_rot.valueChanged.connect(self.on_rot_spin_changed)
        self.combo_mode.currentTextChanged.connect(self.on_mode_changed)
        self.chk_wrap.stateChanged.connect(self.on_wrap_changed)
        self.combo_anchor.currentTextChanged.connect(self.on_anchor_changed)
        self.combo_bezier.currentTextChanged.connect(self.on_bezier_preset)
        self.spin_x1.valueChanged.connect(self.on_x1_changed)
        self.spin_y1.valueChanged.connect(self.on_y1_changed)
        self.canvas_bezier.valueChanged.connect(self.on_canvas_changed)
        self.combo_falloff.currentTextChanged.connect(self.on_falloff_changed)
        self.spin_span.valueChanged.connect(self.on_span_changed)
        self.spin_shrink_up.valueChanged.connect(self.on_weight_param_changed)
        self.spin_shrink_down.valueChanged.connect(self.on_weight_param_changed)
        self.spin_smooth_iter.valueChanged.connect(self.on_weight_param_changed)
        self.chk_lock_root.stateChanged.connect(self.on_lock_changed)
        self.chk_lock_end.stateChanged.connect(self.on_lock_changed)
        self.spin_prune.valueChanged.connect(self.on_prune_changed)

        self.spin_lat_seg.valueChanged.connect(self.on_lat_seg_changed)
        self.combo_lat_anchor.currentTextChanged.connect(self.on_lat_anchor_changed)
        self.combo_lat_bezier.currentTextChanged.connect(self.on_lat_bezier_preset)
        self.spin_lat_x1.valueChanged.connect(self.on_lat_x1_changed)
        self.spin_lat_y1.valueChanged.connect(self.on_lat_y1_changed)
        self.spin_lat_x2.valueChanged.connect(self.on_lat_x2_changed)
        self.spin_lat_y2.valueChanged.connect(self.on_lat_y2_changed)
        self.canvas_lat_bezier.valueChanged.connect(self.on_lat_canvas_changed)
        self.combo_lat_falloff.currentTextChanged.connect(self.on_lat_falloff_changed)
        self.spin_lat_span.valueChanged.connect(self.on_lat_span_changed)
        self.spin_lat_shrink_up.valueChanged.connect(self.on_weight_param_changed)
        self.spin_lat_shrink_down.valueChanged.connect(self.on_weight_param_changed)

        self.button_5.clicked.connect(self.create_patch_chain)
        self.button_6.clicked.connect(self.delete_patch_chain)

        # 实时模式切换：勾选时立即刷新并给出明显的视觉反馈
        self.chk_realtime.stateChanged.connect(self.on_realtime_changed)
        self._update_realtime_style(False)

    # 实时模式复选框状态变化：勾选即对已生成网格刷新一次，并高亮复选框
    # 注意：PySide2 5.6（Maya2018）的 stateChanged 传裸 int，不能与 Qt.Checked 枚举直接比较
    def on_realtime_changed(self, state):
        checked = bool(state)
        self._update_realtime_style(checked)
        if checked:
            self.realtime_refresh(rebuild_geometry=False)

    def _update_realtime_style(self, checked):
        if checked:
            self.chk_realtime.setStyleSheet('QCheckBox{color:rgb(60,170,80);font-weight:bold;}')
        else:
            self.chk_realtime.setStyleSheet('')

    # 当前生效的根骨骼列表（输入框支持逗号/空格分隔的多个根骨骼）
    def get_roots(self):
        text = self.line_edit_1.text().strip()
        roots = []
        for part in text.replace(';', ',').replace(' ', ',').split(','):
            part = part.strip()
            if part and part not in roots:
                roots.append(part)
        return roots

    # ---- 设置模板：保存 / 应用 / 删除当前所有设置 ----
    def _preset_path(self):
        return os.path.join(self.file_path, 'patch_chain_presets.json')

    def _load_presets(self):
        try:
            with open(self._preset_path(), 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_presets(self):
        try:
            with open(self._preset_path(), 'w') as f:
                json.dump(self.presets, f, ensure_ascii=False, indent=1)
        except Exception as e:
            cmds.warning('模板保存失败: ' + str(e))

    def _refresh_preset_combo(self, select_name=None):
        self.combo_preset.blockSignals(True)
        self.combo_preset.clear()
        self.combo_preset.addItem('')
        for name in sorted(self.presets.keys()):
            self.combo_preset.addItem(name)
        if select_name:
            self.combo_preset.setCurrentText(select_name)
        self.combo_preset.blockSignals(False)

    # 收集当前所有设置
    def _settings_dict(self):
        return {
            'segments': self.slider_seg.value(),
            'width': self.spin_width.value(),
            'rot': self.slider_rot.value(),
            'mode': self.combo_mode.currentText(),
            'wrap': self.chk_wrap.isChecked(),
            'anchor': self.combo_anchor.currentText(),
            'falloff': self.combo_falloff.currentText(),
            'span': self.spin_span.value(),
            'shrink_up': self.spin_shrink_up.value(),
            'shrink_down': self.spin_shrink_down.value(),
            'smooth_iter': self.spin_smooth_iter.value(),
            'lock_root': self.chk_lock_root.isChecked(),
            'lock_end': self.chk_lock_end.isChecked(),
            'auto_switch': self.chk_auto_switch.isChecked(),
            'bez': [self.spin_x1.value(), self.spin_y1.value(),
                    self.spin_x2.value(), self.spin_y2.value()],
            'lat_seg': self.spin_lat_seg.value(),
            'lat_anchor': self.combo_lat_anchor.currentText(),
            'lat_falloff': self.combo_lat_falloff.currentText(),
            'lat_span': self.spin_lat_span.value(),
            'lat_shrink_up': self.spin_lat_shrink_up.value(),
            'lat_shrink_down': self.spin_lat_shrink_down.value(),
            'lat_bez': [self.spin_lat_x1.value(), self.spin_lat_y1.value(),
                        self.spin_lat_x2.value(), self.spin_lat_y2.value()],
            'prune': self.spin_prune.value(),
        }

    # 应用一组设置到界面（最后统一触发一次实时刷新）
    def _apply_settings(self, st):
        self._applying = True
        try:
            self.slider_seg.setValue(st.get('segments', 4))
            self.spin_width.setValue(st.get('width', 2.0))
            self.slider_rot.setValue(st.get('rot', 0))
            self.combo_mode.setCurrentText(st.get('mode', '条状面片'))
            self.chk_wrap.setChecked(st.get('wrap', False))
            self.combo_anchor.setCurrentText(st.get('anchor', '自身骨骼权重=1'))
            self.combo_falloff.setCurrentText(st.get('falloff', '平滑'))
            self.spin_span.setValue(st.get('span', 0))
            self.spin_shrink_up.setValue(st.get('shrink_up', 0))
            self.spin_shrink_down.setValue(st.get('shrink_down', 0))
            self.spin_smooth_iter.setValue(st.get('smooth_iter', 0))
            self.chk_lock_root.setChecked(st.get('lock_root', False))
            self.chk_lock_end.setChecked(st.get('lock_end', False))
            self.chk_auto_switch.setChecked(st.get('auto_switch', True))
            b = st.get('bez', [1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0])
            for spin, val in zip((self.spin_x1, self.spin_y1, self.spin_x2, self.spin_y2), b):
                spin.setValue(val)
            self.canvas_bezier.set_values(*b)
            self.spin_lat_seg.setValue(st.get('lat_seg', 2))
            self.combo_lat_anchor.setCurrentText(st.get('lat_anchor', '自身骨骼权重=1'))
            self.combo_lat_falloff.setCurrentText(st.get('lat_falloff', '平滑'))
            self.spin_lat_span.setValue(st.get('lat_span', 0))
            self.spin_lat_shrink_up.setValue(st.get('lat_shrink_up', 0))
            self.spin_lat_shrink_down.setValue(st.get('lat_shrink_down', 0))
            lb = st.get('lat_bez', [1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0])
            for spin, val in zip((self.spin_lat_x1, self.spin_lat_y1,
                                  self.spin_lat_x2, self.spin_lat_y2), lb):
                spin.setValue(val)
            self.canvas_lat_bezier.set_values(*lb)
            self.spin_prune.setValue(st.get('prune', 0.01))
        finally:
            self._applying = False
        # 设置里可能包含布线参数，统一按重建几何刷新一次
        self.realtime_refresh(rebuild_geometry=True)

    def save_preset(self):
        name = self.combo_preset.currentText().strip()
        if not name:
            cmds.warning('请先在模板输入框中输入名称')
            return
        self.presets[name] = self._settings_dict()
        self._write_presets()
        self._refresh_preset_combo(name)
        print('模板已保存: ' + name)

    def delete_preset(self):
        name = self.combo_preset.currentText().strip()
        if name not in self.presets:
            cmds.warning('模板不存在: ' + name)
            return
        self.presets.pop(name)
        self._write_presets()
        self._refresh_preset_combo()
        print('模板已删除: ' + name)

    def apply_preset_by_index(self, index):
        self.apply_preset(self.combo_preset.itemText(index))

    def apply_preset(self, name):
        if name not in self.presets:
            return
        self._apply_settings(self.presets[name])
        print('模板已应用: ' + name)

    # 生成模式切换
    def on_mode_changed(self, text):
        sheet = (text == '连续面片')
        self.chk_wrap.setEnabled(sheet)
        self.tab_weights.setTabEnabled(1, sheet)
        self.spin_width.setEnabled(not sheet)
        self.label_width.setEnabled(not sheet)

    # 链接末端
    def on_wrap_changed(self, state):
        self.realtime_refresh(rebuild_geometry=True)

    # 分段滑块
    def on_seg_changed(self, value):
        self.label_seg_val.setText(str(value))
        self.realtime_refresh(rebuild_geometry=True)

    # 面片宽度变化
    def on_width_changed(self, value):
        self.realtime_refresh(rebuild_geometry=True)

    # 旋转角度滑块（实时）
    def on_rot_changed(self, value):
        self.spin_rot.blockSignals(True)
        self.spin_rot.setValue(value)
        self.spin_rot.blockSignals(False)
        self.realtime_refresh(rebuild_geometry=True)

    # 旋转角度填写（实时）
    def on_rot_spin_changed(self, value):
        self.slider_rot.setValue(value)  # 触发 on_rot_changed -> 实时刷新

    # 侧向分段数
    def on_lat_seg_changed(self, value):
        self.realtime_refresh(rebuild_geometry=True)

    # 侧向锚点变化（只重新赋权）
    def on_lat_anchor_changed(self, text):
        self.realtime_refresh(rebuild_geometry=False)

    # 锁定根/末端（只重新赋权）
    def on_lock_changed(self, state):
        self.realtime_refresh(rebuild_geometry=False)

    # 跨越骨骼数（只重新赋权）
    def on_span_changed(self, value):
        self.realtime_refresh(rebuild_geometry=False)

    def on_lat_span_changed(self, value):
        self.realtime_refresh(rebuild_geometry=False)

    # 收缩环边 / 算法平滑次数（只重新赋权）
    def on_weight_param_changed(self, *args):
        self.realtime_refresh(rebuild_geometry=False)

    # 清理阈值（只重新赋权）
    def on_prune_changed(self, value):
        self.realtime_refresh(rebuild_geometry=False)

    # 锚点变化（只重新赋权）
    def on_anchor_changed(self, text):
        self.realtime_refresh(rebuild_geometry=False)

    # 贝塞尔方案切换
    def on_bezier_preset(self, text):
        if text not in BEZIER_PRESETS:
            return
        x1, y1, x2, y2 = BEZIER_PRESETS[text]
        for spin, val in ((self.spin_x1, x1), (self.spin_y1, y1),
                          (self.spin_x2, x2), (self.spin_y2, y2)):
            spin.blockSignals(True)
            spin.setValue(val)
            spin.blockSignals(False)
        self.canvas_bezier.set_values(x1, y1, x2, y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_x1_changed(self, value):
        self.canvas_bezier.set_values(value, self.canvas_bezier.y1, self.canvas_bezier.x2, self.canvas_bezier.y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_y1_changed(self, value):
        self.canvas_bezier.set_values(self.canvas_bezier.x1, value, self.canvas_bezier.x2, self.canvas_bezier.y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_x2_changed(self, value):
        self.canvas_bezier.set_values(self.canvas_bezier.x1, self.canvas_bezier.y1, value, self.canvas_bezier.y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_y2_changed(self, value):
        self.canvas_bezier.set_values(self.canvas_bezier.x1, self.canvas_bezier.y1, self.canvas_bezier.x2, value)
        self.realtime_refresh(rebuild_geometry=False)

    def on_canvas_changed(self, x1, y1, x2, y2):
        for spin, val in ((self.spin_x1, x1), (self.spin_y1, y1),
                          (self.spin_x2, x2), (self.spin_y2, y2)):
            spin.blockSignals(True)
            spin.setValue(val)
            spin.blockSignals(False)
        self.realtime_refresh(rebuild_geometry=False)

    # 平滑模式下才启用贝塞尔相关控件
    def on_falloff_changed(self, text):
        smooth = (text == '平滑')
        for w in (self.label_bezier, self.combo_bezier, self.canvas_bezier,
                  self.label_x1, self.spin_x1, self.label_y1, self.spin_y1,
                  self.label_x2, self.spin_x2, self.label_y2, self.spin_y2):
            w.setEnabled(smooth)
        self.realtime_refresh(rebuild_geometry=False)

    # 侧向贝塞尔方案切换
    def on_lat_bezier_preset(self, text):
        if text not in BEZIER_PRESETS:
            return
        x1, y1, x2, y2 = BEZIER_PRESETS[text]
        for spin, val in ((self.spin_lat_x1, x1), (self.spin_lat_y1, y1),
                          (self.spin_lat_x2, x2), (self.spin_lat_y2, y2)):
            spin.blockSignals(True)
            spin.setValue(val)
            spin.blockSignals(False)
        self.canvas_lat_bezier.set_values(x1, y1, x2, y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_lat_x1_changed(self, value):
        c = self.canvas_lat_bezier
        c.set_values(value, c.y1, c.x2, c.y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_lat_y1_changed(self, value):
        c = self.canvas_lat_bezier
        c.set_values(c.x1, value, c.x2, c.y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_lat_x2_changed(self, value):
        c = self.canvas_lat_bezier
        c.set_values(c.x1, c.y1, value, c.y2)
        self.realtime_refresh(rebuild_geometry=False)

    def on_lat_y2_changed(self, value):
        c = self.canvas_lat_bezier
        c.set_values(c.x1, c.y1, c.x2, value)
        self.realtime_refresh(rebuild_geometry=False)

    def on_lat_canvas_changed(self, x1, y1, x2, y2):
        for spin, val in ((self.spin_lat_x1, x1), (self.spin_lat_y1, y1),
                          (self.spin_lat_x2, x2), (self.spin_lat_y2, y2)):
            spin.blockSignals(True)
            spin.setValue(val)
            spin.blockSignals(False)
        self.realtime_refresh(rebuild_geometry=False)

    # 侧向平滑模式下才启用侧向贝塞尔控件
    def on_lat_falloff_changed(self, text):
        smooth = (text == '平滑')
        for w in (self.label_lat_bezier, self.combo_lat_bezier, self.canvas_lat_bezier,
                  self.label_lat_x1, self.spin_lat_x1, self.label_lat_y1, self.spin_lat_y1,
                  self.label_lat_x2, self.spin_lat_x2, self.label_lat_y2, self.spin_lat_y2):
            w.setEnabled(smooth)
        self.realtime_refresh(rebuild_geometry=False)

    # 从根骨骼向下按第一个子骨骼收集成线性骨骼链
    def get_joint_chain(self, root):
        chain = [root]
        current = root
        while True:
            children = cmds.listRelatives(current, c=1, type='joint') or []
            if not children:
                break
            current = children[0]
            chain.append(current)
        return chain

    # 骨骼短名称
    def _short(self, name):
        return name.split('|')[-1]

    # 计算每个关节世界坐标
    def get_joint_positions(self, joints):
        return [cmds.xform(j, q=1, ws=1, t=1) for j in joints]

    # 环 r 对应的 (骨骼段 b, 段内参数 u)
    def _ring_bu(self, r, R, n, segments):
        if r == R - 1:
            return n - 2, 1.0
        return r // segments, (r % segments) / float(segments)

    # 关节世界朝向的候选「上方向」轴（按优先级：关节自身Y -> 关节自身Z -> 世界Y -> 世界Z）
    def _joint_ref_axes(self, jnt):
        refs = []
        m = cmds.xform(jnt, q=True, ws=True, m=True)
        for base in (4, 8):  # 世界矩阵第2行=局部Y轴，第3行=局部Z轴
            ax = (m[base], m[base + 1], m[base + 2])
            al = math.sqrt(ax[0] * ax[0] + ax[1] * ax[1] + ax[2] * ax[2])
            if al > 1e-9:
                refs.append((ax[0] / al, ax[1] / al, ax[2] / al))
        refs.append((0.0, 1.0, 0.0))
        refs.append((0.0, 0.0, 1.0))
        return refs

    # 计算一条骨骼链每环的位置 / 切向 / 侧向
    # 侧向跟随每根关节自身朝向（骨骼扭转面片跟着扭转），段内两根关节朝向 nlerp 混合
    def compute_rings(self, joints, segments):
        n = len(joints)
        R = (n - 1) * segments + 1
        positions = self.get_joint_positions(joints)

        rings_pos = []
        tangents = []
        for r in range(R):
            b, u = self._ring_bu(r, R, n, segments)
            p0 = positions[b]
            p1 = positions[b + 1]
            rings_pos.append((p0[0] + (p1[0] - p0[0]) * u,
                              p0[1] + (p1[1] - p0[1]) * u,
                              p0[2] + (p1[2] - p0[2]) * u))
            tx = p1[0] - p0[0]
            ty = p1[1] - p0[1]
            tz = p1[2] - p0[2]
            ln = math.sqrt(tx * tx + ty * ty + tz * tz)
            tangents.append((tx / ln, ty / ln, tz / ln) if ln > 1e-9 else (1.0, 0.0, 0.0))

        # 每根关节自身朝向的候选参考轴
        ref_axes = [self._joint_ref_axes(j) for j in joints]

        sides = []
        for r in range(R):
            t = tangents[r]
            b, u = self._ring_bu(r, R, n, segments)
            side = None
            # 按优先级尝试：段首尾两根关节的 Y 轴混合 -> Z 轴混合 -> 世界轴
            for ai in range(len(ref_axes[0])):
                a0 = ref_axes[b][ai]
                a1 = ref_axes[b + 1][ai]
                rx = a0[0] + (a1[0] - a0[0]) * u
                ry = a0[1] + (a1[1] - a0[1]) * u
                rz = a0[2] + (a1[2] - a0[2]) * u
                rl = math.sqrt(rx * rx + ry * ry + rz * rz)
                if rl < 1e-6:  # 两轴反向混合抵消时退化用首轴
                    rx, ry, rz = a0
                    rl = math.sqrt(rx * rx + ry * ry + rz * rz)
                rx, ry, rz = rx / rl, ry / rl, rz / rl
                # 投影到切向垂直平面
                d = rx * t[0] + ry * t[1] + rz * t[2]
                sx = rx - d * t[0]
                sy = ry - d * t[1]
                sz = rz - d * t[2]
                ln = math.sqrt(sx * sx + sy * sy + sz * sz)
                if ln > 1e-6:
                    side = (sx / ln, sy / ln, sz / ln)
                    break
            if side is None:
                side = (1.0, 0.0, 0.0)
            sides.append(side)
        return rings_pos, tangents, sides

    # 生成面片链（支持多根骨骼 / 条状与连续面片两种模式）
    def create_patch_chain(self):
        roots = self.get_roots()
        segments = self.slider_seg.value()
        width = self.spin_width.value()
        rot = self.slider_rot.value()
        lat_seg = self.spin_lat_seg.value()
        wrap = self.chk_wrap.isChecked()
        anchor = self.combo_anchor.currentText()
        smooth = self.combo_falloff.currentText() == '平滑'
        bez = (self.spin_x1.value(), self.spin_y1.value(),
               self.spin_x2.value(), self.spin_y2.value())
        lat_anchor = self.combo_lat_anchor.currentText()
        lat_smooth = self.combo_lat_falloff.currentText() == '平滑'
        lat_bez = (self.spin_lat_x1.value(), self.spin_lat_y1.value(),
                   self.spin_lat_x2.value(), self.spin_lat_y2.value())
        span = self.spin_span.value()
        lat_span = self.spin_lat_span.value()
        shrink_up = self.spin_shrink_up.value()
        shrink_down = self.spin_shrink_down.value()
        lat_shrink_up = self.spin_lat_shrink_up.value()
        lat_shrink_down = self.spin_lat_shrink_down.value()
        smooth_iter = self.spin_smooth_iter.value()
        prune = self.spin_prune.value()
        lock_root = self.chk_lock_root.isChecked()
        lock_end = self.chk_lock_end.isChecked()
        mode = self.combo_mode.currentText()

        if not roots:
            cmds.warning('请先加载或添加骨骼链根骨骼')
            return
        for rt in roots:
            if not cmds.objExists(rt) or cmds.nodeType(rt) != 'joint':
                cmds.warning('骨骼链根骨骼无效: ' + rt)
                return

        if mode == '条状面片':
            cmds.undoInfo(openChunk=True, chunkName='Create Patch Chain')
            made = []
            try:
                for rt in roots:
                    joints = self.get_joint_chain(rt)
                    if len(joints) < 2:
                        cmds.warning('骨骼链至少需要 2 个关节: ' + rt)
                        continue
                    key = self._short(rt)
                    old = self.generated.get(key)
                    if old and cmds.objExists(old['mesh']):
                        cmds.delete(old['mesh'])
                    mesh = self.build_mesh(joints, segments, width, rot)
                    self.apply_weights(mesh, joints, segments, anchor, smooth, bez,
                                       span=span, prune=prune, lock_root=lock_root, lock_end=lock_end,
                                       shrink_up=shrink_up, shrink_down=shrink_down,
                                       smooth_iter=smooth_iter)
                    self.generated[key] = {'mesh': mesh, 'mode': 'strip', 'chains': [joints]}
                    made.append(mesh)
            finally:
                cmds.undoInfo(closeChunk=True)
            if made:
                cmds.select(made)
                print('面片链已生成: ' + ', '.join(made))
                self._enter_interactive_if_requested()
        else:  # 连续面片
            chains = []
            for rt in roots:
                joints = self.get_joint_chain(rt)
                if len(joints) < 2:
                    cmds.warning('骨骼链至少需要 2 个关节: ' + rt)
                    return
                chains.append(joints)
            if len(chains) < 2:
                cmds.warning('连续面片至少需要 2 根骨骼链，请把根骨骼添加到列表')
                return
            if wrap and len(chains) < 3:
                cmds.warning('链接末端至少需要 3 根骨骼链')
                return
            sheet_key = self._sheet_key(chains)
            old = self.generated.get(sheet_key)
            if old and cmds.objExists(old['mesh']):
                cmds.delete(old['mesh'])
            cmds.undoInfo(openChunk=True, chunkName='Create Patch Sheet')
            sheet_ok = False
            try:
                chains_t, cols, R, grid, mesh = self.build_sheet_mesh(chains, segments, lat_seg, rot, wrap)
                self.apply_sheet_weights(mesh, chains_t, segments, lat_seg, anchor, smooth,
                                         bez, lat_anchor, lat_smooth, lat_bez, wrap, cols=cols, R=R, grid=grid,
                                         span=span, lat_span=lat_span, prune=prune,
                                         lock_root=lock_root, lock_end=lock_end,
                                         shrink_up=shrink_up, shrink_down=shrink_down,
                                         lat_shrink_up=lat_shrink_up, lat_shrink_down=lat_shrink_down,
                                         smooth_iter=smooth_iter)
                self.generated[sheet_key] = {'mesh': mesh, 'mode': 'sheet',
                                             'chains': chains, 'wrap': wrap}
                sheet_ok = True
            finally:
                cmds.undoInfo(closeChunk=True)
            if sheet_ok:
                cmds.select(mesh)
                print('连续面片已生成: ' + mesh)
                self._enter_interactive_if_requested()

    # 生成完成后按选项进入交互式权重：勾选「实时计算权重」并把蒙皮归一化切为 Interactive
    def _enter_interactive_if_requested(self):
        if not self.chk_auto_switch.isChecked():
            return
        # 所有刚生成的 skinCluster 从 Post(2) 切到 Interactive(1)
        for info in self.generated.values():
            mesh = info.get('mesh')
            if mesh and cmds.objExists(mesh):
                skin = self.get_skin_cluster(mesh)
                if skin and cmds.getAttr(skin + '.normalizeWeights') != 1:
                    cmds.setAttr(skin + '.normalizeWeights', 1)
        self.chk_realtime.setChecked(True)
        QtWidgets.QApplication.processEvents()  # 强制复选框立即重绘
        print('[面片链] 已进入交互式权重模式：蒙皮归一化=Interactive，调整参数实时更新')

    # 构建条状面片网格（undo 友好：polyPlane + 移动顶点）
    def build_mesh(self, joints, segments, width, rot_deg):
        n = len(joints)
        R = (n - 1) * segments + 1
        rings_pos, tangents, sides = self.compute_rings(joints, segments)

        theta = math.radians(rot_deg)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        root = self._short(joints[0])
        mesh = cmds.polyPlane(n='%s_patchChain_mesh' % root, sx=R - 1, sy=1, w=1, h=1, ch=0)[0]
        hw = width * 0.5
        for r in range(R):
            p = rings_pos[r]
            s = sides[r]
            if theta:
                # 侧向绕骨骼轴（切向）旋转，罗德里格斯公式（侧向与切向垂直）
                t = tangents[r]
                cx = t[1] * s[2] - t[2] * s[1]
                cy = t[2] * s[0] - t[0] * s[2]
                cz = t[0] * s[1] - t[1] * s[0]
                s = (s[0] * cos_t + cx * sin_t,
                     s[1] * cos_t + cy * sin_t,
                     s[2] * cos_t + cz * sin_t)
            lx = p[0] - s[0] * hw
            ly = p[1] - s[1] * hw
            lz = p[2] - s[2] * hw
            rx = p[0] + s[0] * hw
            ry = p[1] + s[1] * hw
            rz = p[2] + s[2] * hw
            cmds.xform('%s.vtx[%d]' % (mesh, r), ws=1, t=(lx, ly, lz))
            cmds.xform('%s.vtx[%d]' % (mesh, R + r), ws=1, t=(rx, ry, rz))
        return mesh

    # 连续面片的侧向列：[(链i, 链j, u)]，wrap 时首尾链相接
    def sheet_columns(self, nc, lat_seg, wrap):
        pairs = [(i, i + 1) for i in range(nc - 1)]
        if wrap:
            pairs.append((nc - 1, 0))
        cols = []
        for (i, j) in pairs:
            for c in range(lat_seg):
                cols.append((i, j, c / float(lat_seg)))
        if not wrap:
            cols.append((nc - 2, nc - 1, 1.0))
        return cols

    # 连续面片所有格点位置：grid[列][环]
    def compute_sheet_positions(self, chains, segments, lat_seg, rot_deg, wrap):
        n = min(len(c) for c in chains)
        chains = [c[:n] for c in chains]
        nc = len(chains)
        R = (n - 1) * segments + 1

        rings = []
        tans = []
        for c in chains:
            rp, tg, _sd = self.compute_rings(c, segments)
            rings.append(rp)
            tans.append(tg)

        cols = self.sheet_columns(nc, lat_seg, wrap)
        theta = math.radians(rot_deg)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        grid = []
        for (i, j, u) in cols:
            row = []
            for r in range(R):
                pi = rings[i][r]
                pj = rings[j][r]
                vx = pj[0] - pi[0]
                vy = pj[1] - pi[1]
                vz = pj[2] - pi[2]
                bx = pi[0] + vx * u
                by = pi[1] + vy * u
                bz = pi[2] + vz * u
                if theta:
                    # 旋转轴取两条链切向的平均方向
                    ax = tans[i][r][0] + tans[j][r][0]
                    ay = tans[i][r][1] + tans[j][r][1]
                    az = tans[i][r][2] + tans[j][r][2]
                    an = math.sqrt(ax * ax + ay * ay + az * az)
                    if an > 1e-9:
                        ax /= an
                        ay /= an
                        az /= an
                        # 跨链向量的垂轴分量绕轴旋转，内部列按 sin(pi*u) 鼓出，端点保持在链上
                        d = vx * ax + vy * ay + vz * az
                        px = vx - d * ax
                        py = vy - d * ay
                        pz = vz - d * az
                        pl = math.sqrt(px * px + py * py + pz * pz)
                        if pl > 1e-9:
                            cx = ay * pz - az * py
                            cy = az * px - ax * pz
                            cz = ax * py - ay * px
                            rx = px * cos_t + cx * sin_t
                            ry = py * cos_t + cy * sin_t
                            rz = pz * cos_t + cz * sin_t
                            k = math.sin(math.pi * u)
                            bx += (rx - px) * k
                            by += (ry - py) * k
                            bz += (rz - pz) * k
                row.append((bx, by, bz))
            grid.append(row)
        return chains, cols, R, grid

    # 构建连续面片网格（多根骨骼链横向连成一张；wrap 时首尾焊接闭合）
    def build_sheet_mesh(self, chains, segments, lat_seg, rot_deg, wrap):
        chains, cols, R, grid = self.compute_sheet_positions(chains, segments, lat_seg, rot_deg, wrap)
        C = len(cols)
        rows = C + 1 if wrap else C
        # 名称带各链根骨骼短名，避免换一套骨骼加载时与上一张连续面片重名被替换
        root_tags = [self._short(c[0]) for c in chains]
        safe = [''.join(ch if ch.isalnum() or ch == '_' else '_' for ch in t) for t in root_tags]
        base_name = 'sheet_' + '_'.join(safe) + '_patchChain_mesh'
        mesh = cmds.polyPlane(n=base_name, sx=R - 1, sy=rows - 1, w=1, h=1, ch=0)[0]
        for ci in range(C):
            for r in range(R):
                cmds.xform('%s.vtx[%d]' % (mesh, ci * R + r), ws=1, t=grid[ci][r])
        if wrap:
            # 末行复制首行位置，逐对焊接闭合侧向；
            # 倒序焊接使已移除的索引不影响未焊接的对，且只焊接指定对（不误伤重合顶点）
            for r in range(R):
                cmds.xform('%s.vtx[%d]' % (mesh, C * R + r), ws=1, t=grid[0][r])
            for r in range(R - 1, -1, -1):
                cmds.polyMergeVertex('%s.vtx[%d]' % (mesh, C * R + r),
                                     '%s.vtx[%d]' % (mesh, r), d=1e-5, ch=0)
        return chains, cols, R, grid, mesh

    # 单环权重（沿骨骼方向）：返回 {joint: weight}
    # 平滑 = 在「权重=1」的硬归属基础上沿环方向做贝塞尔核扩散：
    #   默认向上下游各扩散 1 段（相邻两根骨骼受影响）；span 每+1 扩散多 1 段；
    #   shrink_up/down=收缩环边，数值越大该方向扩散半径越小，影响骨骼越少。
    # lock_root/lock_end：锁定根/末端骨骼位置的边权重为 1（过渡自动重排）
    def ring_weights(self, joints, b, u, anchor, smooth, bez, span=0,
                     lock_root=False, lock_end=False, segments=4,
                     shrink_up=0, shrink_down=0):
        x1, y1, x2, y2 = bez
        n = len(joints)
        weights = {}
        if smooth:
            seg = max(1, segments)
            total = (n - 1) * seg + 1
            q = b * seg + int(round(u * seg))
            base = (span + 1) * seg
            radius_up = max(0, base - shrink_up)
            radius_down = max(0, base - shrink_down)

            def owner_at(k):
                res = []
                kb = k // seg
                for off, sw in ring_owner_offsets(k, seg, anchor):
                    idx = kb + off
                    if 0 <= idx < n:
                        res.append((joints[idx], sw))
                return res

            weights = diffuse_along_rings(owner_at, q, total,
                                          radius_up, radius_down, bez, periodic=False)
            # 端点骨骼位置（首/末关节本身）权重=1：网格首/末环就是端点锚点，
            # 扩散窗口向段内截断会让末端环被上一段拉软，这里把两端点还原为纯 1
            # （上一根锚点的末环归倒数第二骨，由其自身语义决定，不做此处理）
            if anchor != '上一根骨骼权重=1':
                if q == 0:
                    weights = {joints[0]: 1.0}
                elif q == total - 1:
                    weights = {joints[n - 1]: 1.0}
        else:
            if anchor == '自身骨骼权重=1':
                owner = joints[b] if u < 1.0 else joints[b + 1]
                weights[owner] = 1.0
            elif anchor == '上一根骨骼权重=1':
                owner = joints[b - 1] if (u == 0.0 and b > 0) else joints[b]
                weights[owner] = 1.0
            else:  # 就近骨骼权重=1：按距离归最近的骨骼，恰好在中心时各占 0.5
                if u < 0.5:
                    weights[joints[b]] = 1.0
                elif u > 0.5:
                    weights[joints[b + 1]] = 1.0
                else:
                    weights[joints[b]] = 0.5
                    weights[joints[b + 1]] = 0.5

        # 锁定根/末端骨骼位置的边权重为 1：
        # 只在锁定侧相邻的一个骨骼段内，用同一贝塞尔把「锁定=1」平滑混入标准分布
        # （L 恒为 1 段：根/末端被锁住，中间骨骼的计算完全不受影响；
        #  权重和恒为 1，边界处严格为 1，过渡重排而非硬夹最近环）
        if smooth and (lock_root or lock_end):
            s = float(b) + u
            L = 1.0
            if lock_root and s < L:
                lam = bezier_weight(s / L, x1, y1, x2, y2)
                for j in list(weights.keys()):
                    if j == joints[0]:
                        weights[j] = (1.0 - lam) + weights[j] * lam
                    else:
                        weights[j] = weights[j] * lam
            if lock_end:
                se = (n - 1) - s
                if se < L:
                    lam = bezier_weight(se / L, x1, y1, x2, y2)
                    for j in list(weights.keys()):
                        if j == joints[n - 1]:
                            weights[j] = (1.0 - lam) + weights[j] * lam
                        else:
                            weights[j] = weights[j] * lam
        return weights

    # 侧向单点权重（跨骨骼链方向）：返回 {链索引: weight}
    # s 为侧向连续参数：链 i 位于 s=i；wrap 时侧向为环形（链顺序 0..nc-1 循环）
    # 平滑时由贝塞尔曲线直接定义相邻两链的交叉淡化（y=下一根链占比，0..1 全程可编辑）；
    # span 才向更远处的链扩散，shrink_up/down 收缩这段额外扩散的范围
    def lat_weights(self, nc, s, anchor, smooth, bez, wrap, span=0, lat_seg=2,
                    shrink_up=0, shrink_down=0):
        x1, y1, x2, y2 = bez
        weights = {}
        if smooth:
            seg = max(1, lat_seg)
            # 列所在的「相邻两链」段 b 与段内比例 u（链 b 在 u=0，链 b+1 在 u=1）
            if wrap:
                total = nc * seg
                q = int(round(s * seg)) % total
                b = q // seg
                u = (q % seg) / float(seg)
            else:
                total = (nc - 1) * seg + 1
                q = max(0, min(total - 1, int(round(s * seg))))
                b = q // seg
                u = (q % seg) / float(seg)
                if b >= nc - 1:  # 最后一个环 = 末段( nc-2 -> nc-1 )的 u=1，纯归末链
                    b = nc - 2
                    u = 1.0
            # 侧向权重直接由贝塞尔曲线定义（可在 0..1 全程编辑）：
            # 曲线 y=B(u) 即「下一根链」占比，「上一根链」占 1-B(u)；
            # 几何中点 u=0.5 时对称曲线两侧各 0.5。端点 u=0/1 自然纯 1。
            B = bezier_weight(u, x1, y1, x2, y2)
            w_prev = 1.0 - B
            w_next = B

            def add_chain(idx, val):
                if val <= 0.0:
                    return
                if wrap:
                    idx %= nc
                elif not (0 <= idx < nc):
                    return
                weights[idx] = weights.get(idx, 0.0) + val

            add_chain(b, w_prev)
            add_chain(b + 1, w_next)
            # 只有 lat_span>0 时，权重才继续向更远处的链扩散；收缩环边只缩减
            # 这段「额外扩散」能到达的链数，主相邻两链始终由曲线决定。
            # 尾部分别乘 B /(1-B)，保证恰在链位置(u=0/1)时远处权重为 0，端点恒纯 1。
            reach_up = max(0, span - shrink_up // seg)
            reach_down = max(0, span - shrink_down // seg)
            for t in range(1, reach_up + 1):
                f = B * w_prev * (1.0 - bezier_weight(float(t) / (reach_up + 1),
                                                       x1, y1, x2, y2))
                add_chain(b - t, f)
            for t in range(1, reach_down + 1):
                f = w_next * (1.0 - B) * (1.0 - bezier_weight(float(t) / (reach_down + 1),
                                                              x1, y1, x2, y2))
                add_chain(b + 1 + t, f)
            tot = sum(weights.values()) or 1.0
            weights = dict((idx, v / tot) for idx, v in weights.items())
        else:
            b = int(math.floor(s + 1e-9))
            u = s - b
            if not wrap and b >= nc - 1:
                b = nc - 2
                u = 1.0
            if anchor == '自身骨骼权重=1':
                owner = b if u < 1.0 else (b + 1) % nc
                weights[owner % nc] = 1.0
            elif anchor == '上一根骨骼权重=1':
                owner = (b - 1) % nc if (u < 1e-9 and (b > 0 or wrap)) else b % nc
                weights[owner % nc] = 1.0
            else:  # 就近骨骼权重=1：按距离归最近的链，恰好在中心时各占 0.5
                if u < 0.5:
                    weights[b % nc] = 1.0
                elif u > 0.5:
                    weights[(b + 1) % nc] = 1.0
                else:
                    weights[b % nc] = 0.5
                    weights[(b + 1) % nc] = 0.5
        return weights

    # 清理过小权重：低于 eps 的清 0 后归一化；eps<=0 不清理
    def _prune_weights(self, W, eps):
        if eps <= 0.0 or not W:
            return W
        out = dict((j, v) for j, v in W.items() if v >= eps)
        if not out:
            # 全部被清掉时保留最大的一项，避免顶点无权重
            k = max(W, key=W.get)
            return {k: 1.0}
        total = sum(out.values())
        if total <= 0.0:
            return out
        return dict((j, v / total) for j, v in out.items())

    # 纯算法模拟 Maya 自带「后期」笔刷平滑（artAttrSkinPaintCtx Smooth），但按方向单向计算：
    # 只对一维权重序列（同一列内沿骨骼方向的环序列，或同一环内侧向的列序列）做
    # 含自身的邻居迭代平均，迭代结束后逐项归一化（等价 Post 归一化观感）。
    # 关键：不在整张网格上做二维拓扑平均，否则沿骨骼方向（正面）的权重变化会串到侧面。
    # series: list[dict(影响对象->权重)]；periodic=True 时序列首尾相连（侧向闭环 wrap）
    def _smooth_weight_series(self, series, iterations, periodic=False):
        if iterations <= 0 or not series:
            return series
        work = [dict(d) for d in series]
        L = len(work)
        for _ in range(iterations):
            nxt = []
            for i in range(L):
                acc = dict(work[i])
                if periodic:
                    for key, val in work[(i - 1) % L].items():
                        acc[key] = acc.get(key, 0.0) + val
                    for key, val in work[(i + 1) % L].items():
                        acc[key] = acc.get(key, 0.0) + val
                    denom = 3.0  # 闭环：自身 + 两侧邻居
                else:
                    denom = 1.0
                    if i > 0:
                        for key, val in work[i - 1].items():
                            acc[key] = acc.get(key, 0.0) + val
                        denom += 1.0
                    if i < L - 1:
                        for key, val in work[i + 1].items():
                            acc[key] = acc.get(key, 0.0) + val
                        denom += 1.0
                nxt.append(dict((key, val / denom) for key, val in acc.items()))
            work = nxt
        for d in work:  # 后期归一化：每项权重和收敛回 1
            tot = sum(d.values())
            if tot > 1e-9:
                for key in d:
                    d[key] /= tot
        return work

    # 条状面片：蒙皮并写权重
    # skin 传入已有 skinCluster 时直接复用（只改权重，不重新绑定，模型不刷新）
    def apply_weights(self, mesh, joints, segments, anchor, smooth, bez, span=0, prune=0.01,
                      lock_root=False, lock_end=False, skin=None,
                      shrink_up=0, shrink_down=0, smooth_iter=0):
        n = len(joints)
        R = (n - 1) * segments + 1

        # 单点最大影响骨骼数（扩散窗口 + 算法平滑迭代都会扩大重叠范围）
        mi_need = max(3, min(n, 2 * (span + 1) + 1 + smooth_iter))
        if skin and cmds.objExists(skin):
            if cmds.getAttr(skin + '.mi') < mi_need:
                cmds.setAttr(skin + '.mi', mi_need)
        else:
            skin = cmds.skinCluster(joints, mesh, tsb=True, mi=mi_need, nw=2, dr=4.0)[0]
        valid = set(cmds.skinCluster(skin, q=True, inf=True) or [])

        # 先按环收集权重（左右两行同环同权），沿骨骼方向做一维算法后期平滑，
        # 再复制到左右两行一次写入——条状无侧向维度，不存在方向串扰
        rings = []
        for r in range(R):
            b, u = self._ring_bu(r, R, n, segments)
            weights = self._prune_weights(
                self.ring_weights(joints, b, u, anchor, smooth, bez, span, lock_root,
                                  lock_end, segments, shrink_up, shrink_down),
                prune)
            rings.append(dict((j, weights.get(j, 0.0)) for j in joints if j in valid))
        rings = self._smooth_weight_series(rings, smooth_iter, periodic=False)
        for r in range(R):
            tv = [(j, rings[r].get(j, 0.0)) for j in joints if j in valid]
            cmds.skinPercent(skin, '%s.vtx[%d]' % (mesh, r), tv=tv)
            cmds.skinPercent(skin, '%s.vtx[%d]' % (mesh, R + r), tv=tv)
        return skin

    # 连续面片：蒙皮并写权重（沿骨骼权重 x 侧向权重，两个方向算法完全独立）
    # skin 传入已有 skinCluster 时直接复用（只改权重，不重新绑定，模型不刷新）
    def apply_sheet_weights(self, mesh, chains, segments, lat_seg, anchor, smooth, bez,
                            lat_anchor, lat_smooth, lat_bez, wrap, cols=None, R=None, grid=None,
                            span=0, lat_span=0, prune=0.01, lock_root=False, lock_end=False,
                            skin=None, shrink_up=0, shrink_down=0,
                            lat_shrink_up=0, lat_shrink_down=0, smooth_iter=0):
        n = min(len(c) for c in chains)
        chains = [c[:n] for c in chains]
        nc = len(chains)
        if R is None:
            R = (n - 1) * segments + 1
        if cols is None:
            cols = self.sheet_columns(nc, lat_seg, wrap)
        C = len(cols)

        # 每条链每环的沿骨骼方向权重；算法后期平滑只沿环方向（同一链内）单向进行，
        # 不碰相邻列，正面的权重变化不会串到侧面
        per_chain = []
        for joints in chains:
            rw = []
            for r in range(R):
                b, u = self._ring_bu(r, R, n, segments)
                rw.append(self.ring_weights(joints, b, u, anchor, smooth, bez, span,
                                            lock_root, lock_end, segments,
                                            shrink_up, shrink_down))
            rw = self._smooth_weight_series(rw, smooth_iter, periodic=False)
            per_chain.append(rw)

        # 侧向权重按列直接取值：「算法平滑次数」属于骨骼方向参数，只做沿骨骼方向的
        # 单向平滑，不对侧向列序列做后期平均，保证正面（沿骨骼）的调整绝不改变侧向归属
        lat_series = []
        for ci, (i, j, u) in enumerate(cols):
            s_lat = i + u  # 侧向连续参数：列在链 i 与链 j 之间，u 为插值比例
            lat_series.append(self.lat_weights(nc, s_lat, lat_anchor, lat_smooth, lat_bez, wrap,
                                               lat_span, lat_seg, lat_shrink_up, lat_shrink_down))

        all_joints = [j for chain in chains for j in chain]
        # 单点最大影响骨骼数 = 沿骨骼重叠数（含算法平滑迭代余量） x 侧向重叠数
        mi_along = max(3, min(n, 2 * (span + 1) + 1 + smooth_iter))
        mi_lat = max(3, min(nc, 2 * (lat_span + 1) + 1))
        mi_need = mi_along * mi_lat
        if skin and cmds.objExists(skin):
            if cmds.getAttr(skin + '.mi') < mi_need:
                cmds.setAttr(skin + '.mi', mi_need)
        else:
            skin = cmds.skinCluster(all_joints, mesh, tsb=True, mi=mi_need, nw=2, dr=4.0)[0]
        valid = set(cmds.skinCluster(skin, q=True, inf=True) or [])

        # 两个方向各自平滑后的权重外积合成，逐顶点写入（焊接后 C*R 个有效顶点，索引连续）
        for ci, latW in enumerate(lat_series):
            for r in range(R):
                W = {}
                for c, lw in latW.items():
                    for jt, wv in per_chain[c][r].items():
                        W[jt] = W.get(jt, 0.0) + wv * lw
                W = self._prune_weights(W, prune)
                v = ci * R + r
                cmds.skinPercent(skin, '%s.vtx[%d]' % (mesh, v),
                                 tv=[(jt, W.get(jt, 0.0)) for jt in all_joints if jt in valid])
        return skin

    # 获取网格上的 skinCluster（如有）
    def get_skin_cluster(self, mesh):
        hist = cmds.listHistory(mesh, pdo=True) or []
        for h in hist:
            if cmds.nodeType(h) == 'skinCluster':
                return h
        return None

    # 从网格现有 skinCluster 取影响骨骼（生成后在原链上添加骨骼不影响权重编辑逻辑）
    def _skin_joints_strip(self, mesh, fallback_joints):
        skin = self.get_skin_cluster(mesh)
        infs = []
        if skin:
            infs = [j for j in (cmds.skinCluster(skin, q=True, inf=True) or []) if cmds.objExists(j)]
        if infs:
            return infs
        return [j for j in fallback_joints if cmds.objExists(j)]

    # 连续面片：按存储的链结构从 skinCluster 影响骨骼中重组各链
    def _skin_joints_sheet(self, mesh, fallback_chains):
        skin = self.get_skin_cluster(mesh)
        infs = []
        if skin:
            infs = [j for j in (cmds.skinCluster(skin, q=True, inf=True) or []) if cmds.objExists(j)]
        if not infs:
            return [[j for j in c if cmds.objExists(j)] for c in fallback_chains]
        infs_set = set(infs)
        chains = [[j for j in c if j in infs_set] for c in fallback_chains]
        chains = [c for c in chains if len(c) >= 2]
        if len(chains) < 2:
            # 结构对不上时退化为：按蒙皮影响顺序单链处理不了就回退原链
            return [[j for j in c if cmds.objExists(j)] for c in fallback_chains]
        return chains

    # 连续面片的唯一 key：按其全部根骨骼短名（排序）决定，不同骨骼套生成不同条目，互不替换
    def _sheet_key(self, chains):
        tags = sorted(self._short(c[0]) for c in chains)
        return 'sheet::' + '::'.join(tags)

    # 已生成条目是否属于当前加载的根骨骼（编辑对象按根骨骼识别）
    # 连续面片由多根骨骼链共同定义，需要其全部根骨骼都被加载才纳入编辑对象
    def _match_roots(self, key, info, root_keys):
        if key.startswith('sheet::'):
            sheet_roots = set(self._short(c[0]) for c in info['chains'])
            return sheet_roots <= root_keys
        return key in root_keys

    # 实时计算：勾选后，参数变化时对「当前加载根骨骼」对应的网格即时重建几何 / 重新赋权
    def realtime_refresh(self, rebuild_geometry=False):
        if self._applying:
            return
        if not self.chk_realtime.isChecked():
            return
        if not self.generated:
            return
        root_keys = set(self._short(r) for r in self.get_roots())
        if not root_keys:
            return

        segments = self.slider_seg.value()
        width = self.spin_width.value()
        rot = self.slider_rot.value()
        lat_seg = self.spin_lat_seg.value()
        wrap = self.chk_wrap.isChecked()
        anchor = self.combo_anchor.currentText()
        smooth = self.combo_falloff.currentText() == '平滑'
        bez = (self.spin_x1.value(), self.spin_y1.value(),
               self.spin_x2.value(), self.spin_y2.value())
        lat_anchor = self.combo_lat_anchor.currentText()
        lat_smooth = self.combo_lat_falloff.currentText() == '平滑'
        lat_bez = (self.spin_lat_x1.value(), self.spin_lat_y1.value(),
                   self.spin_lat_x2.value(), self.spin_lat_y2.value())
        span = self.spin_span.value()
        lat_span = self.spin_lat_span.value()
        shrink_up = self.spin_shrink_up.value()
        shrink_down = self.spin_shrink_down.value()
        lat_shrink_up = self.spin_lat_shrink_up.value()
        lat_shrink_down = self.spin_lat_shrink_down.value()
        smooth_iter = self.spin_smooth_iter.value()
        prune = self.spin_prune.value()
        lock_root = self.chk_lock_root.isChecked()
        lock_end = self.chk_lock_end.isChecked()

        cmds.undoInfo(openChunk=True, chunkName='Realtime Patch Chain Update')
        try:
            for key in list(self.generated.keys()):
                info = self.generated.get(key)
                if not info:
                    continue
                # 只更新当前加载根骨骼对应的网格
                if not self._match_roots(key, info, root_keys):
                    continue
                mesh = info['mesh']
                if not mesh or not cmds.objExists(mesh):
                    self.generated.pop(key, None)
                    continue
                if info['mode'] == 'sheet':
                    if rebuild_geometry:
                        # 重建几何时模型和权重一起更新（重新绑定）
                        chains_w = self._skin_joints_sheet(mesh, info['chains'])
                        cmds.delete(mesh)
                        chains, cols, R, grid, mesh = self.build_sheet_mesh(
                            info['chains'], segments, lat_seg, rot, wrap)
                        info['mesh'] = mesh
                        self.apply_sheet_weights(mesh, chains, segments, lat_seg, anchor, smooth,
                                                 bez, lat_anchor, lat_smooth, lat_bez, wrap,
                                                 cols=cols, R=R, grid=grid,
                                                 span=span, lat_span=lat_span, prune=prune,
                                                 lock_root=lock_root, lock_end=lock_end,
                                                 shrink_up=shrink_up, shrink_down=shrink_down,
                                                 lat_shrink_up=lat_shrink_up, lat_shrink_down=lat_shrink_down,
                                                 smooth_iter=smooth_iter)
                    else:
                        # 只改权重：复用现有蒙皮，模型不刷新
                        chains_w = self._skin_joints_sheet(mesh, info['chains'])
                        skin = self.get_skin_cluster(mesh)
                        self.apply_sheet_weights(mesh, chains_w, segments, lat_seg, anchor,
                                                 smooth, bez, lat_anchor, lat_smooth, lat_bez, wrap,
                                                 span=span, lat_span=lat_span, prune=prune,
                                                 lock_root=lock_root, lock_end=lock_end, skin=skin,
                                                 shrink_up=shrink_up, shrink_down=shrink_down,
                                                 lat_shrink_up=lat_shrink_up, lat_shrink_down=lat_shrink_down,
                                                 smooth_iter=smooth_iter)
                else:
                    joints_w = self._skin_joints_strip(mesh, info['chains'][0])
                    if rebuild_geometry:
                        # 重建几何时模型和权重一起更新（重新绑定）
                        cmds.delete(mesh)
                        mesh = self.build_mesh(info['chains'][0], segments, width, rot)
                        info['mesh'] = mesh
                        self.apply_weights(mesh, joints_w, segments, anchor, smooth, bez,
                                           span=span, prune=prune,
                                           lock_root=lock_root, lock_end=lock_end,
                                           shrink_up=shrink_up, shrink_down=shrink_down,
                                           smooth_iter=smooth_iter)
                    else:
                        # 只改权重：复用现有蒙皮，模型不刷新
                        skin = self.get_skin_cluster(mesh)
                        self.apply_weights(mesh, joints_w, segments, anchor, smooth, bez,
                                           span=span, prune=prune,
                                           lock_root=lock_root, lock_end=lock_end, skin=skin,
                                           shrink_up=shrink_up, shrink_down=shrink_down,
                                           smooth_iter=smooth_iter)
                cmds.select(mesh)
        finally:
            cmds.undoInfo(closeChunk=True)

    # 删除面片链（当前根骨骼对应的条状面片 + 相关的连续面片）
    def delete_patch_chain(self):
        keys = set(self._short(r) for r in self.get_roots())
        removed = []
        for key in list(self.generated.keys()):
            info = self.generated[key]
            if not self._match_roots(key, info, keys):
                continue
            mesh = info['mesh']
            if mesh and cmds.objExists(mesh):
                cmds.delete(mesh)
                removed.append(mesh)
            self.generated.pop(key, None)
        if not removed:
            cmds.warning('没有需要删除的面片链')
            return
        print('面片链已删除: ' + ', '.join(removed))


window = Window()
if __name__ == '__main__':
    window.show()
