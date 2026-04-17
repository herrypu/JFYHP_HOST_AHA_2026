import os

# --- 配置区 ---
OUTPUT_FILE = "repo_analysis_data.txt"
# 定义你想包含的文件后缀，留空则处理所有文本文件
INCLUDE_EXTENSIONS = {'.v', '.sv', '.py', '.c', '.cpp', '.h', '.md', '.json', '.sh'}
# 定义要排除的文件夹
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', 'dist', 'build'}

def pack_repo():
    counter = 0
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk('.'):
            # 过滤掉不需要的目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if INCLUDE_EXTENSIONS and ext not in INCLUDE_EXTENSIONS:
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, '.')
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 使用 XML 风格的标签，这是目前 AI（尤其是 Gemini/Claude）最喜欢的格式
                        outfile.write(f"\n<file path=\"{rel_path}\">\n")
                        outfile.write(content)
                        outfile.write(f"\n</file>\n")
                        counter += 1
                        print(f"已处理: {rel_path}")
                except Exception as e:
                    print(f"跳过二进制或无法读取的文件: {rel_path}")

    print(f"\n完成！已将 {counter} 个文件打包至: {OUTPUT_FILE}")

if __name__ == "__main__":
    pack_repo()