# Cinema 4D 2023 Texture Reloader Plugin

A simple Cinema 4D Python plugin that runs a “test” routine every few seconds (via C4D threading) which checks to see if any of the bitmap files referred to in your project’s materials have been modified (by an external application – in my case, Photoshop, always Photoshop).

It skips any unsaved documents, as this was the behaviour I and everyone else in the studio wanted.

There’s no real interface: you just turn it on, it runs until (1) you quit, (2) you turn it off, or (3) you reload your plugins or (4) there’s an error (check the Cinema 4D Python console if you suspect this).

https://github.com/user-attachments/assets/8548e425-e8de-44c4-b13b-6a4f7501205a

Tracking data is stored as a simple dictionary: the key is the full path to the bitmap file, the data is the file’s last modification date/time.

Every few seconds, the plugin queries your project’s assets, gets paths, looks at them on disk and compares modification dates with the stored last known one. If there has been a change, it reloads that bitmap. (It doesn’t warn about any bitmaps which are missing. That’s for you to sort out via `Window` ▶︎ `Project Asset Inspector`, or similar.)

Because there’s no effort to track which files are no longer being referenced/tracked (the plugin doesn’t remove data when you close a project or switch to another one), the data dictionary slowly gets bigger and bigger: depending, obviously, on how many projects you open throughout your session and how many bitmaps they reference.

So the only slight concession to housekeeping is a “Clear data” command, which simply resets the data set to empty. The next periodic execution of the test routine therefore starts from scratch, with nothing to compare against.

I think we found that nobody ever really used this. Even on fairly bitmap heavy projects, in relative terms the size of the data never got THAT big, even at the end of a day’s work. (Compared to the size of everything else that was being wrangled. It is, after all, just a bunch of strings and numbers.)

## Installation

Put the TextureAutoReload into `your-cinema4d-app-folder ▶︎ plugins` folder, and launch (or restart) Cinema 4D. (Simply reloading plugins won’t do it. I think.)

# Bonus: Adobe Photoshop 2020 “Save All” Plugin Command

Another simple scripted plugin that adds a “Save All” command to Adobe Photoshop.

Again, the UI is very simple: a preference to indicating whether or not “Save All” is enabled. Note that this preference ONLY applies when the plugin is being run from a Photoshop event trigger. If you’re running directly from the `scripts` menu, or via a menu with an attached keyboard shortcut, it ALWAYS runs.

The script runs though all your open Photoshop documents, and saves them all. It skips any unsaved documents, ie: ones that have not yet been modified, or ones that have been modified but not yet saved for the first time to disk.

## Installation

### Script Plugins

The three script files go into your Photoshop install’s `▶︎ Presets ▶︎ Scripts` directory. (Possibly there are other shared common install locations they could go? I never bothered investigating, I must admit.) Photoshop has to be restarted.

### Floating Palette Panel

If you want this as well, you need to put the `SaveAllPanel` folder into your `~Library ▶︎ Application Support ▶︎ Adobe ▶︎ CEP ▶︎ extensions` directory. (Again, there are possibly other places just as good. Again, I never bothered checking it out. I’m a bit lazy that way…) If running, Photoshop must be restarted.

The palette sets the same global preference that the script dialog box sets, ie: setting it in one place should be reflected in the other.

Note that this enabled preference ONLY works when you’re using the script triggered via `Photoshop ▶︎ File ▶︎ Scripts ▶︎ Script Event Manager…`. This is because there’s no way (in 2020 at least) to disabled individual Photoshop event triggers. But if/when you run the script as a menu command (with a keyboard shortcut, for instance) it ALWAYS runs, regardless of whether or not this preference is enabled.

<img width="338" height="232" alt="Screenshot 2026-11-14 at 11 02 11" src="https://github.com/user-attachments/assets/ba2fdaf3-a974-4028-9602-74d43fa9de2d" />

# Nota Bene

In both cases, I wrote and fine-tuned these things to specifically cater for the way I found myself working when using Cinema 4D with Photoshop.

I just got so fed up working on multiple bits of artwork in Photoshop, having to save them all individually (usually forgetting a few and then having to go back to them), and then switching to Cinema 4D to hit `Reload Textures`, and then switching back to Photoshop, repeating ad nauseam all day long. A fellow has better things to do with his time…

So you might well find some aspects of them here and there a bit idiosyncratic, but that’s likely down to it just being the way I liked it. I didn’t really write them as “general purpose” products for outside distribution.

I just wanted to be able to have Cinema 4D in the background, viewport/render visible, with my Photoshop windows on top, to be able to paint in any of the windows, hit `Save` ONCE, and have the background update automatically.

## A few thoughts about the Photoshop Save All Extension

<img width="1251" height="1511" alt="Screenshot 2026-11-14 at 11 01 46" src="https://github.com/user-attachments/assets/91b95a44-99fa-4ddb-a190-61af7a5c52db" />

This is a weird one, as I wrote it for myself, used it happily for years, and then other people saw it and I found myself catering for two slightly different scenarios:

(1) people in the studio who wanted to have “save all” trigger when they saved any of their open documents, and didn’t want to mess around with keyboard shortcuts (ie: moving command S from “Save” to the Scripts menu item).

<img width="1338" height="824" alt="Screenshot 2026-11-14 at 10 59 42" src="https://github.com/user-attachments/assets/a38af7d0-fd62-4b4c-95d3-349809e562c9" />

(2) people who didn’t want the save all happening automatically when they hit command S, but wanted it on its own dedicated shortcut. (Which usually turned out to be control command S, as that was the only vaguely intuitive one remaining free, all the others already occupied by existing Photoshop menu items.)

<img width="2324" height="2034" alt="Screenshot 2026-11-14 at 11 11 16" src="https://github.com/user-attachments/assets/a8fd7a7c-41e6-47cb-b7c5-d3fa29f1e1c4" />

If I had my druthers, I’d probably not be so accommodating again. But I don’t have my druthers. They went missing decades ago. I think they might be at the bottom of the sock drawer. That or the dog or the cat ate them.

<img width="200" height="200" alt="Screenshot 2026-11-14 at 13 29 01" src="https://github.com/user-attachments/assets/7f6abb6e-f139-45bf-8596-1c22d3327147" /> <img width="200" height="200" alt="Screenshot 2026-11-14 at 13 16 26" src="https://github.com/user-attachments/assets/aa5512d9-66a5-4fb7-b590-a429c692f536" />



