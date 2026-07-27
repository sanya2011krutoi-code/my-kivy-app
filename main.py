from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainApp(App):
    def build(self):
        self.count = 0
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        self.label = Label(text="Счёт: 0", font_size='36sp')
        btn = Button(
            text="Нажми меня!", 
            font_size='24sp', 
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 1, 1)
        )
        btn.bind(on_press=self.increment)

        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def increment(self, instance):
        self.count += 1
        self.label.text = f"Счёт: {self.count}"

if __name__ == '__main__':
    MainApp().run()
