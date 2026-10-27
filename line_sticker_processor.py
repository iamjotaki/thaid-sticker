"""
line_sticker_processor.py
=============================================================================
High-Performance LINE Sticker Processing Engine (Native Python)
Ported directly from pleng.online/line (stickerProcessor.ts)

5-Step Pipeline:
1. Auto-detect Background Color (4-corner sample analysis)
2. Background Keying (Floodfill BFS inward from edges to preserve eyes, teeth, clothes)
3. Choke Erosion (Trim fringing / white edge halos)
4. Edge Feathering (Gaussian alpha edge smoothing)
5. Auto-Trim & LINE Standard Sizing (10px margin, even dimensions, 370x320, 240x240, 96x74)
=============================================================================
"""

import os
import sys
import io
import math
import site
import zipfile
from collections import deque
from PIL import Image, ImageFilter
import numpy as np

# Ensure CUDA and cuDNN 9 DLL directories are in PATH and DLL search order
def setup_cuda_env():
    for sp in site.getsitepackages():
        for sub in ['cudnn/bin', 'cublas/bin', 'cuda_nvrtc/bin']:
            p = os.path.join(sp, 'nvidia', sub.replace('/', os.sep))
            if os.path.exists(p):
                try:
                    os.add_dll_directory(p)
                except Exception:
                    pass
                if p not in os.environ.get('PATH', ''):
                    os.environ['PATH'] = p + os.pathsep + os.environ.get('PATH', '')

setup_cuda_env()

LINE_SPECS = {
    "sticker": {"max_w": 370, "max_h": 320, "margin": 10},
    "main": {"w": 240, "h": 240, "margin": 10},
    "tab": {"w": 96, "h": 74, "margin": 5}
}

STICKER_SPECS = {
    "standard": {
        "name": "Standard Sticker",
        "name_th": "สติกเกอร์มาตรฐาน (Standard)",
        "width": 370,
        "height": 320,
        "max_size": (370, 320),
        "margin": 10,
        "main_w": 240,
        "main_h": 240,
        "main_size": (240, 240),
        "tab_w": 96,
        "tab_h": 74,
        "tab_size": (96, 74),
        "has_main": True,
        "name_pattern": "01",
        "allowed_counts": [8, 16, 24, 32, 40]
    },
    "big": {
        "name": "Big Sticker",
        "name_th": "สติกเกอร์ขนาดใหญ่ (Big Sticker)",
        "width": 396,
        "height": 660,
        "max_size": (396, 660),
        "margin": 10,
        "main_w": 240,
        "main_h": 240,
        "main_size": (240, 240),
        "tab_w": 96,
        "tab_h": 74,
        "tab_size": (96, 74),
        "has_main": True,
        "name_pattern": "01",
        "allowed_counts": [8, 16, 24, 32, 40]
    },
    "emoji": {
        "name": "LINE Emoji",
        "name_th": "ไลน์อิโมจิ (Emoji)",
        "width": 180,
        "height": 180,
        "max_size": (180, 180),
        "margin": 2,
        "main_w": 0,
        "main_h": 0,
        "main_size": (0, 0),
        "tab_w": 96,
        "tab_h": 74,
        "tab_size": (96, 74),
        "has_main": False,
        "name_pattern": "001",
        "allowed_counts": [8, 16, 24, 32, 40]
    }
}

