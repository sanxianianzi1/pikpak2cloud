      - name: Process and Download
        id: downloading
        run: |
          mkdir -p downloads
          # 从数据库获取链接并保存到文件
          if ! python task.py --opt="query" --con="${{ secrets.DB_CONNECT }}" > input_links.txt 2>error.log; then
            echo "数据库查询失败或没有待处理任务"
            cat error.log
            exit 1
          fi
          
          if [ ! -s input_links.txt ]; then
            echo "没有找到链接"
            exit 1
          fi
          
          # 使用process_links.py处理链接
          if ! python scripts/process_links.py input_links.txt; then
            echo "链接处理失败"
            exit 1
          fi
          
          if [ ! -s urls.txt ]; then
            echo "没有有效的链接"
            exit 1
          fi
          
          # 下载文件
          success=false
          while IFS= read -r url; do
            if [[ -z "$url" ]]; then
              continue
            fi
            if aria2c --seed-time=0 -d downloads -c "$url"; then
              success=true
              break
            fi
          done < urls.txt
          
          if [ "$success" = false ]; then
            echo "所有下载都失败了"
            exit 1
          fi
          
          # 检查是否有文件被下载
          if [ ! "$(ls -A downloads)" ]; then
            echo "下载目录为空"
            exit 1
          fi
          
          filename=$(ls downloads | head -n1)
          echo "filename=$filename" >> $GITHUB_OUTPUT
          echo "path=downloads/$filename" >> $GITHUB_OUTPUT
          size=$(ls -l downloads/$filename | awk '{print $5}' )
          echo "size=$size" >> $GITHUB_OUTPUT
