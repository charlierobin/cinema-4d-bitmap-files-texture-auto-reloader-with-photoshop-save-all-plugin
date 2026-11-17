# Cinema 4D 2023 Automatic Texture Updater/Reloader Plugin

When you set the plug in running, it launches a Cinema 4D thread…

https://developers.maxon.net/docs/py/2023_2/modules/c4d.threading/index.html

… which then periodically (every few seconds, look in `constants.py` for `CHECK_INTERVAL`) schedules a special C4D event:

https://developers.maxon.net/docs/py/2023_2/modules/c4d/index.html?highlight=specialeventadd#c4d.SpecialEventAdd

Back in the main thread, when this event is detected (command plugin with ID `TIMER_MESSAGE_DELEGATE` in `constants.py`, `class TextureAutoReloadMessage ▶︎ def CoreMessage`), `test()` is run.

That’s where the projects assets are interrogated and enumerated:

```
assets = []

result = c4d.documents.GetAllAssetsNew( doc, False, "", c4d.ASSETDATA_FLAG_TEXTURESONLY, assets )
```

https://developers.maxon.net/docs/py/2023_2/modules/c4d.documents/index.html?highlight=c4d.documents.getallassetsnew#c4d.documents.GetAllAssetsNew

If it’s the first time an external file has been encountered, its date/time modified is stored in the global dictionary `g_Data`. If it’s already in `g_Data`, the last mod date is compared with the current one, and if it’s been modified by an external app, it’s scheduled for reload (`modifiedShaders`). Then the modified date/time is updated.

For each shader in modifiedShaders, we mark for updating/reloading with `c4d.CallButton( shader, c4d.BITMAPSHADER_RELOADIMAGE )`:

https://developers.maxon.net/docs/py/2023_2/modules/c4d/index.html?highlight=c4d.callbutton#c4d.CallButton

Look in `lib.py` for the periodic timer thread code. At the time it was done in a way designed to allow for the code being reused for other timer functions. In the end, I don’t think that ever happened, but then my memory is dim…

The rest of the code is simple enough, mostly checking to make sure we don’t end up with multiple events being scheduled all on top of each other (if the test takes longer than the timer period interval) via `self.eventLock = threading.Lock()` etc, and of course some other basic error checking.

It’s not perfect, but it seems to have worked pretty well over all of these years. For me, at least. Maybe other people will get some mileage out of it.

 