def detect_background_color(pil_img, sample_size=5):
    """
    Step 1: Auto-detect Background Color
    Samples all 4 outer borders (Top, Bottom, Left, Right) to determine dominant background color.
    Uses median/mode of border pixels to avoid pollution from character content touching a corner.
    """
    img = pil_img.convert("RGBA")
    w, h = img.size
    arr = np.array(img, dtype=np.uint8)

    # Collect border pixels from all 4 sides
    b_size = max(2, min(sample_size, 8))
    top = arr[:b_size, :, :3].reshape(-1, 3)
    bottom = arr[-b_size:, :, :3].reshape(-1, 3)
    left = arr[:, :b_size, :3].reshape(-1, 3)
    right = arr[:, -b_size:, :3].reshape(-1, 3)
    border_pixels = np.concatenate([top, bottom, left, right], axis=0)

    # Robust mode detection by quantizing to 8-bin grid
    quantized = (border_pixels // 8) * 8
    unique, counts = np.unique(quantized, axis=0, return_counts=True)
    mode_bin = unique[np.argmax(counts)]

    # Take mean of border pixels in the dominant bin
    bin_mask = np.all(quantized == mode_bin, axis=1)
    if np.any(bin_mask):
        dominant_rgb = border_pixels[bin_mask].mean(axis=0)
    else:
        dominant_rgb = np.median(border_pixels, axis=0)

    avg_r = int(round(dominant_rgb[0]))
    avg_g = int(round(dominant_rgb[1]))
    avg_b = int(round(dominant_rgb[2]))

    # Check color characteristics
    is_white = avg_r > 215 and avg_g > 215 and avg_b > 215
    is_black = avg_r < 35 and avg_g < 35 and avg_b < 35
    is_magenta = (avg_r > 150 and avg_b > 150 and avg_g < 130 and (avg_r - avg_g) > 35 and (avg_b - avg_g) > 35)
    is_green = (avg_g > 150 and avg_r < 120 and avg_b < 120 and (avg_g - avg_r) > 40)

    return {
        "r": avg_r, "g": avg_g, "b": avg_b,
        "is_white": is_white,
        "is_black": is_black,
        "is_magenta": is_magenta,
        "is_green": is_green,
        "recommended_mode": "floodfill"
    }

def remove_background_keying(pil_img, tolerance=25, remove_shadows=True, remove_enclosed_gaps=True, custom_bg=None, defringe=True):
    """
    Step 2: High-Precision Chroma Keying & Floodfill
    - Supports Magenta (#FC02F6), Green Screen, White, and Black backgrounds.
    - Connects border components inward.
    - Enclosed gap removal: cleanly removes background trapped inside armholes and legs.
    - Chroma despill filter: completely neutralizes pink/magenta fringe on anti-aliased character edges.
    """
    img = pil_img.convert("RGBA")
    w, h = img.size
    arr = np.array(img, dtype=np.uint8)

    bg_info = detect_background_color(img)
    target_r = custom_bg[0] if custom_bg else bg_info["r"]
    target_g = custom_bg[1] if custom_bg else bg_info["g"]
    target_b = custom_bg[2] if custom_bg else bg_info["b"]

    is_magenta = bg_info.get("is_magenta", False)
    is_green = bg_info.get("is_green", False)

    # Tolerance mapping: 0..100 -> 0..200 Euclidean distance
    effective_tol = max(tolerance, 18) if (is_magenta or is_green) else tolerance
    max_dist = (effective_tol / 100.0) * 200.0
    if is_magenta:
        # Magenta screen (#FC02F6) is extremely clean; cap max_dist at 38 to protect lavender/purple hair
        max_dist = min(max_dist, 38.0)

    rgb = arr[:, :, :3].astype(np.float32)
    diff = rgb - np.array([target_r, target_g, target_b], dtype=np.float32)
    dist = np.sqrt(np.sum(diff * diff, axis=2))

    is_bg = (dist <= max_dist)

    # Magenta outer shadow detection:
    # Meta AI generates outer drop-shadows under text and stickers against magenta backgrounds.
    # In these shadow pixels: G < 28, R > 65, B > 65, |R - B| < 35 (pure magenta shadow hue).
    if is_magenta:
        r_c = arr[:, :, 0].astype(np.int32)
        g_c = arr[:, :, 1].astype(np.int32)
        b_c = arr[:, :, 2].astype(np.int32)
        magenta_shadow = (g_c < 28) & (r_c > 65) & (b_c > 65) & (np.abs(r_c - b_c) < 35)
        is_bg = is_bg | magenta_shadow

    # Detect neutral gray contact shadows for white backgrounds
    if remove_shadows and bg_info["is_white"]:
        r_chan = rgb[:, :, 0]
        g_chan = rgb[:, :, 1]
        b_chan = rgb[:, :, 2]
        neutral_gray = (
            (np.abs(r_chan - g_chan) < 18) &
            (np.abs(g_chan - b_chan) < 18) &
            (np.abs(r_chan - b_chan) < 18) &
            (r_chan > 180) & (g_chan > 180) & (b_chan > 180) &
            (dist <= max_dist * 1.5)
        )
        is_bg = is_bg | neutral_gray

    # Outer background removal using cv2 connected components
    try:
        import cv2
        bg_uint8 = is_bg.astype(np.uint8)
        num_labels, labels = cv2.connectedComponents(bg_uint8, connectivity=4)
        border_labels = np.unique(np.concatenate([labels[0, :], labels[h - 1, :], labels[:, 0], labels[:, w - 1]]))
        border_labels = border_labels[border_labels > 0]
        outer_bg = np.isin(labels, border_labels)
    except Exception:
        # Fallback BFS Floodfill
        outer_bg = np.zeros((h, w), dtype=bool)
        queue = deque()
        for x in range(w):
            if is_bg[0, x]: outer_bg[0, x] = True; queue.append((0, x))
            if is_bg[h - 1, x]: outer_bg[h - 1, x] = True; queue.append((h - 1, x))
        for y in range(h):
            if is_bg[y, 0] and not outer_bg[y, 0]: outer_bg[y, 0] = True; queue.append((y, 0))
            if is_bg[y, w - 1] and not outer_bg[y, w - 1]: outer_bg[y, w - 1] = True; queue.append((y, w - 1))
        while queue:
            cy, cx = queue.popleft()
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < h and 0 <= nx < w:
                    if not outer_bg[ny, nx] and is_bg[ny, nx]:
                        outer_bg[ny, nx] = True
                        queue.append((ny, nx))

    # Enclosed gaps (holes inside arms, legs, loops of Thai letters):
    if remove_enclosed_gaps or is_magenta or is_green:
        enclosed_bg = is_bg & (~outer_bg)
    else:
        enclosed_bg = np.zeros((h, w), dtype=bool)

    # Apply transparency to both outer background and enclosed holes
    arr[outer_bg, 3] = 0
    arr[enclosed_bg, 3] = 0

    # Chroma Despill (ลบขอบเหลือบสีชมพู / เขียว บนเส้นขอบตัวละครและตัวหนังสือ)
    if defringe or is_magenta or is_green:
        if is_magenta:
            try:
                import cv2
                # Dilate transparent background by 7px to inspect the outer edge transition zone
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
                bg_dilated = cv2.dilate((arr[:, :, 3] == 0).astype(np.uint8), kernel).astype(bool)
                edge_zone = (arr[:, :, 3] > 0) & bg_dilated
            except Exception:
                edge_zone = (arr[:, :, 3] > 0)

            r_out = arr[:, :, 0].astype(np.int32)
            g_out = arr[:, :, 1].astype(np.int32)
            b_out = arr[:, :, 2].astype(np.int32)

            # Any edge pixel with magenta tint (high R and B, depressed G):
            # Neutralize magenta by restoring G = max(G, min(R, B)) on white borders and steam
            magenta_edge = edge_zone & (r_out > 130) & (b_out > 130) & ((r_out - g_out > 20) | (b_out - g_out > 20))
            arr[magenta_edge, 1] = np.maximum(arr[magenta_edge, 1], np.minimum(arr[magenta_edge, 0], arr[magenta_edge, 2]))
        elif is_green:
            r_out = arr[:, :, 0].astype(np.float32)
            g_out = arr[:, :, 1].astype(np.float32)
            b_out = arr[:, :, 2].astype(np.float32)
            spill = np.maximum(0, g_out - np.maximum(r_out, b_out))
            has_spill = (arr[:, :, 3] > 0) & (spill > 15) & (g_out > 120)
            arr[has_spill, 1] = np.clip(g_out[has_spill] - spill[has_spill] * 0.9, 0, 255).astype(np.uint8)

    return Image.fromarray(arr, "RGBA")

def apply_choke_erosion(pil_img, choke=1.2):
    """
    Step 3: Choke / Erosion (กัดขอบ)
    Eliminates color halos/fringing from AI generation around character borders.
    """
    if choke <= 0:
        return pil_img

    img = pil_img.convert("RGBA")
    arr = np.array(img, dtype=np.uint8)
    alpha = arr[:, :, 3]

    try:
        import cv2
        radius = max(1, int(round(choke)))
        k_size = radius * 2 + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_size, k_size))
        eroded_alpha = cv2.erode(alpha, kernel, iterations=1)
        arr[:, :, 3] = eroded_alpha
    except Exception:
        alpha_img = Image.fromarray(alpha, mode="L")
        radius = max(1, int(round(choke)))
        size = radius * 2 + 1
        eroded_alpha = alpha_img.filter(ImageFilter.MinFilter(size))
        arr[:, :, 3] = np.array(eroded_alpha)

    return Image.fromarray(arr, "RGBA")

