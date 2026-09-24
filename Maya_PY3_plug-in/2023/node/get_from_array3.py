# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys
import maya.mel as mel


class GetFromArray(ompx.MPxNode):
    def __init__(self):
        super(GetFromArray, self).__init__()

    node_name = "GetFromArray"
    n = 111  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    def compute(self, plug, data_block):
        if plug != GetFromArray.out_data:
            return

        select_handle = data_block.inputValue(self.select)
        select_value = select_handle.asInt()

        in_data_handle = data_block.inputArrayValue(self.in_data)
        element_count = in_data_handle.elementCount()
        if element_count == 0:
            return

        if select_value >= element_count:
            select_value = element_count - 1

        in_data_handle.jumpToElement(select_value)
        input_handle = in_data_handle.inputValue()
        input_data = input_handle.data()

        try:
            output_handle = data_block.outputValue(self.out_data)
            output_handle.setMObject(input_data)
        except:
            return
        data_block.setClean(plug)

    @classmethod
    def nodeInitializer(cls):
        nAttr = om.MFnNumericAttribute()
        cls.select = nAttr.create("select", "sel", om.MFnNumericData.kInt, 1)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setMin(0)
        cls.addAttribute(cls.select)

        cls.commend_read_int = nAttr.create("commendReadInt", "cri", om.MFnNumericData.kInt, 0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setMin(0)
        cls.addAttribute(cls.commend_read_int)

        tAttr = om.MFnTypedAttribute()
        cls.text_input = tAttr.create("textInput", "txt", om.MFnData.kString)
        stringData = om.MFnStringData().create("")
        tAttr.setDefault(stringData)
        tAttr.setStorable(True)
        tAttr.setKeyable(True)
        tAttr.setWritable(True)
        tAttr.setReadable(True)
        cls.addAttribute(cls.text_input)

        tAttr = om.MFnTypedAttribute()
        cls.in_data = tAttr.create("in_data", "indata", om.MFnData.kAny)
        tAttr.setArray(True)
        tAttr.setConnectable(True)
        tAttr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.in_data)

        tAttr = om.MFnTypedAttribute()
        cls.out_data = tAttr.create("out_data", "outdata", om.MFnData.kAny)
        tAttr.setConnectable(True)
        tAttr.setWritable(True)
        cls.addAttribute(cls.out_data)

        cls.attributeAffects(cls.in_data, cls.out_data)
        cls.attributeAffects(cls.select, cls.out_data)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(GetFromArray())


