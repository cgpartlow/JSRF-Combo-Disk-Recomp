# JSRF launcher

The launcher for the [Jet Set Radio Future recompilation](https://github.com/Miggas/JSRF-Recomp):
downloads the project, builds the game from your `default.xbe`, updates it,
edits `jsrf.ini` and starts the game. Windows and Linux (Steam Deck included).
Nothing has to be installed: it downloads its own tools.

This is a fork of the launcher with support for the **Sega GT + Jet Set Radio
Future combo disc** (see below). It downloads the project from
[Miggas/JSRF-Recomp](https://github.com/Miggas/JSRF-Recomp); the original
launcher and the instructions for playing are on that page.

## Controller

| Button | Does |
|---|---|
| D-pad / left stick | Moves between buttons (the highlighted one has a yellow frame) |
| A | Presses the highlighted button, opens a list, picks from it |
| B | Closes an open list |
| Left / right on a slider | Changes its value |
| Right stick | Scrolls |
| LB / RB | Previous / next tab |
| Start | PLAY |

In the settings lists, up / down go through the whole list and it scrolls along; up from the top of a list goes back to the tabs.

The launcher closes once the game has started.

## The Sega GT + Jet Set Radio Future combo disc

This version of the launcher also works with the game files from the Xbox
combo disc, whose game program is `SegaJSRF.xbe` instead of `default.xbe`.

- Put the game files from **your own disc** in the game folder (`jsrf/`),
  with `SegaJSRF.xbe` in it. Nothing has to be renamed: if there is no
  `default.xbe`, the launcher makes one as a copy of `SegaJSRF.xbe` (the
  original stays). A `default.xbe` that is already there is used as it is.
- **Generate code** looks at which game program is in the folder. For the
  combo disc's `SegaJSRF.xbe` it translates the project's analysis and
  hand-written code to that version's addresses first; for the standard
  `default.xbe` it puts the original files back. Build and Play are the
  same for both.
- The scripts and the address map this needs are built into the launcher
  (`src/overlay_data.inc`) and written into `source/` after each Update and
  before each Generate/Build, so Update does not take them away. The map holds
  only addresses and checksums, no game code.
- Only the combo disc's `SegaJSRF.xbe` and the standard NTSC `default.xbe`
  are recognised. Any other version is refused with a message.
- No game files are included or downloaded: you need your own disc.
- Use **Update** for the project, but not **Update launcher**: it would put
  the official launcher, without combo disc support, in place of this one.

## Updating the launcher

When it opens, the launcher checks for a newer game and a newer launcher; if
there is one, the **Play** tab says so, and clicking that line opens **Update**.
PLAY and Build can be used while it checks.

**Update → Check for updates** also looks for a newer launcher on the
[Releases](https://github.com/Miggas/JSRF-Recomp/releases) page; **Update launcher**
downloads it, puts it in place of this one and starts it. From a terminal:
`jsrf_launcher --self-update`.

## How it decides what to do

- **Update** only downloads the project (nothing when GitHub says it is
  already the newest). The generated code is kept.
- **Generate code** runs only when what it is made from changed: `default.xbe`,
  `jsrf_recomp/analysis`, `jsrf_recomp/tools`, `recomp_manual.c`,
  `xboxrecomp/tools`.
- **Build** runs only when the source, the generated code or the compiler
  changed. It asks for Generate code first when the code is missing or old.
- **Play → Build** does both. **Force Generate/Build** (Debug tab) forces them.

## The Debug tab

`DEBUG_MENU=1` in `launcher.ini` shows it: Force Generate/Build, Download
tools, the checks (generated code, `default.xbe`, the
hard-disk cache), Play stopping after 30 s with a dump, Sample a hang, Trace
one frame, and the whole log.

## Building it

| | |
|---|---|
| Windows 10 / 11 | double-click `build_launcher.bat` → `jsrf_launcher.exe` |
| Linux / Steam Deck | `bash build_launcher.sh` → `jsrf_launcher` |

If the combo disc scripts or the map change, run
`py -3 tools\embed_overlay.py <folder>` first (see the comment at the top of
that script), then build. Nothing else is needed. The first time, the script downloads Zig (the C
compiler, about 80 MB) and SDL2 into `deps/`. On Linux the launcher uses the
system's SDL2 (SteamOS has it).

## Files

| | |
|---|---|
| `src/main.c` | the window: Play, Settings, Build, Update |
| `src/jobs.c` | setting up the tools, building, updating, starting the game, the combo disc's `SegaJSRF.xbe` |
| `src/overlay_data.inc` | the combo disc scripts and address map, built into the launcher (made by `tools/embed_overlay.py`) |
| `tools/embed_overlay.py` | makes `src/overlay_data.inc`; run it before building when a script or the map changes |
| `src/ini.c` | reading and saving `jsrf.ini`, keeping its comments |
| `src/util.c` | files, the log, running programs |
| `src/version.h` | the launcher's version |
| `third_party/nuklear` | [Nuklear](https://github.com/Immediate-Mode-UI/Nuklear), draws the window (public domain / MIT) |
| `third_party/sdl2_linux` | SDL2's configuration header for Linux (zlib) |

## Folders it makes

Next to the launcher:

| | |
|---|---|
| `jsrf/` | your game files (or the folder set in Play), and the built game; made at the first start |
| `source/` | the project, downloaded by Update |
| `tools/` | Python, Zig, CMake, Ninja (about 400 MB) |
| `build/` | the compiler's work files |
| `launcher_log.txt` | the log of the last run (the one before: `launcher_log.txt.old`) |
| `launcher.ini` | the launcher's settings: `BRANCH=test` makes Update download the `test` branch (missing = `main`); `DEBUG_MENU=1` shows the Debug tab |
