import os
import re

# ===== 改成你的新仓库名 =====
NEW_REPO = "old-blog"
# ============================

PREFIX = f"/{NEW_REPO}/"

# href="/xxx" / src="/xxx"，排除 // 开头的协议相对 URL
attr_pat = re.compile(r'(href|src)="/(?!/)')
# CSS 里的 url(/xxx
css_url_pat = re.compile(r'url\(/(?!/)')

changed_files = 0
changed_hits = 0

for root, dirs, files in os.walk("."):
    # 跳过 .git
    if ".git" in root.split(os.sep):
        continue
    for name in files:
        ext = os.path.splitext(name)[1].lower()
        if ext not in (".html", ".css", ".xml"):
            continue

        path = os.path.join(root, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # 极少数非 UTF-8 文件直接跳过
            continue

        new_content, n1 = attr_pat.subn(r'\1="' + PREFIX, content)
        new_content, n2 = css_url_pat.subn("url(" + PREFIX, new_content)

        if n1 + n2 > 0:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            changed_files += 1
            changed_hits += n1 + n2

print(f"修改文件数: {changed_files}")
print(f"替换路径数: {changed_hits}")