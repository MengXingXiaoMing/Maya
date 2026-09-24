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
    n = 151  # 0-63
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

        # 添加布尔属性 ifPy
        cls.if_py = nAttr.create("ifPy", "ifpy", om.MFnNumericData.kBoolean, 0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.if_py)

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
    """修复节点查询问题的属性编辑器模板"""

    template = '''
global proc AEGetFromArrayTemplate(string $nodeName) {
    editorTemplate -beginScrollLayout;

    // 基本属性部分
    editorTemplate -beginLayout "基本属性" -collapse 0;
        editorTemplate -addControl "select";
        editorTemplate -addControl "commendReadInt";
        editorTemplate -addControl "ifPy";  // 添加ifPy属性控制
        
        // 添加说明文本
        editorTemplate -callCustom "AECreateHelpText" "" "helpText" $nodeName;
        
        editorTemplate -addControl "textInput";
    editorTemplate -endLayout;
    

    
    // 按钮部分
    editorTemplate -beginLayout "操作" -collapse 0;
        editorTemplate -callCustom "AECreateButton" "AEUpdateButton" "nodeName" $nodeName;
    editorTemplate -endLayout;

    editorTemplate -addExtraControls;
    editorTemplate -endScrollLayout;
}

// 创建帮助文本
global proc AECreateHelpText(string $attrName, string $nodeName) {
    columnLayout;
    text -label "可用变量";
    text -label "MEL:$localSelectVal,$localIfPyVal$localCommendVal,$cleanName";
    text -label "PY:selectVal,ifPyVal,commendVal,cleanNameVal";
    setParent ..;
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

    // 使用原始节点名称，确保查询当前节点
    button -label ("获取节点属性并运行填写的代码") 
           -command ("getCurrentNodeInfo(\\"" + $nodeName + "\\")")
           -annotation "获取当前属性编辑器中的节点信息"
           btnGetNode;
           
    button -label ("自动链接形状(Mesh.outMesh,nurbsCurve.worldSpace,nurbsSurface.worldSpace)") 
           -command ("autoConnectShapes(\\"" + $nodeName + "\\")")
           -annotation "自动连接形状节点"
           btnAutoConnect;
           
    setParent ..;
}

global proc AEUpdateButton(string $attrName, string $nodeName) {
    // 获取干净的节点名称用于标签显示
    string $cleanName = getCleanNodeName($nodeName);

    // 更新按钮文本和命令
    if (`button -exists btnGetNode`) {
        button -edit -label ("获取节点: " + $cleanName) btnGetNode;
        // 更新按钮命令，使用原始节点名称
        button -edit -command ("getCurrentNodeInfo(\\"" + $nodeName + "\\")") btnGetNode;
    }
}

// 简化的获取节点信息函数 - 只获取当前节点
global proc getCurrentNodeInfo(string $nodeName) {
    //print("传入的节点名称: " + $nodeName + "\\n");
    string $cleanName;
    int $selectVal;
    int $ifPyVal;
    int $commendVal;
    string $textVal;
    
    $cleanName = getCleanNodeName($nodeName);

    // 获取并打印属性值
    if (`attributeExists "select" $cleanName`) {
        $selectVal = `getAttr ($cleanName + ".select")`;
    }

    if (`attributeExists "commendReadInt" $cleanName`) {
        $commendVal = `getAttr ($cleanName + ".commendReadInt")`;
    }
        
    if (`attributeExists "ifPy" $cleanName`) {
        $ifPyVal = `getAttr ($cleanName + ".ifPy")`;
    }
    
    if (`attributeExists "textInput" $cleanName`) {
        $textVal = `getAttr ($cleanName + ".textInput")`;
    }
    print("使用节点: " + $cleanName + "\\n");
    print("select 值: " + $selectVal + "\\n");
    print("ifPy 值: " + $ifPyVal + "\\n");
    print("commendReadInt 值: " + $commendVal + "\\n");
    print("textInput 值: " + $textVal + "\\n");
    
    // MEL模式 - 构建增强代码
    string $enhancedCode = "int $localSelectVal = " + $selectVal + ";";
    $enhancedCode = $enhancedCode + "int $localIfPyVal = " + $ifPyVal + ";";
    $enhancedCode = $enhancedCode + "int $localCommendVal = " + $commendVal + ";";
    $enhancedCode = $enhancedCode + "string $localCleanName = \\"" + $cleanName + "\\";";
    //$enhancedCode = $enhancedCode + $textVal;
    eval($enhancedCode);
    
    if (size($textVal) > 0) {
        if ($ifPyVal == 0) {
            print("执行MEL代码:" + $enhancedCode );
            eval($textVal);
        } else {
            // Python模式
            print("执行Python代码: " + $textVal);
            // 通过python命令传递变量值
            string $pythonCode = "selectVal = " + $selectVal + "; ";
            $pythonCode = $pythonCode + "ifPyVal = " + $ifPyVal + "; ";
            $pythonCode = $pythonCode + "commendVal = " + $commendVal + "; ";
            $pythonCode = $pythonCode + "cleanNameVal = \\"" + $cleanName + "\\"; ";
            
            python($pythonCode);
            python($textVal);
        }
    }
}

// 自动连接形状节点
global proc autoConnectShapes(string $nodeName) {
    string $cleanName = getCleanNodeName($nodeName);
    print("自动连接形状节点: " + $cleanName + "\\n");
    
    // 获取当前选择的变换节点
    string $selected[] = `ls -sl -type "transform"`;
    
    if (size($selected) == 0) {
        warning("请先选择一个或多个变换节点");
        return;
    }
    
    for ($obj in $selected) {
        // 获取形状节点
        string $shapes[] = `listRelatives -shapes $obj`;
        
        if (size($shapes) > 0) {
            for ($shape in $shapes) {
                string $shapeType = `nodeType $shape`;
                print("处理形状节点: " + $shape + " (" + $shapeType + ")\\n");
                
                // 目标属性
                string $targetAttr = $cleanName + ".in_data";
                
                // 从索引0开始检查连接
                int $connectedIndex = 0;
                
                // 获取in_data数组的大小
                int $arraySize = `getAttr -size ($cleanName + ".in_data")`;
                //print("    in_data数组大小: " + $arraySize);
                
                // 检查每个索引是否有连接
                for ($i = 0; $i < ($arraySize+1); $i++) {
                    string $elementAttr = $targetAttr + "[" + $i + "]";
                    
                    // 检查该索引是否有连接
                    if (`connectionInfo -isSource $elementAttr` || `connectionInfo -isDestination $elementAttr`) {
                        // 获取连接的源或目标
                        string $connections[] = `listConnections -source true -destination true -plugs true $elementAttr`;
                        
                        if (size($connections) > 0) {
                            print("    索引 " + $i + " 已有连接: " + $connections[0] + "\\n");
                        }
                    } else {
                        // 找到第一个未连接的索引
                        $connectedIndex = $i;
                        print("    索引 " + $i + " 未连接，可以连接\\n");
                        break;
                    }
                }
    
                // 根据形状类型连接相应的属性
                if ($shapeType == "mesh") {
                    // 连接网格
                    if (!`isConnected ($shape + ".outMesh") ($cleanName + ".in_data["+$connectedIndex+"]")`) {
                        connectAttr ($shape + ".outMesh") ($cleanName + ".in_data["+$connectedIndex+"]");
                        print("连接: " + $shape + ".outMesh 到 " + $cleanName + ".in_data["+$connectedIndex+"]\\n");
                    }
                } else if ($shapeType == "nurbsCurve") {
                    // 连接NURBS曲线
                    if (!`isConnected ($shape + ".worldSpace") ($cleanName + ".in_data["+$connectedIndex+"]")`) {
                        connectAttr ($shape + ".worldSpace") ($cleanName + ".in_data["+$connectedIndex+"]");
                        print("连接: " + $shape + ".worldSpace 到 " + $cleanName + ".in_data["+$connectedIndex+"]\\n");
                    }
                } else if ($shapeType == "nurbsSurface") {
                    // 连接NURBS曲面
                    if (!`isConnected ($shape + ".worldSpace") ($cleanName + ".in_data["+$connectedIndex+"]")`) {
                        connectAttr ($shape + ".worldSpace") ($cleanName + ".in_data["+$connectedIndex+"]");
                        print("连接: " + $shape + ".worldSpace 到 " + $cleanName + ".in_data["+$connectedIndex+"]\\n");
                    }
                }
            }
        }
    }
    
    print("自动连接完成\\n");
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