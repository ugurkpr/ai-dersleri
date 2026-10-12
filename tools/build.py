#!/usr/bin/env python3
"""Build the no-account (static) version of "AI Dersleri Sınıfı".

usage: python3 build.py <template.html> <lessons_dir> <outline.json> <out_dir>
  template.html  page source with the marker  /*__LOCAL__*/null  where the data goes
  lessons_dir    folder of lesson JSON files (dNN.json) exported from the artifact database
  outline.json   course outline document
  out_dir        where index.html is written (img/ is expected to be there already)
"""
import json, os, sys, glob, datetime

MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def main():
    tpl, ldir, outline_p, out = sys.argv[1:5]
    lessons = []
    for f in sorted(glob.glob(os.path.join(ldir, "d*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        d.pop("__name__", None)
        if d.get("n"):
            lessons.append(d)
    lessons.sort(key=lambda d: int(d["n"]))
    outline = json.load(open(outline_p, encoding="utf-8"))
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)  # Istanbul
    built = f"{now.day} {MONTHS[now.month - 1]} {now.year} {now:%H:%M}"
    data = json.dumps({"lessons": lessons, "outline": outline, "built": built}, ensure_ascii=False)
    data = data.replace("</", "<\\/")
    html = open(tpl, encoding="utf-8").read()
    assert "/*__LOCAL__*/null" in html, "marker missing"
    html = html.replace("/*__LOCAL__*/null", data, 1)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    print(f"built {len(lessons)} lessons, {len(html)//1024} KB, {built}")


if __name__ == "__main__":
    main()
