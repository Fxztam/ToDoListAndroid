#class widgets
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty,StringProperty,ListProperty
from kivymd.theming import ThemableBehavior

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineAvatarListItem, ILeftBodyTouch, MDList
from kivymd.uix.picker import MDDatePicker
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDCheckbox

from datetime import date, datetime

DATE_FORMAT = r"%Y %B %d,%A"

#Add_Task Dialog
class DialogContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #first
        self.ids.date_label.text = str(datetime.now().strftime(DATE_FORMAT))
    
    def show_date_picker(self):
        last_pick = datetime.strptime(self.ids.date_label.text, DATE_FORMAT)
        self.date_dialog = MDDatePicker(
            year=last_pick.year,
            month=last_pick.month,
            day=last_pick.day
        )
        self.date_dialog.bind(on_save=self.on_date_picker_save)
        self.date_dialog.open()
    
    def on_date_picker_save(self, instance, value, date_range):
        date = value.strftime(DATE_FORMAT)
        self.ids.date_label.text = str(date)

#Edit_Task Dialog
class EditDialogContent(BoxLayout):
    pass

#Task List
class TaskDueDate(OneLineAvatarListItem):
    pass
class TaskList(MDExpansionPanel):
    id = StringProperty()
class TaskListPanel(MDExpansionPanelTwoLine):
    pass
class TaskListContent(BoxLayout):
    checkbox_status =BooleanProperty()
class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass
class ScreenTaskList(ScrollView):
    pass

#Nav Draw
class ContentNavigationDrawer(BoxLayout):
    pass
class NavDrawPriorityList(ThemableBehavior,MDList):
    def set_color_item(self, instance):
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance.text_color = self.theme_cls.primary_color
class NavDrawPriorityIcon(OneLineAvatarIconListItem):
    icon = StringProperty()
    text = StringProperty()
    text_color = ListProperty()