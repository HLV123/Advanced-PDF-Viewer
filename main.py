import os
import fitz
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.graphics.texture import Texture
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

Window.size = (400, 620)

class DocumentScrollArea(ScrollView):
    from kivy.properties import NumericProperty
    scale_factor = NumericProperty(1.0)
    min_scale = 0.3
    max_scale = 4.0
    scale_increment = 0.15

    def enlarge_content(self):
        if self.scale_factor < self.max_scale:
            self.scale_factor += self.scale_increment
            self.update_display_size()

    def shrink_content(self):
        if self.scale_factor > self.min_scale:
            self.scale_factor -= self.scale_increment
            self.update_display_size()

    def reset_scale(self):
        self.scale_factor = 0.8
        self.update_display_size()

    def update_display_size(self):
        if hasattr(self, 'content') and self.content:
            page_widget = self.content
            if page_widget.texture:
                page_widget.size = (page_widget.texture.width * self.scale_factor,
                                   page_widget.texture.height * self.scale_factor)
                page_widget.size_hint = (None, None)

class PageRenderer(Image):
    pass

class DigitalDocumentReader(MDApp):
    active_file = StringProperty("")
    night_mode = BooleanProperty(False)
    zoom_percentage = StringProperty("100%")
    document_history = ListProperty([])
    current_page_num = NumericProperty(0)
    total_page_count = NumericProperty(0)
    pdf_handler = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.browser_opened = False
        self.file_explorer = MDFileManager(
            exit_manager=self.close_browser, 
            select_path=self.process_selection
        )

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.title = "Advanced Document Viewer"
        self.load_history()
        return Builder.load_file("redesigned_interface.kv")

    def on_start(self):
        self.root.ids.content_area.content = self.root.ids.page_viewer

    def get_drives(self):
        drive_list = []
        if platform == "win":
            import string
            for letter in string.ascii_uppercase:
                path = f"{letter}:\\"
                if os.path.exists(path):
                    drive_list.append(path)
        else:
            drive_list = ["/"]
        return drive_list

    def open_browser(self, *args):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE])
            start_dir = os.path.expanduser("~")
        else:
            self.show_drive_dialog()
            return
        
        self.file_explorer.show(start_dir)
        self.browser_opened = True

    def show_drive_dialog(self):
        drives = self.get_drives()
        
        if not drives:
            self.show_error("No drives found!")
            return
        
        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        from kivymd.uix.label import MDLabel
        content.add_widget(MDLabel(
            text="Select Drive:",
            size_hint_y=None,
            height="45dp",
            theme_text_color="Primary",
            font_style="H6"
        ))
        
        for drive in drives:
            try:
                if platform == "win":
                    import shutil
                    total, used, free = shutil.disk_usage(drive)
                    free_gb = free // (1024**3)
                    total_gb = total // (1024**3)
                    label = f"Drive {drive} ({free_gb}GB free / {total_gb}GB)"
                else:
                    label = drive
            except:
                label = drive
            
            from kivymd.uix.button import MDRaisedButton
            btn = MDRaisedButton(
                text=label,
                size_hint_y=None,
                height="45dp",
                md_bg_color="#6A1B9A",
                theme_text_color="Custom",
                text_color="white",
                on_release=lambda x, p=drive: self.select_drive(p)
            )
            content.add_widget(btn)
        
        self.drive_dialog = MDDialog(
            title="Select Drive",
            type="custom",
            content_cls=content,
            size_hint=(0.85, 0.65),
            md_bg_color="#F3E5F5"
        )
        self.drive_dialog.open()

    def select_drive(self, drive):
        self.drive_dialog.dismiss()
        self.file_explorer.show(drive)
        self.browser_opened = True

    def process_selection(self, path):
        self.close_browser()
        if path.endswith('.pdf'):
            self.load_document(path)
            self.add_to_history(path)
        else:
            self.show_error("Please select a PDF file")

    def close_browser(self, *args):
        self.file_explorer.close()

    def load_document(self, path):
        try:
            if self.pdf_handler:
                self.pdf_handler.close()

            self.pdf_handler = fitz.open(path)
            self.total_page_count = len(self.pdf_handler)
            self.current_page_num = 1
            self.display_page()

            self.active_file = os.path.basename(path)
            self.root.ids.page_counter.text = f"Page {self.current_page_num}/{self.total_page_count}"

        except Exception as e:
            self.show_error(f"Error loading PDF: {str(e)}")

    def display_page(self):
        if not self.pdf_handler or not (1 <= self.current_page_num <= self.total_page_count):
            return
        try:
            page = self.pdf_handler[self.current_page_num - 1]
            matrix = fitz.Matrix(2.5, 2.5).prerotate(page.rotation)
            pix = page.get_pixmap(matrix=matrix)

            texture = Texture.create(size=(pix.width, pix.height), colorfmt="rgb")
            texture.blit_buffer(pix.samples, colorfmt="rgb", bufferfmt="ubyte")
            texture.flip_vertical()

            self.root.ids.page_viewer.texture = texture
            self.root.ids.page_viewer.size = (
                pix.width * self.root.ids.content_area.scale_factor,
                pix.height * self.root.ids.content_area.scale_factor
            )
            self.root.ids.page_viewer.size_hint = (None, None)
        except Exception as e:
            self.show_error(f"Error displaying page: {str(e)}")

    def next_page(self, *args):
        if self.current_page_num < self.total_page_count:
            self.current_page_num += 1
            self.display_page()
            self.root.ids.page_counter.text = f"Page {self.current_page_num}/{self.total_page_count}"
            self.root.ids.page_slider.value = self.current_page_num

    def prev_page(self, *args):
        if self.current_page_num > 1:
            self.current_page_num -= 1
            self.display_page()
            self.root.ids.page_counter.text = f"Page {self.current_page_num}/{self.total_page_count}"
            self.root.ids.page_slider.value = self.current_page_num

    def jump_to_page(self, instance, value):
        if self.pdf_handler and 1 <= value <= self.total_page_count:
            self.current_page_num = int(value)
            self.display_page()
            self.root.ids.page_counter.text = f"Page {self.current_page_num}/{self.total_page_count}"

    def zoom_in(self, *args):
        self.root.ids.content_area.enlarge_content()
        self.update_zoom_info()

    def zoom_out(self, *args):
        self.root.ids.content_area.shrink_content()
        self.update_zoom_info()

    def reset_zoom(self, *args):
        self.root.ids.content_area.reset_scale()
        self.update_zoom_info()

    def update_zoom_info(self):
        percent = int(self.root.ids.content_area.scale_factor * 100)
        self.zoom_percentage = f"{percent}%"
        self.root.ids.zoom_info.text = self.zoom_percentage

    def toggle_theme(self, *args):
        self.night_mode = not self.night_mode
        self.theme_cls.theme_style = "Dark" if self.night_mode else "Light"

    def show_error(self, message):
        dialog = MDDialog(
            title="Error", 
            text=message, 
            size_hint=(0.8, 0.3),
            md_bg_color="#FFEBEE"
        )
        dialog.open()

    def add_to_history(self, path):
        if path in self.document_history:
            self.document_history.remove(path)
        self.document_history.insert(0, path)
        if len(self.document_history) > 10:
            self.document_history = self.document_history[:10]
        self.save_history()

    def load_history(self):
        try:
            data_dir = self.user_data_dir
            os.makedirs(data_dir, exist_ok=True)
            history_path = os.path.join(data_dir, "history.txt")
            if os.path.exists(history_path):
                with open(history_path, 'r', encoding='utf-8') as f:
                    files = f.read().splitlines()
                    self.document_history = [f for f in files if os.path.exists(f)]
        except:
            self.document_history = []

    def save_history(self):
        try:
            data_dir = self.user_data_dir
            os.makedirs(data_dir, exist_ok=True)
            history_path = os.path.join(data_dir, "history.txt")
            with open(history_path, 'w', encoding='utf-8') as f:
                for path in self.document_history:
                    f.write(path + '\n')
        except:
            pass

if __name__ == "__main__":
    DigitalDocumentReader().run()