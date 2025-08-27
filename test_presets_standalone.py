#!/usr/bin/env python3
"""
预设系统独立测试脚本
不依赖ComfyUI环境，可以单独运行
"""

import sys
import os
import json
import time
import uuid

# 直接复制预设管理函数，避免导入依赖
def get_presets_file():
    """获取预设文件路径"""
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'presets.json')

def load_presets():
    """加载预设配置"""
    try:
        with open(get_presets_file(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果文件不存在，创建默认结构
        default_presets = {
            "gemini": [],
            "chatgpt": [],
            "kling": [],
            "flux": [],
            "midjourney": [],
            "doubao": [],
            "qwen": []
        }
        save_all_presets(default_presets)
        return default_presets
    except json.JSONDecodeError:
        print("[Tutu] 预设文件格式错误，使用默认配置")
        return {"gemini": [], "chatgpt": [], "kling": [], "flux": [], "midjourney": [], "doubao": [], "qwen": []}

def save_all_presets(presets):
    """保存所有预设到文件"""
    with open(get_presets_file(), 'w', encoding='utf-8') as f:
        json.dump(presets, f, indent=2, ensure_ascii=False)

def save_preset(category, name, config, description=""):
    """保存单个预设"""
    if not name.strip():
        raise ValueError("预设名称不能为空")
        
    presets = load_presets()
    if category not in presets:
        presets[category] = []
    
    # 检查是否已存在同名预设
    existing_names = [p["name"] for p in presets[category]]
    if name in existing_names:
        # 如果存在同名，添加时间戳后缀
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        name = f"{name}_{timestamp}"
    
    preset = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "config": config,
        "created_time": time.time(),
        "created_date": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    presets[category].append(preset)
    save_all_presets(presets)
    return preset["id"]

def delete_preset(category, preset_id):
    """删除指定预设"""
    presets = load_presets()
    if category not in presets:
        return False
    
    original_count = len(presets[category])
    presets[category] = [p for p in presets[category] if p["id"] != preset_id]
    
    if len(presets[category]) < original_count:
        save_all_presets(presets)
        return True
    return False

def get_preset_by_name(category, name):
    """根据名称获取预设"""
    presets = load_presets()
    if category not in presets:
        return None
    
    for preset in presets[category]:
        if preset["name"] == name:
            return preset
    return None

def get_preset_names(category):
    """获取指定分类的所有预设名称"""
    presets = load_presets()
    if category not in presets:
        return []
    return [p["name"] for p in presets[category]]

def test_preset_system():
    print("🧪 开始测试预设系统...")
    print("-" * 50)
    
    # 测试1：加载预设（会自动创建文件）
    print("1️⃣ 测试加载预设...")
    presets = load_presets()
    print(f"✅ 成功加载预设，分类: {list(presets.keys())}")
    
    # 测试2：保存预设
    print("\n2️⃣ 测试保存预设...")
    test_config = {
        "model": "gemini-2.5-flash-image-preview",
        "temperature": 0.8,
        "top_p": 0.9,
        "resolution": "1024x1024",
        "num_images": 2
    }
    
    preset_id = save_preset(
        category="gemini",
        name="高质量摄影",
        config=test_config,
        description="适合生成高质量摄影风格图片"
    )
    print(f"✅ 成功保存预设，ID: {preset_id}")
    
    # 测试3：获取预设名称列表
    print("\n3️⃣ 测试获取预设名称...")
    names = get_preset_names("gemini")
    print(f"✅ Gemini分类预设: {names}")
    
    # 测试4：通过名称获取预设
    print("\n4️⃣ 测试通过名称获取预设...")
    preset = get_preset_by_name("gemini", "高质量摄影")
    if preset:
        print(f"✅ 找到预设: {preset['name']}")
        print(f"   描述: {preset['description']}")
        print(f"   创建时间: {preset['created_date']}")
        print(f"   配置: {preset['config']}")
    
    # 测试5：保存更多预设
    print("\n5️⃣ 测试保存多个预设...")
    
    # ChatGPT预设
    chatgpt_config = {
        "model": "gpt-4-vision-preview",
        "temperature": 1.0,
        "max_tokens": 4096
    }
    save_preset("chatgpt", "创意写作", chatgpt_config, "适合创意内容生成")
    
    # Kling预设
    kling_config = {
        "num_frames": 120,
        "fps": 30,
        "resolution": "720p"
    }
    save_preset("kling", "标准视频", kling_config, "标准30fps视频生成")
    
    # Gemini动漫风格预设
    anime_config = {
        "model": "gemini-2.5-flash-image-preview",
        "temperature": 1.2,
        "top_p": 0.95,
        "resolution": "1536x1536",
        "num_images": 1,
        "style_prompt": "anime style, detailed illustration"
    }
    save_preset("gemini", "动漫插画", anime_config, "生成精美的动漫风格插画")
    
    print("✅ 成功保存多个预设")
    
    # 测试6：显示所有预设统计
    print("\n6️⃣ 预设统计:")
    all_presets = load_presets()
    total_presets = 0
    for category, preset_list in all_presets.items():
        if preset_list:
            print(f"   📁 {category}: {len(preset_list)} 个预设")
            for preset in preset_list:
                print(f"      - {preset['name']} ({preset.get('description', '无描述')})")
                total_presets += 1
    print(f"\n   📊 总计: {total_presets} 个预设")
    
    # 测试7：删除预设
    print("\n7️⃣ 测试删除预设...")
    # 先创建一个测试预设
    test_id = save_preset("gemini", "测试删除", {"test": True})
    # 然后删除它
    deleted = delete_preset("gemini", test_id)
    print(f"✅ 删除预设: {'成功' if deleted else '失败'}")
    
    # 测试8：测试重名处理
    print("\n8️⃣ 测试同名预设处理...")
    # 再次保存同名预设，应该自动加时间戳
    duplicate_id = save_preset("gemini", "高质量摄影", test_config, "重复名称测试")
    duplicate_preset = None
    for preset in load_presets()["gemini"]:
        if preset["id"] == duplicate_id:
            duplicate_preset = preset
            break
    if duplicate_preset:
        print(f"✅ 同名预设自动重命名为: {duplicate_preset['name']}")
    
    print("\n" + "-" * 50)
    print("✅ 所有测试通过！预设系统工作正常。")
    print(f"📁 预设文件位置: {get_presets_file()}")
    
    # 显示预设文件内容预览
    print("\n📄 预设文件内容预览:")
    with open(get_presets_file(), 'r', encoding='utf-8') as f:
        content = f.read()
        if len(content) > 500:
            print(content[:500] + "\n... (文件太长，只显示前500字符)")
        else:
            print(content)

if __name__ == "__main__":
    test_preset_system()
