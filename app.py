# -*- coding: utf-8 -*-
"""
ThaiD LINE Sticker AI Studio - Web Application Server
Production FastAPI Backend for https://sticker.thaid.online
Apple Cupertino Luxury Aesthetic & Dual-Engine REST Generation
"""

import os
import sys
import time
import json
import uuid
import shutil
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

import caption_library as cl
import line_sticker_processor as lsp
import image_engine as ie

app = FastAPI(
    title="ThaiD LINE Sticker AI Studio",
    description="Official AI Line Sticker Generator for Thai Creators",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and output paths
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

# Category metadata with luxury icons and themes
CATEGORY_METADATA = {
    "ทักทาย & ชีวิตประจำวัน": {"icon": "waving_hand", "badge": "Daily", "color": "#0071e3"},
    "ทำงาน & ออฟฟิศ": {"icon": "laptop_mac", "badge": "Work", "color": "#e85a2d"},
    "ให้กำลังใจ & สู้ชีวิต": {"icon": "favorite", "badge": "Cheer", "color": "#10b981"},
    "เงินทอง & สายเปย์": {"icon": "payments", "badge": "Money", "color": "#f59e0b"},
    "สายกิน & ชวนหิว": {"icon": "restaurant", "badge": "Food", "color": "#ef4444"},
    "กวนๆ & มุกตลก": {"icon": "mood", "badge": "Humor", "color": "#8b5cf6"},
    "คำแสลง & วัยรุ่น 2026": {"icon": "bolt", "badge": "Trendy", "color": "#ec4899"},
    "ความรัก & เทคแคร์": {"icon": "volunteer_activism", "badge": "Love", "color": "#f43f5e"},
    "ขอโทษ & ขอบคุณ": {"icon": "handshake", "badge": "Polite", "color": "#06b6d4"},
    "วันหยุด & พักผ่อน": {"icon": "beach_access", "badge": "Holiday", "color": "#14b8a6"},
    "ดราม่า & อารมณ์เหวี่ยง": {"icon": "sentiment_very_dissatisfied", "badge": "Drama", "color": "#64748b"},
    "อวยพร & มงคล": {"icon": "auto_awesome", "badge": "Blessing", "color": "#d97706"},
}


class GenerateStickerRequest(BaseModel):
    project_id: str
    slot: int  # 1 to 40, or 0 for main, -1 for tab
    character_desc: str
    art_style: str = "chibi_3d"
    caption: str = ""
    pose_prompt: str = ""
    engine: str = "flux"  # flux or flow
    tolerance: int = 22
    white_stroke: bool = True
    stroke_width: int = 4


class RematRequest(BaseModel):
    project_id: str
    slot: int
    tolerance: int = 22
    choke: float = 1.2
    feather: float = 0.8
    white_stroke: bool = True
    stroke_width: int = 4


class PackageRequest(BaseModel):
    project_id: str
    title: str = "ThaiD LINE Sticker Set"
    package_type: str = "standard"


class SaveProjectRequest(BaseModel):
    project_id: str
    title: str
    character_desc: str
    art_style: str
    engine: str
    package_size: int
    slots: Dict[str, Any]


@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "ThaiD LINE Sticker AI Studio API Live"}


@app.get("/api/status")
def get_system_status():
    """Health check and engine status."""
    total_outputs = len(os.listdir(OUTPUT_DIR)) if os.path.exists(OUTPUT_DIR) else 0
    return {
        "ok": True,
        "service": "ThaiD LINE Sticker AI Studio",
        "domain": "sticker.thaid.online",
        "status": "online",
        "total_projects": total_outputs,
        "available_engines": [
            {"id": "flux", "name": "Flux Turbo REST (Instant 4-8s)", "status": "active", "recommended": True},
            {"id": "flow", "name": "Google Flow Cloud REST (Dual-Lane)", "status": "active", "recommended": False}
        ],
        "art_styles": [
            {"id": "chibi_3d", "name": "3D Pixar Chibi", "tag": "ฮิตที่สุด", "desc": "3D สไตล์การ์ตูนดิสนีย์ โมเดลนุ่มเนียนตา"},
            {"id": "cute_2d", "name": "Cute 2D Anime", "tag": "ลายเส้นญี่ปุ่น", "desc": "อนิเมะน่ารัก เส้นเวกเตอร์คมชัด สีสด"},
            {"id": "kawaii_doodle", "name": "Kawaii Doodle", "tag": "มินิมอล", "desc": "ดูเดิ้ลวาดมือน่ารัก สีพาสเทลคลีนๆ"},
            {"id": "retro_pixel", "name": "Retro Pixel", "tag": "ย้อนยุค", "desc": "พิกเซลอาร์ต 16-bit สุดคลาสสิก"},
            {"id": "watercolor", "name": "Storybook Watercolor", "tag": "สีน้ำ", "desc": "ภาพวาดสีน้ำนุ่มนวล อบอุ่นละมุน"}
        ]
    }


