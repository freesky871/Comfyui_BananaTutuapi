# Comfyui_Tutuapi

**Version: 2.0** | [中文](#chinese) | [English](#english)

---

`<a id="chinese"></a>`

## 中文

一个功能强大的ComfyUI自定义节点套装，专为Google Gemini图像生成打造，采用先进的双节点架构和全面的模板系统。

### 主要特色

- **🎯 双节点架构**：主生成节点 + 高级提示词优化节点
- **🖼️ 多图像处理**：支持最多5张图像同时输入，用于复杂的图像编辑任务
- **🌐 多平台支持**：完全兼容 ai.comfly.chat 和 OpenRouter API提供商
- **🎨 专业模板系统**：内置12个专业预设，涵盖摄影、艺术和数字设计
- **⚡ 高级提示词大师**：智能场景检测、多语言优化和风格增强
- **🔧 Base64优化**：增强的图像处理，保持质量并消除白边
- **📡 SSE流处理优化**：针对不同API提供商的实时流处理优化

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

### 节点规格说明

#### 🚀 Tutu Nano Banana (主生成节点)

**必需输入**：

- `prompt` - 文本提示词（STRING，推荐连接提示词大师输出）
- `api_provider` - API提供商选择（ai.comfly.chat / OpenRouter）
- `model` - 带提供商标签的模型选择
- `num_images` - 生成图像数量（1-4）
- `temperature` - 创造性控制（0.0-2.0，默认：1.0）
- `top_p` - 采样控制（0.0-1.0，默认：0.95）
- `timeout` - 请求超时时间（10-600秒，默认：120）

**可选输入**：

- `comfly_api_key` - ai.comfly.chat API密钥（自动保存到配置）
- `openrouter_api_key` - OpenRouter API密钥（自动保存到配置）
- `input_image_1` 到 `input_image_5` - 最多5张参考图像用于编辑任务

#### 🎨 Tutu Nano Banana Prompt Master (优化节点)

**必需输入**：

- `template_selection` - 模板系统（自定义输入 / 自动检测场景 / 保存的模板）
- `user_idea` - 您的创意概念（多行文本输入）
- `language` - 优化语言（英文优化 / 中文优化）
- `detail_level` - 质量增强级别（基础 / 专业 / 高级 / 大师级）

**可选输入**：

- `camera_control` - 摄影控制（广角镜头 / 微距拍摄 / 低角度 / 高角度 / 特写 / 中景）
- `lighting_control` - 灯光设置（工作室灯光 / 自然光 / 黄金时刻 / 戏剧性 / 柔和）
- `quality_enhancement` - 启用高级质量条款（布尔值，默认：True）
- `custom_additions` - 额外自定义条款

**节点输出：**

#### 🚀 Tutu Nano Banana 输出

- `generated_images` - 生成的图像张量（IMAGE）
- `response` - 详细的API响应和处理信息（STRING）
- `image_url` - 第一张生成图像的URL（如果可用）（STRING）

#### 🎨 提示词大师输出

- `optimized_prompt` - 增强和优化的提示词（STRING）
- `template_used` - 应用的模板信息（STRING）
- `optimization_report` - 详细的处理报告和应用的增强功能（STRING）

### 专业模板系统

#### 🎨 内置专业预设（12个模板）

我们的模板系统包括为不同创意场景精心制作的预设：

**📸 摄影预设**：

- **专业人像摄影** - 专业灯光和构图的工作室人像
- **电影级风景摄影** - 戏剧性灯光的史诗风景摄影
- **商品摄影** - 简洁呈现的商业产品摄影
- **建筑摄影** - 简洁线条的专业建筑摄影
- **美食摄影** - 完美呈现的诱人美食摄影
- **复古胶片摄影** - 怀旧氛围的经典胶片摄影

**🎨 艺术与数字预设**：

- **数字概念艺术** - 奇幻元素的高质量数字概念艺术
- **日式动漫插画** - 鲜艳色彩的日式动漫风格插画
- **古典油画** - 大师级质量的传统油画
- **水彩画** - 柔和流动色彩的精致水彩画
- **超写实渲染** - 完美细节的超真实3D渲染
- **赛博朋克未来** - 霓虹和高科技元素的未来主义赛博朋克美学

#### 模板功能特点

- **🔥 一键增强**：选择任何预设即可立即应用专业级参数
- **🧠 智能提示词融合**：模板使用 `{prompt}` 占位符与您的创意想法无缝融合
- **📏 优化长度**：所有模板优化为50字符以内，提高API效率
- **🎯 场景特定**：每个模板针对特定创意场景和艺术风格调优
- **💾 自动检测**：提示词大师可以自动检测场景类型并建议合适的模板

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

1. 加载文件夹中的示例工作流
2. 在Gemini节点中，从"预设"下拉菜单选择预设，输入您的提示词
3. 可选择上传参考图片，输入API密钥
4. 运行节点生成内容

#### 图像编辑模式

- 上传图片到任一图片输入端口即自动启用图像编辑模式
- 支持同时使用多张参考图片
- 提示词将与预设模板智能合并
- 每张参考图在上传的时候已经内部标注，你可以直接使用诸如“将图一中的兔子放在图二的桌子上，使用图三的风格，生成一张全新的图片”这样的语句。

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

#### v2.0 (当前版本 - 重大架构升级)

- **🎯 全新**: 双节点架构，配备专用提示词大师节点
- **🖼️ 全新**: 多图处理 - 最多5张图输入，智能标注，方便描述
- **🎨 增强**: 专业模板系统，12个优化预设
- **⚡ 全新**: 高级提示词大师，智能场景检测
- **🌐 全新**: 多语言优化支持（英文/中文）
- **📡 改进**: 增强SSE流处理，更好的兼容性
- **🎛️ 全新**: 高级质量控制（基础/专业/高级/大师级）
- **📸 全新**: 相机和灯光控制系统

#### v1.1

- **修复**: 节点名称冲突 - 内部使用TutuGeminiAPI
- **增强**: 统一base64图像处理，支持所有API提供商
- **修复**: 消除生成图像的白边问题
- **改进**: OpenRouter API兼容性，直接base64处理

#### v1.0

- 初始版本，核心功能发布
- 多平台API支持
- 基础预设系统
- 流式响应支持

### 教程与资源

📺 **视频教程**：

- **Bilibili**: [@zhaotutu](https://space.bilibili.com/431046154) - 详细的使用教程、工作流演示、模型训练指南等丰富内容
- **YouTube**: [@zhaotutu](https://www.youtube.com/@zhaotutu) - 英文教程和创意案例分享

📦 **工作流下载**：

- 在 [RunningHub](https://www.runninghub.ai/user-center/1936823199386537986/webapp?inviteCode=rh-v0990) 下载配套工作流
- 包含各种创意示例、高级技巧和实战案例

### 系统要求与技术栈

#### 🖥️ 系统要求

- **ComfyUI**: 最新版本
- **Python**: 3.8+ （推荐3.10+）
- **操作系统**: Windows / macOS / Linux

#### 📦 核心依赖库

```text
aiohttp              # 异步HTTP客户端
aiohttp-cors         # CORS支持
GitPython           # Git集成
numpy               # 数值计算
Pillow              # 图像处理
requests            # HTTP请求库
torch               # PyTorch深度学习框架
transformers        # Hugging Face模型库
huggingface-hub     # Hugging Face Hub集成
psutil              # 系统监控
matrix-client       # Matrix通讯协议支持
```

#### ⚙️ 节点架构

- **主节点**: `TutuGeminiAPI` (显示为 "🚀 Tutu Nano Banana")
- **辅助节点**: `TutuNanaBananaPromptMaster` (显示为 "🎨 Tutu Nano Banana Prompt Master")
- **工具函数**: `utils.py` - 专业的PIL/Tensor转换工具
- **配置管理**: `Tutuapi.json` - API密钥和设置存储
- **模板系统**: `presets.json` - 预设模板持久化存储

### 支持与反馈

如遇到问题或有功能建议，请在 [GitHub Issues](https://github.com/zhaotututu/Comfyui_Tutuapi/issues) 提交。

### 许可证

本项目基于Apache-2.0许可证开源。

### 致谢

本项目参考了 [Comfyui_Comfly](https://github.com/ainewsto/Comfyui_Comfly) 项目的部分代码实现，特此感谢原作者的优秀工作。

---

`<a id="english"></a>`

## English

A powerful ComfyUI custom node suite for Google Gemini image generation with advanced dual-node architecture and comprehensive template system.

### Features

- **🎯 Dual-Node Architecture**: Main generation node + advanced prompt optimization node
- **🖼️ Multi-Image Processing**: Supports up to 5 simultaneous image inputs for complex editing tasks
- **🌐 Multi-Platform Support**: Full compatibility with ai.comfly.chat and OpenRouter API providers
- **🎨 Professional Template System**: 12 built-in professional presets covering photography, art, and digital design
- **⚡ Advanced Prompt Master**: Intelligent scene detection, multi-language optimization, and style enhancement
- **🔧 Base64 Optimization**: Enhanced image processing with quality preservation and no white borders
- **📡 SSE Stream Processing**: Optimized real-time streaming for different API providers

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

1. Load example workflows from the folder
2. In the Gemini node, select from preset dropdown menu and input your prompt
3. Optionally upload reference images and input API keys
4. Run the node to generate content

#### Image Editing Mode

- Upload images to any image input port to automatically enable image editing mode
- Support simultaneous use of multiple reference images
- Prompts intelligently merge with preset templates
- Each reference image is internally labeled upon upload, allowing you to use instructions like "Place the rabbit from image 1 on the table from image 2, using the style of image 3, to generate a new image"

#### Text-to-Image Mode

- Automatically uses text-to-image mode when no images are uploaded
- System automatically adds size and quality optimization prompts
- Supports generating 1-4 different images

### Node Specifications

#### 🚀 Tutu Nano Banana (Main Generation Node)

**Required Inputs**:

- `prompt` - Text prompt (STRING, force input from Prompt Master recommended)
- `api_provider` - API provider selection (ai.comfly.chat / OpenRouter)
- `model` - Model selection with provider tags
- `num_images` - Number of images to generate (1-4)
- `temperature` - Creativity control (0.0-2.0, default: 1.0)
- `top_p` - Sampling control (0.0-1.0, default: 0.95)
- `timeout` - Request timeout (10-600 seconds, default: 120)

**Optional Inputs**:

- `comfly_api_key` - ai.comfly.chat API key (auto-saves to config)
- `openrouter_api_key` - OpenRouter API key (auto-saves to config)
- `input_image_1` to `input_image_5` - Up to 5 reference images for editing tasks

#### 🎨 Tutu Nano Banana Prompt Master (Optimization Node)

**Required Inputs**:

- `template_selection` - Template system (Custom Input / Auto Detect Scene / Saved Templates)
- `user_idea` - Your creative concept (multiline text input)
- `language` - Optimization language (English / Chinese)
- `detail_level` - Quality enhancement level (Basic / Professional / Premium / Masterpiece)

**Optional Inputs**:

- `camera_control` - Photography controls (Wide-angle / Macro / Low-angle / High-angle / Close-up / Medium Shot)
- `lighting_control` - Lighting setup (Studio / Natural / Golden Hour / Dramatic / Soft)
- `quality_enhancement` - Enable advanced quality terms (Boolean, default: True)
- `custom_additions` - Additional custom terms

**Node Outputs:**

#### 🚀 Tutu Nano Banana Outputs

- `generated_images` - Generated image tensor (IMAGE)
- `response` - Detailed API response with processing info (STRING)
- `image_url` - First generated image URL if available (STRING)

#### 🎨 Prompt Master Outputs

- `optimized_prompt` - Enhanced and optimized prompt (STRING)
- `template_used` - Applied template information (STRING)
- `optimization_report` - Detailed processing report with applied enhancements (STRING)

### Professional Template System

#### 🎨 Built-in Professional Presets (12 Templates)

Our template system includes carefully crafted presets optimized for different creative scenarios:

**📸 Photography Presets:**

- **Professional Portrait** - Studio portrait with professional lighting and composition
- **Cinematic Landscape** - Epic landscape photography with dramatic lighting
- **Product Photography** - Commercial product photography with clean presentation
- **Architectural Photography** - Professional architectural photography with clean lines
- **Gourmet Food Photography** - Appetizing food photography with perfect presentation
- **Vintage Film Photography** - Classic film photography with nostalgic atmosphere

**🎨 Art & Digital Presets:**

- **Digital Concept Art** - High-quality digital concept art with fantasy elements
- **Anime Style Art** - Japanese anime-style illustration with vibrant colors
- **Classical Oil Painting** - Traditional oil painting with masterpiece quality
- **Watercolor Painting** - Delicate watercolor painting with soft, flowing colors
- **Photorealistic Render** - Ultra-realistic 3D rendering with perfect detail
- **Cyberpunk Future** - Futuristic cyberpunk aesthetic with neon and high-tech elements

#### Template Features

- **🔥 One-Click Enhancement**: Select any preset to instantly apply professional-grade parameters
- **🧠 Smart Prompt Integration**: Templates use `{prompt}` placeholders to seamlessly merge with your creative ideas
- **📏 Optimized Length**: All templates optimized to stay under 50 characters for API efficiency
- **🎯 Scene-Specific**: Each template tuned for specific creative scenarios and art styles
- **💾 Auto-Detection**: Prompt Master can automatically detect scene type and suggest appropriate templates

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

#### v2.0 (Current - Major Architecture Update)

- **🎯 NEW**: Dual-node architecture with dedicated Prompt Master node
- **🖼️ NEW**: Multi-image processing - supports up to 5 simultaneous image inputs
- **🎨 ENHANCED**: Professional template system with 12 optimized presets
- **⚡ NEW**: Advanced Prompt Master with intelligent scene detection
- **🌐 NEW**: Multi-language optimization support (English/Chinese)
- **📡 IMPROVED**: Enhanced SSE stream processing for better compatibility
- **🔧 OPTIMIZED**: Base64 image processing with quality preservation
- **💾 NEW**: Persistent template system with auto-save functionality
- **🎛️ NEW**: Advanced quality controls (Basic/Professional/Premium/Masterpiece levels)
- **📸 NEW**: Camera and lighting control systems

#### v1.1

- **Fixed**: Node name conflicts - uses TutuGeminiAPI internally
- **Enhanced**: Unified base64 image processing for all API providers
- **Fixed**: Eliminated white borders on generated images
- **Improved**: OpenRouter API compatibility with direct base64 processing

#### v1.0

- Initial release with core functionality
- Multi-platform API support
- Basic preset system
- Streaming response support

### Tutorials & Resources

📺 **Video Tutorials**:

- **Bilibili**: [@zhaotutu](https://space.bilibili.com/431046154) - Comprehensive tutorials, workflow demonstrations, and model training guides (Chinese)
- **YouTube**: [@zhaotutu](https://www.youtube.com/@zhaotutu) - Step-by-step guides and use cases

📦 **Workflow Gallery**:

- Download ready-to-use workflows at [RunningHub](https://www.runninghub.ai/user-center/1936823199386537986/webapp?inviteCode=rh-v0990)
- Includes various creative examples and advanced techniques

### System Requirements & Technical Stack

#### 🖥️ System Requirements

- **ComfyUI**: Latest version
- **Python**: 3.8+ (recommended 3.10+)
- **Operating System**: Windows / macOS / Linux

#### 📦 Core Dependencies

```text
aiohttp              # Async HTTP client
aiohttp-cors         # CORS support
GitPython           # Git integration
numpy               # Numerical computing
Pillow              # Image processing
requests            # HTTP request library
torch               # PyTorch deep learning framework
transformers        # Hugging Face model library
huggingface-hub     # Hugging Face Hub integration
psutil              # System monitoring
matrix-client       # Matrix communication protocol support
```

#### ⚙️ Node Architecture

- **Main Node**: `TutuGeminiAPI` (displays as "🚀 Tutu Nano Banana")
- **Assistant Node**: `TutuNanaBananaPromptMaster` (displays as "🎨 Tutu Nano Banana Prompt Master")
- **Utility Functions**: `utils.py` - Professional PIL/Tensor conversion tools
- **Configuration Management**: `Tutuapi.json` - API key and settings storage
- **Template System**: `presets.json` - Preset template persistence storage

### Support & Feedback

For issues or feature suggestions, please submit at [GitHub Issues](https://github.com/zhaotututu/Comfyui_Tutuapi/issues).

### License

This project is open source under the Apache-2.0 license.

### Acknowledgments

This project references some code implementations from the [Comfyui_Comfly](https://github.com/ainewsto/Comfyui_Comfly) project. Special thanks to the original authors for their excellent work.
