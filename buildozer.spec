[app]
title = My First App
package.name = myfirstapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,telethon,pyaes
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
