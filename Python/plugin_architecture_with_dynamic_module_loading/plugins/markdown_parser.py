from core.plugin_base import PluginBase # import base class

# Plugin class
class MarkdownParser(PluginBase):

    name = "markdown-parser"
    version = "2.1.0"
    dependencies = []  # no dependencies

    def activate(self):
        print("-> Registered: Markdown -> HTML converter")

    
    def deactivate(self):
        print("Markdown parser stopped")