import os
import glob
import shutil
import asyncio

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from telethon import TelegramClient, events

API_ID = 2040
API_HASH = 'b18441a1ed609e120130348a49019a21'

class SessionCheckerApp(App):
    def build(self):
        self.client = None
        self.loop = asyncio.get_event_loop()

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        header = Label(
            text="[b]SESSION CHECKER v1.0[/b]\n[size=12]Kivy Android Edition[/size]",
            markup=True,
            size_hint_y=0.12,
            halign='center'
        )
        root.add_widget(header)

        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        scan_btn = Button(text="🔄 Сканировать память", background_color=(0.2, 0.6, 1, 1))
        scan_btn.bind(on_press=self.scan_sessions)
        btn_layout.add_widget(scan_btn)

        stop_btn = Button(text="🛑 Остановить", background_color=(1, 0.3, 0.3, 1))
        stop_btn.bind(on_press=self.stop_checker)
        btn_layout.add_widget(stop_btn)

        root.add_widget(btn_layout)

        self.log_input = TextInput(
            readonly=True, 
            multiline=True, 
            size_hint_y=0.5,
            hint_text="Здесь будут отображаться логи и входящие коды..."
        )
        root.add_widget(self.log_input)

        self.sessions_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.sessions_container.bind(minimum_height=self.sessions_container.setter('height'))
        
        scroll = ScrollView(size_hint_y=0.28)
        scroll.add_widget(self.sessions_container)
        root.add_widget(scroll)

        self.scan_sessions()

        return root

    def log(self, text):
        def _update(dt):
            self.log_input.text += text + "\n"
        Clock.schedule_once(_update)

    def collect_all_sessions(self):
        search_paths = [
            "/sdcard/Download/",
            "/sdcard/Download/AyuGram/",
            "/sdcard/Download/Telegram/",
            "/sdcard/Telegram/Telegram Documents/",
            "/sdcard/Android/data/com.exteragram.messenger/files/Telegram/Telegram Documents/"
        ]
        for path in search_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith('.session'):
                        src = os.path.join(path, file)
                        dst = os.path.join(".", file)
                        try:
                            shutil.copy(src, dst)
                        except Exception:
                            pass

    def scan_sessions(self, instance=None):
        self.log_input.text = ""
        self.log("[*] Поиск .session файлов...")
        self.collect_all_sessions()
        
        files = glob.glob("*.session")
        sessions = [os.path.splitext(f)[0] for f in files]

        self.sessions_container.clear_widgets()

        if not sessions:
            self.log("[❌] Файлы .session не найдены в папках!")
            return

        self.log(f"[✅] Найдено сессий: {len(sessions)}. Выберите сессию снизу:")

        for sess in sessions:
            btn = Button(text=f"📄 {sess}.session", size_hint_y=None, height=45)
            btn.bind(on_press=lambda inst, s=sess: self.start_checker(s))
            self.sessions_container.add_widget(btn)

    def start_checker(self, session_name):
        self.log(f"\n[*] Запуск проверки для: {session_name}.session")
        self.loop.create_task(self.run_telethon(session_name))

    async def run_telethon(self, session_name):
        try:
            if self.client and self.client.is_connected():
                await self.client.disconnect()

            self.client = TelegramClient(session_name, API_ID, API_HASH)

            @self.client.on(events.NewMessage(chats=777000))
            async def handler(event):
                self.log("\n========================================")
                self.log(" [!] ВХОДЯЩИЙ КОД АВТОРИЗАЦИИ:")
                self.log(event.message.text)
                self.log("========================================\n")

            await asyncio.wait_for(self.client.connect(), timeout=10.0)

            if not await self.client.is_user_authorized():
                self.log(f"[❌] СЕССИЯ НЕАКТИВНА: '{session_name}.session' сброшена.")
                await self.client.disconnect()
                return

            me = await self.client.get_me()
            self.log("[✅] СЕССИЯ УСПЕШНО АКТИВИРОВАНА!")
            self.log(f" ├─ Имя: {me.first_name} {me.last_name or ''}")
            self.log(f" ├─ ID: {me.id}")
            self.log(f" └─ Телефон: +{me.phone}" if me.phone else " └─ Телефон: Не указан")
            self.log("[ℹ️] Ожидание кода от Telegram (777000)...")

        except Exception as e:
            self.log(f"[❌] Ошибка подключения: {e}")

    def stop_checker(self, instance=None):
        if self.client and self.client.is_connected():
            self.loop.create_task(self.client.disconnect())
            self.log("\n[*] Прослушивание сессии остановлено.")
        else:
            self.log("\n[*] Нет активных подключений.")

if __name__ == '__main__':
    SessionCheckerApp().run()
