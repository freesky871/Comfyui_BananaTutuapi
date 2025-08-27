# Comfyui_Tutuapi - Google Gemini AI图像生成插件

一个专为ComfyUI优化的Google Gemini图像生成自定义节点插件，支持多种API提供商。

## 主要特色

- **多平台支持**：支持 ai.comfly.chat 和 OpenRouter 两个API提供商
- **专注Gemini**：专门优化的Google Gemini 2.5 Flash图像生成和编辑能力
- **预设系统**：内置12个专业预设模板，支持自定义保存和加载
- **流式响应**：优化API调用，支持Server-Sent Events流式处理
- **多图输入**：支持object_image、subject_image、scene_image多图参考生成

## 支持的AI服务

### API提供商

1. **ai.comfly.chat**

   - 稳定可靠的API服务
   - 支持图片上传和base64传输
2. **OpenRouter**

   - 支持多种模型路由
   - 标准OpenAI格式

### Google Gemini 模型

**Comfly平台模型**：

- **[Comfly] gemini-2.5-flash-image-preview** - 推荐使用，支持图片生成
- **[Comfly] gemini-2.0-flash-preview-image-generation** - 备用旧版

**OpenRouter平台模型**：

- **[OpenRouter] google/gemini-2.5-flash-image-preview** - 推荐使用

## 预设系统

### 内置预设模板 (12个)

**Gemini专业预设**：

- **专业人像摄影** - portrait photography风格，适合人物拍摄
- **风景摄影大片** - landscape photography，黄金时刻拍摄
- **微距摄影** - macro photography，近距离细节拍摄
- **日系动漫插画** - anime style，cel shading动漫风格
- **水彩画风格** - watercolor painting，柔和边缘水彩效果
- **油画大师风格** - oil painting，Rembrandt经典油画风格
- **电商产品图** - product photo，白色背景商品拍摄
- **Logo设计** - logo design，极简主义设计
- **社交媒体配图** - social media，时尚潮流风格
- **赛博朋克风格** - cyberpunk style，霓虹灯未来感
- **复古怀旧风** - vintage style，胶片颗粒复古感
- **超现实主义** - surrealist art，梦幻逻辑艺术风格

### 预设功能特点

- **一键加载**: 从下拉列表选择预设，自动应用所有参数
- **快速保存**: 配置好参数后输入名称即可保存为新预设
- **提示词模板**: 支持 `{prompt}` 占位符，智能融合用户输入
- **参数覆盖**: 加载预设后仍可手动调整任何参数
- **持久存储**: 预设保存在 `presets.json` 中，重启后依然可用
- **轻量优化**: 所有模板优化至50字符以内，避免API请求过大

## 安装教程

### 方法一：Git克隆安装（推荐）

1. 打开终端/命令提示符
2. 切换到ComfyUI的custom_nodes目录:

   ```bash
   cd /path/to/ComfyUI/custom_nodes
   ```
3. 克隆本项目:

   ```bash
   git clone https://github.com/yourusername/Comfyui_Tutuapi.git
   ```
4. 重启ComfyUI

### 方法二：直接下载安装

1. 访问项目GitHub页面
2. 点击绿色的"Code"按钮，选择"Download ZIP"
3. 下载并解压ZIP文件
4. 将解压后的文件夹重命名为 `Comfyui_Tutuapi-main`
5. 复制整个文件夹到ComfyUI的 `custom_nodes`目录下
6. 重启ComfyUI

### 文件夹结构确认

安装完成后，您的目录结构应该如下：

```text
ComfyUI/
├── custom_nodes/
│   └── Comfyui_Tutuapi-main/
│       ├── __init__.py
│       ├── Tutu.py
│       ├── Tutuapi.json
│       ├── presets.json
│       ├── requirements.txt
│       └── web/
└── ...
```

## 配置说明

### 1. 安装依赖包

安装后首次运行可能需要安装Python依赖：

```bash
cd custom_nodes/Comfyui_Tutuapi-main
pip install -r requirements.txt
```

### 2. 配置API Key

编辑 `Tutuapi.json` 文件，填入您的API密钥：

