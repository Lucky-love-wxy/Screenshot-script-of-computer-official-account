# 微信公众号文章自动长截图工具

这是一个基于 Python 和 Playwright 的桌面工具，可以自动将微信公众号文章保存为包含完整排版的长截图。

## 功能特点
- 自动处理图片懒加载，确保截图完整。
- 支持 Windows 界面操作，带记忆功能。
- 去除多余的顶部和底部无关元素。

## 如何使用 (如果你懂编程)
1. 下载本项目代码。
2. 安装依赖：
   ```bash
   pip install playwright
   playwright install chromium
   ```
3. 运行程序：
   ```
   python app.py
   ```

## 如何使用 (如果你不懂编程)
请点击右侧 "Releases" 下载打包好的 `.exe` 文件，双击即可直接使用，无需安装 Python。


3.  点击底部的绿色按钮 **Commit changes**。


如果你的电脑上没有 `playwright` 库。标准的做法是提供一个清单。

1.  在 GitHub 页面点击 Add file -> Create new file。
2.  文件名填写：`requirements.txt`
3.  内容填写：
    ```text
    playwright
    tk
    ```
4.  提交保存。
