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
    n = 3  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    def compute(self, plug, data_block):
        # print('实行了计算')
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
        # 获取 ifShape 属性值
        ifshape_handle = data_block.inputValue(self.if_shape)
        ifshape_value = ifshape_handle.asBool()
        # 如果 ifShape 为 True，进行形状节点数据重建
        if ifshape_value:
            # print('获取的数据是形状节点')
            # 检查数据类型
            fn_data = om.MFnData(input_data)
            data_type = fn_data.type()
            # print(data_type)

            # 如果 ifShape 为 True，进行形状节点数据重建
            if ifshape_value:
                # print('获取的数据是形状节点')

                # 1. 判断并处理 网格数据 (Mesh)
                if input_data.hasFn(om.MFn.kMeshData):
                    # print('是网格(Mesh)')

                    # 创建新的网格数据载体
                    mesh_data_fn = om.MFnMeshData()
                    new_mesh_data = mesh_data_fn.create()

                    # 直接将传入的数据对象(MObject)交给 MFnMesh 解析
                    fn_mesh = om.MFnMesh(input_data)

                    num_vertices = fn_mesh.numVertices()
                    num_faces = fn_mesh.numPolygons()

                    # Maya API 1.0 建议使用 MFloatPointArray 匹配 create 参数
                    vertices = om.MFloatPointArray()
                    fn_mesh.getPoints(vertices, om.MSpace.kWorld)

                    face_counts = om.MIntArray()
                    face_connects = om.MIntArray()
                    fn_mesh.getVertices(face_counts, face_connects)

                    # 创建新的网格，【极其重要】：必须把 new_mesh_data 作为最后一个参数传入！
                    new_fn_mesh = om.MFnMesh()
                    new_fn_mesh.create(num_vertices, num_faces, vertices, face_counts, face_connects, new_mesh_data)

                    # 更新输出数据
                    input_data = new_mesh_data

                # 2. 判断并处理 曲线数据 (NurbsCurve)
                elif input_data.hasFn(om.MFn.kNurbsCurveData):
                    # print('是曲线(NurbsCurve)')

                    curve_data_fn = om.MFnNurbsCurveData()
                    new_curve_data = curve_data_fn.create()

                    fn_curve = om.MFnNurbsCurve(input_data)

                    # API 1.0 获取属性是方法，必须加括号
                    degree = fn_curve.degree()
                    form = fn_curve.form()

                    cvs = om.MPointArray()
                    knots = om.MDoubleArray()
                    fn_curve.getCVs(cvs, om.MSpace.kWorld)
                    fn_curve.getKnots(knots)

                    # 创建新曲线，结尾必须传入 new_curve_data 承载数据
                    new_fn_curve = om.MFnNurbsCurve()
                    new_fn_curve.create(cvs, knots, degree, form, False, False, new_curve_data)

                    input_data = new_curve_data

                # 3. 判断并处理 曲面数据 (NurbsSurface)
                elif input_data.hasFn(om.MFn.kNurbsSurfaceData):
                    # print('是曲面(NurbsSurface)')

                    surface_data_fn = om.MFnNurbsSurfaceData()
                    new_surface_data = surface_data_fn.create()

                    fn_surface = om.MFnNurbsSurface(input_data)

                    # 必须加括号调用
                    degree_u = fn_surface.degreeU()
                    degree_v = fn_surface.degreeV()
                    form_u = fn_surface.formInU()
                    form_v = fn_surface.formInV()

                    cvs = om.MPointArray()
                    fn_surface.getCVs(cvs, om.MSpace.kWorld)

                    knots_u = om.MDoubleArray()
                    knots_v = om.MDoubleArray()
                    fn_surface.getKnotsInU(knots_u)
                    fn_surface.getKnotsInV(knots_v)

                    # API 1.0 的曲面 create 传参不需要显式给 num_cvs_u / v
                    # 结尾必须传入 new_surface_data 承载数据
                    new_fn_surface = om.MFnNurbsSurface()
                    new_fn_surface.create(cvs, knots_u, knots_v, degree_u, degree_v,
                                          form_u, form_v, False, new_surface_data)

                    input_data = new_surface_data

        # try:
        output_handle = data_block.outputValue(self.out_data)
        output_handle.setMObject(input_data)
        # except:
        #     return
        data_block.setClean(plug)

    @classmethod
    def nodeInitializer(cls):
        nAttr = om.MFnNumericAttribute()
        cls.select = nAttr.create("select", "sel", om.MFnNumericData.kInt, 0)
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

        # 添加布尔属性 ifShape
        cls.if_shape = nAttr.create("ifShape", "ifshape", om.MFnNumericData.kBoolean, 0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        cls.addAttribute(cls.if_shape)

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
        tAttr.setKeyable(True)
        cls.addAttribute(cls.in_data)

        tAttr = om.MFnTypedAttribute()
        cls.out_data = tAttr.create("out_data", "outdata", om.MFnData.kAny)
        tAttr.setConnectable(True)
        tAttr.setWritable(True)
        cls.addAttribute(cls.out_data)

        cls.attributeAffects(cls.in_data, cls.out_data)
        cls.attributeAffects(cls.select, cls.out_data)
        cls.attributeAffects(cls.if_shape, cls.out_data)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(GetFromArray())


def createAETemplate():
    """修复节点查询问题的属性编辑器模板"""

    template = '''
global proc AEGetFromArrayTemplate(string $nodeName) {
    editorTemplate -beginScrollLayout;

    // 基本属性部分
    editorTemplate -beginLayout "基本属性(base attribute)" -collapse 0;
        editorTemplate -addControl "select";
        editorTemplate -addControl "commendReadInt";
        editorTemplate -addControl "ifPy";  // 添加ifPy属性控制
        editorTemplate -addControl "ifShape";  // 添加ifShape属性控制

        // 添加说明文本
        editorTemplate -callCustom "AECreateHelpText" "" "helpText" $nodeName;

        editorTemplate -addControl "textInput";
    editorTemplate -endLayout;

    // 按钮部分
    editorTemplate -beginLayout "操作(operate)" -collapse 0;
        editorTemplate -callCustom "AECreateButton" "AEUpdateButton" "nodeName" $nodeName;
    editorTemplate -endLayout;

    editorTemplate -addExtraControls;
    editorTemplate -endScrollLayout;
}

// 创建帮助文本
global proc AECreateHelpText(string $attrName, string $nodeName) {
    columnLayout;
    text -label "可用变量";
    text -label "MEL:$localSelectVal, $localIfPyVal, $localCommendVal, $cleanName";
    text -label "Python:selectVal, ifPyVal, commendVal, cleanNameVal";
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
        button -edit -label ("获取节点并运行代码: " + $cleanName) btnGetNode;
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
            print("执行MEL代码:" + $enhancedCode + "\\n");
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
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.1.0")

    try:
        plugin.registerNode(
            GetFromArray.node_name,
            GetFromArray.Uv_id,
            GetFromArray.nodeCreator,
            GetFromArray.nodeInitializer,
        )
        # 创建属性编辑器模板
        createAETemplate()
        print(f"成功注册节点: {GetFromArray.node_name}")
        txt = GetFromArray.node_name + '内置变量：' + '''
MEL:
print("select 值: " + $localSelectVal + "\\n");
print("ifPy 值: " + $localIfPyVal + "\\n");
print("commendReadInt 值: " + $localCommendVal + "\\n");
print("name 值: " + $localCleanName + "\\n");
PY：
print('');
print(selectVal);
print(ifPyVal);
print(commendVal);
print(cleanNameVal);
        '''
        print(txt)
    except Exception as e:
        sys.stderr.write(f"注册节点失败: {GetFromArray.node_name}, 错误: {str(e)}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(GetFromArray.Uv_id)