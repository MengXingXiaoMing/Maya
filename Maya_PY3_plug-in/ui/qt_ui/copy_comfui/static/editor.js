// --- 单独注册每个节点 ---

// 图像加载器节点
function ImageLoaderNode() {
    this.addInput("trigger", null);
    this.addOutput("IMAGE", null);
    this.addOutput("PATH", null);

    this.properties = { path: "/images/default.jpg" };
    this.addWidget("text", "path", this.properties.path, "path", function(v) {
        this.properties.path = v;
    });

    this.size = [220, 120];
    this.title = "图像加载器";
}
ImageLoaderNode.title = "图像加载器";
ImageLoaderNode.desc = "加载图像文件";
ImageLoaderNode.prototype.onExecute = function() {
    // 节点执行逻辑
};
LiteGraph.registerNodeType("loaders/image_loader", ImageLoaderNode);

// 逻辑引擎节点
function LogicEngineNode() {
    this.addInput("IN_A", null);
    this.addInput("IN_B", null);
    this.addOutput("OUT", null);

    this.properties = { operation: "and", threshold: 0.5 };

    this.addWidget("combo", "operation", this.properties.operation, function(v) {
        this.properties.operation = v;
    }, { values: ["and", "or", "xor", "not"] });

    this.addWidget("number", "threshold", this.properties.threshold, "threshold", function(v) {
        this.properties.threshold = v;
    });

    this.size = [220, 140];
    this.title = "逻辑引擎";
}
LogicEngineNode.title = "逻辑引擎";
LogicEngineNode.desc = "执行逻辑运算";
LogicEngineNode.prototype.onExecute = function() {
    // 节点执行逻辑
};
LiteGraph.registerNodeType("math/logic_engine", LogicEngineNode);

// 监视器输出节点
function MonitorNode() {
    this.addInput("A", null);
    this.addInput("B", null);

    this.properties = { name: "Monitor", auto_refresh: true };

    this.addWidget("text", "name", this.properties.name, "name", function(v) {
        this.properties.name = v;
    });

    this.addWidget("toggle", "auto_refresh", this.properties.auto_refresh, function(v) {
        this.properties.auto_refresh = v;
    });

    this.size = [220, 120];
    this.title = "监视器";
}
MonitorNode.title = "监视器";
MonitorNode.desc = "显示输出结果";
MonitorNode.prototype.onExecute = function() {
    // 节点执行逻辑
};
LiteGraph.registerNodeType("output/monitor", MonitorNode);

// 算术运算节点
function ArithmeticNode() {
    this.addInput("A", null);
    this.addInput("B", null);
    this.addOutput("OUT", null);

    this.properties = { operation: "add" };

    this.addWidget("combo", "operation", this.properties.operation, function(v) {
        this.properties.operation = v;
    }, { values: ["add", "subtract", "multiply", "divide"] });

    this.size = [220, 100];
    this.title = "算术运算";
}
ArithmeticNode.title = "算术运算";
ArithmeticNode.desc = "执行基本算术运算";
ArithmeticNode.prototype.onExecute = function() {
    // 节点执行逻辑
};
LiteGraph.registerNodeType("math/arithmetic", ArithmeticNode);

// 模糊滤镜节点
function BlurNode() {
    this.addInput("IMAGE", null);
    this.addOutput("OUT", null);

    this.properties = { radius: 5, type: "gaussian" };

    this.addWidget("number", "radius", this.properties.radius, "radius", function(v) {
        this.properties.radius = v;
    });

    this.addWidget("combo", "type", this.properties.type, function(v) {
        this.properties.type = v;
    }, { values: ["gaussian", "box", "median"] });

    this.size = [220, 120];
    this.title = "模糊滤镜";
}
BlurNode.title = "模糊滤镜";
BlurNode.desc = "应用模糊效果";
BlurNode.prototype.onExecute = function() {
    // 节点执行逻辑
};
LiteGraph.registerNodeType("filters/blur", BlurNode);

