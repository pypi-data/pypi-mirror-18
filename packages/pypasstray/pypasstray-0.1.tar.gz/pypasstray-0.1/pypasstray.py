#!/usr/bin/env python
from gi.repository import Gtk, GObject

import sys
import subprocess
import os
import json
import re

# class Indicator is copied from https://github.com/sorrowless/battery_systray/

class Indicator:
    """
    This class defines the standard GTK3 system tray indicator.
    """
    def __init__(self, icon):
        self.appicon = icon
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_file(self.appicon)

        self.menu = Gtk.Menu()
        self.icon.connect('popup-menu', self.right_click_event_statusicon)

    def set_refresh(self, timeout, callback, *callback_args):
        """
        A stub to simplify setting timeout.
        Args:
          timeout (int): timeout in milliseconds, after which callback will be called
          callback (callable): usually, just a function that will be called each time after timeout
          *callback_args (any type): arguments that will be passed to callback function
        """
        GObject.timeout_add(timeout, callback, *callback_args)

    def set_icon(self, icon):
        self.icon.set_from_file(icon)

    # create a menu out of a tree
    def create_menu(self, pt, path):
	root_menu = Gtk.Menu()

	for k, v in pt.tree.iteritems():
	    menu_item = Gtk.MenuItem(k)
	    file_path = path + k

	    if len(v.tree) > 0:
	        menu_item.set_submenu(self.create_menu(v, file_path + "/"))
	    else:
	        menu_item.connect('activate',lambda x: subprocess.call(["pass", file_path, "-c"]))

	    root_menu.append(menu_item)

	root_menu.show_all()
	self.menu = root_menu

	return root_menu

    def add_menu_item(self, command, title):
        m_item = Gtk.MenuItem(title)
        m_item.connect('activate', command)
        self.menu.append(m_item)
        self.menu.show_all()

    def add_separator(self):
        m_item = Gtk.SeparatorMenuItem()
        self.menu.append(m_item)
        self.menu.show_all()

    def right_click_event_statusicon(self, icon, button, time):

        def pos(menu, aicon):
            return Gtk.StatusIcon.position_menu(menu, aicon)

        self.menu.popup(None, None, pos, icon, button, time)


class PathTree:

    def __init__(self):
        self.tree={}

    def add(self,path):
        if len(path) > 0:
           if path[0] in self.tree:
                self.tree[path[0]].add(path[1:])
           else:
                self.tree[path[0]]=PathTree()
                self.tree[path[0]].add(path[1:])


class Application:

    def populate_menu_items(self):
        root_path = os.path.expanduser("~") + "/.password-store/"
        pt = PathTree()

        for dirpath, dirnames, filenames in os.walk(root_path):
            for name in filenames:
                if name.endswith(".gpg"):
		    abs_path = os.path.join(dirpath, name)
		    rel_path = abs_path.replace(root_path, "").replace(".gpg", "")
		    list = rel_path.split("/")
		    pt.add(list)

	self.indicator.create_menu(pt,"")
	self.indicator.add_menu_item(lambda x: Gtk.main_quit(), "Quit")
	return True

    def __init__(self):
        self.deficon = "lock.png"
        self.indicator = Indicator(self.deficon)
        self.populate_menu_items()

	#check for new and removed entries every 15 seconds
        self.indicator.set_refresh(15*1000, self.populate_menu_items)
        self.indicator.icon.set_has_tooltip(True)
        self.indicator.icon.connect("query-tooltip", self.tooltip_query)

    def tooltip_query(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_text("pass")
        return True

def main():
    Application()
    Gtk.main()

if __name__ == '__main__':
    main()
