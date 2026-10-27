# -*- coding: utf-8 -*-
"""
ThaiD LINE Sticker AI Engine
Combines:
1. Google Flow Cloud REST Engine (from yayni.com in C:\\NV, Ports 9222 / 9223)
2. Flux Turbo High-Speed REST Engine (Instant generation)
3. Native LINE Sticker Processor (Auto-matting, white stroke border, official LINE specs)
4. Comprehensive Thai Caption Library (530+ Curated Captions across 12 categories)
"""

import os
import re
import sys
import time
import json
import uuid
import random
import urllib.parse
import urllib.request
import subprocess
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

import line_sticker_processor as lsp
import caption_library as cl

SSH_KEY = r"C:\NV\oracle_key.pem"
REMOTE_FLOW_HOST = "129.221.220.121"

def build_sticker_prompt(
    character_desc: str,
    caption: str = "",
    pose_prompt: str = "",
    art_style: str = "chibi_3d",
    with_thai_text: bool = True
) -> str:
    """Builds an optimized prompt for high-consistency LINE sticker generation."""
    style_keywords = {
        "chibi_3d": "cute 3D Pixar Disney style chibi character, vibrant clay render, soft ambient lighting, smooth glossy surface",
        "cute_2d": "cute Japanese chibi 2D anime sticker style, clean vector lineart, bold expressive outlines, cel shaded",
        "kawaii_doodle": "minimal kawaii hand-drawn doodle sticker, cheerful bold rounded outlines, pastel flat colors",
        "retro_pixel": "chibi 16-bit retro arcade pixel art sticker, crisp borders, nostalgic game sprite",
        "watercolor": "soft watercolor storybook chibi illustration, pastel color palette, gentle hand-painted texture"
    }

    selected_style = style_keywords.get(art_style, style_keywords["chibi_3d"])
    
    # Prompt construction
    prompt_parts = [
        f"A standalone LINE sticker of {character_desc}",
        selected_style,
        pose_prompt if pose_prompt else "cute happy expression, energetic pose",
        "die-cut sticker border, solid plain white background, isolated on pure white background for clean cutout",
        "centered composition, full body visible, masterpiece, highest quality, crisp sharp details, 8k"
    ]

    if with_thai_text and caption:
        prompt_parts.append(f"glossy 3D Thai typography badge reading '{caption}' placed naturally next to character")

    return ", ".join(prompt_parts)


def generate_via_flow_rest(prompt: str, output_path: str, lane: int = 9222, timeout: int = 90) -> Optional[str]:
    """Generates image using Google Flow REST service running on yayni server (129.221.220.121)."""
    try:
        payload = json.dumps({"prompt": prompt, "timeout": timeout}).encode("utf-8")
        
        # When running on Windows host, we can query via SSH tunnel or direct curl on remote
        if os.name == "nt":
            ssh_cmd = [
                "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", f"ubuntu@{REMOTE_FLOW_HOST}",
                f"""curl -s -X POST -H "Content-Type: application/json" -d '{json.dumps({"prompt": prompt, "timeout": timeout})}' http://127.0.0.1:{lane}/generate"""
            ]
            p = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = p.communicate(timeout=timeout + 30)
            res = json.loads(stdout)
        else:
            # Running directly on remote/docker network
            req = urllib.request.Request(
                f"http://127.0.0.1:{lane}/generate",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout + 15) as resp:
                res = json.loads(resp.read().decode("utf-8"))

        if res.get("ok"):
            img_url = res.get("image_url") or res.get("local_url")
            if img_url and img_url.startswith("http"):
                # Download image
                dl_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://flow.google.com/"})
                with urllib.request.urlopen(dl_req, timeout=30) as dresp:
                    with open(output_path, "wb") as f:
                        f.write(dresp.read())
                return output_path
            elif res.get("local_path"):
                # SCP from remote server if needed
                remote_path = res["local_path"]
                scp_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", f"ubuntu@{REMOTE_FLOW_HOST}:{remote_path}", output_path]
                subprocess.run(scp_cmd, timeout=30, check=True)
                return output_path
    except Exception as e:
        print(f"[FlowREST] Error generating with Flow: {e}")
    return None


def generate_via_flux_rest(prompt: str, output_path: str, width: int = 768, height: int = 768) -> Optional[str]:
    """Generates high-res image via Flux / Turbo REST API in 4-8 seconds."""
    safe_prompt = urllib.parse.quote(prompt)
    seed = random.randint(100000, 9999999)
    
    urls = [
        f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&model=flux&nologo=true&seed={seed}",
        f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&model=turbo&nologo=true&seed={seed}",
        f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&nologo=true&seed={seed}"
    ]

    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = resp.read()
                if len(data) > 5000:
                    with open(output_path, "wb") as f:
                        f.write(data)
                    return output_path
        except Exception as e:
            print(f"[FluxREST] Retrying alternate model due to: {e}")
            time.sleep(1.0)
    return None