// 边缘检测节点
function EdgeDetectionNode() {
    this.addInput("IMAGE", null);
    this.addOutput("OUT", null);

    this.properties = { threshold: 0.1, algorithm: "canny" };

    this.addWidget("number", "threshold", this.properties.threshold, "threshold", function(v) {
        this.properties.threshold = v;
    });

    this.addWidget("combo", "algorithm", this.properties.algorithm, function(v) {
        this.properties.algorithm = v;
    }, { values: ["canny", "sobel", "laplacian"] });

    this.size = [220, 120];
    this.title = "边缘检测";
}
EdgeDetectionNode.title = "边缘检测";
EdgeDetectionNode.desc = "检测图像边缘";
EdgeDetectionNode.prototype.onExecute = function() {
    // 节点执行逻辑
};
LiteGraph.registerNodeType("filters/edge_detection", EdgeDetectionNode);

// 日志记录器节点
function LoggerNode() {
    this.addInput("data", null);
    this.addInput("log", null);

    this.properties = { log_level: "info", file_path: "/logs/process.log" };

    this.addWidget("combo", "log_level", this.properties.log_level, function(v) {
        this.properties.log_level = v;
    }, { values: ["debug", "info", "warning", "error"] });

    this.addWidget("text", "file_path", this.properties.file_path, "file_path", function(v) {
        this.properties.file_path = v;
    });

    this.size = [220, 140];
    this.title = "日志记录器";
}
LoggerNode.title = "日志记录器";
LoggerNode.desc = "记录处理日志";
LoggerNode.prototype.onExecute = function() {
    // 节点执行逻辑
};
LiteGraph.registerNodeType("output/logger", LoggerNode);

// --- 图形初始化 ---
const graph = new LGraph();
const canvasElement = document.getElementById("mainCanvas");
const lCanvas = new LGraphCanvas("#mainCanvas", graph);

// --- 工作流加载功能 ---
async function fetchWorkflow() {
    const filename = document.getElementById("fileList").value;
    try {
        const res = await fetch(`/api/load/${filename}`);
        const data = await res.json();

        graph.clear();

        // 节点映射
        const nodeMap = {};

        // 创建节点
        if (data.nodes && Array.isArray(data.nodes)) {
            data.nodes.forEach(nodeData => {
                const node = LiteGraph.createNode(nodeData.type);
                if (node) {
                    node.id = nodeData.id;
                    node.pos = nodeData.pos;
                    if (nodeData.title) node.title = nodeData.title;
                    if (nodeData.properties) {
                        // 确保属性正确设置
                        for (const key in nodeData.properties) {
                            if (node.properties.hasOwnProperty(key)) {
                                node.properties[key] = nodeData.properties[key];
                            }
                        }
                    }
                    graph.add(node);
                    nodeMap[nodeData.id] = node;
                    console.log(`创建节点: ${nodeData.type} (ID: ${nodeData.id})`);
                }
            });
        }

        // 创建连接
        if (data.links && typeof data.links === 'object') {
            console.log("开始处理链接:", data.links);

            // 修正：遍历所有链接，确保正确处理
            Object.keys(data.links).forEach(linkKey => {
                const linkData = data.links[linkKey];
                if (linkData && typeof linkData === 'object') {
                    const originId = linkData.origin_id;
                    const targetId = linkData.target_id;
                    const originSlot = linkData.origin_slot;
                    const targetSlot = linkData.target_slot;

                    console.log(`处理链接: ${originId}:${originSlot} -> ${targetId}:${targetSlot}`);

                    const originNode = nodeMap[originId];
                    const targetNode = nodeMap[targetId];

                    if (originNode && targetNode) {
                        // 修正：使用正确的连接方法
                        try {
                            // 方法1: 使用LiteGraph的标准连接方式
                            const link = originNode.connect(originSlot, targetNode, targetSlot);
                            if (link) {
                                console.log(`连接成功: ${originId}:${originSlot} -> ${targetId}:${targetSlot}`);
                            } else {
                                console.warn(`连接失败: ${originId}:${originSlot} -> ${targetId}:${targetSlot}`);

                                // 方法2: 尝试反向连接
                                const reverseLink = targetNode.connect(targetSlot, originNode, originSlot);
                                if (reverseLink) {
                                    console.log(`反向连接成功: ${targetId}:${targetSlot} -> ${originId}:${originSlot}`);
                                }
                            }
                        } catch (e) {
                            console.error(`连接异常: ${originId}:${originSlot} -> ${targetId}:${targetSlot}`, e);
                        }
                    } else {
                        console.error(`节点不存在: originId=${originId}, targetId=${targetId}`);
                    }
                }
            });
        }
        graph.start();

        // 确保正确渲染
        setTimeout(() => lCanvas.draw(true), 50);
        setTimeout(() => lCanvas.draw(true), 150);
        setTimeout(() => lCanvas.draw(true), 300);

        console.log(`成功重建节点: ${graph._nodes.length}, 链接: ${graph.links.length}`);
        resize();
    } catch (e) {
        console.error(e);
        alert("加载失败，请查看控制台(F12)");
    }
}