@app.get("/api/categories")
def list_categories():
    """Lists all 12 sticker caption categories with count and sample items."""
    cats = cl.get_categories()
    result = []
    for cat_name in cats:
        items = cl.get_captions_by_category(cat_name)
        meta = CATEGORY_METADATA.get(cat_name, {"icon": "category", "badge": "General", "color": "#0071e3"})
        result.append({
            "name": cat_name,
            "count": len(items),
            "icon": meta["icon"],
            "badge": meta["badge"],
            "color": meta["color"],
            "samples": [item["caption"] for item in items[:6]]
        })
    return {"ok": True, "categories": result, "total_captions": len(cl.CAPTIONS_DATABASE)}


@app.get("/api/captions")
def get_captions(
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    limit: int = Query(50)
):
    """Searches or filters captions from the 530+ database."""
    if q:
        items = cl.search_captions(q)
    elif category:
        items = cl.get_captions_by_category(category)
    else:
        items = cl.CAPTIONS_DATABASE
    
    return {
        "ok": True,
        "total": len(items),
        "items": items[:limit]
    }


@app.get("/api/presets")
def get_preset_packages(size: int = Query(40)):
    """
    Returns curated ready-to-generate packages of 8, 16, 24, or 40 stickers
    well-balanced across everyday communication needs.
    """
    if size not in [8, 16, 24, 40]:
        size = 40
    
    preset_dict = cl.get_preset_48_stickers()
    preset_items = preset_dict.get("caption_stickers", [])[:size]
    result = []
    for idx, item in enumerate(preset_items, 1):
        result.append({
            "slot": idx,
            "caption": item["caption"],
            "pose": item["pose"],
            "emotion": item["emotion"],
            "prompt_en": item["prompt_en"],
            "category": item["category"],
            "color": item.get("color", "#3B82F6")
        })
    
    return {"ok": True, "size": size, "stickers": result}


