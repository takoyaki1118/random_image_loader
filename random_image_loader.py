import os
import random
from PIL import Image
import numpy as np
import torch
import folder_paths # ComfyUIのヘルパーライブラリ

class LoadRandomImageFromInput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "subfolder": ("STRING", {"default": "", "multiline": False, "dynamicPrompts": False, "placeholder": "例: my_images/landscapes"}),
                "extensions": ("STRING", {"default": ".png,.jpg,.jpeg,.webp", "multiline": False, "dynamicPrompts": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING") # 読み込んだ画像と、そのファイル名を返します
    RETURN_NAMES = ("image", "filename")
    FUNCTION = "load_random_image"
    CATEGORY = "image/loaders" # カテゴリは適宜変更してください

    def load_random_image(self, seed, subfolder, extensions):
        input_base_dir = folder_paths.get_input_directory()
        
        if subfolder:
            # サブフォルダパスの先頭や末尾のスラッシュ/バックスラッシュを正規化
            subfolder = subfolder.strip("/\\")
            image_dir = os.path.join(input_base_dir, subfolder)
        else:
            image_dir = input_base_dir

        if not os.path.isdir(image_dir):
            error_message = f"Error: Directory not found: {image_dir}"
            print(f"[LoadRandomImageFromInput] {error_message}")
            # エラー時は空のテンソルとエラーメッセージを返す
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), error_message)

        valid_extensions = [ext.strip().lower() for ext in extensions.split(',') if ext.strip()]
        if not valid_extensions:
            error_message = "Error: No valid file extensions provided. Please provide a comma-separated list like '.png,.jpg'."
            print(f"[LoadRandomImageFromInput] {error_message}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), error_message)

        image_files = []
        try:
            for f_name in os.listdir(image_dir):
                if os.path.isfile(os.path.join(image_dir, f_name)):
                    if any(f_name.lower().endswith(ext) for ext in valid_extensions):
                        image_files.append(f_name)
        except OSError as e:
            error_message = f"Error listing files in '{image_dir}': {e}"
            print(f"[LoadRandomImageFromInput] {error_message}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), error_message)

        if not image_files:
            error_message = f"No images found in '{image_dir}' with extensions: {', '.join(valid_extensions)}"
            print(f"[LoadRandomImageFromInput] {error_message}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), error_message)

        # シードを設定してランダム選択の再現性を確保
        random.seed(seed)
        selected_filename = random.choice(image_files)
        image_path = os.path.join(image_dir, selected_filename)

        try:
            img = Image.open(image_path)
            
            # RGBAやPモードなどの画像をRGBに変換
            if img.mode == 'RGBA' or img.mode == 'LA' or (img.mode == 'P' and 'transparency' in img.info):
                # アルファチャンネルを持つ可能性のある画像を処理
                # 透明部分を白で塗りつぶす場合 (ComfyUIの標準LoadImageはこうなっているはず)
                img_rgb = Image.new("RGB", img.size, (255, 255, 255))
                img_rgb.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' or img.mode == 'LA' else None)
                img = img_rgb
            elif img.mode != 'RGB':
                img = img.convert("RGB")

            image_np = np.array(img).astype(np.float32) / 255.0  # 値を0.0-1.0に正規化
            image_tensor = torch.from_numpy(image_np)[None,]     # バッチ次元を追加 (1, H, W, C)
            
            print(f"[LoadRandomImageFromInput] Loaded: {selected_filename} (from {image_dir})")
            return (image_tensor, selected_filename)
        except Exception as e:
            error_message = f"Error loading image '{image_path}': {e}"
            print(f"[LoadRandomImageFromInput] {error_message}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), error_message)

# ComfyUIにノードを登録するためのマッピング
NODE_CLASS_MAPPINGS = {
    "LoadRandomImageFromInput_Shin": LoadRandomImageFromInput # クラス名をユニークにするためサフィックス追加を推奨
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadRandomImageFromInput_Shin": "Load Random Image (Input Folder)"
}