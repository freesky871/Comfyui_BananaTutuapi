# Comfyui_Tutuapi

**Version: 1.1** | [English](#english) | [中文](#chinese)

---

`<a id="english"></a>`

## English

A ComfyUI custom node for Google Gemini image generation with multiple API providers support.

### Features

- **Multi-Platform Support**: Supports ai.comfly.chat and OpenRouter API providers
- **Google Gemini Focus**: Optimized for Google Gemini 2.5 Flash image generation and editing
- **Preset System**: 12 built-in professional presets with custom save/load support
- **Multi-Image Input**: Supports object_image, subject_image, scene_image for reference generation

### Supported Services

#### API Providers

1. **ai.comfly.chat**

   - Stable and reliable API service
   - Supports image upload and base64 transfer
2. **OpenRouter**

   - Multiple model routing support
   - Standard OpenAI format

#### Google Gemini Models

**Comfly Platform Models**:

- **[Comfly] gemini-2.5-flash-image-preview** - Recommended, supports image generation
- **[Comfly] gemini-2.0-flash-preview-image-generation** - Legacy version

**OpenRouter Platform Models**:

- **[OpenRouter] google/gemini-2.5-flash-image-preview** - Recommended

### Installation

#### Method 1: Git Clone (Recommended)

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/zhaotututu/Comfyui_Tutuapi.git
# Restart ComfyUI
```

#### Method 2: Direct Download

1. Download ZIP from [GitHub releases](https://github.com/zhaotututu/Comfyui_Tutuapi/releases)
2. Extract to `ComfyUI/custom_nodes/`
3. Rename folder to `Comfyui_Tutuapi`
4. Restart ComfyUI

### Configuration

1. **Install Dependencies**:

   ```bash
   cd custom_nodes/Comfyui_Tutuapi
   pip install -r requirements.txt
   ```
2. **Configure API Keys**:

   Edit `Tutuapi.json`:

   ```json
   {
     "comfly_api_key": "your_comfly_api_key_here",
     "openrouter_api_key": "your_openrouter_api_key_here"
   }
   ```

   Or input directly in the node interface (will auto-save).
3. **Get API Keys**:

   - **ai.comfly.chat**: Register at [https://ai.comfly.chat](https://ai.comfly.chat)
   - **OpenRouter**: Register at [https://openrouter.ai](https://openrouter.ai)

### Quick Start

1. **Using Presets**: Select from the preset dropdown menu
2. **Image Generation**: Input prompt without any image
3. **Image Editing**: Upload reference image(s) and input edit instructions
4. **Save Custom Preset**: Configure parameters and input preset name

### Node Parameters

**Required Inputs**:

- `preset` - Preset selection (Custom + 12 built-in presets)
- `prompt` - Text prompt
- `api_provider` - API provider (ai.comfly.chat or OpenRouter)
- `model` - Model selection (based on API provider)
- `resolution` - Output resolution (512x512 to 2048x2048)
- `num_images` - Number of images (1-4)
- `temperature` - Creativity control (0.0-2.0)
- `top_p` - Sampling control (0.0-1.0)
- `seed` - Random seed
- `timeout` - Timeout setting (10-600 seconds)

**Optional Inputs**:

- `comfly_api_key` - ai.comfly.chat API key
- `openrouter_api_key` - OpenRouter API key
- `save_as_preset` - Save current configuration as preset
- `object_image` - Object reference image
- `subject_image` - Subject reference image
- `scene_image` - Scene reference image

**Outputs**:

- `generated_images` - Generated image tensor
- `response` - API response text
- `image_url` - First image URL (if available)

### Troubleshooting

**Model Selection Error**:

- ai.comfly.chat must use models with [Comfly] tag
- OpenRouter must use models with [OpenRouter] tag
- Don't mix models from different platforms

**API Call Failed**:

- Check API key configuration
- Verify network connection
- Check API balance
- Ensure correct model selection

**Node Not Found in ComfyUI**:

- Restart ComfyUI after installation
- Check if node appears as "Tutu Nano Banana" in the node library
- If conflicts occur with other extensions, the node uses TutuGeminiAPI as internal name

**Image Quality Issues**:

- The node now preserves original AI-generated image quality
- No more white borders or unwanted resizing
- Images maintain their native resolution and quality

### Version History

#### v1.1 (Latest)

- **Fixed**: Node name conflicts with other ComfyUI extensions - now uses TutuGeminiAPI internally
- **Enhanced**: Unified base64 image processing for all API providers, improved stability
- **Fixed**: Eliminated white borders on generated images by preserving original AI output
- **Improved**: OpenRouter API compatibility with direct base64 processing

#### v1.0

- Initial release with core functionality
- Multi-platform API support
- 12 professional presets
- Streaming response support

### Tutorials & Resources

📺 **Video Tutorials**:

- **Bilibili**: [@zhaotutu](https://space.bilibili.com/431046154) - Comprehensive tutorials, workflow demonstrations, and model training guides (Chinese)
- **YouTube**: [@zhaotutu](https://www.youtube.com/@zhaotutu) - Step-by-step guides and use cases

📦 **Workflow Gallery**:

- Download ready-to-use workflows at [RunningHub](https://www.runninghub.ai/user-center/1936823199386537986/webapp?inviteCode=rh-v0990)
- Includes various creative examples and advanced techniques

---

`<a id="chinese"></a>`

## 中文

一个专为ComfyUI优化的Google Gemini图像生成自定义节点插件，支持多种API提供商。

### 主要特色

- **多平台支持**：支持 ai.comfly.chat 和 OpenRouter 两个API提供商
- **专注Gemini**：专门优化的Google Gemini 2.5 Flash图像生成和编辑能力
- **预设系统**：内置12个专业预设模板，支持自定义保存和加载
- **多图输入**：支持object_image、subject_image、scene_image多图参考生成

### 支持的AI服务

#### API提供商

1. **ai.comfly.chat**

   - 稳定可靠的API服务
   - 支持图片上传和base64传输
2. **OpenRouter**

   - 支持多种模型路由
   - 标准OpenAI格式

#### Google Gemini 模型

**Comfly平台模型**：

- **[Comfly] gemini-2.5-flash-image-preview** - 推荐使用，支持图片生成
- **[Comfly] gemini-2.0-flash-preview-image-generation** - 备用旧版

**OpenRouter平台模型**：

- **[OpenRouter] google/gemini-2.5-flash-image-preview** - 推荐使用

### 预设系统

#### 内置预设模板 (12个)

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

#### 预设功能特点

- **一键加载**: 从下拉列表选择预设，自动应用所有参数
- **快速保存**: 配置好参数后输入名称即可保存为新预设
- **提示词模板**: 支持 `{prompt}` 占位符，智能融合用户输入
- **参数覆盖**: 加载预设后仍可手动调整任何参数
- **持久存储**: 预设保存在 `presets.json` 中，重启后依然可用
- **轻量优化**: 所有模板优化至50字符以内，避免API请求过大

### 安装教程

#### 方法一：Git克隆安装（推荐）

```bash
cd /path/to/ComfyUI/custom_nodes
git clone https://github.com/zhaotututu/Comfyui_Tutuapi.git
# 重启ComfyUI
```

#### 方法二：直接下载安装

1. 从 [GitHub releases](https://github.com/zhaotututu/Comfyui_Tutuapi/releases) 下载ZIP文件
2. 解压到 `ComfyUI/custom_nodes/` 目录
3. 将文件夹重命名为 `Comfyui_Tutuapi`
4. 重启ComfyUI

### 配置说明

1. **安装依赖包**：

   ```bash
   cd custom_nodes/Comfyui_Tutuapi
   pip install -r requirements.txt
   ```
2. **配置API Key**：

   编辑 `Tutuapi.json` 文件：

   ```json
   {
     "comfly_api_key": "your_comfly_api_key_here",
     "openrouter_api_key": "your_openrouter_api_key_here"
   }
   ```

   注：也可以在节点界面中直接输入API Key，会自动保存到配置文件。
3. **获取API Key**：

   - **ai.comfly.chat**: 访问 [https://ai.comfly.chat](https://ai.comfly.chat) 注册并获取API Key
   - **OpenRouter**: 访问 [https://openrouter.ai](https://openrouter.ai) 注册并获取API Key

### 快速使用

#### 使用预设

1. 在Gemini节点中，从"预设"下拉菜单选择预设
2. 输入您的提示词
3. 可选择上传参考图片
4. 运行节点生成内容

#### 保存预设

1. 配置好节点所有参数
2. 在"保存为预设"输入框输入名称
3. 运行节点，预设自动保存

#### 图像编辑模式

- 上传图片到任一图片输入端口即自动启用图像编辑模式
- 支持同时使用多张参考图片
- 提示词将与预设模板智能合并

#### 文本生成图像模式

- 不上传图片时自动使用文本生成图像模式
- 系统会自动添加尺寸和质量优化提示词
- 支持生成1-4张不同内容的图片

### 故障排除

**模型选择错误**：

- ai.comfly.chat 必须选择带 [Comfly] 标签的模型
- OpenRouter 必须选择带 [OpenRouter] 标签的模型
- 不要混用不同平台的模型

**API调用失败**：

- 检查API Key是否正确配置
- 确认网络连接正常
- 检查API余额是否充足
- 确保选择了正确的模型

**节点库中找不到节点**：

- 安装后请重启ComfyUI
- 节点显示名称为"Tutu Nano Banana"，请在节点库中搜索
- 如与其他扩展发生冲突，节点内部使用TutuGeminiAPI名称以避免冲突

**图像质量问题**：

- 节点现在保持AI生成图像的原始质量
- 不会出现白边或不必要的尺寸调整
- 图像保持其原生分辨率和质量

### 版本更新

#### v1.1 (最新版)

- **修复**: 与其他ComfyUI扩展的节点名称冲突问题 - 现在内部使用TutuGeminiAPI
- **增强**: 统一base64图像处理，支持所有API提供商，提升稳定性
- **修复**: 消除生成图像的白边问题，保持AI原始输出质量
- **改进**: OpenRouter API兼容性，使用直接base64处理方式

#### v1.0

- 初始版本，核心功能发布
- 多平台API支持
- 12个专业预设
- 流式响应支持

### 教程与资源

📺 **视频教程**：

- **Bilibili**: [@zhaotutu](https://space.bilibili.com/431046154) - 详细的使用教程、工作流演示、模型训练指南等丰富内容
- **YouTube**: [@zhaotutu](https://www.youtube.com/@zhaotutu) - 英文教程和创意案例分享

📦 **工作流下载**：

- 在 [RunningHub](https://www.runninghub.ai/user-center/1936823199386537986/webapp?inviteCode=rh-v0990) 下载配套工作流
- 包含各种创意示例、高级技巧和实战案例

### 系统要求

- ComfyUI 最新版本
- Python 3.8+
- 依赖包: `requests`, `aiohttp`, `pillow`, `numpy`等

### 支持与反馈

如遇到问题或有功能建议，请在 [GitHub Issues](https://github.com/zhaotututu/Comfyui_Tutuapi/issues) 提交。

### 许可证

本项目基于Apache-2.0许可证开源。

### 致谢

本项目参考了 [Comfyui_Comfly](https://github.com/ainewsto/Comfyui_Comfly) 项目的部分代码实现，特此感谢原作者的优秀工作。
