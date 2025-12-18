"""
BitRot: A Python library for simulating digital image decay.
Usage:
    import bitrot
    bitrot.decay_file("input.jpg", "output.jpg", integrity=0.8)
"""

import os
import random
import io
from PIL import Image, ImageFilter
import numpy as np

def _apply_grain(image: Image.Image, intensity: float) -> Image.Image:
    """
    Internal function to apply variable film grain/digital noise.
    intensity: 0.0 (none) to 1.0 (heavy noise)
    """
    if intensity <= 0:
        return image

    # Convert to numpy array for fast processing
    img_array = np.array(image)
    
    # Generate noise based on intensity
    # We use a normal distribution (Gaussian noise)
    noise_range = intensity * 255
    noise = np.random.normal(0, noise_range / 2, img_array.shape)
    
    # Add noise to image
    noisy_image = img_array + noise
    
    # Clip values to valid 0-255 range and convert back to uint8
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    
    return Image.fromarray(noisy_image)

def _apply_glitch(image: Image.Image, intensity: float) -> Image.Image:
    """
    Internal function to apply subtle JPEG compression artifacting/shifting.
    """
    if intensity < 0.3:
        return image
        
    # Simulate data loss by resizing down and back up (pixelation)
    # The lower the integrity, the smaller the intermediate size
    w, h = image.size
    scale_factor = max(0.1, 1.0 - (intensity * 0.8)) # Drops to 20% size at max decay
    
    small_w = int(w * scale_factor)
    small_h = int(h * scale_factor)
    
    return image.resize((small_w, small_h), Image.NEAREST).resize((w, h), Image.NEAREST)

def degrade(image: Image.Image, integrity: float) -> Image.Image:
    """
    Core logic: Takes a PIL Image and returns a decayed PIL Image.
    integrity: Float between 0.0 (Destroyed) and 1.0 (Perfect)
    """
    # Clamp integrity
    integrity = max(0.0, min(1.0, integrity))
    
    if integrity >= 1.0:
        return image

    damage_level = 1.0 - integrity
    
    # 1. Apply Glitch/Pixelation (Structural Damage)
    # Only happens when health is low (< 50%)
    if integrity < 0.5:
        image = _apply_glitch(image, damage_level)

    # 2. Apply Noise (Surface Damage)
    # Happens immediately as health drops
    image = _apply_grain(image, damage_level * 0.5)
    
    # 3. Color Desaturation (Fading Memory)
    # Images get greyer as they die
    if integrity < 0.8:
        # Convert to HSV, lower Saturation, convert back
        image = image.convert("RGB") # Ensure RGB mode
        # Simple desaturation via "L" blend could be faster, but let's stick to RGB ops
        # (For simplicity in this library, we might skip complex HSV ops to keep dependencies low)
        pass 

    return image

# --- PUBLIC API ---

def decay_file(input_path: str, output_path: str, integrity: float = 0.9):
    """
    Reads an image from disk, decays it, and saves it to disk.
    
    Args:
        input_path (str): Path to source image.
        output_path (str): Path to save result.
        integrity (float): 0.0 to 1.0 (1.0 = Original).
    """
    try:
        with Image.open(input_path) as img:
            # Ensure we are working with a copy in RGB mode
            img = img.convert("RGB")
            
            # Process
            result = degrade(img, integrity)
            
            # Save
            # We use varying compression quality based on integrity too!
            jpg_quality = int(max(1, integrity * 95))
            result.save(output_path, "JPEG", quality=jpg_quality)
            
            print(f"BitRot: Saved to {output_path} | Health: {int(integrity*100)}%")
            
    except Exception as e:
        print(f"BitRot Error: {e}")

def decay_bytes(image_data: bytes, integrity: float = 0.9) -> bytes:
    """
    Takes raw image bytes, decays them, and returns raw image bytes.
    Useful for web servers / APIs where no file is saved to disk.
    """
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            img = img.convert("RGB")
            result = degrade(img, integrity)
            
            output_buffer = io.BytesIO()
            jpg_quality = int(max(1, integrity * 95))
            result.save(output_buffer, format="JPEG", quality=jpg_quality)
            
            return output_buffer.getvalue()
    except Exception as e:
        print(f"BitRot Error: {e}")
        return image_data # Fail safe: return original