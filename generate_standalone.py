#!/usr/bin/env python3
"""将 screenshots 目录下的 PNG 图片转换为 Base64 并生成独立 HTML 文件"""

import base64
import os
from pathlib import Path

# 配置
SCREENSHOTS_DIR = Path.home() / "tmp" / "wukong-app-screenshots" / "screenshots"
OUTPUT_HTML = Path.home() / "tmp" / "wukong-app-screenshots" / "standalone.html"

# 图片列表（按顺序）
IMAGES = [
    ("01-enterprise-ai-platform.png", "企业级AI平台架构", "钉钉+悟空的AI原生之路，展示Agent智能平台的分层架构与核心组件"),
    ("02-wukong-vs-aily.png", "钉钉悟空 vs 飞书Aily", "五层企业级治理体系、OPT行业场景能力、AI操控能力等多维度对比"),
    ("03-ai-listening-vs-miaoji.png", "钉钉AI听记 vs 飞书妙记", "语音智能、AI生成纪要、录制互动、安全管控等核心功能对比"),
    ("04-ai-vs-recording-bean.png", "钉钉AI vs 飞书录音豆", "硬件参数、语音智能、AI纪要分析、企业级能力全方位对比"),
    ("05-ai-tables-vs-multidimensional.png", "钉钉AI表格 vs 飞书多维表格", "AI字段处理、电商生态、低代码联动、自动化流程等深度对比"),
    ("06-docs-vs-feishu-docs.png", "钉钉文档 vs 飞书文档", "Office兼容、编辑体验、协同协作、知识库归档等核心能力对比"),
    ("07-yida-vs-lowcode.png", "钉钉宜搭 vs 飞书低代码", "企业级保障、生态闭环、表单流程落地效率等产品演示对比"),
    ("08-teambition-vs-meego.png", "钉钉Teambition vs 飞书Meego", "安全部署、底座生态融合、私有化与混合云支持对比"),
    ("09-security-comparison.png", "钉钉专属安全 vs 飞书安全", "安全运营中心、权限管控、DLP防泄漏、终端网络安全全面对比"),
    ("10-mail-comparison.png", "阿里企业邮箱 vs 飞书邮箱", "独立协同融合、安全合规、存储容量、管理后台、AI能力全球化对比"),
]