def apply_edge_feather(pil_img, feather=0.8):
    """
    Step 4: Edge Feather (เกลี่ยขอบนุ่ม)
    Smooths alpha boundary so stickers have silky smooth cartoon edges on any LINE chat background.
    """
    if feather <= 0:
        return pil_img

    img = pil_img.convert("RGBA")
    arr = np.array(img)
    alpha = Image.fromarray(arr[:, :, 3], mode="L")

    # Gaussian blur the alpha mask slightly
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=feather))
    blurred_arr = np.array(blurred_alpha)

    # Only apply smoothing along the edge transition (where 0 < alpha < 255)
    edge_mask = (arr[:, :, 3] > 0) & (arr[:, :, 3] < 255)
    arr[edge_mask, 3] = blurred_arr[edge_mask]

    return Image.fromarray(arr, "RGBA")

def auto_trim_and_line_specs(pil_img, target_type="sticker", margin=10, sticker_type="standard"):
    """
    Step 5: Auto-Trim & LINE Standard Sizing
    - Finds non-transparent bounding box.
    - Adds minimum 10px transparent margin on all sides (strict LINE Creators Market requirement!).
    - Resizes to exact specifications with EVEN DIMENSIONS (width and height must both be even numbers).
      Sticker: W <= 370, H <= 320 px
      Main: 240 x 240 px
      Tab: 96 x 74 px
    """
    img = pil_img.convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]

    # Find bounding box of non-transparent content
    non_zero = np.argwhere(alpha > 10)
    if non_zero.size == 0:
        # Blank image fallback
        bbox = (0, 0, img.width, img.height)
    else:
        min_y, min_x = non_zero.min(axis=0)
        max_y, max_x = non_zero.max(axis=0)
        bbox = (min_x, min_y, max_x + 1, max_y + 1)

    cropped = img.crop(bbox)
    cw, ch = cropped.size

    if target_type == "main":
        # Fixed 240x240 px (standard & big)
        canvas_w, canvas_h = 240, 240
        avail_w = canvas_w - (margin * 2)
        avail_h = canvas_h - (margin * 2)
        scale = min(avail_w / cw, avail_h / ch)
        nw = max(2, int(round(cw * scale)))
        nh = max(2, int(round(ch * scale)))
        resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
        
        result = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        ox = (canvas_w - nw) // 2
        oy = (canvas_h - nh) // 2
        result.paste(resized, (ox, oy), resized)
        return result

    elif target_type == "tab":
        # Fixed 96x74 px
        canvas_w, canvas_h = 96, 74
        avail_w = canvas_w - (margin * 2)
        avail_h = canvas_h - (margin * 2)
        scale = min(avail_w / cw, avail_h / ch)
        nw = max(2, int(round(cw * scale)))
        nh = max(2, int(round(ch * scale)))
        resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)

        result = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        ox = (canvas_w - nw) // 2
        oy = (canvas_h - nh) // 2
        result.paste(resized, (ox, oy), resized)
        return result

    else:
        # Chat sticker: Standard (370x320), Big (396x660), or Emoji (180x180)
        if sticker_type == "big":
            max_canvas_w = 396
            max_canvas_h = 660
            eff_margin = margin if margin is not None else 10
        elif sticker_type == "emoji":
            max_canvas_w = 180
            max_canvas_h = 180
            eff_margin = margin if margin is not None else 2
        else: # "standard"
            max_canvas_w = 370
            max_canvas_h = 320
            eff_margin = margin if margin is not None else 10

        avail_w = max_canvas_w - (eff_margin * 2)
        avail_h = max_canvas_h - (eff_margin * 2)
        scale = min(avail_w / cw, avail_h / ch)
        scale = min(scale, 1.0) # don't upscale beyond original resolution

        nw = max(2, int(round(cw * scale)))
        nh = max(2, int(round(ch * scale)))

        # LINE requirement: Canvas width and height MUST be even numbers!
        canvas_w = nw + (eff_margin * 2)
        canvas_h = nh + (eff_margin * 2)
        if canvas_w % 2 != 0: canvas_w += 1
        if canvas_h % 2 != 0: canvas_h += 1

        canvas_w = min(canvas_w, max_canvas_w)
        canvas_h = min(canvas_h, max_canvas_h)
        if canvas_w % 2 != 0: canvas_w -= 1
        if canvas_h % 2 != 0: canvas_h -= 1

        resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
        result = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        ox = (canvas_w - nw) // 2
        oy = (canvas_h - nh) // 2
        result.paste(resized, (ox, oy), resized)
        return result