def generate_single_sticker(
    prompt: str,
    output_raw_path: str,
    output_processed_path: str,
    engine: str = "flux",
    tolerance: int = 22,
    white_stroke: bool = True
) -> Dict[str, Any]:
    """
    End-to-end generator:
    1. Generates raw image via requested REST API (Flow or Flux)
    2. Runs 5-step LINE matting and specification processing
    """
    t0 = time.time()
    raw_file = None

    if engine == "flow":
        raw_file = generate_via_flow_rest(prompt, output_raw_path)
        if not raw_file:
            print("[Engine] Flow failed or timed out, falling back to Flux Turbo REST...")
            raw_file = generate_via_flux_rest(prompt, output_raw_path)
    else:
        raw_file = generate_via_flux_rest(prompt, output_raw_path)

    if not raw_file or not os.path.exists(raw_file):
        raise RuntimeError("Failed to generate raw sticker image")

    # Run LINE Sticker Processing Pipeline
    raw_img = Image.open(raw_file)
    processed_img = lsp.process_sticker_image_pipeline(
        raw_img,
        target_type="sticker",
        tolerance=tolerance,
        choke=1.2,
        feather=0.8,
        margin=10,
        white_stroke=white_stroke,
        stroke_width=4
    )
    processed_img.save(output_processed_path, format="PNG")

    elapsed = round(time.time() - t0, 2)
    return {
        "ok": True,
        "elapsed": elapsed,
        "raw_path": output_raw_path,
        "processed_path": output_processed_path,
        "dimensions": processed_img.size
    }


def create_line_package(
    project_id: str,
    sticker_images: List[str],
    package_type: str = "standard",
    title: str = "ThaiD LINE Sticker Set"
) -> str:
    """Packages all stickers + main.png (240x240) + tab.png (96x74) into official LINE ZIP."""
    import shutil
    project_dir = os.path.join(OUTPUT_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    zip_path = os.path.join(project_dir, f"line_stickers_{project_id}.zip")
    
    file_list = []
    
    # Copy/Save stickers as 01.png, 02.png, etc.
    for idx, src_path in enumerate(sticker_images, 1):
        target_name = f"{idx:02d}.png"
        target_path = os.path.join(project_dir, target_name)
        if os.path.abspath(src_path) != os.path.abspath(target_path):
            shutil.copyfile(src_path, target_path)
        file_list.append(target_path)
    
    # Process main and tab
    if sticker_images:
        first_img = Image.open(sticker_images[0])
        main_img = lsp.process_sticker_image_pipeline(first_img, target_type="main", tolerance=20, white_stroke=True)
        tab_img = lsp.process_sticker_image_pipeline(first_img, target_type="tab", tolerance=20, white_stroke=True)
        
        main_path = os.path.join(project_dir, "main.png")
        tab_path = os.path.join(project_dir, "tab.png")
        main_img.save(main_path, format="PNG")
        tab_img.save(tab_path, format="PNG")
        
        file_list.extend([main_path, tab_path])

    info_meta = f"""=== ข้อมูลสำหรับลงทะเบียน LINE Creators Market ===

ชื่อชุดสติกเกอร์ (ไทย)
{title}

ชื่อชุดสติกเกอร์ (อังกฤษ)
{title} - ThaiD AI Edition

คำอธิบายสติกเกอร์ (ไทย)
ชุดสติกเกอร์คาแรคเตอร์สุดน่ารัก สร้างสรรค์โดย ThaiD LINE Sticker AI Studio (https://sticker.thaid.online)

คำอธิบายสติกเกอร์ (อังกฤษ)
Official high-quality cute character LINE sticker set generated with ThaiD AI Studio.

=== LINE Sticker Specifications ===
- Main: 240x240 px (main.png)
- Tab: 96x74 px (tab.png)
- Stickers: Max 370x320 px, transparent PNG, 10px margins, even dimensions.
- Engine: ThaiD LINE Sticker AI
"""

    lsp.package_line_sticker_set(
        output_zip_path=zip_path,
        processed_images=file_list,
        info_text=info_meta,
        sticker_type=package_type
    )

    # Optional: Generate composite sheet preview poster
    try:
        composite_img = lsp.generate_composite_sheet_4x10(
            images_source=sticker_images,
            title=title,
            sticker_type=package_type
        )
        composite_path = os.path.join(project_dir, "composite_preview.png")
        composite_img.save(composite_path, format="PNG")
    except Exception as e:
        print(f"[Package] Note: Composite sheet skipped: {e}")

    return zip_path
