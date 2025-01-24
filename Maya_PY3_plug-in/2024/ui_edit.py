# -*- coding: utf-8 -*-
import maya.cmds as cmds
# 编辑ui
class UiEdit:
    # 将选择的物体加载到ui
    def load_select_for_ui_text(self, soure_ui, soure_ui_type):
        sel = cmds.ls(sl=1, fl=1)
        attribute = cmds.channelBox('mainChannelBox', q=1, sma=1)
        if sel or attribute:
            # 建立具体的文本
            if attribute:
                all_attribute_sel = []
                for i in sel:
                    for j in range(0, len(attribute)):
                        attribute_sel = i + '.' + attribute[j]
                        all_attribute_sel.append(attribute_sel)
                all_sel = all_attribute_sel[0]
                for i in range(1, len(all_attribute_sel)):
                    all_sel = all_sel + ',' + all_attribute_sel[i]
            else:
                all_sel = sel[0]
                for i in range(1, len(sel)):
                    all_sel = all_sel + ',' + sel[i]
            # 有属性加载物体属性，没属性加载物体
            if soure_ui_type[0] == 'QLineEdit':
                soure_ui.setMaxLength(len(all_sel)*100+999999)
                # soure_ui.maxLength(len(all_sel))
                soure_ui.setText(all_sel)
        else:
            cmds.warning('请选择物体或者属性')

    # 自动调整滑块范围且返回数值
    def automatically_adjust_the_slider_range_and_return_the_value(self, soure_ui, soure_ui_type):
        if soure_ui_type == 'QSlider':
            num = soure_ui.sliderPosition()
            min_num = soure_ui.minimum()
            max_num = soure_ui.maximum()

            width = max_num - min_num
            # 判断是否达到前后四分之一的位置
            min_threshold = min_num + width / 10.0
            max_threshold = max_num - width / 10.0

            if num < min_threshold:
                soure_ui.setMinimum(min_num - width)
                soure_ui.setMaximum(max_threshold)
            if num > max_threshold:
                soure_ui.setMinimum(min_threshold)
                soure_ui.setMaximum(max_num + width)
            return num

    # 将数值给到滑块
    def give_the_value_to_the_slider(self, num, target_ui, target_ui_type):
        if target_ui_type == 'QSlider':
            max_num = target_ui.maximum()
            max_num = float(max_num)
            if max_num < num:
                target_ui.setMaximum(num)
            min_num = target_ui.minimum()
            if min_num > num:
                target_ui.setMinimum(num)
            target_ui.setValue(num)