def createAETemplate():
    """修复后的属性编辑器模板 - 使用tokenize替代split"""

    template = '''
global proc AEGetFromArrayTemplate(string $nodeName) {
    editorTemplate -beginScrollLayout;

    // 基本属性部分
    editorTemplate -beginLayout "基本属性" -collapse 0;
        editorTemplate -addControl "select";
        editorTemplate -addControl "commendReadInt";
        editorTemplate -addControl "textInput";
    editorTemplate -endLayout;

    // 按钮部分
    editorTemplate -beginLayout "操作" -collapse 0;
        editorTemplate -callCustom "AECreateButton" "AEUpdateButton" "nodeName" $nodeName;
    editorTemplate -endLayout;

    editorTemplate -addExtraControls;
    editorTemplate -endScrollLayout;
}

// 获取最后一个点号前的完整内容
global proc string getCleanNodeName(string $fullName) {
    // 如果包含点号，可能是完整路径
    string $parts[];
    tokenize $fullName "." $parts;
    if (size($parts) > 1) {
        // 获取最后一个点号前的所有部分
        string $result = "";
        for ($i = 0; $i < size($parts)-1; $i++) {
            if ($i > 0) {
                $result = $result + "." + $parts[$i];
            } else {
                $result = $parts[$i];
            }
        }
        return $result;
    } else {
        return $fullName;
    }
}

global proc AECreateButton(string $attrName, string $nodeName) {
    columnLayout;

    // 获取干净的节点名称
    string $cleanName = getCleanNodeName($nodeName);

    // 使用干净的节点名称
    button -label ("获取节点属性并打印") 
           -command ("getNodeInfo(\\"" + $cleanName + "\\")")
           -annotation "获取当前属性编辑器中的节点信息"
           btnGetNode;

    setParent ..;
}

global proc AEUpdateButton(string $attrName, string $nodeName) {
    // 获取干净的节点名称
    string $cleanName = getCleanNodeName($nodeName);

    // 更新按钮文本
    if (`button -exists btnGetNode`) {
        button -edit -label ("获取节点: " + $cleanName) btnGetNode;
    }
}

// 修复后的获取节点信息函数
global proc getNodeInfo(string $nodeName) {
    print("=== 节点信息 ===\\n");

    // 首先尝试直接使用节点名称
    if (`objExists $nodeName`) {
        print("使用节点: " + $nodeName + "\\n");
        processNodeInfo($nodeName);
        return;
    }

    // 如果节点不存在，尝试不同的可能性
    print("尝试查找节点: " + $nodeName + "\\n");

    // 1. 尝试查找所有GetFromArray节点
    string $allNodes[] = `ls -type "GetFromArray"`;

    // 使用stringArrayToString将数组转换为字符串
    if (size($allNodes) > 0) {
        string $allNodesStr = stringArrayToString($allNodes, ", ");
        print("找到的GetFromArray节点: " + $allNodesStr + "\\n");
    } else {
        print("没有找到任何GetFromArray节点\\n");
    }

    if (size($allNodes) > 0) {
        // 2. 尝试匹配节点名称
        for ($i = 0; $i < size($allNodes); $i++) {
            string $node = $allNodes[$i];
            string $cleanNode = getCleanNodeName($node);
            if ($cleanNode == $nodeName) {
                print("匹配到节点: " + $node + "\\n");
                processNodeInfo($node);
                return;
            }
        }

        // 3. 如果没有精确匹配，使用第一个找到的节点
        print("使用第一个找到的节点: " + $allNodes[0] + "\\n");
        processNodeInfo($allNodes[0]);
    } else {
        warning("没有找到任何GetFromArray节点");
    }

    print("================\\n");
}

// 处理节点信息的辅助函数
global proc processNodeInfo(string $nodeName) {
    // 检查节点类型
    string $nodeType = `nodeType $nodeName`;
    print("节点类型: " + $nodeType + "\\n");

    // 如果是变换节点，尝试获取其形状节点
    if ($nodeType == "transform") {
        string $shapes[] = `listRelatives -shapes $nodeName`;
        if (size($shapes) > 0) {
            $nodeName = $shapes[0];
            $nodeType = `nodeType $nodeName`;
            print("转换为形状节点: " + $nodeName + "\\n");
        }
    }

    // 检查是否是GetFromArray节点
    if ($nodeType == "GetFromArray") {
        // 获取并打印属性值
        if (`attributeExists "select" $nodeName`) {
            int $selectVal = `getAttr ($nodeName + ".select")`;
            print("select 值: " + $selectVal + "\\n");
        }

        if (`attributeExists "commendReadInt" $nodeName`) {
            int $commendVal = `getAttr ($nodeName + ".commendReadInt")`;
            print("commendReadInt 值: " + $commendVal + "\\n");
        }

        if (`attributeExists "textInput" $nodeName`) {
            string $textVal = `getAttr ($nodeName + ".textInput")`;
            print("textInput 值: " + $textVal + "\\n");
        }
    } else {
        warning("节点不是 GetFromArray 类型: " + $nodeType);
    }
}
'''
    # 执行模板
    mel.eval(template)


def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")

    try:
        plugin.registerNode(
            GetFromArray.node_name,
            GetFromArray.Uv_id,
            GetFromArray.nodeCreator,
            GetFromArray.nodeInitializer
        )

        # 创建属性编辑器模板
        createAETemplate()

        print(f"? 成功注册节点: {GetFromArray.node_name}")

    except Exception as e:
        sys.stderr.write(f"注册节点失败: {GetFromArray.node_name}, 错误: {str(e)}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(GetFromArray.Uv_id)