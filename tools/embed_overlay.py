#!/usr/bin/env python3
"""Makes src/overlay_data.inc for the launcher from the combo pack files.

Run it before building the launcher, from the launcher's source folder:
    py -3 tools\\embed_overlay.py <folder with jsrf_recomp\\tools\\*.py and
                                   jsrf_recomp\\combo\\combo_map.json>
For example the old overlay folder:
    py -3 tools\\embed_overlay.py C:\\Users\\camer\\Downloads\\jsrf_launcher-windows\\overlay
Only the files listed in FILES are used, so nothing else in that folder can
end up in the launcher.
"""
import os, sys

FILES = [
    "jsrf_recomp/tools/combo_port.py",
    "jsrf_recomp/tools/generate_code.py",
    "jsrf_recomp/tools/make_combo_map.py",
    "jsrf_recomp/tools/xbe_info.py",
    "jsrf_recomp/combo/combo_map.json",
]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "src", "overlay_data.inc")
    parts = ["/* made by tools/embed_overlay.py: do not edit */\n",
             "struct overlay_file { const char *path; const unsigned char *data; size_t len; };\n"]
    for i, rel in enumerate(FILES):
        p = os.path.join(root, *rel.split("/"))
        if not os.path.isfile(p):
            sys.exit("missing: " + p)
        d = open(p, "rb").read()
        body = ",".join(str(b) for b in d) if d else "0"
        parts.append("static const unsigned char ov_%d[] = {%s};\n" % (i, body))
    parts.append("static const struct overlay_file g_overlay[] = {\n")
    for i, rel in enumerate(FILES):
        n = os.path.getsize(os.path.join(root, *rel.split("/")))
        parts.append('    { "%s", ov_%d, %d },\n' % (rel, i, n))
    parts.append("};\n#define OVERLAY_COUNT ((int)(sizeof g_overlay / sizeof g_overlay[0]))\n")
    with open(out, "w", newline="\n") as f:
        f.write("".join(parts))
    print("wrote %s (%d files)" % (out, len(FILES)))


if __name__ == "__main__":
    main()
