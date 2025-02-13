import re
import sys

def process_links(input_links):
    """处理输入链接"""
    try:
        # 移除可能的前缀
        cleaned_links = input_links.replace('https://vod-jo-https://pikpak', 'https://pikpak')
        
        # 分割多个链接（如果有的话）
        links = [link.strip() for link in cleaned_links.split('\n') if link.strip()]
        
        # 处理每个链接
        formatted_links = []
        for link in links:
            if '##' in link:
                url, filename = link.split('##')
                # 确保URL格式正确
                if url.startswith('https://pikpak'):
                    url = url.replace('https://pikpak', 'https://vod-jo-https://pikpak')
                    formatted_links.append(f"{url}##{filename}")
        
        return formatted_links
    except Exception as e:
        print(f"Error processing links: {str(e)}", file=sys.stderr)
        return []

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("Usage: python process_links.py <input_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_links = file.read()
        
        formatted_links = process_links(input_links)
        if not formatted_links:
            print("No valid links found after processing", file=sys.stderr)
            sys.exit(1)
            
        with open('urls.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(formatted_links))
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
