import os

# ===== 改成你的真实仓库名 =====
REAL_REPO = "blog-old"
# =============================

OLD = "/你的真实仓库名/"
NEW = f"/{REAL_REPO}/"

changed_files = 0
changed_hits = 0

for root, dirs, files in os.walk("."):
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
            continue
        if OLD in content:
            new_content = content.replace(OLD, NEW)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            changed_files += 1
            changed_hits += content.count(OLD)

print(f"修改文件数: {changed_files}")
print(f"替换路径数: {changed_hits}")