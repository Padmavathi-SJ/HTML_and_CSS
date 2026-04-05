from core.loader import PluginLoader # import loader

print("=== Application Startup ===")

# create loader object
loader = PluginLoader("plugins")

# step 1: discover plugins
loader.discover()

# step 2: resolve dependency order
order = loader.resolve_dependencies()

# step 3: activate plugins
loader.activate_plugins(order)