def image_to_base64(image_path):
    """将图片转换为 Base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_html():
    """生成包含 Base64 图片的独立 HTML 文件"""
    
    # 转换所有图片为 Base64
    images_data = []
    for idx, (filename, title, description) in enumerate(IMAGES, 1):
        image_path = SCREENSHOTS_DIR / filename
        if not image_path.exists():
            print(f"️  警告: 图片不存在 - {filename}")
            continue
        
        base64_str = image_to_base64(image_path)
        file_size = image_path.stat().st_size
        images_data.append({
            "index": idx,
            "filename": filename,
            "title": title,
            "description": description,
            "base64": base64_str,
            "size_mb": file_size / (1024 * 1024)
        })
        print(f"✅ 已转换: {filename} ({file_size / 1024:.1f} KB)")
    
    total_size = sum(img["size_mb"] for img in images_data)
    print(f"\n📊 总图片大小: {total_size:.2f} MB")
    
    # 生成 HTML
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>钉钉 vs 飞书 - 产品能力对比</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #e0e6ed;
            min-height: 100vh;
            line-height: 1.6;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 40px 20px; }}
        header {{
            text-align: center;
            margin-bottom: 60px;
            padding: 40px 0;
            border-bottom: 2px solid rgba(0, 120, 255, 0.3);
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #0078ff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }}
        .subtitle {{ font-size: 1.1rem; color: #8b9dc3; max-width: 600px; margin: 0 auto; }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }}
        .card {{
            background: rgba(20, 25, 50, 0.8);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid rgba(0, 120, 255, 0.2);
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 48px rgba(0, 120, 255, 0.2);
        }}
        .card-image {{ width: 100%; height: auto; display: block; cursor: pointer; }}
        .card-content {{ padding: 20px; }}
        .card-number {{
            display: inline-block;
            background: linear-gradient(135deg, #0078ff, #00d4ff);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .card-title {{ font-size: 1.2rem; font-weight: 600; color: #ffffff; margin-bottom: 8px; }}
        .card-description {{ font-size: 0.9rem; color: #8b9dc3; line-height: 1.5; }}
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            animation: fadeIn 0.3s ease;
        }}
        .modal.active {{ display: flex; justify-content: center; align-items: center; }}
        .modal-content {{ max-width: 90%; max-height: 90%; position: relative; }}
        .modal-img {{
            max-width: 100%;
            max-height: 90vh;
            border-radius: 8px;
            box-shadow: 0 0 50px rgba(0, 120, 255, 0.3);
        }}
        .close-btn {{
            position: absolute;
            top: -40px;
            right: 0;
            color: white;
            font-size: 2.5rem;
            cursor: pointer;
            transition: color 0.3s ease;
        }}
        .close-btn:hover {{ color: #0078ff; }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        footer {{
            text-align: center;
            margin-top: 60px;
            padding: 30px 0;
            border-top: 1px solid rgba(0, 120, 255, 0.2);
            color: #8b9dc3;
            font-size: 0.9rem;
        }}
        .info-box {{
            background: rgba(0, 120, 255, 0.1);
            border-left: 4px solid #0078ff;
            padding: 15px 20px;
            margin-bottom: 30px;
            border-radius: 4px;
        }}
        .info-box p {{ margin: 5px 0; font-size: 0.9rem; }}
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.8rem; }}
            .gallery {{ grid-template-columns: 1fr; gap: 20px; }}
            .container {{ padding: 20px 15px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>钉钉 vs 飞书</h1>
            <p class="subtitle">企业级产品核心能力差异化对比 · 10大维度深度解析</p>
        </header>
        
        <div class="info-box">
            <p>💡 <strong>使用说明：</strong>点击图片可全屏查看高清原图，按 ESC 键或点击 × 关闭</p>
            <p>📦 <strong>文件大小：</strong>本页面已内嵌所有图片，无需网络连接，可直接发送给客户</p>
        </div>
        
        <div class="gallery">
'''
    
    # 添加图片卡片
    for img in images_data:
        html_content += f'''
            <div class="card">
                <img src="data:image/png;base64,{img['base64']}" 
                     alt="{img['title']}" 
                     class="card-image"
                     onclick="openModal(this.src)">
                <div class="card-content">
                    <span class="card-number">{img['index']:02d}</span>
                    <h3 class="card-title">{img['title']}</h3>
                    <p class="card-description">{img['description']}</p>
                </div>
            </div>
'''
    
    html_content += '''
        </div>
        
        <footer>
            <p>© 2026 钉钉 vs 飞书产品对比 | 内部培训材料 · 仅供参考</p>
            <p style="margin-top: 10px; font-size: 0.85rem;">独立HTML文件 · 无需网络即可查看</p>
        </footer>
    </div>
    
    <div id="imageModal" class="modal" onclick="closeModal()">
        <div class="modal-content">
            <span class="close-btn">&times;</span>
            <img id="modalImg" class="modal-img" src="" alt="">
        </div>
    </div>
    
    <script>
        function openModal(src) {
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImg');
            modal.classList.add('active');
            modalImg.src = src;
            document.body.style.overflow = 'hidden';
        }
        
        function closeModal() {
            const modal = document.getElementById('imageModal');
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
    </script>
</body>
</html>
'''
    
    # 写入文件
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = OUTPUT_HTML.stat().st_size
    print(f"\n✅ HTML 文件已生成: {OUTPUT_HTML}")
    print(f"📊 文件大小: {file_size / (1024*1024):.2f} MB")
    print(f"\n💡 提示: 此文件可直接双击打开，或通过微信/邮件发送给客户")

if __name__ == "__main__":
    generate_html()
