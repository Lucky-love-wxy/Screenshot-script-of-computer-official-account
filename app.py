import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import time
import json
from datetime import datetime

# === 尝试导入你的截图脚本 ===
try:
    # 假设你的脚本叫 gzh.py，里面有 save_wechat_article_as_image 函数
    from gzh import save_wechat_article_as_image
except ImportError:
    print("⚠️ 未找到 gzh.py，请确保它和本程序在同一目录下！")
    # 为了防止报错导致界面打不开，这里定义一个空函数做测试
    def save_wechat_article_as_image(url, path):
        time.sleep(2) # 模拟耗时
        print(f"模拟下载: {url} -> {path}")

CONFIG_FILE = "config.json"

class WechatDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("公众号文章自动截图工具")
        self.root.geometry("600x450")
        
        # 加载上次保存的配置
        self.config = self.load_config()
        self.default_save_path = self.config.get("save_path", os.getcwd())

        # === 界面布局 ===
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. 标题
        lbl_title = ttk.Label(main_frame, text="微信文章转长图工具", font=("微软雅黑", 16, "bold"))
        lbl_title.pack(pady=(0, 20))

        # 2. 文章链接输入区
        lbl_url = ttk.Label(main_frame, text="文章链接 (URL):", font=("微软雅黑", 10))
        lbl_url.pack(anchor=tk.W)
        
        self.url_entry = ttk.Entry(main_frame, width=50, font=("Consolas", 10))
        self.url_entry.pack(fill=tk.X, pady=(5, 15))
        
        # 3. 保存位置设置区
        lbl_path = ttk.Label(main_frame, text="保存位置:", font=("微软雅黑", 10))
        lbl_path.pack(anchor=tk.W)

        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(5, 15))

        self.path_var = tk.StringVar(value=self.default_save_path)
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, state="readonly")
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_browse = ttk.Button(path_frame, text="选择文件夹...", command=self.choose_directory)
        btn_browse.pack(side=tk.RIGHT, padx=(10, 0))

        # 4. 状态显示
        self.status_var = tk.StringVar(value="准备就绪")
        self.lbl_status = ttk.Label(main_frame, textvariable=self.status_var, foreground="gray")
        self.lbl_status.pack(pady=(0, 10))

        # 5. 操作按钮
        self.btn_start = ttk.Button(main_frame, text="开始截图", command=self.start_thread)
        self.btn_start.pack(ipady=10, fill=tk.X)

        # 底部版权
        ttk.Label(main_frame, text="Powered by Python & Playwright", font=("Arial", 8), foreground="#ccc").pack(side=tk.BOTTOM, pady=10)

    def load_config(self):
        """读取配置文件"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {}

    def save_config(self):
        """保存配置文件"""
        config = {"save_path": self.path_var.get()}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f)

    def choose_directory(self):
        """打开文件夹选择框"""
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.path_var.set(selected_path)
            self.save_config() # 记住这个选择

    def start_thread(self):
        """启动后台线程防止界面卡死"""
        url = self.url_entry.get().strip()
        save_dir = self.path_var.get()

        if not url:
            messagebox.showwarning("提示", "请先粘贴文章链接！")
            return
        if not save_dir:
            messagebox.showwarning("提示", "请选择保存位置！")
            return

        # 禁用按钮防止重复点击
        self.btn_start.config(state="disabled")
        self.status_var.set("正在初始化浏览器，请稍候...")
        
        # 开启新线程运行任务
        thread = threading.Thread(target=self.run_task, args=(url, save_dir))
        thread.daemon = True # 设为守护线程，主程序关闭时它也关闭
        thread.start()

    def run_task(self, url, save_dir):
        """实际执行截图逻辑"""
        try:
            # 生成文件名 (使用当前时间戳)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"article_{timestamp}.png"
            full_path = os.path.join(save_dir, filename)

            self.status_var.set(f"正在加载页面并截图... (这可能需要几秒钟)")
            
            # === 调用你的核心脚本 ===
            save_wechat_article_as_image(url, full_path)
            # ======================

            self.status_var.set(f"✅ 成功！已保存至: {filename}")
            messagebox.showinfo("完成", f"截图成功！\n文件已保存至：\n{full_path}")

        except Exception as e:
            self.status_var.set(f"❌ 发生错误")
            messagebox.showerror("错误", f"截图失败：\n{str(e)}")
        finally:
            # 恢复按钮状态 (需要用 root.after 确保在主线程更新 UI)
            self.root.after(0, lambda: self.btn_start.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    # 设置一下图标（如果有的话），没有就跳过
    # root.iconbitmap("icon.ico") 
    app = WechatDownloaderApp(root)
    root.mainloop()