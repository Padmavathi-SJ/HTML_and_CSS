import os # file handling
import importlib # dynamic import

from core.plugin_base import PluginBase

class PluginLoader:

    def __init__(self, plugin_folder):
        self.plugin_folder = plugin_folder  # folder path
        self.plugins = {} # store plugin instances


    # ===========================
    # STEP 1: DISCOVER PLUGINS
    # ===========================

    def discover(self):
        print("[CORE] Scanning plugin directory:", self.plugin_folder)

        for file in os.listdir(self.plugin_folder): # list files

            if file.endswith(".py") and file != "__init__.py":
                module_name = f"{self.plugin_folder}.{file[:-3]}"

                module = importlib.import_module(module_name) # import file

                    # find plugin class inside module
                for attr in dir(module):
                    obj = getattr(module, attr)

                    if isinstance(obj, type) and issubclass(obj, PluginBase) and obj != PluginBase:
                        plugin_instance = obj()  # create object
                        self.plugins[plugin_instance.name] = plugin_instance

        print(f"[CORE] Discovered {len(self.plugins)} plugins:")
        for name, plugin in self.plugins.items():
            print(f" - {name} v{plugin.version}")
        

    # =============================
    # STEP 2: RESOLVE DEPENDENCIES
    # =============================
    def resolve_dependencies(self):
        print("\n[CORE] Resolving dependencies.....")

        resolved = []
        unresolved = list(self.plugins.keys())

        while unresolved:
            plugin_name = unresolved.pop(0)
            plugin = self.plugins[plugin_name]

            # check dependencies
            if all(dep in resolved for dep in plugin.dependencies):
                print(f"{plugin_name} OK")
                resolved.append(plugin_name)
            else:
                unresolved.append(plugin_name) # try later
            
        return resolved  # activation order
    
    # ==========================
    # STEP 3: ACTIVATE PLUGINS
    # ==========================

    def activate_plugins(self, order):
        print("\n[CORE] Activating plugins.....")

        for i, name in enumerate(order, 1):
            plugin = self.plugins[name]

            print(f"[{i}] {name}.activate()")

            plugin.activate()  # call plugin method


    
