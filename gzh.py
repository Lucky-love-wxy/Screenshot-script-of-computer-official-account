import time
from playwright.sync_api import sync_playwright

def save_wechat_article_as_image(article_url, output_path="article_long.png"):
    """
    将微信公众号文章保存为长截图
    """
    with sync_playwright() as p:
        # 1. 启动浏览器 (headless=True 表示不显示界面，后台运行)
        browser = p.chromium.launch(headless=True)
        # 模拟手机或桌面设备，这里设为桌面宽度，方便阅读
        context = browser.new_context(viewport={'width': 800, 'height': 800})
        page = context.new_page()

        print(f"正在加载文章: {article_url}")
        page.goto(article_url)

        # 2. 核心关键：处理图片懒加载 (Lazy Loading)
        # 微信文章的图片不会一次性加载，必须滚动视窗才会显示
        print("正在滚动页面以加载图片...")
        page.evaluate("""
            async () => {
                await new Promise((resolve, reject) => {
                    var totalHeight = 0;
                    var distance = 100;
                    var timer = setInterval(() => {
                        var scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        
                        // 如果滚到底部了
                        if(totalHeight >= scrollHeight){
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100); // 每100毫秒滚一次，模拟人眼浏览速度
                });
            }
        """)
        
        # 滚动完后，稍微等待一下，确保最后一张图加载完成
        time.sleep(2)

        # 3. 净化页面 (可选)
        # 通过 JS 移除底部的“写留言”、“阅读原文”或顶部的关注栏，让截图更干净
        # 下面是一个示例，移除微信底部的某些固定栏（根据需要调整）
        page.evaluate("""
            // 隐藏底部的“在看/点赞”工具栏 (如果有)
            var footer = document.getElementById('js_pc_qr_code');
            if (footer) { footer.style.display = 'none'; }
            
            // 也可以隐藏底部的广告 iframe
            var ads = document.getElementsByClassName('ad_area');
            for(var i=0; i<ads.length; i++){ ads[i].style.display = 'none'; }
        """)

        # 4. 执行全页长截图
        print("正在截图...")
        page.screenshot(path=output_path, full_page=True)
        
        print(f"保存成功：{output_path}")
        browser.close()

# --- 测试运行 ---
if __name__ == "__main__":
    # 替换为你想要测试的微信文章链接
    test_url = "https://mp.weixin.qq.com/s/5swKUtlxvxBTuoTWSJKSrg" 
    
    # 注意：文件名最好加上时间戳避免覆盖
    filename = f"wechat_article_{int(time.time())}.png"
    
    try:
        save_wechat_article_as_image(test_url, filename)
    except Exception as e:
        print(f"发生错误: {e}")