def apply_white_stroke(pil_img, stroke_width=3, stroke_color=(255, 255, 255, 255)):
    """
    Applies an outer stroke/border around the alpha contour of the sticker character.
    Official LINE style white border.
    """
    if stroke_width <= 0:
        return pil_img
    img = pil_img.convert("RGBA")
    alpha = img.split()[3]
    radius = int(round(stroke_width))
    dilated_alpha = alpha.filter(ImageFilter.MaxFilter(radius * 2 + 1))

    stroke_layer = Image.new("RGBA", img.size, stroke_color)
    stroke_layer.putalpha(dilated_alpha)

    return Image.alpha_composite(stroke_layer, img)

def process_sticker_image_pipeline(
    input_image_path_or_pil,
    target_type="sticker",
    mode="floodfill",
    tolerance=15,
    choke=1.2,
    feather=0.8,
    margin=10,
    sticker_type="standard",
    white_stroke=False,
    stroke_width=3,
    remove_shadows=True,
    remove_enclosed_gaps=True,
    defringe=True
):
    """
    Complete 5-Step Pipeline execution on a single image.
    Supports mode='floodfill'/'chroma' (100% Offline Floodfill BFS) or mode='ai' (Studio AI Matting).
    Supports sticker_type: 'standard', 'big', 'emoji'.
    Supports white_stroke and stroke_width.
    Returns: PIL Image (RGBA, transparent background, compliant with LINE specs).
    """
    if isinstance(input_image_path_or_pil, str):
        img = Image.open(input_image_path_or_pil).convert("RGBA")
    else:
        img = input_image_path_or_pil.convert("RGBA")

    # Step 2: Background Removal (Chroma Keying or AI Matting)
    bg_info = detect_background_color(img)
    if mode == "ai" and not bg_info.get("is_magenta", False):
        try:
            from ai_matting_service import remove_bg_ai_pil
            keyed = remove_bg_ai_pil(img)
        except Exception:
            keyed = remove_background_keying(
                img, tolerance=tolerance,
                remove_shadows=remove_shadows,
                remove_enclosed_gaps=remove_enclosed_gaps,
                defringe=defringe
            )
    else:
        keyed = remove_background_keying(
            img, tolerance=tolerance,
            remove_shadows=remove_shadows,
            remove_enclosed_gaps=remove_enclosed_gaps,
            defringe=defringe
        )

    # Step 3: Choke Erosion (applied if requested)
    choked = apply_choke_erosion(keyed, choke=choke) if choke > 0 else keyed

    # Step 4: Edge Feather
    feathered = apply_edge_feather(choked, feather=feather) if feather > 0 else choked

    # Step 4.5: Optional White Sticker Stroke
    if white_stroke and stroke_width > 0:
        feathered = apply_white_stroke(feathered, stroke_width=stroke_width)

    # Step 5: Trim, Margin & LINE Sizing (standard, big, emoji)
    final_img = auto_trim_and_line_specs(feathered, target_type=target_type, margin=margin, sticker_type=sticker_type)

    return final_img

