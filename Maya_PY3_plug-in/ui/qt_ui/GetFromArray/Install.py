#coding=gbk
import os
import inspect
import maya.cmds as cmds
import sys
# 获取maya mod 文件夹并写入mod

# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
print(file_path)
def get_maya_mod_path(user_path):
	path = os.environ['MAYA_MODULE_PATH']
	# path = path.split(';')[-1]
	#####################################
	mat_docs_path = os.getenv('MAYA_APP_DIR')
	maya_version = cmds.about(version=True)
	maya_version_path = os.path.join(mat_docs_path, maya_version)
	maya_docs_path_modules = os.path.join(maya_version_path, 'modules')
	file_path = os.path.join(maya_docs_path_modules, 'GetFromArray.mod')
	directory = os.path.dirname(file_path)
	if directory and not os.path.exists(directory):
		os.makedirs(directory, exist_ok=True)
	# print(path)
	directory = os.path.dirname(file_path)
	if directory and not os.path.exists(directory):
		os.makedirs(directory, exist_ok=True)
	path = maya_docs_path_modules
	# print(path)
	####################################
	# 构建完整的文件路径
	full_file_path = path +'/GetFromArray.mod'
	full_file_path = full_file_path.replace("/", "\\")
	# print(full_file_path)
	# 使用open函数创建文件，如果文件不存在则会被创建
	# 'w' 模式表示写入（如果文件已存在则会被覆盖）
	text = ('+ GetFromArray_mod 1.0 ' + user_path +'\n'
			'MAYA_PLUG_IN_PATH +:= \n'
			'MAYA_SCRIPT_PATH +:= ./mel_scripts\n'
			'PYTHONPATH +:= ./python_libs\n')
	with open(full_file_path, 'w') as new_file:
		# 可选：向文件中写入一些初始Python代码
		new_file.write(text)
	# print(full_file_path)
	cmds.pluginInfo(user_path + '/get_from_array.py', edit=1, autoload=True)
	# 目标插件目录（示例路径）
	new_plugin_path = user_path.replace("\\", "/")

	# 获取当前 MAYA_PLUG_IN_PATH 的值
	current_path = os.getenv("MAYA_PLUG_IN_PATH", "")
	# print(current_path)
	path_list = current_path.split(os.pathsep) if current_path else []
	# print(path_list)
	# 添加新路径（避免重复）
	if new_plugin_path not in path_list:
		path_list.append(new_plugin_path)
		updated_path = os.pathsep.join(path_list)
		os.environ["MAYA_PLUG_IN_PATH"] = updated_path  # 更新当前会话环境变量
	# print(path_list)
	# print(f"已添加路径: {new_plugin_path}")
	print('路径文件：', path)
	cmds.loadPlugin('get_from_array')

get_maya_mod_path(file_path)
cmds.warning('已经安装get_from_array节点')