@app.post("/api/generate-single")
def generate_single_sticker(req: GenerateStickerRequest):
    """
    Generates a single sticker for a given slot:
    1. Builds AI prompt
    2. Calls REST image generation (Flux Turbo or Google Flow)
    3. Runs 5-step LINE matting & sizing pipeline
    """
    proj_dir = os.path.join(OUTPUT_DIR, req.project_id)
    os.makedirs(proj_dir, exist_ok=True)
    
    slot_label = "main" if req.slot == 0 else ("tab" if req.slot == -1 else f"{req.slot:02d}")
    target_type = "main" if req.slot == 0 else ("tab" if req.slot == -1 else "sticker")

    raw_filename = f"raw_{slot_label}.png"
    proc_filename = f"{slot_label}.png"
    raw_path = os.path.join(proj_dir, raw_filename)
    proc_path = os.path.join(proj_dir, proc_filename)

    prompt = ie.build_sticker_prompt(
        character_desc=req.character_desc,
        caption=req.caption,
        pose_prompt=req.pose_prompt,
        art_style=req.art_style,
        with_thai_text=bool(req.caption)
    )

    try:
        t0 = time.time()
        # Generate raw image
        if req.engine == "flow":
            raw_file = ie.generate_via_flow_rest(prompt, raw_path)
            if not raw_file:
                raw_file = ie.generate_via_flux_rest(prompt, raw_path)
        else:
            raw_file = ie.generate_via_flux_rest(prompt, raw_path)

        if not raw_file or not os.path.exists(raw_file):
            raise HTTPException(status_code=500, detail="Failed to generate image from AI REST API")

        # Process with LINE Sticker Processor
        raw_img = Image.open(raw_file)
        processed_img = lsp.process_sticker_image_pipeline(
            raw_img,
            target_type=target_type,
            tolerance=req.tolerance,
            choke=1.2,
            feather=0.8,
            margin=10,
            white_stroke=req.white_stroke,
            stroke_width=req.stroke_width
        )
        processed_img.save(proc_path, format="PNG")
        elapsed = round(time.time() - t0, 2)

        return {
            "ok": True,
            "slot": req.slot,
            "slot_label": slot_label,
            "caption": req.caption,
            "raw_url": f"/output/{req.project_id}/{raw_filename}?t={int(time.time())}",
            "processed_url": f"/output/{req.project_id}/{proc_filename}?t={int(time.time())}",
            "dimensions": processed_img.size,
            "elapsed": elapsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/remat-single")
def remat_single_sticker(req: RematRequest):
    """
    Instantly re-processes existing raw image with updated tolerance and stroke width
    without re-generating from AI (takes ~0.2s).
    """
    proj_dir = os.path.join(OUTPUT_DIR, req.project_id)
    slot_label = "main" if req.slot == 0 else ("tab" if req.slot == -1 else f"{req.slot:02d}")
    target_type = "main" if req.slot == 0 else ("tab" if req.slot == -1 else "sticker")

    raw_filename = f"raw_{slot_label}.png"
    proc_filename = f"{slot_label}.png"
    raw_path = os.path.join(proj_dir, raw_filename)
    proc_path = os.path.join(proj_dir, proc_filename)

    if not os.path.exists(raw_path):
        raise HTTPException(status_code=404, detail="Raw image not found. Generate sticker first.")

    t0 = time.time()
    raw_img = Image.open(raw_path)
    processed_img = lsp.process_sticker_image_pipeline(
        raw_img,
        target_type=target_type,
        tolerance=req.tolerance,
        choke=req.choke,
        feather=req.feather,
        margin=10,
        white_stroke=req.white_stroke,
        stroke_width=req.stroke_width
    )
    processed_img.save(proc_path, format="PNG")
    elapsed = round(time.time() - t0, 3)

    return {
        "ok": True,
        "slot": req.slot,
        "slot_label": slot_label,
        "processed_url": f"/output/{req.project_id}/{proc_filename}?t={int(time.time())}",
        "dimensions": processed_img.size,
        "elapsed": elapsed
    }


@app.post("/api/package-zip")
def package_line_zip(req: PackageRequest):
    """
    Packages all ready stickers into official LINE ZIP structure:
    01.png .. 40.png, main.png, tab.png, info.txt
    """
    proj_dir = os.path.join(OUTPUT_DIR, req.project_id)
    if not os.path.exists(proj_dir):
        raise HTTPException(status_code=404, detail="Project not found")

    # Find all ready sticker images
    sticker_images = []
    for i in range(1, 41):
        cand = os.path.join(proj_dir, f"{i:02d}.png")
        if os.path.exists(cand):
            sticker_images.append(cand)

    if not sticker_images:
        raise HTTPException(status_code=400, detail="No generated stickers found in project")

    zip_file = ie.create_line_package(
        project_id=req.project_id,
        sticker_images=sticker_images,
        package_type=req.package_type,
        title=req.title
    )

    composite_path = os.path.join(proj_dir, "composite_preview.png")
    has_composite = os.path.exists(composite_path)

    return {
        "ok": True,
        "project_id": req.project_id,
        "total_stickers": len(sticker_images),
        "zip_url": f"/output/{req.project_id}/line_stickers_{req.project_id}.zip",
        "composite_preview_url": f"/output/{req.project_id}/composite_preview.png" if has_composite else None,
        "zip_size_bytes": os.path.getsize(zip_file)
    }


@app.get("/api/download-zip/{project_id}")
def download_zip(project_id: str):
    """Direct download of official LINE package ZIP."""
    zip_path = os.path.join(OUTPUT_DIR, project_id, f"line_stickers_{project_id}.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP package not found. Click package first.")
    return FileResponse(zip_path, filename=f"line_stickers_{project_id}.zip", media_type="application/zip")


@app.post("/api/project/save")
def save_project_state(req: SaveProjectRequest):
    """Persists project configuration and current slot states to JSON."""
    proj_file = os.path.join(DATA_DIR, f"{req.project_id}.json")
    with open(proj_file, "w", encoding="utf-8") as f:
        json.dump(req.dict(), f, ensure_ascii=False, indent=2)
    return {"ok": True, "saved_to": proj_file}


@app.get("/api/project/{project_id}")
def load_project_state(project_id: str):
    """Loads saved project configuration."""
    proj_file = os.path.join(DATA_DIR, f"{project_id}.json")
    if not os.path.exists(proj_file):
        return {"ok": False, "message": "Project not found"}
    with open(proj_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"ok": True, "project": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8090, reload=True)
