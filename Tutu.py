import os
import io
import math
import random
import torch
import requests
import time
import numpy as np
from PIL import Image
from io import BytesIO
import json
import comfy.utils
import re
import aiohttp
import asyncio
import base64
import uuid
import folder_paths
import mimetypes
import cv2
import shutil
from .utils import pil2tensor, tensor2pil
from comfy.utils import common_upscale
from comfy.comfy_types import IO


def get_config():
    try:
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Tutuapi.json')
        with open(config_path, 'r') as f:  
            config = json.load(f)
        return config
    except:
        return {}

def save_config(config):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Tutuapi.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)


# ===== 预设管理系统 =====
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
            "gemini": []
        }
        save_all_presets(default_presets)
        return default_presets
    except json.JSONDecodeError:
        print("[Tutu] 预设文件格式错误，使用默认配置")
        return {"gemini": []}

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

def get_preset_by_id(category, preset_id):
    """根据ID获取预设"""
    presets = load_presets()
    if category not in presets:
        return None
    
    for preset in presets[category]:
        if preset["id"] == preset_id:
            return preset
    return None

def get_preset_names(category):
    """获取指定分类的所有预设名称"""
    presets = load_presets()
    if category not in presets:
        return []
    return [p["name"] for p in presets[category]]

def update_preset(category, preset_id, new_config=None, new_name=None, new_description=None):
    """更新现有预设"""
    presets = load_presets()
    if category not in presets:
        return False
    
    for preset in presets[category]:
        if preset["id"] == preset_id:
            if new_config is not None:
                preset["config"] = new_config
            if new_name is not None:
                preset["name"] = new_name
            if new_description is not None:
                preset["description"] = new_description
            preset["updated_time"] = time.time()
            preset["updated_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            save_all_presets(presets)
            return True
    return False

# ===== 预设管理系统结束 =====

# ===== 基础视频适配器类 =====
class ComflyVideoAdapter:
    def __init__(self, url):
        self.url = url if url else ""
        
    def __str__(self):
        return self.url


############################# Gemini ###########################

class ComflyGeminiAPI:
    @classmethod
    def INPUT_TYPES(cls):
        # 获取Gemini预设列表
        preset_names = ["自定义"] + get_preset_names("gemini")
        
        return {
            "required": {
                "preset": (preset_names, {"default": "自定义"}),
                "prompt": ("STRING", {"multiline": True}),
                "api_provider": (
                    [
                        "ai.comfly.chat",
                        "OpenRouter"
                    ],
                    {"default": "ai.comfly.chat"}
                ),
                "model": (
                    [
                        "[Comfly] gemini-2.5-flash-image-preview",
                        "[Comfly] gemini-2.0-flash-preview-image-generation", 
                        "[OpenRouter] google/gemini-2.5-flash-image-preview"
                    ],
                    {"default": "[Comfly] gemini-2.5-flash-image-preview"}
                ),
                "resolution": (
                    [
                        "512x512",
                        "768x768",
                        "1024x1024",
                        "1280x1280",
                        "1536x1536",
                        "2048x2048",
                        "object_image size",
                        "subject_image size",
                        "scene_image size"
                    ],
                    {"default": "1024x1024"}
                ),
                "num_images": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1}),
                "temperature": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "top_p": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0, "step": 0.01}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647}),
                "timeout": ("INT", {"default": 120, "min": 10, "max": 600, "step": 10}),
            },
            "optional": {
                "comfly_api_key": ("STRING", {"default": "", "placeholder": "ai.comfly.chat API Key (可选，留空则使用配置文件)"}),
                "openrouter_api_key": ("STRING", {"default": "", "placeholder": "OpenRouter API Key (可选，留空则使用配置文件)"}),
                "save_as_preset": ("STRING", {"default": "", "placeholder": "输入预设名称以保存当前配置"}),
                "object_image": ("IMAGE",),  
                "subject_image": ("IMAGE",),
                "scene_image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("generated_images", "response", "image_url")
    FUNCTION = "process"
    CATEGORY = "Tutu/Gemini"

    def __init__(self):
        config = get_config()
        self.comfly_api_key = config.get('comfly_api_key', config.get('api_key', ''))  # 向后兼容
        self.openrouter_api_key = config.get('openrouter_api_key', '')
        self.timeout = 120

    def get_current_api_key(self, api_provider):
        """根据API提供商获取对应的API key"""
        if api_provider == "OpenRouter":
            return self.openrouter_api_key
        else:
            return self.comfly_api_key

    def get_headers(self, api_provider="ai.comfly.chat"):
        current_api_key = self.get_current_api_key(api_provider)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {current_api_key}"
        }
        
        # OpenRouter需要额外的headers
        if api_provider == "OpenRouter":
            headers.update({
                "HTTP-Referer": "https://comfyui.com",
                "X-Title": "ComfyUI Tutu Nano Banana"
            })
        
        print(f"[Tutu DEBUG] Generated headers for {api_provider}: {headers}")
        return headers

    def image_to_base64(self, image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def upload_image(self, image, max_retries=3):
        """上传图像到临时托管服务，支持多个备选服务"""
        
        # 准备图像数据
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)
        
        # 备选上传服务列表（按优先级排序，使用最简单可靠的服务）
        upload_services = [
            {
                "name": "0x0.st",
                "url": "https://0x0.st",
                "method": "POST",
                "files_key": "file", 
                "response_key": "url"
            },
            {
                "name": "tmpfiles.org", 
                "url": "https://tmpfiles.org/api/v1/upload",
                "method": "POST", 
                "files_key": "file",
                "response_key": "data.url"
            },
            {
                "name": "uguu.se",
                "url": "https://uguu.se/upload",
                "method": "POST",
                "files_key": "files[]",
                "response_key": "url"
            },
            {
                "name": "x0.at",
                "url": "https://x0.at",
                "method": "POST",
                "files_key": "file",
                "response_key": "url"
            }
        ]
        
        for service in upload_services:
            for attempt in range(max_retries):
                try:
                    print(f"[Tutu DEBUG] 尝试上传到 {service['name']} (尝试 {attempt + 1}/{max_retries})...")
                    
                    # 重置buffer位置
                    buffered.seek(0)
                    
                    # 准备文件上传
                    files = {service['files_key']: ('image.png', buffered.getvalue(), 'image/png')}
                    
                    # 准备额外数据（如果需要）
                    data = service.get('extra_data', {})
                    
                    # 发送上传请求
                    response = requests.post(
                        service['url'], 
                        files=files,
                        data=data,
                        timeout=30,
                        headers={'User-Agent': 'ComfyUI-Tutu/1.0'}
                    )
                    
                    if response.status_code == 200:
                        # 根据服务类型提取URL
                        if service['name'] in ["0x0.st", "x0.at"]:
                            # 这些服务返回纯文本URL
                            image_url = response.text.strip()
                        elif service['name'] == "uguu.se":
                            # uguu.se 返回JSON数组
                            try:
                                result = response.json()
                                if isinstance(result, list) and len(result) > 0:
                                    image_url = result[0].get('url', '')
                                else:
                                    image_url = result.get('url', '')
                            except:
                                image_url = response.text.strip()
                        else:
                            # 其他服务返回JSON
                            try:
                                result = response.json()
                                if service['name'] == "tmpfiles.org" and 'data' in result:
                                    image_url = result['data'].get('url', '')
                                else:
                                    # 通用解析
                                    keys = service['response_key'].split('.')
                                    image_url = result
                                    for key in keys:
                                        if isinstance(image_url, dict):
                                            image_url = image_url.get(key, '')
                                        else:
                                            image_url = ''
                                            break
                                        if not image_url:
                                            break
                            except Exception as e:
                                print(f"[Tutu DEBUG] JSON解析失败: {str(e)}")
                                # JSON解析失败，尝试纯文本
                                image_url = response.text.strip()
                        
                        if image_url and image_url.startswith('http'):
                            print(f"[Tutu DEBUG] 成功上传到 {service['name']}: {image_url}")
                            return image_url
                        else:
                            print(f"[Tutu DEBUG] {service['name']} 响应格式异常: {result}")
                    else:
                        print(f"[Tutu DEBUG] {service['name']} 上传失败，状态码: {response.status_code}")
                        
                except Exception as e:
                    print(f"[Tutu DEBUG] {service['name']} 上传出错 (尝试 {attempt + 1}): {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(1)  # 等待1秒后重试
                    continue
                    
        # 所有服务都失败，返回None
        print(f"[Tutu DEBUG] 所有上传服务都失败，将使用压缩的base64格式")
        return None

    def process_sse_stream(self, response, api_provider="ai.comfly.chat"):
        """Process Server-Sent Events (SSE) stream from the API with provider-specific handling"""
        accumulated_content = ""
        chunk_count = 0
        raw_response_parts = []
        current_json_buffer = ""
        
        print(f"[Tutu DEBUG] 开始处理SSE流 (API: {api_provider})...")
        
        # Different APIs might have different response structures
        is_comfly = api_provider == "ai.comfly.chat"
        is_openrouter = api_provider == "OpenRouter"
        
        try:
            for line in response.iter_lines(decode_unicode=True, chunk_size=None):
                if line:
                    print(f"[Tutu DEBUG] SSE原始行: {repr(line[:100])}")
                    
                if line and line.startswith('data: '):
                    chunk_count += 1
                    data_content = line[6:]  # Remove 'data: ' prefix
                    
                    print(f"[Tutu DEBUG] 处理第{chunk_count}个数据块...")
                    
                    if data_content.strip() == '[DONE]':
                        print(f"[Tutu DEBUG] 收到结束信号[DONE]")
                        break
                    
                    # 累积可能被分割的JSON数据
                    current_json_buffer += data_content
                    
                    try:
                        # 尝试解析累积的JSON
                        chunk_data = json.loads(current_json_buffer)
                        print(f"[Tutu DEBUG] JSON解析成功: {list(chunk_data.keys())}")
                        
                        # 清空缓冲区，因为JSON解析成功了
                        current_json_buffer = ""
                        
                        # Extract content from the chunk
                        if 'choices' in chunk_data and chunk_data['choices']:
                            choice = chunk_data['choices'][0]
                            print(f"[Tutu DEBUG] 完整Choice结构: {choice}")
                            
                            # 检查delta中的所有字段
                            if 'delta' in choice:
                                delta = choice['delta']
                                print(f"[Tutu DEBUG] Delta所有字段: {list(delta.keys())}")
                                
                                # 检查content字段
                                if 'content' in delta:
                                    content = delta['content']
                                    print(f"[Tutu DEBUG] Delta.content: {repr(content[:200]) if content else 'None/Empty'}")
                                    if content:
                                        # 修复编码问题
                                        try:
                                            if isinstance(content, str):
                                                content = content.encode('latin1').decode('utf-8')
                                        except (UnicodeDecodeError, UnicodeEncodeError):
                                            pass
                                        accumulated_content += content
                                        print(f"[Tutu DEBUG] 添加delta.content: {repr(content[:100])}")
                                
                                # 检查是否有其他包含图片数据的字段
                                for key, value in delta.items():
                                    if key != 'content' and isinstance(value, str):
                                        print(f"[Tutu DEBUG] Delta.{key}: {repr(value[:200]) if len(str(value)) > 200 else repr(value)}")
                                        # 检查是否是图片数据
                                        if 'data:image/' in str(value) or 'base64,' in str(value):
                                            print(f"[Tutu DEBUG] 🎯找到图片数据在delta.{key}中!")
                                            accumulated_content += str(value)
                                            print(f"[Tutu DEBUG] 添加图片数据: {len(str(value))}字符")
                                    
                            # 检查message中的内容
                            elif 'message' in choice:
                                message = choice['message']
                                print(f"[Tutu DEBUG] Message所有字段: {list(message.keys())}")
                                
                                if 'content' in message:
                                    content = message['content']
                                    print(f"[Tutu DEBUG] Message.content: {repr(content[:200]) if content else 'None/Empty'}")
                                    if content:
                                        try:
                                            if isinstance(content, str):
                                                content = content.encode('latin1').decode('utf-8')
                                        except (UnicodeDecodeError, UnicodeEncodeError):
                                            pass
                                        accumulated_content += content
                                        print(f"[Tutu DEBUG] 添加message.content: {repr(content[:100])}")
                                
                                # 检查message中的其他字段
                                for key, value in message.items():
                                    if key != 'content' and isinstance(value, str):
                                        print(f"[Tutu DEBUG] Message.{key}: {repr(value[:200]) if len(str(value)) > 200 else repr(value)}")
                                        # 检查是否是图片数据
                                        if 'data:image/' in str(value) or 'base64,' in str(value):
                                            print(f"[Tutu DEBUG] 🎯找到图片数据在message.{key}中!")
                                            accumulated_content += str(value)
                                            print(f"[Tutu DEBUG] 添加图片数据: {len(str(value))}字符")
                            
                            # 检查choice的其他字段，可能图片数据在别处
                            for key, value in choice.items():
                                if key not in ['delta', 'message', 'index', 'finish_reason', 'native_finish_reason', 'logprobs']:
                                    if isinstance(value, str) and ('data:image/' in value or 'base64,' in value):
                                        print(f"[Tutu DEBUG] 🎯找到图片数据在choice.{key}中!")
                                        accumulated_content += value
                                        print(f"[Tutu DEBUG] 添加图片数据: {len(value)}字符")
                                    elif value:
                                        print(f"[Tutu DEBUG] Choice.{key}: {repr(str(value)[:200])}")
                        
                        # 检查整个chunk中是否有图片数据 - 针对不同API提供商
                        chunk_str = json.dumps(chunk_data)
                        
                        if is_comfly:
                            # comfly可能把图片数据放在不同的位置
                            print(f"[Tutu DEBUG] 🔍 comfly专用检查: 搜索整个响应块")
                            
                            # 检查是否有任何图片相关的字段
                            for key, value in chunk_data.items():
                                if key not in ['id', 'object', 'created', 'model', 'system_fingerprint', 'choices', 'usage']:
                                    if isinstance(value, str) and ('data:image/' in value or 'http' in value):
                                        print(f"[Tutu DEBUG] 🎯 comfly在{key}字段发现可能的图片数据!")
                                        accumulated_content += " " + value
                                    elif value:
                                        print(f"[Tutu DEBUG] comfly额外字段{key}: {repr(str(value)[:100])}")
                            
                            # 检查choices之外的图片数据
                            if 'data:image/' in chunk_str or 'generated_image' in chunk_str or 'image_url' in chunk_str:
                                print(f"[Tutu DEBUG] 🎯 comfly JSON中发现图片相关数据!")
                                print(f"[Tutu DEBUG] 完整chunk (前500字符): {chunk_str[:500]}")
                                
                                # 尝试提取所有可能的图片URL
                                import re
                                patterns = [
                                    r'data:image/[^",\s]+',  # base64 图片
                                    r'https?://[^",\s]+\.(?:png|jpg|jpeg|gif|webp)',  # 图片URL
                                    r'"image_url":\s*"([^"]+)"',  # JSON中的image_url字段
                                    r'"generated_image":\s*"([^"]+)"'  # 生成图片字段
                                ]
                                
                                for pattern in patterns:
                                    urls = re.findall(pattern, chunk_str)
                                    if urls:
                                        print(f"[Tutu DEBUG] 🎯 comfly用模式 {pattern} 找到: {len(urls)}个URL")
                                        for url in urls:
                                            if url.startswith('data:image/'):
                                                print(f"[Tutu DEBUG] 🎯 comfly提取base64图片")
                                            else:
                                                print(f"[Tutu DEBUG] 🎯 comfly提取URL: {url[:50]}...") 
                                            accumulated_content += " " + url
                                            
                        elif is_openrouter:
                            # OpenRouter的原有处理逻辑
                            if 'data:image/' in chunk_str:
                                print(f"[Tutu DEBUG] 🎯 OpenRouter在JSON中发现图片数据!")
                                import re
                                image_urls_in_chunk = re.findall(r'data:image/[^"]+', chunk_str)
                                if image_urls_in_chunk:
                                    for url in image_urls_in_chunk:
                                        if url.startswith('data:image/'):
                                            print(f"[Tutu DEBUG] 🎯 OpenRouter提取base64图片")
                                        else:
                                            print(f"[Tutu DEBUG] 🎯 OpenRouter提取URL: {url[:50]}...")
                                        accumulated_content += " " + url
                        
                        # 保存完整的响应数据用于调试
                        raw_response_parts.append(chunk_data)
                                
                    except json.JSONDecodeError as e:
                        print(f"[Tutu DEBUG] JSON解析失败: {e}")
                        print(f"[Tutu DEBUG] 当前缓冲区内容: {repr(current_json_buffer[:200])}")
                        # 不要清空缓冲区，可能还有更多数据到来
                        
                elif line:
                    # 处理不以"data: "开头的行，它们可能是JSON的续行
                    print(f"[Tutu DEBUG] 非data行: {repr(line[:100])}")
                    if current_json_buffer:
                        # 如果有未完成的JSON，尝试添加这行
                        # 先尝试修复编码问题
                        try:
                            # 如果line包含二进制数据，尝试解码
                            if isinstance(line, str) and '\\x' in repr(line):
                                # 尝试修复UTF-8编码问题
                                fixed_line = line.encode('latin1').decode('utf-8')
                                print(f"[Tutu DEBUG] 编码修复后: {repr(fixed_line)}")
                            else:
                                fixed_line = line
                        except (UnicodeDecodeError, UnicodeEncodeError):
                            fixed_line = line
                        
                        current_json_buffer += fixed_line
                        try:
                            chunk_data = json.loads(current_json_buffer)
                            print(f"[Tutu DEBUG] 续行JSON解析成功: {list(chunk_data.keys())}")
                            
                            # 清空缓冲区
                            current_json_buffer = ""
                            
                            # 处理这个合并后的chunk_data（重要！）
                            if 'choices' in chunk_data and chunk_data['choices']:
                                choice = chunk_data['choices'][0]
                                print(f"[Tutu DEBUG] 续行完整Choice结构: {choice}")
                                
                                # 检查delta中的所有字段
                                if 'delta' in choice:
                                    delta = choice['delta']
                                    print(f"[Tutu DEBUG] 续行Delta所有字段: {list(delta.keys())}")
                                    
                                    # 检查content字段
                                    if 'content' in delta:
                                        content = delta['content']
                                        print(f"[Tutu DEBUG] 续行Delta.content: {repr(content[:200]) if content else 'None/Empty'}")
                                        if content:
                                            try:
                                                if isinstance(content, str):
                                                    content = content.encode('latin1').decode('utf-8')
                                            except (UnicodeDecodeError, UnicodeEncodeError):
                                                pass
                                            accumulated_content += content
                                            print(f"[Tutu DEBUG] 从续行添加delta.content: {repr(content[:100])}")
                                    
                                    # 检查其他字段中的图片数据
                                    for key, value in delta.items():
                                        if key != 'content' and isinstance(value, str):
                                            print(f"[Tutu DEBUG] 续行Delta.{key}: {repr(value[:200]) if len(str(value)) > 200 else repr(value)}")
                                            if 'data:image/' in str(value) or 'base64,' in str(value):
                                                print(f"[Tutu DEBUG] 🎯续行中找到图片数据在delta.{key}!")
                                                accumulated_content += str(value)
                                                print(f"[Tutu DEBUG] 从续行添加图片数据: {len(str(value))}字符")
                                        
                                # 检查message中的内容
                                elif 'message' in choice:
                                    message = choice['message']
                                    print(f"[Tutu DEBUG] 续行Message所有字段: {list(message.keys())}")
                                    
                                    if 'content' in message:
                                        content = message['content']
                                        print(f"[Tutu DEBUG] 续行Message.content: {repr(content[:200]) if content else 'None/Empty'}")
                                        if content:
                                            try:
                                                if isinstance(content, str):
                                                    content = content.encode('latin1').decode('utf-8')
                                            except (UnicodeDecodeError, UnicodeEncodeError):
                                                pass
                                            accumulated_content += content
                                            print(f"[Tutu DEBUG] 从续行添加message.content: {repr(content[:100])}")
                                    
                                    # 检查message中的其他字段
                                    for key, value in message.items():
                                        if key != 'content' and isinstance(value, str):
                                            if 'data:image/' in str(value) or 'base64,' in str(value):
                                                print(f"[Tutu DEBUG] 🎯续行中找到图片数据在message.{key}!")
                                                accumulated_content += str(value)
                                                print(f"[Tutu DEBUG] 从续行添加图片数据: {len(str(value))}字符")
                                
                                # 检查choice中的其他字段
                                for key, value in choice.items():
                                    if key not in ['delta', 'message', 'index', 'finish_reason', 'native_finish_reason', 'logprobs']:
                                        if isinstance(value, str) and ('data:image/' in value or 'base64,' in value):
                                            print(f"[Tutu DEBUG] 🎯续行中找到图片数据在choice.{key}!")
                                            accumulated_content += value
                                            print(f"[Tutu DEBUG] 从续行添加图片数据: {len(value)}字符")
                            
                            # 续行中的图片数据检查 - 针对不同API提供商
                            chunk_str = json.dumps(chunk_data)
                            
                            if is_comfly:
                                # comfly续行处理
                                print(f"[Tutu DEBUG] 🔍 comfly续行检查: 搜索图片数据")
                                
                                # 检查顶级字段中的图片数据
                                for key, value in chunk_data.items():
                                    if key not in ['id', 'object', 'created', 'model', 'system_fingerprint', 'choices', 'usage']:
                                        if isinstance(value, str) and ('data:image/' in value or 'http' in value):
                                            print(f"[Tutu DEBUG] 🎯 comfly续行在{key}发现图片数据!")
                                            accumulated_content += " " + value
                                
                                # 全面搜索续行中的图片数据
                                if 'data:image/' in chunk_str or 'generated_image' in chunk_str or 'image_url' in chunk_str:
                                    print(f"[Tutu DEBUG] 🎯 comfly续行JSON中发现图片相关数据!")
                                    import re
                                    patterns = [
                                        r'data:image/[^",\s]+',
                                        r'https?://[^",\s]+\.(?:png|jpg|jpeg|gif|webp)',
                                        r'"image_url":\s*"([^"]+)"',
                                        r'"generated_image":\s*"([^"]+)"'
                                    ]
                                    
                                    for pattern in patterns:
                                        urls = re.findall(pattern, chunk_str)
                                        if urls:
                                            print(f"[Tutu DEBUG] 🎯 comfly续行用模式找到: {len(urls)}个URL")
                                            for url in urls:
                                                if url.startswith('data:image/'):
                                                    print(f"[Tutu DEBUG] 🎯 comfly续行提取base64图片")
                                                else:
                                                    print(f"[Tutu DEBUG] 🎯 comfly续行提取URL: {url[:50]}...")
                                                accumulated_content += " " + url
                                                
                            elif is_openrouter:
                                # OpenRouter续行处理
                                if 'data:image/' in chunk_str:
                                    print(f"[Tutu DEBUG] 🎯 OpenRouter续行中发现图片数据!")
                                    import re
                                    image_urls_in_chunk = re.findall(r'data:image/[^"]+', chunk_str)
                                    if image_urls_in_chunk:
                                        for url in image_urls_in_chunk:
                                            if url.startswith('data:image/'):
                                                print(f"[Tutu DEBUG] 🎯 OpenRouter续行提取base64图片")
                                            else:
                                                print(f"[Tutu DEBUG] 🎯 OpenRouter续行提取URL: {url[:50]}...")
                                            accumulated_content += " " + url
                            
                            # 保存完整的响应数据用于调试
                            raw_response_parts.append(chunk_data)
                            
                        except json.JSONDecodeError as e:
                            print(f"[Tutu DEBUG] 续行JSON仍然解析失败: {e}")
                            # 仍然不完整，继续等待
                            pass
                        
        except Exception as e:
            print(f"[Tutu ERROR] SSE流处理错误: {e}")
            
        print(f"[Tutu DEBUG] SSE处理完成:")
        print(f"[Tutu DEBUG] - 总共处理了{chunk_count}个数据块")
        print(f"[Tutu DEBUG] - 累积内容长度: {len(accumulated_content)}")
        
        # 简单截断长内容，避免base64刷屏
        if 'data:image/' in accumulated_content:
            base64_count = accumulated_content.count('data:image/')
            print(f"[Tutu DEBUG] - 累积内容: 包含{base64_count}个base64图片 + 文本({len(accumulated_content)}字符)")
        elif len(accumulated_content) > 200:
            print(f"[Tutu DEBUG] - 累积内容: {repr(accumulated_content[:200])}...")
        else:
            print(f"[Tutu DEBUG] - 累积内容: {repr(accumulated_content)}")
        
        print(f"[Tutu DEBUG] - 完整响应块数: {len(raw_response_parts)}")
            
        return accumulated_content

    def extract_image_urls(self, response_text):
        print(f"[Tutu DEBUG] 开始提取图片URL...")
        print(f"[Tutu DEBUG] 响应文本长度: {len(response_text)}")
        
        # 简单处理响应文本，避免base64刷屏
        if 'data:image/' in response_text:
            base64_count = response_text.count('data:image/')
            print(f"[Tutu DEBUG] 响应文本: 包含{base64_count}个base64图片({len(response_text)}字符)")
        elif len(response_text) > 500:
            print(f"[Tutu DEBUG] 响应文本内容: {response_text[:500]}...")
        else:
            print(f"[Tutu DEBUG] 响应文本内容: {response_text}")
        
        # Check for markdown image format
        print(f"[Tutu DEBUG] 1. 检查markdown图片格式...")
        image_pattern = r'!\[.*?\]\((.*?)\)'
        matches = re.findall(image_pattern, response_text)
        if matches:
            # 简单显示URL数量，避免刷屏
            base64_count = sum(1 for url in matches if url.startswith('data:image/'))
            http_count = len(matches) - base64_count
            print(f"[Tutu DEBUG] 找到markdown图片: {base64_count}个base64图片, {http_count}个HTTP链接")
            return matches

        # Check for direct HTTP image URLs  
        print(f"[Tutu DEBUG] 2. 检查直接HTTP图片URL...")
        url_pattern = r'https?://\S+\.(?:jpg|jpeg|png|gif|webp)'
        matches = re.findall(url_pattern, response_text)
        if matches:
            print(f"[Tutu DEBUG] 找到HTTP图片URL: {len(matches)}个")
            return matches
        
        # Check for any URLs
        print(f"[Tutu DEBUG] 3. 检查任何URL...")
        all_url_pattern = r'https?://[^\s)]+'
        matches = re.findall(all_url_pattern, response_text)
        if matches:
            print(f"[Tutu DEBUG] 找到一般URL: {len(matches)}个")
            return matches
            
        # Check for base64 data URLs
        print(f"[Tutu DEBUG] 4. 检查base64数据URL...")
        base64_pattern = r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+'
        matches = re.findall(base64_pattern, response_text)
        if matches:
            print(f"[Tutu DEBUG] 找到base64 URL: {len(matches)}个")
            return matches
        
        print(f"[Tutu DEBUG] 未找到任何图片URL")
        return []

    def resize_to_target_size(self, image, target_size):
        """Resize image to target size while preserving aspect ratio with padding"""

        img_width, img_height = image.size
        target_width, target_height = target_size

        width_ratio = target_width / img_width
        height_ratio = target_height / img_height
        scale = min(width_ratio, height_ratio)

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        resized_img = image.resize((new_width, new_height), Image.LANCZOS)

        new_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))

        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
 
        new_img.paste(resized_img, (paste_x, paste_y))
        
        return new_img

    def parse_resolution(self, resolution_str):
        """Parse resolution string (e.g., '1024x1024') to width and height"""
        width, height = map(int, resolution_str.split('x'))
        return (width, height)

    def _sanitize_content_for_debug(self, content):
        """Sanitize content for debug logging"""
        if isinstance(content, str):
            # String format (comfly)
            return content[:200] + ('...' if len(content) > 200 else '')
        elif isinstance(content, list):
            # Array format (OpenRouter)
            sanitized = []
            for item in content:
                if item.get('type') == 'text':
                    text = item.get('text', '')[:100]
                    sanitized.append({
                        'type': 'text',
                        'text': text + ('...' if len(item.get('text', '')) > 100 else '')
                    })
                elif item.get('type') == 'image_url':
                    sanitized.append({
                        'type': 'image_url',
                        'image_url': '[IMAGE_DATA]'
                    })
            return sanitized
        else:
            return '[UNKNOWN_CONTENT_TYPE]'

    def _parse_and_validate_model(self, model_with_tag, api_provider):
        """解析带标签的模型名称并验证是否与API提供商匹配"""
        # 模型格式：[Provider] model_name
        if not model_with_tag.startswith('['):
            # 如果没有标签，直接返回（向后兼容）
            return model_with_tag
        
        try:
            # 解析标签和模型名
            tag_end = model_with_tag.find(']')
            if tag_end == -1:
                return model_with_tag
                
            provider_tag = model_with_tag[1:tag_end]  # 去掉方括号
            actual_model = model_with_tag[tag_end + 2:]  # 去掉"] "
            
            # 验证提供商匹配
            if api_provider == "OpenRouter" and provider_tag != "OpenRouter":
                print(f"[Tutu WARNING] 选择了OpenRouter但模型是{provider_tag}的")
                return None
            elif api_provider == "ai.comfly.chat" and provider_tag != "Comfly":
                print(f"[Tutu WARNING] 选择了ai.comfly.chat但模型是{provider_tag}的")
                return None
            
            print(f"[Tutu DEBUG] 解析模型: {provider_tag} -> {actual_model}")
            return actual_model
            
        except Exception as e:
            print(f"[Tutu ERROR] 模型名称解析失败: {e}")
            return model_with_tag

    def _get_model_suggestions(self, api_provider):
        """根据API提供商获取推荐的模型选择"""
        if api_provider == "OpenRouter":
            return "• [OpenRouter] google/gemini-2.5-flash-image-preview (推荐，支持图片生成)"
        else:  # ai.comfly.chat
            return "• [Comfly] gemini-2.5-flash-image-preview (推荐)\n• [Comfly] gemini-2.0-flash-preview-image-generation"

    def process(self, preset, prompt, api_provider, model, resolution, num_images, temperature, top_p, seed, timeout=120, 
                object_image=None, subject_image=None, scene_image=None, comfly_api_key="", openrouter_api_key="", save_as_preset=""):

        print(f"\n[Tutu DEBUG] ========== Starting Gemini API Process ==========")
        print(f"[Tutu DEBUG] Original parameters:")
        print(f"[Tutu DEBUG] - API Provider: {api_provider}")
        print(f"[Tutu DEBUG] - Preset: {preset}")
        print(f"[Tutu DEBUG] - Model: {model}")
        print(f"[Tutu DEBUG] - Resolution: {resolution}")
        print(f"[Tutu DEBUG] - Prompt length: {len(prompt) if prompt else 0}")
        print(f"[Tutu DEBUG] - Has object_image: {object_image is not None}")
        print(f"[Tutu DEBUG] - Has subject_image: {subject_image is not None}")
        print(f"[Tutu DEBUG] - Has scene_image: {scene_image is not None}")
        
        # 显示模型选择指南
        print(f"\n[Tutu INFO] 💡 模型选择指南:")
        print(f"[Tutu INFO] • ai.comfly.chat 请选择 [Comfly] 标签的模型")
        print(f"[Tutu INFO] • OpenRouter 请选择 [OpenRouter] 标签的模型")
        print(f"[Tutu INFO] • 当前组合: {api_provider} + {model}")
        
        # 根据API提供商设置端点
        if api_provider == "OpenRouter":
            api_endpoint = "https://openrouter.ai/api/v1/chat/completions"
        else:
            api_endpoint = "https://ai.comfly.chat/v1/chat/completions"
        
        print(f"[Tutu DEBUG] API Endpoint: {api_endpoint}")

        # 处理模型选择并验证
        actual_model = self._parse_and_validate_model(model, api_provider)
        if not actual_model:
            suggestions = self._get_model_suggestions(api_provider)
            error_msg = f"❌ 模型选择错误！\n\n当前选择: '{model}'\nAPI提供商: '{api_provider}'\n\n💡 建议选择:\n{suggestions}\n\n请重新选择正确的模型。"
            print(f"[Tutu ERROR] {error_msg}")
            return self.handle_error(object_image, subject_image, scene_image, error_msg, resolution)
        
        model = actual_model
        print(f"[Tutu DEBUG] Using actual model: {model}")

        # 保存原始提示词用于后续处理
        original_prompt = prompt
        prompt_template_used = None

        # 处理预设加载
        if preset != "自定义":
            print(f"[Tutu DEBUG] Loading preset: {preset}")
            preset_data = get_preset_by_name("gemini", preset)
            if preset_data and preset_data.get("config"):
                preset_config = preset_data["config"]
                print(f"[Tutu DEBUG] 简化预设加载: 仅应用提示词模板")
                
                # 预设系统简化：只应用提示词模板，所有其他参数保持用户界面选择
                # 如果预设中有提示词模板，应用它
                if "prompt_template" in preset_config and preset_config["prompt_template"]:
                    prompt_template_used = preset_config["prompt_template"]
                    prompt = preset_config["prompt_template"].replace("{prompt}", original_prompt)
                    print(f"[Tutu DEBUG] ✅ 应用提示词模板:")
                    print(f"[Tutu DEBUG] - 原始提示词: {original_prompt}")
                    print(f"[Tutu DEBUG] - 模板: {prompt_template_used}")
                    print(f"[Tutu DEBUG] - 增强后: {prompt}")
                    print(f"[Tutu DEBUG] ✅ 保持用户界面的所有其他设置 (模型、分辨率、温度等)")
                else:
                    print(f"[Tutu DEBUG] ⚠️ 预设中没有提示词模板")
            else:
                print(f"[Tutu DEBUG] No preset config found for: {preset}")
        
        # 保存为新预设（如果指定了名称）
        if save_as_preset.strip():
            # 简化预设：只保存提示词模板和描述
            if prompt_template_used:
                # 如果使用了模板，保存模板
                current_config = {
                    "prompt_template": prompt_template_used
                }
                description = f"提示词模板: {prompt_template_used[:50]}..." if len(prompt_template_used) > 50 else f"提示词模板: {prompt_template_used}"
            else:
                # 如果没有模板，保存当前提示词作为模板
                current_config = {
                    "prompt_template": original_prompt  # 保存原始提示词
                }
                description = f"提示词模板: {original_prompt[:50]}..." if len(original_prompt) > 50 else f"提示词模板: {original_prompt}"
            
            try:
                preset_id = save_preset("gemini", save_as_preset, current_config, description)
                print(f"[Tutu] ✅ 成功保存简化预设 '{save_as_preset}' (ID: {preset_id})")
                print(f"[Tutu] 📝 预设内容: 仅包含提示词模板，所有其他设置由界面控制")
            except Exception as e:
                print(f"[Tutu] ❌ 保存预设失败: {str(e)}")
        
        # 处理API Key更新和保存
        config_changed = False
        config = get_config()
        
        # 处理 comfly API key
        if comfly_api_key.strip():
            print(f"[Tutu DEBUG] Using provided comfly API key: {comfly_api_key[:10]}...")
            self.comfly_api_key = comfly_api_key
            config['comfly_api_key'] = comfly_api_key
            config_changed = True
            
        # 处理 OpenRouter API key
        if openrouter_api_key.strip():
            print(f"[Tutu DEBUG] Using provided OpenRouter API key: {openrouter_api_key[:10]}...")
            self.openrouter_api_key = openrouter_api_key
            config['openrouter_api_key'] = openrouter_api_key
            config_changed = True
            
        # 保存配置
        if config_changed:
            save_config(config)
            
        # 显示当前使用的API key
        current_api_key = self.get_current_api_key(api_provider)
        print(f"[Tutu DEBUG] Using {api_provider} API key: {current_api_key[:10] if current_api_key else 'None'}...")

        self.timeout = timeout
        
        print(f"[Tutu DEBUG] Final parameters:")
        print(f"[Tutu DEBUG] - Model: {model}")
        print(f"[Tutu DEBUG] - Resolution: {resolution}")
        print(f"[Tutu DEBUG] - Temperature: {temperature}")
        print(f"[Tutu DEBUG] - API Key length: {len(current_api_key) if current_api_key else 0}")
        
        try:

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            target_size = None

            if resolution == "object_image size" and object_image is not None:
                pil_image = tensor2pil(object_image)[0]
                target_size = pil_image.size
            elif resolution == "subject_image size" and subject_image is not None:
                pil_image = tensor2pil(subject_image)[0]
                target_size = pil_image.size
            elif resolution == "scene_image size" and scene_image is not None:
                pil_image = tensor2pil(scene_image)[0]
                target_size = pil_image.size
            else:
                target_size = self.parse_resolution(resolution)

            has_images = object_image is not None or subject_image is not None or scene_image is not None

            # 使用标准OpenAI格式（数组）- 适用于所有API提供商
            content = []
            
            if has_images:
                # 对于图片编辑任务，先添加图片，再添加指令文本
                for image_var, image_tensor in [("object_image", object_image), 
                                             ("subject_image", subject_image), 
                                             ("scene_image", scene_image)]:
                    if image_tensor is not None:
                        pil_image = tensor2pil(image_tensor)[0]
                        print(f"[Tutu DEBUG] 处理 {image_var} (标准数组格式)...")
                        
                        # 优先尝试上传
                        uploaded_url = self.upload_image(pil_image)
                        
                        if uploaded_url:
                            image_url = uploaded_url
                            print(f"[Tutu DEBUG] {image_var} 使用上传URL")
                        else:
                            # 使用base64
                            print(f"[Tutu DEBUG] {image_var} 上传失败，使用base64...")
                            image_base64 = self.image_to_base64(pil_image)
                            image_url = f"data:image/png;base64,{image_base64}"
                            print(f"[Tutu DEBUG] {image_var} base64大小: {len(image_base64)} 字符")
                        
                        content.append({
                            "type": "image_url", 
                            "image_url": {"url": image_url}
                        })
                
                # 添加文本指令
                if api_provider == "ai.comfly.chat":
                    # 为ai.comfly.chat添加明确的图片生成指令
                    image_edit_instruction = f"Please analyze the provided image(s) and create a NEW edited image based on the following request: {prompt}. Generate the modified image, don't just describe it. Return the actual image."
                    content.append({"type": "text", "text": image_edit_instruction})
                else:
                    content.append({"type": "text", "text": prompt})
                
                print(f"[Tutu DEBUG] content数组长度: {len(content)} (图片: {len(content)-1}, 文本: 1)")
            else:
                # 生成图片任务（无输入图片）
                dimensions = f"{target_size[0]}x{target_size[1]}"
                aspect_ratio = "1:1" if target_size[0] == target_size[1] else f"{target_size[0]}:{target_size[1]}"
                
                if num_images == 1:
                    enhanced_prompt = f"Generate a high-quality, detailed image with dimensions {dimensions} and aspect ratio {aspect_ratio}. Based on this description: {prompt}"
                else:
                    enhanced_prompt = f"Generate {num_images} DIFFERENT high-quality images with VARIED content, each with unique and distinct visual elements, all having the exact same dimensions of {dimensions} and aspect ratio {aspect_ratio}. Important: make sure each image has different content but maintains the same technical dimensions. Based on this description: {prompt}"
                
                content.append({"type": "text", "text": enhanced_prompt})

            messages = [{
                "role": "user",
                "content": content
            }]

            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
                "seed": seed if seed > 0 else None,
                "max_tokens": 8192,
                "stream": True  # Required for gemini-2.5-flash-image-preview
            }

            # 添加调试日志
            print(f"\n[Tutu DEBUG] API Request Details:")
            print(f"[Tutu DEBUG] API Provider: {api_provider}")
            print(f"[Tutu DEBUG] Model: {model}")
            print(f"[Tutu DEBUG] Has images: {has_images}")
            print(f"[Tutu DEBUG] Target size: {target_size}")
            print(f"[Tutu DEBUG] Messages count: {len(messages)}")
            print(f"[Tutu DEBUG] Content type: {type(content)}")
            print(f"[Tutu DEBUG] Content length: {len(str(content))}")
            
            # 记录payload大小（但不打印图片数据）
            payload_copy = payload.copy()
            payload_copy['messages'] = [{
                'role': msg['role'],
                'content': self._sanitize_content_for_debug(msg['content'])
            } for msg in payload['messages']]
            
            print(f"[Tutu DEBUG] Payload structure: {json.dumps(payload_copy, indent=2, ensure_ascii=False)}")
            
            # 检查API Key
            headers = self.get_headers(api_provider)
            print(f"[Tutu DEBUG] Headers: {dict(headers)}")
            if not current_api_key or len(current_api_key) < 10:
                print(f"[Tutu DEBUG] WARNING: API Key seems invalid: '{current_api_key[:10] if current_api_key else 'None'}...")

            pbar = comfy.utils.ProgressBar(100)
            pbar.update_absolute(10)

            try:
                print(f"[Tutu DEBUG] Sending request to: {api_endpoint}")
                response = requests.post(
                    api_endpoint,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                    stream=True  # Enable streaming for SSE
                )
                
                print(f"[Tutu DEBUG] Response status: {response.status_code}")
                print(f"[Tutu DEBUG] Response headers: {dict(response.headers)}")
                
                # 如果状态码不是200，尝试读取错误响应
                if response.status_code != 200:
                    try:
                        error_text = response.text[:1000]  # 只读取前1000字符
                        print(f"[Tutu DEBUG] Error response body: {error_text}")
                    except:
                        print(f"[Tutu DEBUG] Could not read error response body")
                
                response.raise_for_status()
                
                # Process Server-Sent Events (SSE) stream with API-specific handling
                response_text = self.process_sse_stream(response, api_provider)
                print(f"[Tutu DEBUG] SSE流处理完成，获得响应文本长度: {len(response_text)}")
                
            except requests.exceptions.Timeout:
                print(f"[Tutu DEBUG] Request timeout after {self.timeout} seconds")
                raise TimeoutError(f"API request timed out after {self.timeout} seconds")
            except requests.exceptions.HTTPError as e:
                print(f"[Tutu DEBUG] HTTP Error: {e}")
                print(f"[Tutu DEBUG] Response status: {e.response.status_code}")
                try:
                    error_detail = e.response.text[:500]
                    print(f"[Tutu DEBUG] Error detail: {error_detail}")
                    
                    # 特殊处理404错误（模型不存在）
                    if e.response.status_code == 404 and "No endpoints found" in error_detail:
                        suggestions = self._get_model_suggestions(api_provider)
                        model_error = f"""❌ **模型不存在错误**

**当前选择的模型**: `{model}`
**错误**: 此模型在 {api_provider} 上不可用

**💡 建议选择可用的模型**:
{suggestions}

**解决方案**:
1. 切换到上面推荐的可用模型
2. 确认模型名称拼写正确
3. 检查 {api_provider} 官方文档获取最新支持的模型列表"""
                        raise Exception(model_error)
                    else:
                        raise Exception(f"HTTP {e.response.status_code} Error: {error_detail}")
                except:
                    raise Exception(f"HTTP Error: {str(e)}")
            except requests.exceptions.RequestException as e:
                print(f"[Tutu DEBUG] Request Exception: {str(e)}")
                raise Exception(f"API request failed: {str(e)}")
            
            pbar.update_absolute(40)

            formatted_response = f"**User prompt**: {prompt}\n\n**Response** ({timestamp}):\n{response_text}"
            
            print(f"[Tutu DEBUG] 准备提取图片URL，响应文本长度: {len(response_text)}")
            image_urls = self.extract_image_urls(response_text)
            print(f"[Tutu DEBUG] 图片URL提取完成，找到{len(image_urls)}个URL")
            
            if image_urls:
                try:
                    images = []
                    first_image_url = ""  
                    
                    for i, url in enumerate(image_urls):
                        pbar.update_absolute(40 + (i+1) * 50 // len(image_urls))
                        
                        if i == 0:
                            first_image_url = url  
                        
                        try:
                            if url.startswith('data:image/'):
                                # Handle base64 data URL
                                base64_data = url.split(',', 1)[1]
                                image_data = base64.b64decode(base64_data)
                                pil_image = Image.open(BytesIO(image_data))
                            else:
                                # Handle HTTP URL
                                img_response = requests.get(url, timeout=self.timeout)
                                img_response.raise_for_status()
                                pil_image = Image.open(BytesIO(img_response.content))

                            resized_image = self.resize_to_target_size(pil_image, target_size)
                            img_tensor = pil2tensor(resized_image)
                            images.append(img_tensor)
                            
                        except Exception as img_error:
                            print(f"Error processing image URL {i+1}: {str(img_error)}")
                            continue
                    
                    if images:
                        try:
                            combined_tensor = torch.cat(images, dim=0)
                        except RuntimeError:
                            combined_tensor = images[0] if images else None
                            
                        pbar.update_absolute(100)
                        return (combined_tensor, formatted_response, first_image_url)
                    else:
                        raise Exception("No images could be processed successfully")
                    
                except Exception as e:
                    print(f"Error processing image URLs: {str(e)}")

            # No image URLs found in response - 可能是SSE解析问题
            print(f"[Tutu WARNING] ⚠️  响应中未找到图片URL - 可能是SSE解析问题")
            # 简单显示响应内容，避免base64刷屏
            if 'data:image/' in response_text:
                base64_count = response_text.count('data:image/')
                print(f"[Tutu DEBUG] 📝 当前解析响应: 包含{base64_count}个base64图片({len(response_text)}字符)")
            elif len(response_text) > 200:
                print(f"[Tutu DEBUG] 📝 当前解析响应: {repr(response_text[:200])}...")
            else:
                print(f"[Tutu DEBUG] 📝 当前解析响应: {repr(response_text)}")
            print(f"[Tutu DEBUG] 🔍 Gemini 2.5 Flash Image Preview 支持图片生成，问题可能在数据解析上")
            print(f"[Tutu DEBUG] 💡 检查点:")
            print(f"[Tutu DEBUG]    1. SSE流是否完整解析？")
            print(f"[Tutu DEBUG]    2. JSON数据是否被正确拼接？")
            print(f"[Tutu DEBUG]    3. 编码是否正确处理？")
            
            pbar.update_absolute(100)

            reference_image = None
            if object_image is not None:
                reference_image = object_image
            elif subject_image is not None:
                reference_image = subject_image
            elif scene_image is not None:
                reference_image = scene_image
                
            # 添加调试说明到响应中
            debug_info = f"""

## 🔧 **调试信息：SSE解析问题**

**当前状态**: 响应解析可能不完整
**解析到的内容**: {response_text}
**问题**: Gemini 2.5 Flash Image Preview 支持图片生成，但我们的SSE流解析可能有bug

**请检查控制台日志获取详细的解析过程**
"""
            formatted_response += debug_info
                
            if reference_image is not None:
                return (reference_image, formatted_response, "")
            else:
                default_image = Image.new('RGB', target_size, color='white')
                default_tensor = pil2tensor(default_image)
                return (default_tensor, formatted_response, "")
            
        except TimeoutError as e:
            error_message = f"API timeout error: {str(e)}"
            print(f"[Tutu DEBUG] TimeoutError occurred: {error_message}")
            return self.handle_error(object_image, subject_image, scene_image, error_message, resolution)
            
        except Exception as e:
            error_message = f"Error calling Gemini API: {str(e)}"
            print(f"[Tutu DEBUG] Exception occurred:")
            print(f"[Tutu DEBUG] - Type: {type(e).__name__}")
            print(f"[Tutu DEBUG] - Message: {str(e)}")
            print(f"[Tutu DEBUG] - Full error: {repr(e)}")
            
            # 打印更多上下文信息
            print(f"[Tutu DEBUG] Context at error:")
            print(f"[Tutu DEBUG] - Current model: {model if 'model' in locals() else 'undefined'}")
            print(f"[Tutu DEBUG] - API key present: {bool(current_api_key)}")
            print(f"[Tutu DEBUG] - API key length: {len(current_api_key) if current_api_key else 0}")
            
            return self.handle_error(object_image, subject_image, scene_image, error_message, resolution)
    
    def handle_error(self, object_image, subject_image, scene_image, error_message, resolution="1024x1024"):
        """Handle errors with appropriate image output"""
        if object_image is not None:
            return (object_image, error_message, "")
        elif subject_image is not None:
            return (subject_image, error_message, "")
        elif scene_image is not None:
            return (scene_image, error_message, "")
        else:
            if resolution in ["object_image size", "subject_image size", "scene_image size"]:
                target_size = (1024, 1024)  
            else:
                target_size = self.parse_resolution(resolution)
                
            default_image = Image.new('RGB', target_size, color='white')
            default_tensor = pil2tensor(default_image)
            return (default_tensor, error_message, "")


WEB_DIRECTORY = "./web"    
        
NODE_CLASS_MAPPINGS = {
    "ComflyGeminiAPI": ComflyGeminiAPI,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComflyGeminiAPI": "Tutu Nano Banana",
}