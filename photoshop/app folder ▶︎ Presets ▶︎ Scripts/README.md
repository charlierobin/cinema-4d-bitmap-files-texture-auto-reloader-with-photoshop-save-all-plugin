# Adobe Photoshop 2020 “Save All” Plugin Command

Uses `var isEvent = (arguments.length > 0 && arguments[0] != null)` to decide if it’s being called from an event, or called directly from a menu/keyboard shortcut.

If from an event, Photoshop adds `arguments` specifying the kind of event. Check out `IsBeginSaveEvent( arguments[0] )` in the script `Save Extra JPEG.jsx` in your local Photoshop app presets:

`Adobe Photoshop 2020 ▶︎ Presets ▶︎ Scripts ▶︎ Event Scripts Only ▶︎ Save Extra JPEG.jsx`

Saves the currently active document, ie: front most active image being edited (`var origActive = app.activeDocument`). Why? You’ll see…

Then loops through all the user’s documents.

```
for (var i = 0; i < app.documents.length; i++) {
   var doc = app.documents[i];
```
        
If document has never been saved (no `doc.fullName`), skips it. (`doc.fullName` would in fact be the full path.)

If `isEvent`, also skips the `origActive` document, as Photoshop will take care of saving that.

`if (isEvent && doc == origActive) continue`

If not `isEvent`, ie: a menu command, we need to do all of them, including `origActive`.

For the actual save, we need to first activate the document. (You can’t just `save()` on any document!)

```
if (hasPath && !doc.saved) {

   app.activeDocument = doc;

   try {
      app.activeDocument.save();
   }
   catch (e) {
      errorsSaving = errorsSaving + doc.name + ": " + e.message + "\n";
   }
}
```

Then onto the next document in the collection.

At the end, we have a `finally`, restoring the original `app.activeDocument`.

That’s basically it, all wrapped in a few `try` blocks to hopefully catch the most likely problems and handle them (stop, log, proceed, alert) sensibly.

Because (in up to Photoshop 2020) you can’t disable individual event triggers (only all or none), at some point an `enabled` preference was added, with a simple dialog box for editing that pref. (And then, later, the floating window slider.)

Therefore this `enabled` only applies when `isEvent == true`.

When called from NOT an event, ie: as a menu command, `enabled` is ignored.

(Like I said elsewhere, I think if I was starting this from scratch, I would just refuse to do that. But it seemed like an idea at the time.)

`function getSaveAllEnabled()` shows how to get the saved global pref from the Photoshop registry. The code for the dialog box also shows how to `set`. The code for the floating panel also shows `get` and `set`. The dialog box also shows how to emit a custom `pref changed event` which the floating panel registers a listener for, and reacts to by updating the slider toggle UI.

In that sense, the floating window UI was really more about me just learning a few basics at the time.

https://www.smashingmagazine.com/2013/07/introduction-to-photoshop-scripting/

https://github.com/Adobe-CEP/CEP-Resources/blob/master/Documentation/Product%20specific%20Documentation/Photoshop%20Scripting/photoshop-scripting-guide-2020.pdf

I think the last time all of this was ever used in anger for any great amount of time by a great many users was 2019 or so, hence the “last“ version of Photoshop listed being 2020 (21.2.5). I know I’ve continued to use it all on my Mac (Catalina 10.15.7), but I don’t have any idea what happens with any of this stuff with newer versions.

