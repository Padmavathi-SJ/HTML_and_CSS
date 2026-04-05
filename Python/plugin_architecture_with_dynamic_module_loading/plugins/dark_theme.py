from core.plugin_base import PluginBase

class DarkTheme(PluginBase):

    name = "dark-mode-theme"
    version = "1.3.2"
    dependencies = []

    def activate(self):
        print("-> Registered: Theme 'dark-mode'")
    
    def deactivate(self):
        print("Dark theme removed")