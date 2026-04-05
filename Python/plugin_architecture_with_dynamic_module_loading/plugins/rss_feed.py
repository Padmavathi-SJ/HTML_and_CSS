from core.plugin_base import PluginBase

class RSSFeed(PluginBase):

    name = "rss-feed"
    version = "1.0.0"

    # depends on markdown-parser
    dependencies = ["markdown-parser"]

    def activate(self):
        print("-> Registered: RSS generator")

    def deactivate(self):
        print("RSS disabled")