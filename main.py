from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivy.uix.label import Label
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from rectangle_service import Rectangle_service
from kivymd.uix.button import MDRaisedButton


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alldata = []
        self.mydialog = None
        self.service = None
        self.on_start_called = False

    def build(self):
        self.screen = Builder.load_file("load.kv")
        if not self.on_start_called:
            self.on_start()
            self.on_start_called=True
        return self.screen
    
    def on_start(self):
        if not self.service:
            self.service = Rectangle_service("dev")
            self.rectangles = self.service.get_all_rectangles()
            for rect in self.rectangles:
                self.add_rectangle_to_screen(rect)
                # self.alldata.append({"len": rect.length, "hei": rect.height, "id": rect.id})

    def addnewrectangle(self, len_value, hei_value):
        if len_value and hei_value:
            new_rect = self.service.create_new_rectangle(len_value,hei_value)
            self.add_rectangle_to_screen(new_rect)

            self.screen.ids.input_len.text = ""
            self.screen.ids.input_hei.text = ""
            
    def add_rectangle_to_screen(self, rectangle):
        item_id = str(rectangle.id)
        self.alldata.append({"len": rectangle.length, "hei": rectangle.height, "id": item_id})

        todo_list = self.screen.ids.todo_list
        todo_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="pencil", on_release=lambda x: self.editbtn(item_id, rectangle.length, rectangle.height)),
                IconRightWidget(icon="delete", on_release=lambda x: self.deletebtn(item_id)),
                id=item_id,
                text=f"Len: {rectangle.length}, Hei: {rectangle.height}"
            )
        )
        

    def editbtn(self, dataid, len_value, hei_value):
        self.editlen = MDTextField(hint_text="update length", mode="fill")
        self.edithei = MDTextField(hint_text="update height", mode="fill")
        self.mylayout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=0.8,
            height=300
        )

        self.mylayout.add_widget(Label(text="edit data"))
        if not self.mydialog:
            self.dialog = MDDialog(
                title="edit data",
                type="custom",
                size_hint=(0.8, None),
                height=300,
                content_cls=self.mylayout,
                buttons=[
                    MDFlatButton(
                        text="save",
                        text_color="red",
                        on_release=lambda x: self.savenow(dataid, self.editlen.text, self.edithei.text)
                    )
                ]
            )
        self.dialog.content_cls.add_widget(self.editlen)
        self.dialog.content_cls.add_widget(self.edithei)
        self.dialog.open()

    def savenow(self, id, newlen, newhei):
        # print(data)
        self.service.update_one_rectangle(id,newlen,newhei)
        self.notif = Snackbar(
            text="success edit",
            font_size=30,
            bg_color=(0, 0, 1, 1)
        )

        self.dialog.dismiss()

        for x in self.alldata:
            if x['id'] == id:
                x['len'] = newlen
                x['hei'] = newhei

                todo_list = self.screen.ids.todo_list
                for child in todo_list.children:
                    if child.id == id:
                        child.text = f"Len: {newlen}, Hei: {newhei}"

                self.notif.open()
                
                
    def deletebtn(self, data):
        self.confirm_dialog = MDDialog(
            text="You shure, you whant to delate?",
            buttons=[
                MDRaisedButton(
                    text="Yes",
                    on_release=lambda x: self.delete_confirm(data)
                ),
                MDRaisedButton(
                    text="Anuluj",
                    on_release=lambda x: self.confirm_dialog.dismiss()
                )
            ]
        )
        self.confirm_dialog.open()

    def delete_confirm(self, id):
        for x in self.alldata:
            if x['id'] == id:
                self.alldata.remove(x)
                self.service.deleta_rectangle(id)
                
                todo_list = self.screen.ids.todo_list
                for child in todo_list.children:
                    if child.id == id:
                        todo_list.remove_widget(child)
        self.confirm_dialog.dismiss()
                       


if __name__ == "__main__":
    MyApp().run()
