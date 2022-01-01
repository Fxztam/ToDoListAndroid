import random

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

from datetime import datetime
from jsonfile import json_processing as json
from string import ascii_letters
from text import *
from threading import Thread
from widgets import *


__version__ = "1.0.0"

if platform != "android":
    Window.size=(400,600)

#DEFINE
FLOATBTN_ADDTASKICON = "calendar-edit"
FLOATBTN_MARKICON = "calendar-check"
FLOATBTN_UNMARKICON = "calendar-blank"
FLOATBTN_DELETEICON = "trash-can-outline"

MENU_SETTING = "Setting"
MENU_SAVE = "Save"
MENU_EXIT = "Exit"

ICON_ALLPRIORITY = "image/all_priority.png"
ICON_lOWPRIORITY = "image/low_priority.png"
ICON_MEDIUMPRIORITY = "image/medium_priority.png"
ICON_HIGHPRIORITY = "image/high_priority.png"
ALL_PRIORITY = "all"
LOW_PRIORITY = "low"
MEDIUM_PRIORITY = "med"
HIGH_PRIORITY = "high"

INDEX_ICON = 0
INDEX_PANELTEXT = 1
INDEX_PANELDUETEXT = 2
INDEX_MARKDONE = 3

SAVEFILE = "task.json"
#END_OF_DEFINE

def GENERATE_ID():
    sample = ascii_letters+"1234567890"
    return "".join(random.choice(sample) for i in range(15))

class MainScreen(Screen):
    pass