def package_line_sticker_set(output_zip_path, processed_images, info_text="", sticker_type="standard", **kwargs):
    """
    Packages 42 processed images (main.png, tab.png, 01.png - 40.png) + info.txt
    into a clean ZIP archive ready for LINE Creators Market upload.
    Supports processed_images as:
      - dict of {slot: filepath_or_pil_image}
      - directory path containing processed images
    """
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        if info_text:
            zf.writestr("info.txt", info_text.encode('utf-8'))

        if isinstance(processed_images, str) and os.path.exists(processed_images):
            # Read from directory
            for f in os.listdir(processed_images):
                if f.lower().endswith(".png"):
                    zf.write(os.path.join(processed_images, f), arcname=f)
        elif isinstance(processed_images, (list, tuple)):
            for item in processed_images:
                if isinstance(item, str) and os.path.exists(item):
                    zf.write(item, arcname=os.path.basename(item))
                elif isinstance(item, tuple) and len(item) == 2:
                    name, val = item
                    fname = f"{name}.png" if not str(name).endswith(".png") else str(name)
                    if isinstance(val, str) and os.path.exists(val):
                        zf.write(val, arcname=fname)
                    elif isinstance(val, Image.Image):
                        buf = io.BytesIO()
                        val.save(buf, format="PNG", optimize=True)
                        zf.writestr(fname, buf.getvalue())
        elif isinstance(processed_images, dict):
            for name, item in processed_images.items():
                fname = f"{name}.png" if not str(name).endswith(".png") else str(name)
                if isinstance(item, str) and os.path.exists(item):
                    zf.write(item, arcname=fname)
                elif isinstance(item, Image.Image):
                    buf = io.BytesIO()
                    item.save(buf, format="PNG", optimize=True)
                    zf.writestr(fname, buf.getvalue())

    return True