```json
{
  "comfly_api_key": "your_comfly_api_key_here",
  "openrouter_api_key": "your_openrouter_api_key_here"
}
```

注：也可以在节点界面中直接输入API Key，会自动保存到配置文件。

### 3. 获取API Key

- **ai.comfly.chat**: 访问 [https://ai.comfly.chat](https://ai.comfly.chat) 注册并获取API Key
- **OpenRouter**: 访问 [https://openrouter.ai](https://openrouter.ai) 注册并获取API Key

### 4. 故障排除

如遇到以下问题：

**节点不显示**：

- 确认文件夹名称为 `Comfyui_Tutuapi-main`
- 重启ComfyUI后再检查

**依赖包报错**：

```bash
# Windows用户
pip install -r requirements.txt

# Linux/Mac用户  
python3 -m pip install -r requirements.txt
```

**API调用失败**：

- 检查API Key是否正确配置
- 确认网络连接正常
- 检查API余额是否充足
- 确保选择了正确的模型（Comfly模型用于ai.comfly.chat，OpenRouter模型用于OpenRouter）
- 确保预设模板不会导致请求过大

**模型选择错误**：

- ai.comfly.chat 必须选择带 [Comfly] 标签的模型
- OpenRouter 必须选择带 [OpenRouter] 标签的模型
- 不要混用不同平台的模型

## 快速使用

### 使用预设

1. 在Gemini节点中，从"预设"下拉菜单选择预设
2. 输入您的提示词
3. 可选择上传参考图片（object_image、subject_image、scene_image）
4. 运行节点生成内容

### 保存预设

1. 配置好节点所有参数
2. 在"保存为预设"输入框输入名称
3. 运行节点，预设自动保存

### 图像编辑模式

- 上传图片到任一图片输入端口即自动启用图像编辑模式
- 支持同时使用多张参考图片
- 提示词将与预设模板智能合并

### 文本生成图像模式

- 不上传图片时自动使用文本生成图像模式
- 系统会自动添加尺寸和质量优化提示词
- 支持生成1-4张不同内容的图片

## 主要节点说明

### Tutu Nano Banana

Google Gemini多模态图像生成和编辑节点

**输入参数**：

- `preset` - 预设选择（自定义 + 12个内置预设）
- `prompt` - 文本提示词
- `api_provider` - API提供商选择（ai.comfly.chat 或 OpenRouter）
- `model` - 模型选择（根据API提供商显示对应模型）
- `resolution` - 输出分辨率（512x512到2048x2048，支持参考图尺寸）
- `num_images` - 生成图片数量（1-4张）
- `temperature` - 创意度控制（0.0-2.0）
- `top_p` - 采样控制（0.0-1.0）
- `seed` - 随机种子（可选）
- `timeout` - 超时设置（10-600秒）

**可选输入**：

- `comfly_api_key` - ai.comfly.chat API密钥（覆盖配置文件）
- `openrouter_api_key` - OpenRouter API密钥（覆盖配置文件）
- `save_as_preset` - 保存当前配置为预设
- `object_image` - 物体参考图
- `subject_image` - 主体参考图
- `scene_image` - 场景参考图

**输出**：

- `generated_images` - 生成的图像张量
- `response` - API响应文本
- `image_url` - 第一张图片URL（如果有）

## 技术特性

- **智能图片传输**: 优先尝试上传图片URL，失败时自动回退到base64传输
- **流式处理**: 支持Server-Sent Events (SSE) 实时数据流
- **多图参考**: 支持最多3张参考图片同时输入
- **智能提示词模板**: 自动合并用户输入与预设模板
- **错误处理**: 完善的错误处理和详细调试信息
- **轻量优化**: 预设模板优化，避免API请求过大导致的超时问题

## 系统要求

- ComfyUI 最新版本
- Python 3.8+
- 依赖包: `requests`, `aiohttp`, `pillow`, `numpy`等

## 支持与反馈

如遇到问题或有功能建议，请在GitHub提交Issue。

## 许可证

本项目基于Apache-2.0许可证开源。

## 致谢

本项目参考了 [Comfyui_Comfly](https://github.com/ainewsto/Comfyui_Comfly) 项目的部分代码实现，特此感谢原作者的优秀工作。
