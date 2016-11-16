from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import kivy
from kivy.uix.anchorlayout import AnchorLayout

class MyApp(App):
    def build(self):
        return TopLeftButtons()


class TopLeftButtons(AnchorLayout):
    def __init__(self, **kwargs):
        super(TopLeftButtons, self).__init__(**kwargs)
        AnchorLayout(anchor_x="left", anchor_y="top")
        ButtonFrame("<", "up", ">")

class ButtonFrame(GridLayout, text1, text2, text3):
    def __init__(self, **kwargs):
        super(ButtonFrame, self).__init__(**kwargs)

        self.cols = 3
        self.back = Button(text=text1)
        self.up = Button(text=text2)
        self.forward = Button(text=text3)

        self.add_widget(self.back)
        self.add_widget(self.up)
        self.add_widget(self.forward)



if __name__ == '__main__':
    MyApp().run()