class MainApp(MDApp):
    tasks = {}

    about_dialog = None
    edit_task_dialog = None
    dialog = None

    float_button_data = {
            "Add Task" : FLOATBTN_ADDTASKICON,
            "Mark All" : FLOATBTN_MARKICON,
            "Unmark All" : FLOATBTN_UNMARKICON,
            "Delete All" : FLOATBTN_DELETEICON
        }

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.title = "ToDo List"
        self.screen = MainScreen()
        return self.screen 
    def on_start(self):
        self.task_list = self.screen.ids.task_list_parent
        self.float_button = self.screen.ids.float_button

        self.tasks = json.load_json(SAVEFILE)

        self.on_start_create_navdrawpriorityicon()
        self.on_start_create_menu()

        self.show_task_priority(ALL_PRIORITY,True)
    def on_stop(self):
        self.save_task_to_file()
    
    #On Start Func
    def on_start_create_navdrawpriorityicon(self):
        self.screen.ids.nav_list.add_widget(NavDrawPriorityIcon(
                icon=ICON_ALLPRIORITY,
                text="All Priority",
                text_color=self.theme_cls.primary_color,
                on_release=lambda x:self.show_task_priority(ALL_PRIORITY))
        )
        self.screen.ids.nav_list.add_widget(NavDrawPriorityIcon(
                icon=ICON_lOWPRIORITY,
                text="Low Priority",
                text_color=self.theme_cls.text_color,
                on_release=lambda x:self.show_task_priority(LOW_PRIORITY))
        )
        self.screen.ids.nav_list.add_widget(NavDrawPriorityIcon(
                icon=ICON_MEDIUMPRIORITY,
                text="Medium Priority",
                text_color=self.theme_cls.text_color,
                on_release=lambda x:self.show_task_priority(MEDIUM_PRIORITY))
        )
        self.screen.ids.nav_list.add_widget(NavDrawPriorityIcon(
                icon=ICON_HIGHPRIORITY,
                text="High Priority",
                text_color=self.theme_cls.text_color,
                on_release=lambda x:self.show_task_priority(HIGH_PRIORITY))
        )
    def on_start_create_menu(self):
        menu_text = [MENU_SETTING, MENU_SAVE, MENU_EXIT]
        menu_items = [
            {
                "viewclass":"OneLineListItem",
                "text":f"{i}",
                "height":dp(36),
                "on_release": lambda x=i:self.select_menu(x) 
            } for i in menu_text
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4
        )

    #Menu Func
    def menu_callback(self, button):
        self.menu.caller = button
        self.menu.open()
    def select_menu(self, menu_item):
        self.menu.dismiss()
        if menu_item == MENU_SETTING:
            pass
        elif menu_item == MENU_SAVE:
            self.save_task_to_file()
            self.show_snackbar("Saved.")
        elif menu_item == MENU_EXIT:
            self.stop()

    #Task Func
    def edit_task(self, priority, panel_text, panel_due_text, instance):
        pass 
    def save_task_to_file(self,savefile=SAVEFILE):
        json.save_json(self.tasks, savefile)
    def add_task(self, icon, panel_text, panel_due_text, mark=False, _id=None):
        _icon_tag = icon
        if icon == LOW_PRIORITY: icon = ICON_lOWPRIORITY
        elif icon == MEDIUM_PRIORITY: icon = ICON_MEDIUMPRIORITY
        else: icon = ICON_HIGHPRIORITY
        
        if mark: 
            panel_text = st_text(panel_text)
            _checkbox_status = True
        else:
            panel_text = st_text(panel_text,st=False)
            _checkbox_status = False
        if not _id: 
            _id = GENERATE_ID()

        self.task_list.add_widget(
            TaskList(
                id=_id,
                icon=icon,
                content=TaskListContent(checkbox_status=_checkbox_status),
                panel_cls=TaskListPanel(text=panel_text,
                                        secondary_text=panel_due_text
                 )
              )
           )

        task_data = [_icon_tag, panel_text, panel_due_text, mark]
        self.tasks[_id] = task_data
    def delete_task(self, instance):
        self.task_list.remove_widget(instance)
        self.tasks.pop(instance.id)
    def delete_all_task(self):
        self.task_list.clear_widgets()
        self.tasks.clear()
        self.show_snackbar("All tasks have been deleted", .55)
    def mark_done_task(self, checkbox, value):
        try:
            _parent = checkbox.parent.parent.parent.parent
            parent_panelcls_text = _parent.panel_cls.text
            if value:
                _parent.panel_cls.text = st_text(parent_panelcls_text)
            else:
                _parent.panel_cls.text = st_text(parent_panelcls_text,st=False)
            
            self.tasks[_parent.id][INDEX_MARKDONE] = value
        except:
            pass
    def mark_done_task_all(self):
        for task in self.task_list.children:
           task.content.ids.checkbox.active = True
           task.panel_cls.text = st_text(task.panel_cls.text)
           self.tasks[task.id][INDEX_MARKDONE] = True
        self.show_snackbar("All tasks have been marked as done.", .5)
    def unmark_task_all(self):
        for task in self.task_list.children:
           task.content.ids.checkbox.active = False
           task.panel_cls.text = st_text(task.panel_cls.text, st=False)
           self.tasks[task.id][INDEX_MARKDONE] = False  
        self.show_snackbar("All tasks have been unmarked", .5)
    def float_button_callback(self, instance):
        if instance.icon == FLOATBTN_ADDTASKICON: self.show_add_task_dialog()
        elif instance.icon == FLOATBTN_MARKICON: self.mark_done_task_all()
        elif instance.icon == FLOATBTN_UNMARKICON:self.unmark_task_all()
        elif instance.icon == FLOATBTN_DELETEICON: self.delete_all_task()

        self.float_button.close_stack()

    #Add Task Dialog Func
    def show_add_task_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="ADD TASK",
                type="custom",
                content_cls=DialogContent(),
                size_hint=(.975,None)
            )
        self.dialog.content_cls.ids.task_text.text = ""
        self.dialog.open()
    def close_add_task_dialog(self):
        self.dialog.dismiss()
    def on_priority_checkbox(self, checkbox, value):
        if value: checkbox.parent.parent.priority = checkbox.priority

    #Edit Task Dialog Func
    def show_edit_task_dialog(self, instance):
        if not self.edit_task_dialog:
            self.edit_task_dialog = MDDialog(
                title="IN PROGRESS...",
                type="custom",
                content_cls=EditDialogContent(),
                size_hint=(.975,None)
            )
        self.edit_task_dialog.open()
    def close_edit_task_dialog(self):
        self.edit_task_dialog.dismiss()
    
    #About Dialog Func
    def show_about_dialog(self):
        if not self.about_dialog:
            self.about_dialog = MDDialog(
                title=f"{self.title} {__version__}",
                type="simple",
                text="Created by Aghnat HS \nusing Python, Kivy and KivyMD",
                buttons=[
                    MDRaisedButton(
                        text="Close",
                        md_bg_color=self.theme_cls.primary_dark,
                        on_release=lambda x:self.close_about_dialog()
                    )
                ],
                size_hint=(.975,None)
            )
        self.about_dialog.open()
    def close_about_dialog(self):
        self.about_dialog.dismiss()
    #Show Tasks by Priority
    def show_task_priority(self,priority=LOW_PRIORITY, on_start=False):
        self.task_list.clear_widgets()
        for id in self.tasks.keys():
            _icon = self.tasks[id][INDEX_ICON]
            _paneltext = self.tasks[id][INDEX_PANELTEXT]
            _panelduetext = self.tasks[id][INDEX_PANELDUETEXT]
            _markdone = self.tasks[id][INDEX_MARKDONE]

            if priority == ALL_PRIORITY:
                self.add_task(_icon, _paneltext, _panelduetext, _markdone, id)
            else:
                if _icon == priority:
                    self.add_task(_icon, _paneltext, _panelduetext, _markdone, id)
                else: pass
        if not on_start:
            if priority == ALL_PRIORITY: self.show_snackbar("Showing all priority.")
            elif priority == LOW_PRIORITY: self.show_snackbar("Showing low priority only.")
            elif priority == MEDIUM_PRIORITY: self.show_snackbar("Showing medium priority only.")
            elif priority == HIGH_PRIORITY: self.show_snackbar("Showing high priority only.")
        else:
            pass
    
    #Other
    def show_snackbar(self, text="", duration=.35):
        Snackbar(
                duration=duration,
                text=text, 
                snackbar_x=dp(20),
                snackbar_y=dp(10), 
                size_hint_x=(Window.width - (dp(20) * 2)) / Window.width
            ).open()
App = MainApp()
App.run()
        
