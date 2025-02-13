import re

def process_links(input_links):
    # 删除指定的前缀
    cleaned_links = re.sub(r'https://pikpak\d\.sanxianianzi\d*\.ggff\.net/', '', input_links)

    # 分割链接并过滤掉空行
    links = [link.strip() for link in cleaned_links.split('https://vod-jo-') if link.strip()]

    # 添加前缀并准备输出
    formatted_links = [f'https://vod-jo-{link}' for link in links]

    return formatted_links

def main():
    # 提示用户输入链接
    input_links = input("请输入链接：")

    # 处理链接
    formatted_links = process_links(input_links)

    # 输出到文件
    output_path = r'C:\Users\xiao\Desktop\urls.txt'
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(formatted_links))

    print(f"处理后的链接已写入 {output_path}")

if __name__ == "__main__":
    main()