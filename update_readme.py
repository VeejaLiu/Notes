import os

markdown = """<div align="center">
<img src="https://socialify.git.ci/VeejaLiu/Notes/image?font=Bitter&forks=1&issues=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark" alt="Notes" width="640" height="320" />
</div>

# Notes
"""

excludePath = ['venv', '.git', '.idea']

child_path_name_list = []

for f in os.scandir():
    filename = f.name
    if f.is_dir() and filename not in excludePath:
        dirName = f.name
        child_path_name_list.append(dirName)

child_path_name_list.sort()

markdown += f"""## 目前分类\n"""
for child_path_name in child_path_name_list:
    markdown += f"""- {child_path_name}\n"""

markdown += f"""\n"""
markdown += f"""
## 所有文件：
<div style="color:gray">
（此顺序只代表本仓库先后的添加顺序）
</div>

"""

for child_path_name in child_path_name_list:
    markdown += f"""### {child_path_name}\n"""
    child_path = "./" + child_path_name
    file_name_list = []
    for file in os.scandir('./' + child_path_name):
        file_name = file.name
        file_name_list.append(file_name)
    file_name_list.sort()
    for file_name in file_name_list:
        markdown += f"""- {file_name}\n"""
    markdown += f"""\n"""

print(markdown)

with open("README.md", "w") as file:
    file.write(markdown)
