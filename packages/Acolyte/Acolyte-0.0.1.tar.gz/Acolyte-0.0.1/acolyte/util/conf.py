"""提供配置加载的工具支持
"""
import imp
import os.path


def load_from_py_module(module_path):
    """从module path加载配置，module中必须包含一个CONFIG变量
       :param module_path: 模块文件路径
    """
    module_name = os.path.split(module_path)[1].split(".")[0]
    config_module = imp.load_source(module_name, module_path)
    config_data = getattr(config_module, "CONFIG")
    globals()["config"] = config_data
    return config_data
