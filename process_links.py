import re
import sys

def process_links(input_links):
    # 删除指定的前缀
    cleaned_links = re.sub(r'https://pikpak\d\.sanxianianzi\d*\.ggff\.net/', '', input_links)

    # 分割链接并过滤掉空行
    links = [link.strip() for link in cleaned_links.split('https://vod-jo-') if link.strip()]

    # 添加前缀并准备输出
    formatted_links = [f'https://vod-jo-{link}' for link in links]

    return formatted_links

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("Usage: python process_links.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as file:
            input_links = file.read()

        # 处理链接
        formatted_links = process_links(input_links)

        # 写入结果到urls.txt
        with open('urls.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(formatted_links))

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing links: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
