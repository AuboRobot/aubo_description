import os
import re

def replace_tags_in_dae_files(directory):
    # 获取目录中的所有 DAE 文件
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith('.dae'):
                file_path = os.path.join(root, file_name)

                # 读取 DAE 文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 替换标签
                tags = ['author', 'comments', 'keywords', 'revision', 'subject', 'title']
                for tag in tags:
                    pattern = '<{}/>'.format(tag)
                    replace = '<{}></{}>'.format(tag, tag)
                    content = re.sub(pattern, replace, content)

                # 写入修改后的内容到同一文件中
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

                # 打印更改了哪些文件
                print('Modified file:', file_path)

# 调用函数并传入文件夹路径
replace_tags_in_dae_files('meshes')
#replace_tags_in_dae_files('防爆系列')