def apply_watermark_layer(base_image, text="SAMPLE", position="cell", opacity=0.45, color="white", cell_rects=None):
    """
    Renders customizable watermark on composite sheet or preview image.
    position: 'cell' (each sticker), 'repeat' (diagonal pattern), 'center' (large center)
    color: 'white', 'black', 'red'
    """
    from PIL import ImageDraw, ImageFont

    w, h = base_image.size
    wm_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wm_layer)

    alpha_val = int(255 * max(0.20, min(0.95, opacity if opacity is not None else 0.45)))
    if color == "black":
        fill_color = (0, 0, 0, alpha_val)
        outline_color = (255, 255, 255, int(alpha_val * 0.75))
    elif color == "red":
        fill_color = (239, 68, 68, alpha_val)
        outline_color = (255, 255, 255, int(alpha_val * 0.75))
    else:  # white
        fill_color = (255, 255, 255, alpha_val)
        outline_color = (0, 0, 0, int(alpha_val * 0.75))

    font = None
    for font_path in [
        "C:/Windows/Fonts/tahomabd.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/leelawad.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf"
    ]:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 36)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    if position == "cell" and cell_rects:
        for (cx, cy, cw, ch) in cell_rects:
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                txt_img = Image.new("RGBA", (tw + 30, th + 30), (0, 0, 0, 0))
                tdraw = ImageDraw.Draw(txt_img)
                tdraw.text((15, 15), text, fill=fill_color, font=font, stroke_width=2, stroke_fill=outline_color)
                rotated = txt_img.rotate(25, expand=True, resample=Image.Resampling.BILINEAR)
                rw, rh = rotated.size
                rx = cx + (cw - rw) // 2
                ry = cy + (ch - rh) // 2
                wm_layer.paste(rotated, (rx, ry), rotated)
            except Exception:
                draw.text((cx + cw // 2 - 30, cy + ch // 2 - 10), text, fill=fill_color, font=font, stroke_width=2, stroke_fill=outline_color)

    elif position == "repeat":
        step_x = 320
        step_y = 220
        for y in range(-h, h * 2, step_y):
            for x in range(-w, w * 2, step_x):
                try:
                    bbox = draw.textbbox((0, 0), text, font=font)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1]
                    txt_img = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
                    tdraw = ImageDraw.Draw(txt_img)
                    tdraw.text((20, 20), text, fill=fill_color, font=font, stroke_width=2, stroke_fill=outline_color)
                    rotated = txt_img.rotate(30, expand=True, resample=Image.Resampling.BILINEAR)
                    wm_layer.paste(rotated, (x, y), rotated)
                except Exception:
                    draw.text((x, y), text, fill=fill_color, font=font, stroke_width=2, stroke_fill=outline_color)

    else:  # "center"
        large_font = None
        for font_path in [
            "C:/Windows/Fonts/tahomabd.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
            "C:/Windows/Fonts/arialbd.ttf"
        ]:
            if os.path.exists(font_path):
                try:
                    large_font = ImageFont.truetype(font_path, 90)
                    break
                except Exception:
                    pass
        if large_font is None:
            large_font = font

        bbox = draw.textbbox((0, 0), text, font=large_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        txt_img = Image.new("RGBA", (tw + 80, th + 80), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(txt_img)
        tdraw.text((40, 40), text, fill=fill_color, font=large_font, stroke_width=3, stroke_fill=outline_color)
        rotated = txt_img.rotate(25, expand=True, resample=Image.Resampling.BILINEAR)
        rw, rh = rotated.size
        wm_layer.paste(rotated, ((w - rw) // 2, (h - rh) // 2), rotated)

    return Image.alpha_composite(base_image, wm_layer)

def generate_composite_sheet_4x10(images_source, bg_color="lineblue", title="LINE STICKER 4×10 COMPOSITE PREVIEW", watermark=None, sticker_type="standard"):
    """
    Generate a 4x10 composite sheet image (4 columns x 10 rows = 40 stickers).
    STRICTLY includes only 01 to 40 (excluding main.png and tab.png).
    Supports watermark (text, position, opacity, color).
    Supports sticker_type: standard, big, emoji.
    Returns: PIL Image (RGBA)
    """
    from PIL import ImageDraw

    col_count = 4
    row_count = 10
    total_slots = 40

    if sticker_type == "big":
        cell_w, cell_h = 396, 660
    elif sticker_type == "emoji":
        cell_w, cell_h = 180, 180
    else: # standard
        cell_w, cell_h = 370, 320

    gap = 24
    pad_x, pad_top, pad_bot = 40, 110, 50

    total_w = (pad_x * 2) + (col_count * cell_w) + ((col_count - 1) * gap)
    total_h = pad_top + (row_count * cell_h) + ((row_count - 1) * gap) + pad_bot

    bg_clean = (bg_color or "lineblue").lower().strip()
    is_checker = bg_clean in ["checker", "checkerboard"]

    if bg_clean == "white":
        bg_rgba = (255, 255, 255, 255)
        card_rgba = (248, 250, 252, 255)
        border_rgba = (226, 232, 240, 255)
        title_color = (15, 23, 42, 255)
        subtext_color = (71, 85, 105, 255)
    elif bg_clean in ["dark", "black"]:
        bg_rgba = (15, 23, 42, 255)
        card_rgba = (24, 34, 53, 230)
        border_rgba = (51, 65, 85, 255)
        title_color = (255, 255, 255, 255)
        subtext_color = (148, 163, 184, 255)
    elif is_checker:
        bg_rgba = (240, 243, 246, 255)
        card_rgba = (255, 255, 255, 220)
        border_rgba = (203, 213, 225, 255)
        title_color = (15, 23, 42, 255)
        subtext_color = (71, 85, 105, 255)
    elif bg_clean == "transparent":
        bg_rgba = (0, 0, 0, 0)
        card_rgba = (255, 255, 255, 30)
        border_rgba = (255, 255, 255, 60)
        title_color = (255, 255, 255, 255)
        subtext_color = (200, 200, 200, 255)
    else:  # "lineblue"
        bg_rgba = (105, 138, 171, 255)
        card_rgba = (15, 23, 42, 190)
        border_rgba = (255, 255, 255, 75)
        title_color = (255, 255, 255, 255)
        subtext_color = (226, 232, 240, 255)

    composite = Image.new("RGBA", (total_w, total_h), bg_rgba)
    draw = ImageDraw.Draw(composite)

    # Render pattern if checkerboard
    if is_checker:
        tile_size = 32
        c1 = (245, 247, 250, 255)
        c2 = (224, 231, 239, 255)
        for ty in range(0, total_h, tile_size):
            for tx in range(0, total_w, tile_size):
                tile_fill = c1 if ((tx // tile_size) + (ty // tile_size)) % 2 == 0 else c2
                draw.rectangle([tx, ty, tx + tile_size, ty + tile_size], fill=tile_fill)

    # Title header
    draw.text((pad_x, 32), title, fill=title_color)
    draw.text((pad_x, 64), f"40 Chat Stickers (01-40.png) • LINE Specs: {cell_w}×{cell_h} px",
              fill=subtext_color)

    slot_images = {}
    if isinstance(images_source, dict):
        for k, v in images_source.items():
            clean_k = str(k).lower().replace(".png", "")
            if clean_k in ["main", "tab"]:
                continue
            slot_images[clean_k] = v
    elif isinstance(images_source, str) and os.path.exists(images_source):
        all_files = [f for f in os.listdir(images_source) if f.lower().endswith(('.png', '.webp', '.jpg')) and not f.startswith('test_') and not f.startswith('ref_')]
        for f in all_files:
            clean_k = f.lower().replace(".png", "").replace(".webp", "").replace(".jpg", "")
            if clean_k in ["main", "tab"]:
                continue
            slot_images[clean_k] = os.path.join(images_source, f)

    sorted_keys = sorted(slot_images.keys())
    cell_rects = []

    for i in range(1, total_slots + 1):
        slot_key = f"{i:02d}"
        col = (i - 1) % col_count
        row = (i - 1) // col_count

        x = pad_x + col * (cell_w + gap)
        y = pad_top + row * (cell_h + gap)
        cell_rects.append((x, y, cell_w, cell_h))

        draw.rectangle([x, y, x + cell_w, y + cell_h], fill=card_rgba, outline=border_rgba, width=1)
        draw.text((x + 8, y + 8), f"#{slot_key}", fill=(100, 116, 139, 255))

        img_obj = slot_images.get(slot_key)
        if img_obj is None and str(i) in slot_images:
            img_obj = slot_images[str(i)]
        if img_obj is None and i - 1 < len(sorted_keys):
            img_obj = slot_images[sorted_keys[i - 1]]

        if img_obj is not None:
            try:
                if isinstance(img_obj, str) and os.path.exists(img_obj):
                    pil_item = Image.open(img_obj).convert("RGBA")
                elif isinstance(img_obj, Image.Image):
                    pil_item = img_obj
                else:
                    pil_item = None

                if pil_item is not None:
                    max_iw = cell_w - 20
                    max_ih = cell_h - 20
                    iw, ih = pil_item.size
                    scale = min(max_iw / iw, max_ih / ih, 1.0)
                    scaled_w, scaled_h = int(iw * scale), int(ih * scale)
                    resized = pil_item.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
                    paste_x = x + (cell_w - scaled_w) // 2
                    paste_y = y + (cell_h - scaled_h) // 2
                    composite.paste(resized, (paste_x, paste_y), resized)
            except Exception:
                pass

    # Apply watermark if enabled
    if watermark and watermark.get("enabled", False) and watermark.get("text", "").strip():
        composite = apply_watermark_layer(
            composite,
            text=watermark.get("text", "SAMPLE").strip(),
            position=watermark.get("position", "cell"),
            opacity=float(watermark.get("opacity", 0.45)),
            color=watermark.get("color", "white"),
            cell_rects=cell_rects
        )

    return composite

def package_original_cutouts_zip(output_zip_path, images_source):
    """
    Packages all cutout images (background removed, but original high-res dimensions)
    into a clean ZIP file for the user.
    """
    with zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        if isinstance(images_source, dict):
            for slot, item in images_source.items():
                fname = f"{slot}_original.png" if not str(slot).endswith(".png") else str(slot)
                if isinstance(item, str) and os.path.exists(item):
                    zf.write(item, arcname=fname)
                elif isinstance(item, Image.Image):
                    buf = io.BytesIO()
                    item.save(buf, format="PNG", optimize=True)
                    zf.writestr(fname, buf.getvalue())
        elif isinstance(images_source, str) and os.path.exists(images_source):
            for f in os.listdir(images_source):
                if f.lower().endswith(('.png', '.webp', '.jpg')):
                    zf.write(os.path.join(images_source, f), arcname=f)
    return True

