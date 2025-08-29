"""
🎨 Tutu Nano Banana Prompt Master v2.0
Unified Template System with Advanced Management

Author: Tutu API Team  
Version: 2.0.0 - Unified Architecture
"""

import re
import json
import os
from datetime import datetime

# ======================== Template Management Functions ========================

def get_presets_file():
    """Get the path to presets file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "presets.json")

def load_templates():
    """Load all templates from file"""
    try:
        with open(get_presets_file(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[Prompt Master] Template file not found, using empty config")
        return {"gemini": []}
    except json.JSONDecodeError:
        print("[Prompt Master] Template file format error, using default config")
        return {"gemini": []}

# Template saving functionality removed for simplicity

def get_template_options():
    """Get template options for dropdown"""
    try:
        templates = load_templates()
        gemini_templates = templates.get("gemini", [])
        
        # Start with built-in options
        options = ["Custom Input", "Auto Detect Scene"]
        
        # Add saved templates
        for template in gemini_templates:
            options.append(template["name"])
            
        return options
    except:
        return ["Custom Input", "Auto Detect Scene"]

def get_template_by_name(name):
    """Get template by name"""
    if name in ["Custom Input", "Auto Detect Scene"]:
        return None
        
    try:
        templates = load_templates()
        for template in templates.get("gemini", []):
            if template["name"] == name:
                return template
        return None
    except:
        return None

# Template management functions removed - keeping system simple and focused

# ======================== Auto Detection System ========================

def detect_scene_type(prompt_text):
    """Intelligently detect scene type from prompt"""
    prompt_lower = prompt_text.lower()
    
    detection_map = {
        "Professional Portrait": [
            "person", "man", "woman", "face", "portrait", "headshot", "profile", 
            "character", "people", "human", "model", "actor", "celebrity"
        ],
        "Cinematic Landscape": [
            "landscape", "mountain", "forest", "ocean", "beach", "sky", "sunset", 
            "sunrise", "nature", "outdoor", "scenery", "vista", "horizon"
        ],
        "Product Photography": [
            "product", "bottle", "phone", "car", "watch", "jewelry", "gadget", 
            "device", "object", "item", "commercial", "brand"
        ],
        "Digital Concept Art": [
            "fantasy", "dragon", "magic", "wizard", "castle", "sci-fi", "alien", 
            "spaceship", "futuristic", "concept", "creature", "mythical"
        ],
        "Anime Style Art": [
            "anime", "manga", "kawaii", "chibi", "japanese", "otaku", "waifu", 
            "cartoon", "animated", "character design"
        ],
        "Architectural Photography": [
            "building", "architecture", "house", "tower", "bridge", "city", 
            "urban", "structure", "construction", "skyscraper"
        ],
        "Gourmet Food Photography": [
            "food", "dish", "meal", "restaurant", "cooking", "recipe", "cuisine", 
            "delicious", "tasty", "gourmet", "chef"
        ]
    }
    
    # Score each category
    scores = {}
    for category, keywords in detection_map.items():
        score = sum(1 for keyword in keywords if keyword in prompt_lower)
        if score > 0:
            scores[category] = score
    
    # Return highest scoring category or None
    if scores:
        best_match = max(scores, key=scores.get)
        return best_match
    
    return None

# ======================== Optimization Functions ========================

class PromptOptimizer:
    """Advanced prompt optimization system"""
    
    def __init__(self, language="English Optimization"):
        self.language = language
        self.setup_optimization_data()
    
    def setup_optimization_data(self):
        """Setup optimization data based on official guidelines"""
        
        # Quality enhancement terms - categorized by art style
        self.quality_terms = {
            "English": {
                "basic": ["high quality", "detailed"],
                "professional": ["highly detailed", "professional quality", "exceptional detail"],
                "premium": ["studio-quality", "award-winning", "masterpiece"],
                # Photography-specific terms
                "photography": ["commercial photography", "professional photography", "studio photography"],
                # Art-specific terms
                "painting": ["artistic mastery", "fine art quality", "gallery-worthy"],
                "illustration": ["professional illustration", "high-end artwork", "publication quality"],
                "digital_art": ["digital mastery", "professional rendering", "high-resolution artwork"]
            },
            "Chinese": {
                "basic": ["高质量", "详细"],
                "professional": ["高度详细", "专业品质", "卓越细节"],
                "premium": ["工作室品质", "获奖作品", "杰作"],
                # Photography-specific terms
                "photography": ["商业摄影级别", "专业摄影", "工作室摄影"],
                # Art-specific terms
                "painting": ["艺术大师级", "美术馆品质", "收藏级作品"],
                "illustration": ["专业插画", "高端艺术品", "出版级质量"],
                "digital_art": ["数字艺术大师级", "专业渲染", "高分辨率艺术品"]
            }
        }
        
        # Camera control terms
        self.camera_terms = {
            "wide_angle": {"English": "wide-angle shot", "Chinese": "广角镜头拍摄"},
            "macro": {"English": "macro photography", "Chinese": "微距摄影"},
            "low_angle": {"English": "low-angle perspective", "Chinese": "低角度视角"},
            "high_angle": {"English": "high-angle shot", "Chinese": "高角度俯拍"},
            "close_up": {"English": "close-up composition", "Chinese": "特写构图"},
            "medium_shot": {"English": "medium shot framing", "Chinese": "中景构图"}
        }
        
        # Lighting control terms  
        self.lighting_terms = {
            "studio": {"English": "professional studio lighting", "Chinese": "专业工作室灯光"},
            "natural": {"English": "natural lighting", "Chinese": "自然光照明"},
            "golden": {"English": "golden hour lighting", "Chinese": "黄金时刻光线"},
            "dramatic": {"English": "dramatic lighting", "Chinese": "戏剧性照明"},
            "soft": {"English": "soft lighting", "Chinese": "柔和照明"}
        }
    
    def detect_art_style(self, prompt, template_name="Custom Input"):
        """Detect art style from prompt and template to choose appropriate quality terms"""
        prompt_lower = prompt.lower()
        template_lower = template_name.lower()
        
        # Photography styles
        photography_keywords = ["photography", "photo", "portrait", "product", "commercial", "studio", "camera", "lens"]
        if any(keyword in template_lower or keyword in prompt_lower for keyword in photography_keywords):
            return "photography"
        
        # Painting styles
        painting_keywords = ["painting", "oil", "watercolor", "acrylic", "canvas", "brush", "paint", "classical"]
        if any(keyword in template_lower or keyword in prompt_lower for keyword in painting_keywords):
            return "painting"
            
        # Illustration styles
        illustration_keywords = ["illustration", "anime", "cartoon", "comic", "manga", "character design", "concept art"]
        if any(keyword in template_lower or keyword in prompt_lower for keyword in illustration_keywords):
            return "illustration"
            
        # Digital art styles
        digital_keywords = ["digital", "render", "3d", "cgi", "computer", "photorealistic", "artstation"]
        if any(keyword in template_lower or keyword in prompt_lower for keyword in digital_keywords):
            return "digital_art"
            
        # Default to general terms if no specific style detected
        return "premium"
    
    def add_quality_enhancement(self, prompt, level="professional", template_name="Custom Input"):
        """Add style-appropriate quality enhancement terms"""
        lang_key = "English" if self.language == "English Optimization" else "Chinese"
        
        # Detect art style to choose appropriate quality terms
        art_style = self.detect_art_style(prompt, template_name)
        
        # Choose quality terms based on level and art style
        if level == "Masterpiece Level":
            # For masterpiece level, use style-specific terms when available
            if art_style in self.quality_terms[lang_key]:
                # Use style-specific premium terms
                style_terms = self.quality_terms[lang_key][art_style][:1]  # Take 1 style-specific term
                general_terms = self.quality_terms[lang_key]["premium"][:1]  # Take 1 general premium term
                quality_list = style_terms + general_terms
            else:
                # Fallback to premium general terms
                quality_list = self.quality_terms[lang_key]["premium"]
        else:
            # Use general quality terms for other levels
            quality_list = self.quality_terms[lang_key].get(level, self.quality_terms[lang_key]["professional"])
        
        enhancements = []
        for term in quality_list[:2]:  # Add first 2 terms
            if term.lower() not in prompt.lower():
                prompt += f", {term}"
                enhancements.append(f"Added quality term: {term} (style: {art_style})")
        
        return prompt, enhancements
    
    def add_camera_control(self, prompt, camera_type):
        """Add camera control terms"""
        if camera_type == "Auto Select":
            return prompt, []
            
        lang_key = "English" if self.language == "English Optimization" else "Chinese"
        
        camera_map = {
            "Wide-angle Lens": "wide_angle",
            "Macro Shot": "macro", 
            "Low-angle Perspective": "low_angle",
            "High-angle Shot": "high_angle",
            "Close-up Shot": "close_up",
            "Medium Shot": "medium_shot"
        }
        
        camera_key = camera_map.get(camera_type)
        if camera_key and camera_key in self.camera_terms:
            term = self.camera_terms[camera_key][lang_key]
            if term.lower() not in prompt.lower():
                prompt += f", {term}"
                return prompt, [f"Added camera control: {term}"]
        
        return prompt, []
    
    def add_lighting_control(self, prompt, lighting_type):
        """Add lighting control terms"""
        if lighting_type == "Auto Select":
            return prompt, []
            
        lang_key = "English" if self.language == "English Optimization" else "Chinese"
        
        lighting_map = {
            "Studio Lighting": "studio",
            "Natural Lighting": "natural",
            "Golden Hour": "golden",
            "Dramatic Lighting": "dramatic", 
            "Soft Lighting": "soft"
        }
        
        lighting_key = lighting_map.get(lighting_type)
        if lighting_key and lighting_key in self.lighting_terms:
            term = self.lighting_terms[lighting_key][lang_key]
            if term.lower() not in prompt.lower():
                prompt += f", {term}"
                return prompt, [f"Added lighting control: {term}"]
                
        return prompt, []
    
    def clean_prompt(self, prompt):
        """Clean and format prompt"""
        # Remove extra commas and spaces
        cleaned = re.sub(r'\s*,\s*,\s*', ', ', prompt)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned

# ======================== Main Node Class ========================

class TutuNanaBananaPromptMaster:
    """
    🎨 Unified Template System v2.0
    Advanced prompt optimization with integrated template management
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "template_selection": (get_template_options(), {
                    "default": "Custom Input",
                    "tooltip": "Select template: Custom Input (no template), Auto Detect (smart detection), or saved templates"
                }),
                "user_idea": ("STRING", {
                    "multiline": True, 
                    "default": "",
                    "placeholder": "Enter your creative idea here..."
                }),
                "language": ([
                    "English Optimization",
                    "Chinese Optimization"
                ], {"default": "English Optimization"}),
                "detail_level": ([
                    "Basic Detail",
                    "Professional Detail", 
                    "Premium Quality",
                    "Masterpiece Level"
                ], {"default": "Professional Detail"}),
            },
            "optional": {
                "camera_control": ([
                    "Auto Select",
                    "Wide-angle Lens",
                    "Macro Shot",
                    "Low-angle Perspective", 
                    "High-angle Shot",
                    "Close-up Shot",
                    "Medium Shot"
                ], {"default": "Auto Select"}),
                "lighting_control": ([
                    "Auto Select",
                    "Studio Lighting",
                    "Natural Lighting",
                    "Golden Hour",
                    "Dramatic Lighting",
                    "Soft Lighting"
                ], {"default": "Auto Select"}),
                "quality_enhancement": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Enable Quality Enhancement", 
                    "label_off": "Basic Quality Only"
                }),
                "custom_additions": ("STRING", {
                    "default": "",
                    "placeholder": "Additional custom terms (optional)..."
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("optimized_prompt", "template_used", "optimization_report") 
    FUNCTION = "process_prompt"
    CATEGORY = "Tutu"

    def process_prompt(self, template_selection, user_idea, language, detail_level,
                      camera_control="Auto Select", lighting_control="Auto Select", 
                      quality_enhancement=True, custom_additions=""):
        """
        Main processing function - New unified logic:
        1. Select Template → 2. Optimize Prompt → 3. Combine → 4. Output
        """
        
        print(f"\n[Prompt Master] 🎨 ========== Processing Started ==========")
        print(f"[Prompt Master] 📝 User Input: {user_idea}")
        print(f"[Prompt Master] 🎯 Template: {template_selection}")
        print(f"[Prompt Master] 🌐 Language: {language}")
        print(f"[Prompt Master] 📊 Detail Level: {detail_level}")
        
        # Validate input
        if not user_idea.strip():
            return "Please enter your creative idea", "No Template", "Error: Empty input"
        
        original_input = user_idea.strip()
        optimization_log = []
        
        # ======================== Step 1: Template Selection ========================
        selected_template = None
        template_name = "Custom Input"
        
        if template_selection == "Custom Input":
            # No template, use raw input
            optimized_prompt = original_input
            template_name = "Custom Input"
            print(f"[Prompt Master] 📝 Using custom input (no template)")
            
        elif template_selection == "Auto Detect Scene":
            # Auto detect and apply template
            detected_type = detect_scene_type(original_input)
            if detected_type:
                template = get_template_by_name(detected_type)
                if template:
                    selected_template = template
                    template_name = f"Auto: {detected_type}"
                    print(f"[Prompt Master] 🔍 Auto-detected: {detected_type}")
                else:
                    optimized_prompt = original_input
                    template_name = "Auto: No Match"
                    print(f"[Prompt Master] 🔍 Auto-detected {detected_type}, but template not found")
            else:
                optimized_prompt = original_input
                template_name = "Auto: No Detection"
                print(f"[Prompt Master] 🔍 No scene type detected, using raw input")
        else:
            # Use selected template
            template = get_template_by_name(template_selection)
            if template:
                selected_template = template
                template_name = template_selection
                print(f"[Prompt Master] 📋 Using template: {template_selection}")
            else:
                optimized_prompt = original_input
                template_name = "Template Not Found"
                print(f"[Prompt Master] ❌ Template '{template_selection}' not found")
        
        # ======================== Step 2: Prompt Optimization ========================
        
        # Initialize optimizer
        optimizer = PromptOptimizer(language)
        
        # Apply optimizations to user input
        working_prompt = original_input
        
        # Add quality enhancement
        if quality_enhancement:
            quality_level = {
                "Basic Detail": "basic",
                "Professional Detail": "professional", 
                "Premium Quality": "premium",
                "Masterpiece Level": "Masterpiece Level"
            }.get(detail_level, "professional")
            
            working_prompt, quality_log = optimizer.add_quality_enhancement(working_prompt, quality_level, template_name)
            optimization_log.extend(quality_log)
        
        # Add camera control
        working_prompt, camera_log = optimizer.add_camera_control(working_prompt, camera_control)
        optimization_log.extend(camera_log)
        
        # Add lighting control
        working_prompt, lighting_log = optimizer.add_lighting_control(working_prompt, lighting_control)
        optimization_log.extend(lighting_log)
        
        # Add custom additions
        if custom_additions.strip():
            working_prompt += f", {custom_additions.strip()}"
            optimization_log.append(f"Added custom terms: {custom_additions.strip()}")
        
        # Clean the optimized prompt
        working_prompt = optimizer.clean_prompt(working_prompt)
        
        # ======================== Step 3: Template Combination ========================
        
        if selected_template:
            # Apply template with optimized prompt
            template_text = selected_template["config"]["prompt_template"]
            if "{prompt}" in template_text:
                final_prompt = template_text.replace("{prompt}", working_prompt)
            else:
                final_prompt = f"{template_text}, {working_prompt}"
            optimization_log.append(f"Applied template: {template_name}")
        else:
            # No template, use optimized prompt directly
            final_prompt = working_prompt
        
        # Final cleanup
        final_prompt = optimizer.clean_prompt(final_prompt)
        
        # ======================== Generate Report ========================
        
        report = self.generate_report(
            original_input, final_prompt, template_name, optimization_log, language
        )
        
        print(f"[Prompt Master] ✅ Processing completed")
        print(f"[Prompt Master] 📏 Output length: {len(final_prompt)} characters")
        print(f"[Prompt Master] 🎨 ========== Processing Finished ==========\n")
        
        return final_prompt, template_name, report
    
    def generate_report(self, original, final, template_name, log, language):
        """Generate detailed processing report"""
        report = f"""🎨 Prompt Master Processing Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Original input length: {len(original)} characters
🎯 Template used: {template_name}
📏 Final output length: {len(final)} characters
📈 Growth: {len(final) - len(original)} characters

🛠️ Applied optimizations:
{chr(10).join([f"• {item}" for item in log]) if log else "• No specific optimizations applied"}

⭐ Unified template system - seamless integration
🕒 Processing time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report

# ======================== Node Registration ========================

NODE_CLASS_MAPPINGS = {
    "TutuNanaBananaPromptMaster": TutuNanaBananaPromptMaster
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TutuNanaBananaPromptMaster": "🎨 Tutu Nano Banana Prompt Master"
}