// --- 工作流保存功能 ---
// --- 工作流保存功能 ---
// --- 工作流保存功能 ---
async function saveWorkflow() {
    const filenameInput = document.getElementById("filename");
    const filename = filenameInput.value.trim();

    if (!filename) {
        alert("请输入文件名");
        filenameInput.focus();
        return;
    }

    try {
        // 构建工作流数据
        const workflowData = {
            last_node_id: Math.max(...graph._nodes.map(n => n.id || 0), 0),
            last_link_id: 0,
            nodes: [],
            links: {}
        };

        // 收集节点数据
        graph._nodes.forEach((node, index) => {
            const nodeData = {
                id: node.id || index + 1,
                type: node.type,
                pos: node.pos,
                title: node.title || node.type,
                properties: node.properties || {}
            };
            workflowData.nodes.push(nodeData);
        });

        // 收集链接数据
        let maxLinkId = 0;
        if (graph.links && typeof graph.links === 'object') {
            Object.keys(graph.links).forEach(linkId => {
                const link = graph.links[linkId];
                if (link && link.origin_id && link.target_id) {
                    const id = parseInt(linkId);
                    workflowData.links[linkId] = {
                        id: id,
                        origin_id: link.origin_id,
                        origin_slot: link.origin_slot,
                        target_id: link.target_id,
                        target_slot: link.target_slot,
                        type: link.type || "default"
                    };
                    maxLinkId = Math.max(maxLinkId, id);
                }
            });
        }
        workflowData.last_link_id = maxLinkId;

        console.log("保存的工作流数据:", workflowData);

        // 发送保存请求，确保使用UTF-8编码
        const response = await fetch(`/api/save/${encodeURIComponent(filename)}.json`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
            },
            body: JSON.stringify(workflowData)
        });

        if (response.ok) {
            // 确保响应使用UTF-8解码
            const responseText = await response.text();
            let result;
            try {
                result = JSON.parse(responseText);
            } catch (e) {
                // 如果JSON解析失败，尝试手动解析
                console.warn("JSON解析失败，尝试手动处理响应:", responseText);
                result = { filename: filename + '.json' };
            }

            // 使用中文提示，确保浏览器使用UTF-8编码
            alert(`工作流保存成功: ${result.filename || filename + '.json'}`);

            // 刷新文件列表
            await updateFileList();
        } else {
            const errorText = await response.text();
            throw new Error(`保存失败: ${errorText}`);
        }
    } catch (e) {
        console.error(e);
        // 使用英文提示避免乱码
        alert(`Save failed: ${e.message}`);
    }
}

// --- 更新文件列表 ---
async function updateFileList() {
    try {
        const res = await fetch('/api/list');
        const files = await res.json();
        document.getElementById("fileList").innerHTML = files.map(f => `<option value="${f}">${f}</option>`).join('');
    } catch (e) {
        console.error("更新文件列表失败:", e);
    }
}

// --- 响应式布局 ---
function resize() {
    const dpr = window.devicePixelRatio || 1;
    const container = document.getElementById("canvas_container");
    if (container && canvasElement) {
        canvasElement.width = container.clientWidth * dpr;
        canvasElement.height = container.clientHeight * dpr;
        if (lCanvas && lCanvas.ds) {
            lCanvas.ds.scale = dpr;
            lCanvas.draw(true);
        }
    }
}

// --- 初始化应用 ---
async function init() {
    try {
        await updateFileList();
        resize();
    } catch (e) {
        console.error("初始化失败:", e);
        document.getElementById("fileList").innerHTML = '<option>加载失败</option>';
    }
}

// --- 事件监听 ---
window.addEventListener('resize', resize);

// --- 启动应用 ---
graph.start();
init();