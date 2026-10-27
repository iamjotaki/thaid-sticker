# -*- coding: utf-8 -*-
"""
caption_library.py
=============================================================================
Comprehensive Thai LINE Sticker Caption & Pose Database (530+ Curated Captions)
Built for High-Consistency AI Sticker Generation (Google Flow / Imagen 3)

Features:
- 12 Realistic Categories
- 530+ Unique Modern Thai Captions with matching Poses, Emotions, Props, and English AI Prompts
- Automatic 42-Item Line Sticker Selection (40 Stickers + 1 Main + 1 Tab)
- Structured JSON Prompt Generator for Google Flow & info.txt Market Metadata
=============================================================================
"""

import json
import random
import re

CAPTIONS_DATABASE = [
  {
    "id": "LINE_CAP_001",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดี",
    "pose": "ยืนโบกมือทักทาย ยิ้มหวานสดใส",
    "emotion": "ยิ้มสดชื่น ตาโตมีความสุข",
    "props": "ประกายวิบวับรอบตัว",
    "prompt_en": "waving hand happily, cheerful bright smile, sparkling aura",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_002",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ฮัลโหล",
    "pose": "ถือโทรศัพท์แนบหู ทำท่ากระซิบถาม",
    "emotion": "ตื่นเต้น อยากคุย",
    "props": "คลื่นเสียงสั่นรอบโทรศัพท์",
    "prompt_en": "holding phone to ear, lively expression, animated sound waves",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_003",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "อรุณสวัสดิ์",
    "pose": "บิดขี้เกียจต้อนรับเช้าวันใหม่ พร้อมแก้วกาแฟ",
    "emotion": "ตาสลึมสลือแต่อารมณ์ดี",
    "props": "ไอควันกาแฟรูปหัวใจ",
    "prompt_en": "stretching arms in the morning, holding a steaming mug, sleepy cute smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_004",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "มอร์นิ่ง",
    "pose": "กระโดดออกมาจากหลังประตูทักทาย",
    "emotion": "ยิ้มกว้าง แก้มแดง",
    "props": "ดอกไม้เบ่งบาน",
    "prompt_en": "peeking cheerfully from door, blushing cheeks, floating blossoms",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_005",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ตื่นยัง",
    "pose": "เอานิ้วจิ้มหน้าจอ ยื่นหน้ามาใกล้ๆ",
    "emotion": "สงสัย ขี้เล่น",
    "props": "เครื่องหมายคำถามดุ๊กดิ๊ก",
    "prompt_en": "poking finger close-up, curious playful eyes, floating question mark",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_006",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ตื่นแล้วจ้า",
    "pose": "เด้งตัวขึ้นจากเตียง ชูสองนิ้ว",
    "emotion": "ตาสว่าง สดใสเต็มร้อย",
    "props": "แสงอาทิตย์ส่องด้านหลัง",
    "prompt_en": "springing out of bed energetic, flashing peace sign, morning sunbeams",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_007",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ถึงแล้วนะ",
    "pose": "ยืนกวักมือหน้าแลนด์มาร์ค สะพายกระเป๋า",
    "emotion": "ยิ้มโล่งอก มีความสุข",
    "props": "หมุดแผนที่ Location ปักข้างๆ",
    "prompt_en": "waving happily with backpack on, map pin icon floating nearby",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_008",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "กำลังไป",
    "pose": "วิ่งติดสปีด ขาหมุนเป็นวงล้อ",
    "emotion": "รีบร้อน ลิ้นห้อยนิดๆ",
    "props": "ลมหมุนใต้ฝ่าเท้า ละอองฝุ่นฟุ้ง",
    "prompt_en": "running at top speed, feet spinning like wheels, speed lines",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_009",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "อยู่ไหน",
    "pose": "กางแผนที่ ใช้กล้องส่องทางไกลมองหา",
    "emotion": "มองซ้ายมองขวา เลิกลั่ก",
    "props": "เครื่องหมายตกใจและคำถาม",
    "prompt_en": "looking through binoculars searching left and right, comical confused face",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_010",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "รอแป๊บนะ",
    "pose": "ยกมือห้าม อีกมือรีบผูกเชือกรองเท้า",
    "emotion": "รีบเร่งแต่ส่งสายตาอ้อน",
    "props": "นาฬิกาทรายหมุนติ้วๆ",
    "prompt_en": "raising one hand to signal wait, hurried expression, floating hourglass",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_011",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ว่างไหม",
    "pose": "เกาะขอบหน้าจอ ยื่นหัวมาถามเงียบๆ",
    "emotion": "ตาเป็นประกาย อยากชวนคุย",
    "props": "หัวใจดวงเล็กๆ ลอยเบาๆ",
    "prompt_en": "peeking from screen corner, puppy eyes, tiny floating heart",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_012",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ทำไรอยู่",
    "pose": "นั่งเท้าคาง เอานิ้วเคาะโต๊ะรอคำตอบ",
    "emotion": "อยากรู้อยากเห็น ขี้เล่น",
    "props": "ฟองสบู่แห่งความคิด",
    "prompt_en": "resting chin on hands leaning forward, curious inquisitive look",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_013",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ไปไหนมา",
    "pose": "ยืนกอดอก เคาะเท้าจ้องจับผิด",
    "emotion": "หรี่ตาจับโป๊ะ คิ้วขมวดนิดๆ",
    "props": "แว่นขยายส่องสืบสวน",
    "prompt_en": "standing with arms crossed tapping foot, playful suspicious squint",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_014",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "กลับบ้านแล้ว",
    "pose": "เดินโบกมือถือกระเป๋าหลังเลิกงาน",
    "emotion": "ยิ้มผ่อนคลาย สบายใจ",
    "props": "ท้องฟ้าสีส้มยามเย็น",
    "prompt_en": "walking home swinging bag, relaxed contented smile, sunset backdrop",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_015",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ถึงบ้านปลอดภัย",
    "pose": "นอนแผ่หราบนโซฟา ชูนิ้วโป้ง",
    "emotion": "โล่งใจ หมดแรงแบบสบายๆ",
    "props": "ฟองอากาศ zZ ลอย",
    "prompt_en": "sprawling comfortably on couch, giving thumbs up, relief expression",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_016",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "บายๆ",
    "pose": "โบกมือลาพร้อมส่งจูบ",
    "emotion": "ยิ้มละมุน อบอุ่น",
    "props": "หัวใจลอยตามรอยจูบ",
    "prompt_en": "waving goodbye blowing a kiss, sweet gentle smile, floating hearts",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_017",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "เจอกันนะ",
    "pose": "ทำมือสัญลักษณ์นัดพบ ขยิบตา",
    "emotion": "มั่นใจ กระตือรือร้น",
    "props": "ประกายไฟวิ้งๆ",
    "prompt_en": "making a friendly meet-up hand sign, winking cheekily, star sparks",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_018",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ฝันดีนะ",
    "pose": "นอนห่มผ้านวมนุ่ม กอดตุ๊กตาหมี",
    "emotion": "หลับตาพริ้ม เคลิ้มสุข",
    "props": "พระจันทร์เสี้ยวและดาววิบวับ",
    "prompt_en": "tucked in cozy blanket hugging teddy bear, sweet sleeping face, moon and stars",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_019",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "กู๊ดไนท์",
    "pose": "ทำท่าเป่าเทียนก่อนนอน สวมหมวกนอน",
    "emotion": "ตาปรือ ง่วงนอนสุดๆ",
    "props": "กลุ่มดาวส่องแสงนุ่มนวล",
    "prompt_en": "blowing out candle in cute nightcap, half-closed sleepy eyes, soft starlight",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_020",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "นอนละนะ",
    "pose": "มุดตัวลงถุงนอน ดึงผ้าคลุมโปง",
    "emotion": "หมดสภาพ ชัตดาวน์ตัวเอง",
    "props": "สัญลักษณ์แบตเตอรี่สีแดง 1%",
    "prompt_en": "zipping into sleeping bag, completely drained comical face, low battery icon",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_021",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "โอเคจ้า",
    "pose": "ทำมือรูป OK วงกลมระดับตา",
    "emotion": "ยิ้มสดใส ร่าเริง",
    "props": "ดอกไม้บานรอบตัว",
    "prompt_en": "making big OK sign with fingers, bright cheerful grin",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_022",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "เยี่ยมเลย",
    "pose": "ชูสองนิ้วโป้ง ยิ้มเห็นฟันขาว",
    "emotion": "ภูมิใจ มั่นใจเต็มเปี่ยม",
    "props": "ดาวทองเปล่งประกาย",
    "prompt_en": "double thumbs up enthusiastically, beaming proud smile, golden star sparks",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_023",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ตามนั้นเลย",
    "pose": "พยักหน้ารัวๆ ชี้นิ้วเห็นด้วย",
    "emotion": "เห็นชอบ เต็มใจสุดๆ",
    "props": "เครื่องหมายถูกสีเขียวอันใหญ่",
    "prompt_en": "nodding head vigorously pointing forward, big green checkmark",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_024",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "เอาจริงดิ",
    "pose": "อ้าปากค้าง ตาโตเท่าไข่ห่าน",
    "emotion": "ตกใจสุดขีด ไม่อยากจะเชื่อ",
    "props": "สายฟ้าฟาดเบาๆ ด้านหลัง",
    "prompt_en": "jaw dropped open in shock, eyes wide as saucers, comical lightning bolt",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_025",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "จริงเหรอ",
    "pose": "เอามือทาบอก เอียงคอถาม",
    "emotion": "สงสัย แปลกใจปนตื่นเต้น",
    "props": "เครื่องหมายคำถามคู่สีสด",
    "prompt_en": "hand over chest in disbelief, head tilted, twin colorful question marks",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_026",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ไม่จริงมั้ง",
    "pose": "โบกมือปฏิเสธรัวๆ ส่ายหัวจนภาพเบลอ",
    "emotion": "ไม่เชื่อเด็ดขาด ขำแห้ง",
    "props": "เหงื่อหยดติ๋งที่หน้าผาก",
    "prompt_en": "waving hands frantically in denial, shaking head fast, sweat drop",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_027",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "เรื่องจริงปะเนี่ย",
    "pose": "ดึงแก้มตัวเองเพื่อเช็คว่าฝันไหม",
    "emotion": "มึนงง สับสนตลกๆ",
    "props": "วงกลมมึนงงหมุนบนหัว",
    "prompt_en": "pinching own cheek to check if dreaming, dizzy spiral over head",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_028",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สุดยอดไปเลย",
    "pose": "กระโดดลอยตัวกลางอากาศ ชูกำปั้น",
    "emotion": "ตื่นเต้น ดีใจทะลุพิกัด",
    "props": "พลุกระดาษระเบิดรอบตัว",
    "prompt_en": "leaping mid-air with fist raised, overjoyed triumphant face, confetti party popper",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_029",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "เท่มาก",
    "pose": "สวมแว่นตาดำ เสยผมขึ้นหนึ่งสเต็ป",
    "emotion": "เก๊กหล่อ มั่นหน้ามั่นโหนก",
    "props": "แสงสะท้อนแว่นตาเป็นดาว",
    "prompt_en": "sliding on sunglasses pushing hair back, confident cool pose, star gleam",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_030",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "น่ารักที่สุด",
    "pose": "เอามือกุมแก้ม ตัวบิดเขิน",
    "emotion": "ตาหวานฉ่ำ ปลื้มปริ่ม",
    "props": "หัวใจสีชมพูลอยฟุ้ง",
    "prompt_en": "clasping blushing cheeks squirming cute, melting affectionate expression, floating hearts",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_031",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ยินดีด้วยนะ",
    "pose": "ปรบมือรัวๆ โปรยดอกไม้",
    "emotion": "ยิ้มยินดีจากใจจริง",
    "props": "ช่อดอกไม้ช่อใหญ่และริบบิ้น",
    "prompt_en": "clapping hands warmly showering flower petals, big celebratory bouquet",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_032",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "เก่งมาก",
    "pose": "ลูบหัวชื่นชม ตบมือเปาะแปะ",
    "emotion": "เอ็นดู ภูมิใจในตัวเธอ",
    "props": "มงกุฎทองคำลอยเหนือหัว",
    "prompt_en": "patting head praising gently, proud caring smile, tiny golden crown",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_033",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ภูมิใจในตัวเธอ",
    "pose": "กอดอกยิ้มปลาบปลื้ม น้ำตาซึมแห่งความยินดี",
    "emotion": "ตื้นตันใจ ซาบซึ้ง",
    "props": "แสงออร่าสีทองเปล่งประกาย",
    "prompt_en": "smiling with misty eyes of pride, warm heartfelt aura, golden glow",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_034",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ขอตัวก่อนนะ",
    "pose": "โค้งคำนับสุภาพ ค่อยๆ ถอยหลังออกไป",
    "emotion": "สุภาพ อ่อนน้อม",
    "props": "ทางเดินเปิดออก",
    "prompt_en": "bowing politely walking backwards, courteous respectful gesture",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_035",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ไว้คุยกันใหม่",
    "pose": "ทำมือรูปโทรศัพท์สั่นข้างหู",
    "emotion": "ยิ้มสดใส เป็นมิตร",
    "props": "ตัวโน้ตดนตรีลอย",
    "prompt_en": "making call-me gesture waving, warm friendly grin, floating music notes",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_036",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "ดูแลตัวเองด้วย",
    "pose": "ยื่นผ้าพันคอให้ ทำหน้าห่วงใย",
    "emotion": "อบอุ่น ใจดี เป็นห่วง",
    "props": "ไออุ่นและใบไม้ร่วง",
    "prompt_en": "handing over a warm cozy scarf, deeply caring tender gaze",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_037",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "หายไวๆ นะ",
    "pose": "ถือชามซุปร้อนๆ และยาเม็ด",
    "emotion": "เห็นอกเห็นใจ ให้กำลังใจ",
    "props": "ผ้าประคบหน้าผากและปรอทวัดไข้",
    "prompt_en": "holding hot soup bowl and get-well card, comforting sympathetic look",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_038",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "เดินทางปลอดภัย",
    "pose": "โบกธงปล่อยตัว ชูนิ้วโป้งให้",
    "emotion": "อวยพร ร่าเริง",
    "props": "รถคันจิ๋ววิ่งฉิว",
    "prompt_en": "waving flag wishing safe journey, cheerful encouraging thumbs up, mini car zoom",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_039",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สุขสันต์วันเกิด",
    "pose": "ถือเค้กวันเกิดปักเทียนจุดไฟ",
    "emotion": "ยิ้มกว้าง ร้องเพลงอวยพร",
    "props": "หมวกปาร์ตี้และลูกโป่งหลากสี",
    "prompt_en": "holding birthday cake with lit candles, singing joyfully, colorful party balloons",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_040",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "แฮปปี้เบิร์ธเดย์",
    "pose": "เป่าลิ้นกระดาษปาร์ตี้ สวมแว่นแฟนซี",
    "emotion": "สนุกสนาน เฮฮาเต็มที่",
    "props": "สายรุ้งและกล่องของขวัญ",
    "prompt_en": "blowing party blower horn wearing funky glasses, festive confetti explosion",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_041",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดีวันจันทร์",
    "pose": "ถือแก้วกาแฟใบโต ต้อนรับวันทำงาน",
    "emotion": "ยิ้มสดใสพร้อมลุยงาน",
    "props": "ดอกไม้สีเหลืองสดใส",
    "prompt_en": "holding giant coffee mug ready for work, bright yellow energetic vibe",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_042",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดีวันอังคาร",
    "pose": "ใส่เสื้อสีชมพู ถือช่อดอกไม้",
    "emotion": "หวานแหวว อารมณ์ดี",
    "props": "ผีเสื้อโบยบินรอบตัว",
    "prompt_en": "wearing cute pink outfit holding flower, sweet happy Tuesday vibe",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_043",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดีวันพุธ",
    "pose": "ยืนกางร่มสีเขียว ทักทายสายฝน",
    "emotion": "สดชื่น ชุ่มฉ่ำใจ",
    "props": "ต้นไม้ใบหญ้าเขียวขจี",
    "prompt_en": "holding green umbrella refreshing Wednesday smile, lush green plants",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_044",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดีวันพฤหัส",
    "pose": "จัดโต๊ะอ่านหนังสือ รับแสงแดดอ่อนๆ",
    "emotion": "สงบ ผ่อนคลาย มีสมาธิ",
    "props": "แสงแดดสีส้มอบอุ่น",
    "prompt_en": "reading book at desk warm Thursday sunshine, cozy productive vibe",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_045",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดีวันศุกร์",
    "pose": "กระโดดดีใจยกแขนสองข้าง",
    "emotion": "เริงร่าสุดขีด พรุ่งนี้วันหยุด!",
    "props": "ดาวประกายระยิบระยับ",
    "prompt_en": "jumping with hands raised Friday celebration, sparkling weekend vibes",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_046",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดีวันเสาร์",
    "pose": "ใส่ชุดนอนนั่งดูทีวี กินขนม",
    "emotion": "ชิลล์ขั้นสุด สบายใจเฉิบ",
    "props": "ถังป๊อปคอร์นและหมอนนุ่ม",
    "prompt_en": "sitting in pajamas watching TV snacking popcorn, ultimate Saturday chill",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_047",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "สวัสดีวันอาทิตย์",
    "pose": "นอนอาบแดด จิบน้ำมะพร้าว",
    "emotion": "พักผ่อนเต็มอิ่ม มีความสุข",
    "props": "ต้นมะพร้าวและแว่นกันแดด",
    "prompt_en": "relaxing under sunshine sipping coconut drink, blissful Sunday breeze",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_048",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "กราบสวัสดี",
    "pose": "นั่งพับเพียบยกมือไหว้จรดหน้าผาก",
    "emotion": "นอบน้อมถ่อมตน เรียบร้อยน่ารัก",
    "props": "พวงมาลัยดอกมะลิ",
    "prompt_en": "kneeling down Wai respectfully touching forehead, polite humble Thai greeting",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_049",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "แวะมาทักทาย",
    "pose": "โผล่หน้าออกมาจากขอบข้างจอ",
    "emotion": "ยิ้มทะเล้น ตาหยี",
    "props": "ลูกโป่งรูปยิ้มลอย",
    "prompt_en": "popping head out from side frame, cheeky grinning face, floating smiley balloon",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_050",
    "category": "ทักทาย & ชีวิตประจำวัน",
    "caption": "คิดถึงทุกคนเลย",
    "pose": "อ้าแขนทำท่ากอดกว้างๆ",
    "emotion": "ตาโตเป็นประกาย อบอุ่น",
    "props": "หัวใจดวงโตล้อมรอบ",
    "prompt_en": "arms spread wide offering big group hug, warm loving eyes, giant floating heart",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_051",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "รับทราบครับ",
    "pose": "ยืนตรงทำท่าตะเบ๊ะแบบทหาร",
    "emotion": "มุ่งมั่น ตั้งใจ พร้อมลุย",
    "props": "เครื่องหมายเช็คถูกสีเขียว",
    "prompt_en": "saluting smartly like soldier, determined sharp eyes, green checkmark icon",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_052",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "รับทราบค่ะ",
    "pose": "ผงกศีรษะรับคำสั่ง จดสมุดโน้ต",
    "emotion": "สุภาพ อ่อนหวาน มืออาชีพ",
    "props": "ปากกาและสมุดจดงาน",
    "prompt_en": "nodding politely taking notes in notebook, professional cheerful look",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_053",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ได้เลยครับ",
    "pose": "ชูนิ้วโป้งขยิบตาข้างเดียว",
    "emotion": "มั่นใจเต็มเปี่ยม ไว้วางใจได้",
    "props": "ประกายฟันขาววิ้ง",
    "prompt_en": "giving confident thumbs up and wink, gleaming tooth sparkle",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_054",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ได้เลยค่ะ",
    "pose": "กุมมือที่อก ยิ้มหวานพร้อมช่วย",
    "emotion": "ยินดีบริการ เต็มใจช่วย",
    "props": "ดอกไม้เล็กๆ บาน",
    "prompt_en": "hands clasped at chest with sweet eager smile, ready to help",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_055",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ตามเรื่องให้อยู่นะ",
    "pose": "ถือแว่นขยายตรวจกองเอกสาร",
    "emotion": "ขะมักเขม้น ตั้งใจสืบค้น",
    "props": "โฟลเดอร์เอกสารและรอยเท้า",
    "prompt_en": "examining papers with magnifying glass, focused detective pose",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_056",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ส่งงานแล้วจ้า",
    "pose": "กดปุ่ม Enter แป้นพิมพ์อย่างสะใจ",
    "emotion": "สะใจ โล่งอก ยิ้มร่า",
    "props": "จรวดพุ่งทะยานพร้อมซองจดหมาย",
    "prompt_en": "slamming Enter key triumphantly, email envelope zooming like rocket",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_057",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "กำลังปั่นงาน",
    "pose": "พิมพ์คีย์บอร์ดเร็วรัวจนมือเป็นภาพซ้อน",
    "emotion": "โฟกัสตาเขม็ง เหงื่อตก",
    "props": "เปลวไฟลุกท่วมแป้นพิมพ์",
    "prompt_en": "typing furiously at keyboard with motion blur hands, flames blazing",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_058",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "งานด่วนมาก",
    "pose": "วิ่งถือแฟ้มเอกสารติดไซเรนแดง",
    "emotion": "ตื่นตระหนก ตาเบิกกว้าง",
    "props": "ไฟหมุนไซเรนสีแดงฉุกเฉิน",
    "prompt_en": "running holding file folder with emergency red siren flashing on head",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_059",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ขอเลื่อนเดดไลน์",
    "pose": "พนมมือไหว้น้ำตาคลอเบ้า",
    "emotion": "อ้อนวอนสุดชีวิต สงสารหนูเถอะ",
    "props": "ปฏิทินบินหนีและนาฬิกา",
    "prompt_en": "pleading desperately with hands clasped praying tears welling up, calendar page tearing",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_060",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ติดประชุม",
    "pose": "สวมหูฟังชี้ป้ายห้ามส่งเสียงดัง",
    "emotion": "จริงจัง เงียบสงบ",
    "props": "ป้าย Do Not Disturb สีแดง",
    "prompt_en": "wearing headset pointing at Do Not Disturb sign, serious quiet expression",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_061",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ประชุมอีกแล้ว",
    "pose": "นั่งคอพับหน้าจอโน้ตบุ๊ก",
    "emotion": "หมดอะไรตายอยาก เบื่อหน่าย",
    "props": "วิญญาณหลุดลอยออกจากร่าง",
    "prompt_en": "slumping over laptop during endless meeting, soul leaving body comically",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_062",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ขออนุมัติครับ",
    "pose": "ยื่นเอกสารสองมือพร้อมปากกาเซ็น",
    "emotion": "ลุ้นระทึก ส่งสายตาคาดหวัง",
    "props": "ช่องเซ็นลายเซ็นกระพริบ",
    "prompt_en": "presenting document with two hands offering pen, hopeful pleading eyes",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_063",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "อนุมัติเรียบร้อย",
    "pose": "ประทับตรายาง 'APPROVED' ตัวโตๆ",
    "emotion": "สะใจ มีอำนาจเด็ดขาด",
    "props": "หมึกสีแดงสดกระเซ็นสวยงาม",
    "prompt_en": "slamming big APPROVED rubber stamp down, victorious powerful expression",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_064",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "แก้งานรอบที่ล้าน",
    "pose": "ลบกระดาษจนทะลุ ถือยางลบก้อนกุด",
    "emotion": "หมดพลัง ปลงตกกับชีวิต",
    "props": "เศษยางลบเกลื่อนโต๊ะ",
    "prompt_en": "erasing drawing intensely until paper tears, completely exhausted dead eyes",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_065",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ไฟลุกมาก",
    "pose": "ผูกผ้าคาดหัวสีแดง กำหมัดแน่น",
    "emotion": "ฮึกเหิม มีไฟ พลังล้นเหลือ",
    "props": "เปลวไฟออร่าลุกโชนรอบตัว",
    "prompt_en": "wearing red headband, fists clenched glowing with fiery intense aura",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_066",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ใกล้เสร็จแล้ว",
    "pose": "เช็ดเหงื่อที่หน้าผาก วางบล็อกสุดท้าย",
    "emotion": "เหนื่อยแต่มีความหวัง",
    "props": "เกจพลังงานโหลด 99%",
    "prompt_en": "wiping brow with back of hand placing final piece, 99% progress bar",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_067",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "พักสายตาแป๊บ",
    "pose": "ถอดแว่นตา นวดดั้งจมูกเบาๆ",
    "emotion": "ตาล้า อ่อนเพลีย",
    "props": "แก้วชาอุ่นๆ วางข้างๆ",
    "prompt_en": "taking off glasses rubbing nose bridge weary eyes, warm tea cup beside",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_068",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "พักเที่ยงกินไรดี",
    "pose": "เปิดแอปเดลิเวอรี่ เอานิ้วจิ้มแก้มคิด",
    "emotion": "หิวจัด ตาวาว เลือกไม่ถูก",
    "props": "รูปอาหารลอยเต็มหัว",
    "prompt_en": "tapping chin browsing food app, hungry sparkling eyes, floating food bubbles",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_069",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ไปกินข้าวกัน",
    "pose": "กวักมือเรียก ถือช้อนส้อมพร้อมลุย",
    "emotion": "ร่าเริง มีชีวิตชีวา",
    "props": "กลิ่นอาหารหอมฉุย",
    "prompt_en": "waving friends holding spoon and fork eagerly, delicious aroma swirl",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_070",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "เลิกงานแล้วโว้ย",
    "pose": "กระโดดข้ามโต๊ะทำงาน โยนเอกสารทิ้ง",
    "emotion": "ปลดปล่อย ดีใจสุดขีด",
    "props": "นาฬิกาดิจิทัลบอกเวลา 17:00",
    "prompt_en": "leaping over office desk tossing papers in air, ecstatic freedom celebration",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_071",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "กลับก่อนไม่รอแล้ว",
    "pose": "สะพายเป้วิ่งพุ่งชนประตูออกไป",
    "emotion": "เร็วแสง หายตัวแวบ",
    "props": "รอยฝุ่นเป็นรูปคน",
    "prompt_en": "zooming out office door at light speed with backpack, comical dust silhouette",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_072",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ติดโอที",
    "pose": "นั่งกอดเข่าใต้โต๊ะทำงานตอนดึก",
    "emotion": "เหงา เศร้า เปล่าเปลี่ยว",
    "props": "พระจันทร์มืดมิดนอกหน้าต่าง",
    "prompt_en": "hugging knees under desk working overtime at midnight, gloomy dark window",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_073",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "สมองตัน",
    "pose": "เอามือกุมขมับ จ้องหน้าจอว่างเปล่า",
    "emotion": "คิดไม่ออก มืดแปดด้าน",
    "props": "หลอดไฟดับมีควันขึ้น",
    "prompt_en": "head in hands staring at blank screen, burnt out smoking lightbulb icon",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_074",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ขอไอเดียหน่อย",
    "pose": "ถือกระดาษฟลิปชาร์ต ยื่นหน้าถาม",
    "emotion": "กระตือรือร้น อยากฟังความคิดเห็น",
    "props": "หลอดไฟสีเหลืองสว่างจ้า",
    "prompt_en": "holding flipchart pen, leaning in asking eagerly, bright idea lightbulb",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_075",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "งานงอก",
    "pose": "ยืนมองต้นไม้เอกสารโตพรวดพราด",
    "emotion": "ช็อก ตาค้าง เหงื่อตก",
    "props": "หน่อเอกสารงอกเร็วปานจรวด",
    "prompt_en": "staring in horror at paper stack growing like bamboo shoot, shocked face",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_076",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ระบบล่ม",
    "pose": "ดึงปลั๊กไฟออก โน้ตบุ๊กหน้าจอฟ้าร้องไห้",
    "emotion": "สิ้นหวัง ทำอะไรไม่ถูก",
    "props": "หน้าจอสีฟ้า Blue Screen of Death",
    "prompt_en": "kneeling before blue-screen crashing computer, tearful helpless face",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_077",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "เซฟงานรึยัง",
    "pose": "ชูแผ่นฟลอปปี้ดิสก์ ตะโกนเตือน",
    "emotion": "หวาดเสียว กังวลแทน",
    "props": "ไอคอนปุ่ม Save กระพริบเตือน",
    "prompt_en": "shouting holding up floppy disk reminder, anxious wide-eyed warning",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_078",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "เน็ตหลุด",
    "pose": "เขย่าเราเตอร์ไวไฟ เอามือดึงผม",
    "emotion": "หงุดหงิด อารมณ์เสีย",
    "props": "สัญลักษณ์ Wi-Fi กากบาทสีแดง",
    "prompt_en": "shaking disconnected Wi-Fi router frustrated, red cross on signal icon",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_079",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ลูกค้าคอมเมนต์",
    "pose": "แอบมองคอมเมนต์หลังโล่กำบัง",
    "emotion": "เกร็ง หวาดเสียว กลัวโดนแก้",
    "props": "ลูกศรคอมเมนต์พุ่งเฉียดหัว",
    "prompt_en": "peeking from behind shield reading feedback, tense cringing expression",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_080",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ลูกค้าถูกเสมอ",
    "pose": "ยิ้มแห้งกัดฟัน พยักหน้ารัวๆ",
    "emotion": "กล้ำกลืนฝืนทน ขำขื่น",
    "props": "เส้นเลือดปูดที่ขมับ",
    "prompt_en": "forced tight smile gritting teeth nodding, popping vein on temple",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_081",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "สรุปให้หน่อย",
    "pose": "กางสมุดช็อตโน้ต ปากกาขีดไฮไลท์",
    "emotion": "ตั้งใจจับประเด็น",
    "props": "ปากกาไฮไลท์สีสะท้อนแสง",
    "prompt_en": "holding notebook highlighter pen ready, sharp attentive listening face",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_082",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "เช็คเมลด้วยนะ",
    "pose": "ชี้ไปที่กล่องจดหมายมีปีกบิน",
    "emotion": "เตือนสติ สดใส",
    "props": "ซองจดหมายมีแจ้งเตือนสีแดง (1)",
    "prompt_en": "pointing at flying envelope notification, friendly alert expression",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_083",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ส่งไฟล์ให้แล้ว",
    "pose": "ส่งจรวดกระดาษติดยูเอสบีไดรฟ์",
    "emotion": "ภูมิใจ สำเร็จลุล่วง",
    "props": "แถบดาวน์โหลด 100% Complete",
    "prompt_en": "launching paper airplane with USB drive, proud accomplished grin",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_084",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ช่วยด้วย",
    "pose": "จมลงในกองเอกสารล้นหัว ชูมือขึ้นข้างเดียว",
    "emotion": "ใกล้ขาดใจ ต้องการความช่วยเหลือ",
    "props": "ป้าย SOS ลอยอยู่บนกองเอกสาร",
    "prompt_en": "drowning in mountain of paper with only one hand reaching up, SOS sign",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_085",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "รบกวนด้วยครับ",
    "pose": "โค้งคำนับ 90 องศา ยื่นเอกสาร",
    "emotion": "สุภาพ อ่อนน้อมถ่อมตน",
    "props": "ออร่าความเคารพ",
    "prompt_en": "bowing 90 degrees offering document politely, utmost respectful posture",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_086",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "รบกวนด้วยค่ะ",
    "pose": "พนมมือไหว้งดงาม อ่อนช้อย",
    "emotion": "น่ารัก สุภาพ น่าช่วยเหลือ",
    "props": "ประกายดอกมะลิ",
    "prompt_en": "graceful Thai Wai with sweet courteous pleading smile, jasmine blossoms",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_087",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "เคลียร์งานเสร็จ",
    "pose": "นั่งเอนหลังไขว่ห้าง เป่าปากฟู่",
    "emotion": "โล่งโปร่ง สบายตัว ไร้กังวล",
    "props": "โต๊ะทำงานสะอาดวิ้ง",
    "prompt_en": "leaning back legs crossed blowing air relieved, spotless clean desk",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_088",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "เหนื่อยจังวันนี้",
    "pose": "ทิ้งตัวซบหมอนข้างโต๊ะทำงาน",
    "emotion": "หมดแรง ร่างแหลกสลาย",
    "props": "แบตเตอรี่สีแดงกะพริบเตือน",
    "prompt_en": "resting cheek on office desk totally drained, flashing red battery",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_089",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "สู้ต่อไปพวกเรา",
    "pose": "ยืนบนเก้าอี้ชูกำปั้นนำทีม",
    "emotion": "ปลุกใจ มีพลังผู้นำ",
    "props": "ธงชัยชนะโบกสะบัด",
    "prompt_en": "standing on chair pumping fist rallying team, inspiring leadership pose",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_090",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ทีมเรามันปัง",
    "pose": "กอดคอกลุ่มเพื่อนร่วมงาน หัวเราะร่า",
    "emotion": "อบอุ่น สามัคคี ชนะเลิศ",
    "props": "ถ้วยรางวัลสีทองเปล่งแสง",
    "prompt_en": "arms around teammates laughing together, glowing championship trophy",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_091",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ยินดีที่ได้ร่วมงาน",
    "pose": "จับมือทักทายสองมือ เขย่าเบาๆ",
    "emotion": "จริงใจ อบอุ่น เป็นเกียรติ",
    "props": "ประกายความสัมพันธ์อันดี",
    "prompt_en": "firm two-handed handshake, warm sincere professional smile, sparkle",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_092",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "มือโปรอยู่แล้ว",
    "pose": "ใช้นิ้วชี้ดันแว่นตา แสยะยิ้มมุมปาก",
    "emotion": "มั่นใจ ฉลาดหลักแหลม",
    "props": "แสงสะท้อนแว่นตาแวววับ",
    "prompt_en": "pushing glasses up with index finger, smirk, bright anime glasses glint",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_093",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "งานคุณภาพ",
    "pose": "ชูนิ้วโป้งตรวจงานผ่านแว่นขยาย",
    "emotion": "การันตี เนี๊ยบทุกกระเบียดนิ้ว",
    "props": "ตราสัญลักษณ์เหรียญทอง 5 ดาว",
    "prompt_en": "giving thumbs up inspecting work, 5-star golden badge floating",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_094",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ขอความเห็นชอบ",
    "pose": "ถือป้ายโหวต ชะเง้อมองผล",
    "emotion": "ลุ้นระทึก ใจเต้นตึกตัก",
    "props": "กล่องหย่อนบัตรลงคะแนน",
    "prompt_en": "holding up voting card peeking anxiously, ballot box beside",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_095",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "จัดไปอย่าให้เสีย",
    "pose": "ดีดนิ้วดังเป๊าะ ชี้มือไปข้างหน้า",
    "emotion": "เด็ดขาด รวดเร็ว ทันใจ",
    "props": "ประกายสายฟ้าและดาว",
    "prompt_en": "snapping fingers pointing forward decisively, sparks flying",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_096",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "พร้อมลุยงาน",
    "pose": "สวมถุงมือ ผูกผ้าพันคอทะมัดทะแมง",
    "emotion": "ฮึกเหิม มีพลัง มุ่งมั่น",
    "props": "นาฬิกานับถอยหลังพร้อมออกสตาร์ท",
    "prompt_en": "tightening gloves tying bandana ready for action, energetic stance",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_097",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ตอบช้าขออภัย",
    "pose": "ยกมือไหว้ ก้มศีรษะขอโทษ",
    "emotion": "รู้สึกผิดอย่างจริงใจ",
    "props": "นาฬิกาละลายแบบ Surreal",
    "prompt_en": "bowing apologetically with hands together, sincere guilty smile, melting clock",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_098",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ลุยต่อไม่รอแล้ว",
    "pose": "เหยียบคันเร่งพุ่งทะยานไปข้างหน้า",
    "emotion": "ดุดัน ไม่ยอมแพ้",
    "props": "เปลวไฟพ่นท้ายไอพ่น",
    "prompt_en": "stepping on gas pedal zooming ahead fiercely, turbo flames",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_099",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "ภารกิจลุล่วง",
    "pose": "ปักธงบนยอดเขาเอกสาร",
    "emotion": "สำเร็จอย่างงดงาม ภาคภูมิใจ",
    "props": "แสงแดดส่องเป็นลำบนยอดเขา",
    "prompt_en": "planting flag atop mountain of completed files, triumphant hero pose",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_100",
    "category": "ทำงาน & ออฟฟิศ",
    "caption": "กราบขอบพระคุณ",
    "pose": "กราบแนบตักสองมือ",
    "emotion": "ซาบซึ้งในพระคุณอย่างสูง",
    "props": "ดอกบัวหลวงพับกลีบ",
    "prompt_en": "bowing deeply to knees in traditional Thai gratitude, folded lotus flower",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_101",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "สู้ๆ นะ",
    "pose": "ชูกำปั้นระดับอก ยิ้มตาหยี",
    "emotion": "ส่งพลังใจ สดใส เข้มแข็ง",
    "props": "สายรุ้งและหัวใจสีส้ม",
    "prompt_en": "pumping fist at chest, bright cheering eyes, mini rainbow and heart",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_102",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เป็นกำลังใจให้",
    "pose": "ส่งลูกบอลพลังงานแสงสีทองสองมือ",
    "emotion": "อบอุ่น ห่วงใย เต็มใจให้",
    "props": "ออร่าแสงสีทองอบอุ่น",
    "prompt_en": "offering warm glowing orb of energy with both hands, caring gaze",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_103",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เหนื่อยไหม",
    "pose": "ยื่นแก้วน้ำเย็นพร้อมผ้าเย็นให้",
    "emotion": "เห็นอกเห็นใจ สายตาอ่อนโยน",
    "props": "หยดน้ำเย็นฉ่ำและผ้าขนหนู",
    "prompt_en": "handing cold drink and cooling towel, compassionate gentle eyes",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_104",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "พักผ่อนเยอะๆ นะ",
    "pose": "ห่มผ้าห่มนวมให้ ตบไหล่เบาๆ",
    "emotion": "อบอุ่นเหมือนคนในครอบครัว",
    "props": "ถ้วยชาร้อนและใบคาโมมายล์",
    "prompt_en": "tucking someone in blanket gently patting shoulder, hot chamomile tea",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_105",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "กอดๆ นะ",
    "pose": "อ้าแขนสวมกอดแน่นๆ ตัวกลม",
    "emotion": "อบอุ่น ปลอบประโลม",
    "props": "หัวใจฟูฟ่องสีชมพูอ่อน",
    "prompt_en": "giving big warm squishy hug, comforting soothing expression, fluffy hearts",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_106",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ไม่เป็นไรนะ",
    "pose": "ลูบหลังปลอบโยนเบาๆ ยิ้มอบอุ่น",
    "emotion": "เข้าใจ อ่อนโยน ปลอบขวัญ",
    "props": "ใบโคลเวอร์ 4 แฉกนำโชค",
    "prompt_en": "gently patting back comforting, tender reassuring smile, 4-leaf clover",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_107",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เดี๋ยวมันก็ผ่านไป",
    "pose": "ยืนมองท้องฟ้าหลังฝนตก",
    "emotion": "มีความหวัง สงบนิ่ง",
    "props": "สายรุ้งทอดยาวหลังเมฆฝน",
    "prompt_en": "looking up at sky after rain, peaceful hopeful gaze, clear rainbow arc",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_108",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เก่งที่สุดแล้ว",
    "pose": "ปรบมือชูนิ้วโป้งให้ทั้งสองมือ",
    "emotion": "ยกย่อง ชื่นชมจากหัวใจ",
    "props": "เหรียญรางวัลทองคำส่องแสง",
    "prompt_en": "double thumbs up clapping enthusiastically, glowing gold medal",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_109",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ทำดีที่สุดแล้ว",
    "pose": "ตบหน้าอกตัวเองเบาๆ ยิ้มภูมิใจ",
    "emotion": "ยอมรับความจริงแบบสง่างาม",
    "props": "ดอกทานตะวันเบ่งบาน",
    "prompt_en": "patting chest gently proud of effort, bright blooming sunflower",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_110",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "อย่าคิดมากนะ",
    "pose": "เอานิ้วลูบคิ้วคลายปมให้",
    "emotion": "ผ่อนคลาย ขี้เล่น ห่วงใย",
    "props": "ลูกโป่งลอยปล่อยความเครียด",
    "prompt_en": "gently massaging furrowed brows, playful soothing smile, floating balloon",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_111",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "สู้ชีวิตมาก",
    "pose": "สวมนวมชกมวย พันผ้าคาดหัว",
    "emotion": "บอบช้ำแต่ใจไม่ยอมแพ้",
    "props": "พลาสเตอร์ยาแปะแก้ม เลือดซึม",
    "prompt_en": "wearing boxing gloves and bandage, bruised but unbreakable spirit",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_112",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "แต่ชีวิตสู้กลับ",
    "pose": "โดนนวมยักษ์ชกหน้าหงายขำๆ",
    "emotion": "ตลก เจ็บใจแต่ยังยิ้มได้",
    "props": "นกน้อยและดาวหมุนรอบหัว",
    "prompt_en": "getting comically punched by giant boxing glove, dizzy stars spinning",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_113",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ยังมีพรุ่งนี้เสมอ",
    "pose": "ยืนมองพระอาทิตย์ขึ้นเหนือขอบฟ้า",
    "emotion": "เปี่ยมความหวัง สดใส",
    "props": "แสงตะวันสีทองอบอุ่นยามเช้า",
    "prompt_en": "watching sunrise on horizon, serene hopeful expression, morning sun rays",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_114",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ใจเย็นๆ นะ",
    "pose": "ทำท่ากดมือลงช้าๆ สูดหายใจลึกๆ",
    "emotion": "นิ่ง สงบ สุขุม",
    "props": "ใบชาเขียวและหยดน้ำค้าง",
    "prompt_en": "pressing palms down slowly breathing deep, calm zen expression",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_115",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "อย่าเพิ่งท้อ",
    "pose": "เอื้อมมือดึงคนข้างล่างขึ้นมา",
    "emotion": "มุ่งมั่น ไม่ทิ้งกัน",
    "props": "บันไดปีนสู่แสงสว่าง",
    "prompt_en": "reaching down hand pulling teammate up, determined supportive look",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_116",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เชื่อมั่นในตัวเอง",
    "pose": "ชี้ที่หัวใจตัวเอง ตาเป็นประกาย",
    "emotion": "มั่นใจ หนักแน่น ทรงพลัง",
    "props": "เปลวไฟประกายเพชรในอก",
    "prompt_en": "pointing at own heart with sparkling fierce eyes, glowing diamond spark",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_117",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เธอทำได้อยู่แล้ว",
    "pose": "ชี้นิ้วมาข้างหน้า ส่งยิ้มแห่งชัยชนะ",
    "emotion": "เชื่อใจ มั่นใจในตัวเธอ 100%",
    "props": "ธงนำโชคโบกสะบัด",
    "prompt_en": "pointing finger forward with winning grin, full faith and belief",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_118",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ยิ้มไว้ก่อน",
    "pose": "ใช้นิ้วดึงมุมปากสองข้างให้ยิ้ม",
    "emotion": "ทะเล้น น่ารัก ให้กำลังใจ",
    "props": "รอยยิ้มสีเหลืองสดใส",
    "prompt_en": "using index fingers to push up cheek corners in forced cute smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_119",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ฟ้าหลังฝนย่อมสวยงาม",
    "pose": "ถือร่มโปร่งใส แดดส่องทะลุลงมา",
    "emotion": "สดชื่น เบิกบานใจ",
    "props": "หยดน้ำฝนสะท้อนแสงรุ้ง",
    "prompt_en": "holding clear umbrella under clearing sky, refreshing rain rainbow drops",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_120",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เหนื่อยก็พัก",
    "pose": "ทิ้งตัวลงนอนบนก้อนเมฆนุ่ม",
    "emotion": "ผ่อนคลาย สบายอารมณ์",
    "props": "ก้อนเมฆปุยสีขาวและดาว",
    "prompt_en": "melting onto fluffy white cloud, ultimate cozy relaxing expression",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_121",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "อย่ากดดันตัวเอง",
    "pose": "ปลดกระเป๋าเป้หนักๆ ทิ้งลงพื้น",
    "emotion": "โล่งใจ ปล่อยวาง",
    "props": "ขนนกเบาหวิวค่อยๆ ร่วง",
    "prompt_en": "dropping heavy backpack onto floor, sighing in relief, floating feather",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_122",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ส่งพลังบวกให้",
    "pose": "ยิงลำแสงหัวใจสีรุ้งออกจากอก",
    "emotion": "ร่าเริง เปี่ยมพลังรัก",
    "props": "คลื่นหัวใจสีรุ้งพุ่งกระจาย",
    "prompt_en": "shooting rainbow beam of hearts from chest, joyful energetic smile",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_123",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "คนเก่งของเค้า",
    "pose": "กางแขนโผเข้ากอด อบอุ่นสุดหัวใจ",
    "emotion": "เอ็นดู ปลื้มใจ ทะนุถนอม",
    "props": "ละอองดาวและหัวใจสีชมพู",
    "prompt_en": "running in for warm proud hug, deeply affectionate eyes, pink stardust",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_124",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "อยู่ข้างๆ เสมอนะ",
    "pose": "นั่งเคียงข้าง จับมือให้ความอบอุ่น",
    "emotion": "มั่นคง จริงใจ ไม่ทอดทิ้ง",
    "props": "ร่มคันเดียวบังแดดฝนสองคน",
    "prompt_en": "sitting side by side holding hands firmly, steady comforting presence",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_125",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ทนอีกนิดนะ",
    "pose": "นับถอยหลังบนปฏิทิน กัดฟันสู้",
    "emotion": "อดทน มุ่งมั่น สู้ไม่ถอย",
    "props": "เทียนไขที่ยังส่องสว่าง",
    "prompt_en": "crossing off calendar days gritting teeth, enduring steadfast spirit",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_126",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "พร้อมรับฟังเสมอ",
    "pose": "เอามือป้องหู ส่งสายตาพร้อมฟัง",
    "emotion": "ตั้งใจ ใส่ใจ อบอุ่นใจ",
    "props": "ถ้วยโกโก้ร้อนควันฉุย",
    "prompt_en": "cupping hand to ear leaning in, caring listening posture, hot cocoa mug",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_127",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ไม่เป็นไร เอาใหม่",
    "pose": "ลุกขึ้นปัดฝุ่นที่หัวเข่า ยิ้มสู้",
    "emotion": "ไม่ยอมแพ้ กระตือรือร้น",
    "props": "ผ้าพันแผลรูปหัวใจ",
    "prompt_en": "dusting off knees standing back up with fighting grin, heart bandage",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_128",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เติมพลังแป๊บ",
    "pose": "เสียบปลั๊กชาร์จไฟเข้าตัวเอง",
    "emotion": "ตาหรี่ กำลังรีชาร์จ",
    "props": "สายชาร์จและไอคอนแบตเขียว",
    "prompt_en": "plugging charger into own back recharging, funny cute electric recharge",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_129",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เก่งขึ้นทุกวัน",
    "pose": "ยืนเทียบส่วนสูงกับขีดบนกำแพง",
    "emotion": "ภูมิใจ มั่นใจในพัฒนาการ",
    "props": "เส้นกราฟพุ่งขึ้นสู่ฟ้า",
    "prompt_en": "measuring growth marks on wall, proud confident posture, upward green arrow",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_130",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ความพยายามไม่ทรยศใคร",
    "pose": "ยืนเหงื่อท่วมกำหมัดแน่นบนยอดเขา",
    "emotion": "เข้มแข็ง ภาคภูมิใจ สง่างาม",
    "props": "ธงยอดเขาและพระอาทิตย์",
    "prompt_en": "sweaty but standing victorious on peak, unwavering triumphant spirit",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_131",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เก่งมากคนดี",
    "pose": "เอามือลูบหัวเบาๆ ตบหลังมือ",
    "emotion": "อ่อนโยน ทะนุถนอม",
    "props": "กลีบซากุระร่วงโรย",
    "prompt_en": "gently stroking hair with tender affectionate smile, falling cherry blossoms",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_132",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "สู้ไปด้วยกัน",
    "pose": "ประสานมือเป็นวงกลมรวมพลัง",
    "emotion": "สามัคคี มั่นใจ ไร้พ่าย",
    "props": "ประกายไฟแห่งมิตรภาพ",
    "prompt_en": "hands stacked together in team huddle, united passionate expressions",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_133",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "รักตัวเองเยอะๆ นะ",
    "pose": "กอดตัวเองแน่นๆ ยิ้มให้กระจก",
    "emotion": "มีความสุขกับตัวเอง ภูมิใจ",
    "props": "หัวใจทองคำสว่างในอก",
    "prompt_en": "hugging oneself tightly smiling at mirror, self-love glowing golden heart",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_134",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "อย่าลืมกินข้าวนะ",
    "pose": "ยกปิ่นโตอาหารมาส่งให้",
    "emotion": "ห่วงใย จากใจจริง",
    "props": "ควันหอมของกับข้าวร้อนๆ",
    "prompt_en": "holding out multi-tier lunch tiffin box, warm caring motherly smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_135",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "อย่าลืมดื่มน้ำ",
    "pose": "ยื่นกระติกน้ำใบใหญ่ให้ดื่ม",
    "emotion": "สดชื่น ห่วงใยสุขภาพ",
    "props": "หยดน้ำประกายใสแจ๋ว",
    "prompt_en": "handing giant water bottle, cheerful healthy reminder, water droplets",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_136",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "นอนไวๆ นะคืนนี้",
    "pose": "ชี้เข็มนาฬิกาเตือน สวมชุดนอน",
    "emotion": "ห่วงใย น่ารัก",
    "props": "ดาวตกและพระจันทร์ยิ้ม",
    "prompt_en": "pointing at clock in pajamas, sweet caring bedtime reminder, smiling moon",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_137",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "มีเค้าอยู่ตรงนี้นะ",
    "pose": "โบกมือกระโดดให้เห็น ยิ้มกว้าง",
    "emotion": "ให้ความมั่นใจ ไม่โดดเดี่ยว",
    "props": "แสงไฟสปอตไลต์ส่องลงมา",
    "prompt_en": "jumping and waving brightly here for you, spotlight shining down",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_138",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ปล่อยวางบ้างนะ",
    "pose": "แบมือเป่าดอกแดนดิไลออนลอยไป",
    "emotion": "สงบนิ่ง ผ่อนคลาย โล่งใจ",
    "props": "ปุยดอกไม้ลอยละล่องในลม",
    "prompt_en": "blowing dandelion seeds into wind, peaceful letting-go expression",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_139",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เหนื่อยก็ร้องไห้ได้",
    "pose": "ยื่นกล่องทิชชู่นุ่มๆ ให้ซับน้ำตา",
    "emotion": "เข้าใจ ซึ้งใจ ปลอบประโลม",
    "props": "ทิชชู่ลอยรูปหัวใจ",
    "prompt_en": "offering box of soft tissues with compassionate eyes, comfort gesture",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_140",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ขอบคุณที่พยายามนะ",
    "pose": "ก้มหัวขอบคุณด้วยความซาบซึ้งใจ",
    "emotion": "ตื้นตันใจ ประทับใจอย่างยิ่ง",
    "props": "แสงดาวส่องกระทบตัว",
    "prompt_en": "bowing slightly in heartfelt gratitude for hard work, sparkling appreciation",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_141",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ไม่มีอะไรเกินความสามารถ",
    "pose": "กระโดดข้ามรั้วสูงอย่างคล่องแคล่ว",
    "emotion": "มั่นใจ คล่องแคล่ว แข็งแกร่ง",
    "props": "ปีกสีขาวงอกที่แผ่นหลัง",
    "prompt_en": "leaping over high obstacle gracefully, confident wings on back",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_142",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ใจฟูมาก",
    "pose": "เอามือกุมหน้าอก ตาเป็นประกายหวาน",
    "emotion": "ตื้นตัน มีความสุขล้นปรี่",
    "props": "หัวใจบอลลูนพองโต",
    "prompt_en": "clasping hands over puffed-up heart, starry glowing eyes, heart balloon",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_143",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "มีพลังลุยต่อ",
    "pose": "ซดเครื่องดื่มชูกำลัง ตาติดไฟ",
    "emotion": "พลังงานเต็มเปี่ยม 200%",
    "props": "ประกายสายฟ้าสีทอง",
    "prompt_en": "chugging energy drink, eyes bursting with blazing energy, golden thunder",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_144",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "ขอส่งรอยยิ้มให้",
    "pose": "ยื่นการ์ดรูปยิ้มสดใสสองมือ",
    "emotion": "ส่งความสุข เบิกบาน",
    "props": "ดอกทานตะวันและดวงอาทิตย์",
    "prompt_en": "handing yellow smiley card with two hands, radiating pure happiness",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_145",
    "category": "ให้กำลังใจ & สู้ชีวิต",
    "caption": "เธอคือคนเก่ง",
    "pose": "ชี้มาข้างหน้าพร้อมมอบมงกุฎให้",
    "emotion": "เชิดชู มั่นใจ อบอุ่น",
    "props": "มงกุฎทองประดับเพชร",
    "prompt_en": "pointing forward presenting sparkling golden crown, encouraging smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_146",
    "category": "เงินทอง & สายเปย์",
    "caption": "เงินเดือนออกแล้ว",
    "pose": "ชูปึกธนบัตรโปรยปรายรอบตัว",
    "emotion": "ฟินสุดขีด ยิ้มปากกว้าง",
    "props": "ฝนธนบัตรสีเทาลอยฟุ้ง",
    "prompt_en": "throwing rain of hundred-dollar bills into air, ecstatic grinning face",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_147",
    "category": "เงินทอง & สายเปย์",
    "caption": "โอนไวมาก",
    "pose": "จิ้มหน้าจอมือถือสปีดแสง ชูสลิป",
    "emotion": "เปย์ไว ป๋ามาก มั่นใจ",
    "props": "สลิปโอนเงินติดปีกบิน",
    "prompt_en": "tapping phone screen at lightning speed showing transfer slip, money with wings",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_148",
    "category": "เงินทอง & สายเปย์",
    "caption": "ขอเลขบัญชีหน่อย",
    "pose": "ถือปากการอจดสมุดบัญชี",
    "emotion": "สายเปย์ พร้อมโอนทันที",
    "props": "เหรียญทองหล่นกิ๊งๆ",
    "prompt_en": "pen ready over bank passbook, ready to transfer money, jingling gold coins",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_149",
    "category": "เงินทอง & สายเปย์",
    "caption": "โอนเรียบร้อย",
    "pose": "ชูสลิปเงินแผ่นใหญ่ ยิ้มกริ่ม",
    "emotion": "สบายใจ ภารกิจจ่ายเงินเสร็จ",
    "props": "เครื่องหมายถูกสีเขียวบนสลิป",
    "prompt_en": "flashing big bank receipt with cool confident grin, green verified check",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_150",
    "category": "เงินทอง & สายเปย์",
    "caption": "เปย์หมดหน้าตัก",
    "pose": "เทกระเป๋าตังค์เปิดกว้างไม่มีกั๊ก",
    "emotion": "ใจป๋า ใจถึง พึ่งได้",
    "props": "ประกายเพชรพลอยแวววาว",
    "prompt_en": "dumping wallet wide open without hesitation, diamond sparkles",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_151",
    "category": "เงินทอง & สายเปย์",
    "caption": "ของมันต้องมี",
    "pose": "กอดกล่องพัสดุช็อปปิ้งเต็มสองแขน",
    "emotion": "ตาโตหลงใหล มีความสุข",
    "props": "กล่องพัสดุผูกโบว์กองโต",
    "prompt_en": "hugging stack of parcel delivery boxes tightly, starry obsessed eyes",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_152",
    "category": "เงินทอง & สายเปย์",
    "caption": "กดสั่งไปแล้ว",
    "pose": "กดปุ่มสั่งซื้อในมือถือแล้วหัวเราะหึๆ",
    "emotion": "สะใจ กิเลสระงับด้วยการซื้อ",
    "props": "รถส่งของพุ่งพรวด",
    "prompt_en": "tapping 1-click buy with mischievous laugh, delivery van zooming",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_153",
    "category": "เงินทอง & สายเปย์",
    "caption": "สิ้นเดือนเหมือนสิ้นใจ",
    "pose": "เปิดกระเป๋าตังค์เจอตั๊กแตนบินออกมา",
    "emotion": "หมดอาลัยตายอยาก ซีดเซียว",
    "props": "กระเป๋าแบนแต๊ดแต๋ หย่อมความจน",
    "prompt_en": "opening completely flat empty wallet with moth flying out, pale ghostly face",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_154",
    "category": "เงินทอง & สายเปย์",
    "caption": "เหลือตังค์ร้อยเดียว",
    "pose": "หยิบแบงก์ร้อยใบยับกอดแนบอก",
    "emotion": "ทะนุถนอม น้ำตาซึม",
    "props": "บะหมี่กึ่งสำเร็จรูปชามเล็ก",
    "prompt_en": "hugging single wrinkled bank note teary eyed, instant noodle cup beside",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_155",
    "category": "เงินทอง & สายเปย์",
    "caption": "แกล้งจน",
    "pose": "นั่งนับทองคำแท่งใต้ผ้าห่ม",
    "emotion": "เจ้าเล่ห์ ขี้เล่น รวยเงียบ",
    "props": "หีบสมบัติทองคำซ่อนอยู่",
    "prompt_en": "counting gold bars secretly under blanket, cheeky rich grin, treasure chest",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_156",
    "category": "เงินทอง & สายเปย์",
    "caption": "รวยมากบอกเลย",
    "pose": "ใส่สร้อยทองเส้นโต แหวนเพชรเต็มมือ",
    "emotion": "อวดรวย เก๊กไฮโซ ขำขัน",
    "props": "แว่นตากันแดดขอบทอง ประกายวิ้ง",
    "prompt_en": "draped in thick gold chains and diamond rings, comically flaunting wealth",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_157",
    "category": "เงินทอง & สายเปย์",
    "caption": "รอเงินเข้า",
    "pose": "นั่งเฝ้าหน้าจอมือถือไม่กะพริบตา",
    "emotion": "ลุ้นระทึก จิตใจจดจ่อ",
    "props": "ไอคอนยอดเงินหมุนติ้วๆ",
    "prompt_en": "staring intensely at banking app screen waiting for alert, loading spinner",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_158",
    "category": "เงินทอง & สายเปย์",
    "caption": "ยอดเงินเข้าแล้ว",
    "pose": "กรี๊ดลั่นบ้าน เต้นระบำฉลอง",
    "emotion": "ดีใจสุดขีด สดชื่นกระปรี้กระเปร่า",
    "props": "ดอกไม้ไฟระเบิดตูม",
    "prompt_en": "screaming joyfully dancing victory jig, phone alert dinging, fireworks",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_159",
    "category": "เงินทอง & สายเปย์",
    "caption": "เลี้ยงข้าวหน่อย",
    "pose": "ทำตากลมโต เกาะแขนเขย่าเบาๆ",
    "emotion": "อ้อนวอน น่าสงสารแบบน่ารัก",
    "props": "ชามข้าวเปล่าชูรอ",
    "prompt_en": "holding empty rice bowl with big round begging eyes, shaking arm cute",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_160",
    "category": "เงินทอง & สายเปย์",
    "caption": "มื้อนี้พี่เลี้ยงเอง",
    "pose": "ตบกระเป๋ากางเกง ยิ้มหน้าบาน",
    "emotion": "ป๋าตัวจริง สปอร์ต ใจดี",
    "props": "การ์ดแบล็คการ์ดสีดำสะท้อนแสง",
    "prompt_en": "slapping wallet pocket proudly with big magnanimous smile, black card gleam",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_161",
    "category": "เงินทอง & สายเปย์",
    "caption": "หารกันนะ",
    "pose": "ถือเครื่องคิดเลขกดรัวๆ แยกบิล",
    "emotion": "เป๊ะทุกบาท แฟร์ๆ น่ารัก",
    "props": "ใบเสร็จยาวเป็นหางว่าว",
    "prompt_en": "tapping calculator intensely splitting bill fairly, long paper receipt",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_162",
    "category": "เงินทอง & สายเปย์",
    "caption": "จ่ายสดลดได้ไหม",
    "pose": "ยื่นปึกเงินสด เอียงคอต่อราคา",
    "emotion": "เจ้าเล่ห์ อ้อนขอส่วนลด",
    "props": "ป้าย Sale ลด 50%",
    "prompt_en": "waving cash bundle tilting head bargaining playfully, 50% off tag",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_163",
    "category": "เงินทอง & สายเปย์",
    "caption": "โปรโมชั่นลดแลกแจกแถม",
    "pose": "ถือป้ายเซลล์ 9.9 วิ่งพุ่งตัว",
    "emotion": "ตื่นเต้น ตาเป็นประกายรูปตะกร้า",
    "props": "ป้ายลดราคาและคูปองลอย",
    "prompt_en": "sprinting toward mega sale holding coupons, shopping cart eyes",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_164",
    "category": "เงินทอง & สายเปย์",
    "caption": "เก็บตังค์อยู่",
    "pose": "หยอดเหรียญลงกระปุกหมูอ้วน",
    "emotion": "มัธยัสถ์ ตั้งใจ ออมเงิน",
    "props": "กระปุกหมูยิ้มหวานแก้มชมพู",
    "prompt_en": "dropping coin into chubby smiling piggy bank, determined saving pose",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_165",
    "category": "เงินทอง & สายเปย์",
    "caption": "หมดตัวแล้วจ้า",
    "pose": "ล้วงกระเป๋ากางเกงปลิ้นออกมามีแต่ลม",
    "emotion": "แห้งแล้ง ไส้แห้ง ขำขื่น",
    "props": "ใบไม้แห้งปลิวผ่าน",
    "prompt_en": "pulling out inside-out empty pockets, comical tumbleweed blowing by",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_166",
    "category": "เงินทอง & สายเปย์",
    "caption": "สายเปย์ตัวจริง",
    "pose": "โปรยการ์ดเครดิตเหมือนเล่นไพ่",
    "emotion": "มั่นใจ รวยเสน่ห์ ชิคๆ",
    "props": "ประกายเพชรและช่อกุหลาบ",
    "prompt_en": "fanning out luxury credit cards like playing cards, glamorous charisma",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_167",
    "category": "เงินทอง & สายเปย์",
    "caption": "ใครจ่าย",
    "pose": "ชี้นิ้วเป็นวงกลมมองหน้าเพื่อนทุกคน",
    "emotion": "ระแวง ตาเลิกลั่ก",
    "props": "เครื่องหมายคำถามหมุนรอบโต๊ะ",
    "prompt_en": "pointing fingers in circle looking around table who will pay, awkward grin",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_168",
    "category": "เงินทอง & สายเปย์",
    "caption": "พร้อมเปย์เสมอ",
    "pose": "หยิบกระเป๋าเงินเปิดอ้าพร้อมจ่าย",
    "emotion": "ยินดี ทุ่มสุดตัวเพื่อเธอ",
    "props": "หัวใจทองคำพุ่งจากกระเป๋า",
    "prompt_en": "opening wallet instantly with devoted loving look, gold hearts popping out",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_169",
    "category": "เงินทอง & สายเปย์",
    "caption": "กินหรูอยู่สบาย",
    "pose": "นั่งจิบค็อกเทลหน้าสเต็กจานโต",
    "emotion": "หรูหรา ไฮโซ สบายอารมณ์",
    "props": "แก้วไวน์และเทียนหอม",
    "prompt_en": "sipping cocktail enjoying lavish steak dinner, luxurious sophisticated vibe",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_170",
    "category": "เงินทอง & สายเปย์",
    "caption": "มาม่าทั้งเดือน",
    "pose": "นั่งต้มบะหมี่กึ่งสำเร็จรูป ซดน้ำซุป",
    "emotion": "อดทนเพื่ออนาคต ตาหยี",
    "props": "ควันบะหมี่ลอยเป็นรูปหัวใจ",
    "prompt_en": "slurping instant noodles happily under desk lamp, cozy frugal moment",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_171",
    "category": "เงินทอง & สายเปย์",
    "caption": "เศรษฐีท่านหนึ่ง",
    "pose": "นั่งบนเก้าอี้ทองคำ ถือไม้เท้าทอง",
    "emotion": "เก๊กท่าเศรษฐี รวยล้นฟ้า",
    "props": "ถุงทองคำใบยักษ์ข้างบัลลังก์",
    "prompt_en": "sitting on golden throne holding scepter, comically grandiose billionaire pose",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_172",
    "category": "เงินทอง & สายเปย์",
    "caption": "ช้อปปิ้งบำบัด",
    "pose": "เดินหิ้วถุงแบรนด์เนม 10 ใบสองมือ",
    "emotion": "เบิกบาน หายเครียดทันที",
    "props": "ถุงช้อปปิ้งหลากสีสดใส",
    "prompt_en": "walking triumphantly with ten designer shopping bags, sheer retail bliss",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_173",
    "category": "เงินทอง & สายเปย์",
    "caption": "ขอเงินหน่อย",
    "pose": "แบมือสองข้างส่งสายตาออดอ้อน",
    "emotion": "น่าสงสาร อยากได้ตังค์",
    "props": "ลูกหมาตากลมโตสะท้อนแสง",
    "prompt_en": "cupping hands begging with ultimate puppy eyes, cute pleading aura",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_174",
    "category": "เงินทอง & สายเปย์",
    "caption": "ห้ามใจไม่ไหว",
    "pose": "เอามือปิดตาข้างเดียวแอบดูปุ่มซื้อ",
    "emotion": "แพ้กิเลส ใจสั่น",
    "props": "ปีศาจน้อยกระซิบข้างหู 'ซื้อเลย'",
    "prompt_en": "peeking through fingers at buy button, tiny angel and devil on shoulders",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_175",
    "category": "เงินทอง & สายเปย์",
    "caption": "ลดราคาไม่ได้เหรอ",
    "pose": "พนมมือช้อนตามองแม่ค้า",
    "emotion": "อ้อนขั้นเทพ ต่อราคา",
    "props": "หัวใจกระพริบวิบวับ",
    "prompt_en": "pleading cutely with vendor for discount, batting eyelashes",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_176",
    "category": "เงินทอง & สายเปย์",
    "caption": "พร้อมโอนเสมอ",
    "pose": "นั่งจิ้มสแกน QR Code ทันที",
    "emotion": "รวดเร็วฉับไว ไม่ลีลา",
    "props": "กรอบสแกน QR Code สีฟ้าสด",
    "prompt_en": "scanning QR code instantly on phone screen, snappy responsive grin",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_177",
    "category": "เงินทอง & สายเปย์",
    "caption": "ยอดปังมาก",
    "pose": "ชูกราฟยอดขายพุ่งทะลุเพดาน",
    "emotion": "ดีใจ ธุรกิจรุ่งเรือง",
    "props": "เหรียญทองระเบิดฉลอง",
    "prompt_en": "holding sales chart shooting through the ceiling, ecstatic merchant success",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_178",
    "category": "เงินทอง & สายเปย์",
    "caption": "ขายดีเทน้ำเทท่า",
    "pose": "แพ็คของกล่องพัสดุเป็นภูเขา",
    "emotion": "มือเป็นระวิง ยิ้มแก้มปริ",
    "props": "เทปกาวและกล่องพัสดุล้นห้อง",
    "prompt_en": "packing mountains of parcels with flying hands, booming business smile",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_179",
    "category": "เงินทอง & สายเปย์",
    "caption": "รวยไม่ไหว",
    "pose": "นอนบนกองเหรียญทองคำเหมือนว่ายน้ำ",
    "emotion": "ฟินเกินต้าน อิ่มความรวย",
    "props": "เหรียญทองระยิบระยับทุกทิศ",
    "prompt_en": "swimming gleefully in mountain of gold coins like Scrooge McDuck",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_180",
    "category": "เงินทอง & สายเปย์",
    "caption": "ตังค์หมดแต่ของต้องมี",
    "pose": "นั่งมองของที่เพิ่งซื้อมาด้วยความปลื้ม",
    "emotion": "หมดตัวแต่มีความสุข",
    "props": "กล่องสินค้าส่องแสงวิ้งๆ",
    "prompt_en": "admiring new gadget with empty wallet beside, joyful broke expression",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_181",
    "category": "เงินทอง & สายเปย์",
    "caption": "เงินทองไหลมาเทมา",
    "pose": "กวักมือสองข้างเรียกลาภก้อนโต",
    "emotion": "เบิกบาน มั่งคั่ง ร่ำรวย",
    "props": "สายน้ำทองคำไหลเข้ากระเป๋า",
    "prompt_en": "beckoning with both hands calling wealth, river of gold flowing in",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_182",
    "category": "เงินทอง & สายเปย์",
    "caption": "กระเป๋าตังค์สั่น",
    "pose": "จับกระเป๋าตังค์ที่สั่นดุ๊กดิ๊กจะซื้อของ",
    "emotion": "ต้านทานไม่ไหว กิเลสพุ่ง",
    "props": "สายฟ้าแลบออกจากกระเป๋า",
    "prompt_en": "clutching vibrating wallet ready to spend, comically overwhelmed by urge",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_183",
    "category": "เงินทอง & สายเปย์",
    "caption": "สแกนจ่ายง่ายนิดเดียว",
    "pose": "ยื่นมือถือโชว์หน้าจอแอปธนาคาร",
    "emotion": "ทันสมัย สบายๆ",
    "props": "แสงสแกนสีฟ้าวาบ",
    "prompt_en": "holding up smartphone with mobile banking app ready, sleek modern vibe",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_184",
    "category": "เงินทอง & สายเปย์",
    "caption": "รอโบนัส",
    "pose": "นั่งจ้องปฏิทินสิ้นปี ตาเป็นประกาย",
    "emotion": "เฝ้ารอคอยความหวังสูงสุด",
    "props": "หีบโบนัสมีปีกบินวนเวียน",
    "prompt_en": "staring at year-end calendar with sparkling hopeful eyes, flying bonus chest",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_185",
    "category": "เงินทอง & สายเปย์",
    "caption": "โบนัสออกแล้ว",
    "pose": "โยนหมวกขึ้นฟ้า วิ่งรอบห้อง",
    "emotion": "ตื่นเต้น กรี๊ดสลบ มีความสุข",
    "props": "พลุสีทองและสายรุ้งฉลอง",
    "prompt_en": "tossing hat in air sprinting happily, massive bonus celebration",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_186",
    "category": "เงินทอง & สายเปย์",
    "caption": "เปย์ตัวเองหน่อย",
    "pose": "กินไอศกรีมถ้วยยักษ์ท็อปปิ้งล้น",
    "emotion": "ให้รางวัลชีวิต สบายใจ",
    "props": "ไอศกรีมซันเดย์ประดับเชอร์รี่",
    "prompt_en": "treating oneself to giant sundae with lavish toppings, rewarding self-care",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_187",
    "category": "เงินทอง & สายเปย์",
    "caption": "จ่ายครบจบปิ๊ง",
    "pose": "พับกระเป๋าตังค์เก็บ ดีดนิ้วฉลอง",
    "emotion": "เคลียร์หนี้เสร็จสิ้น ไร้พันธะ",
    "props": "ใบเสร็จตีตรา PAID สีเขียว",
    "prompt_en": "snapping wallet shut with triumphant finger snap, stamped PAID in green",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_188",
    "category": "เงินทอง & สายเปย์",
    "caption": "หนี้หมดแล้ว",
    "pose": "วิ่งกางแขนรับลมบนทุ่งหญ้ากว้าง",
    "emotion": "อิสระ ปลอดโปร่ง โล่งอก",
    "props": "โซ่ตรวนแตกกระจายเป็นผุยผง",
    "prompt_en": "running freely across open meadow, shattered chains breaking into sparkles",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_189",
    "category": "เงินทอง & สายเปย์",
    "caption": "รวยความสุข",
    "pose": "นั่งอมยิ้มกอดเข่า มีความสุขกับสิ่งเล็กๆ",
    "emotion": "อิ่มเอมใจ เพียงพอ สดใส",
    "props": "หัวใจอบอุ่นและใบไม้ผลิ",
    "prompt_en": "smiling warmly hugging knees, rich in simple happiness, warm glowing heart",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_190",
    "category": "เงินทอง & สายเปย์",
    "caption": "ขอค่าขนมหน่อย",
    "pose": "ยื่นซองจดหมายเปล่า ทำตาละห้อย",
    "emotion": "เด็กดีขอตังค์ ออดอ้อน",
    "props": "ขนมเค้กและลูกกวาดลอย",
    "prompt_en": "holding empty allowance envelope with sweet pleading look, candy icons",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_191",
    "category": "สายกิน & ชวนหิว",
    "caption": "หิวข้าวมาก",
    "pose": "เอามือกุมท้องที่ร้องโครกคราก",
    "emotion": "ตาละห้อย หิวโซ ไส้กิ่ว",
    "props": "จานข้าวเปล่ามีช้อนส้อมไขว้",
    "prompt_en": "clutching grumbling belly with teary famished eyes, empty plate icon",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_192",
    "category": "สายกิน & ชวนหิว",
    "caption": "ชานมไข่มุกเยียวยา",
    "pose": "กอดแก้วชานมไข่มุกยักษ์ดูดฟินๆ",
    "emotion": "ฟินสุดติ่ง มีความสุขล้นพ้น",
    "props": "ไข่มุกสีดำเด้งดึ๋งรอบแก้ว",
    "prompt_en": "hugging giant boba bubble tea cup blissfully sipping, bouncing boba",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_193",
    "category": "สายกิน & ชวนหิว",
    "caption": "หมูกระทะไหม",
    "pose": "ถือที่คีบคีบเบคอนย่างบนเตา",
    "emotion": "ตาวาว ชักชวนสุดพลัง",
    "props": "ควันหมูกระทะหอมฉุย",
    "prompt_en": "holding tongs grilling pork on Thai BBQ pan, hungry sparkling eyes, fragrant smoke",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_194",
    "category": "สายกิน & ชวนหิว",
    "caption": "ของหวานคือชีวิต",
    "pose": "ตักเค้กช็อกโกแลตคำโตเข้าปาก",
    "emotion": "เคลิบเคลิ้ม หวานฉ่ำ",
    "props": "เค้กและมาการองลอย",
    "prompt_en": "eating huge slice of chocolate cake with melting blissful expression",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_195",
    "category": "สายกิน & ชวนหิว",
    "caption": "ลดความอ้วนพรุ่งนี้",
    "pose": "กินพิซซ่าชีสยืดคำใหญ่ ไม่สนแคล",
    "emotion": "เอ็นจอยอีตติ้ง ยิ้มกริ่ม",
    "props": "ชีสเยิ้มยืดเป็นสายยาว",
    "prompt_en": "stuffing face with gooey cheesy pizza slice, 'diet starts tomorrow' smirk",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_196",
    "category": "สายกิน & ชวนหิว",
    "caption": "อิ่มจนพุงกาง",
    "pose": "นั่งพิงเก้าอี้ ลูบพุงกลมป่อง",
    "emotion": "อิ่มแป้ แน่นท้อง ฟินสุดๆ",
    "props": "กระดุมเสื้อดีดกระเด็นขำๆ",
    "prompt_en": "leaning back rubbing round full belly, popping shirt button comical",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_197",
    "category": "สายกิน & ชวนหิว",
    "caption": "ขออีกจาน",
    "pose": "ชูจานเปล่า ยื่นช้อนส้อมขอเบิ้ล",
    "emotion": "ยังไม่อิ่ม ตาวิบวับ",
    "props": "ประกายความหิวโซ",
    "prompt_en": "raising empty plate asking for second round, enthusiastic hungry eyes",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_198",
    "category": "สายกิน & ชวนหิว",
    "caption": "แซ่บมาก",
    "pose": "ซดส้มตำพริก 10 เม็ดแลบลิ้นพ่นไฟ",
    "emotion": "เผ็ดซี๊ด อร่อยเด็ด จัดจ้าน",
    "props": "เปลวไฟพ่นออกจากปาก",
    "prompt_en": "slurping spicy papaya salad tongue out breathing fire, sweat drops, chili icons",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_199",
    "category": "สายกิน & ชวนหิว",
    "caption": "กินไม่หยุด",
    "pose": "สองมือถือแฮมเบอร์เกอร์และเฟรนช์ฟรายส์",
    "emotion": "เพลิดเพลิน เคี้ยวตุ้ยๆ",
    "props": "เศษขนมลอยรอบแก้ม",
    "prompt_en": "eating burger in one hand fries in other, cheeks stuffed like hamster",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_200",
    "category": "สายกิน & ชวนหิว",
    "caption": "ของอร่อยบอกต่อ",
    "pose": "ยกนิ้วโป้งให้ชามราเมนร้อนๆ",
    "emotion": "การันตีความอร่อยระดับเทพ",
    "props": "ตราการันตีความอร่อย 5 ดาว",
    "prompt_en": "giving thumbs up to steaming ramen bowl, 5-star delicious stamp",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_201",
    "category": "สายกิน & ชวนหิว",
    "caption": "คาเฟ่ฮอปปิ้ง",
    "pose": "ถือกล้องถ่ายรูปแก้วกาแฟและครัวซองต์",
    "emotion": "ชิคๆ คูลๆ สไตล์มินิมอล",
    "props": "เมล็ดกาแฟและครัวซองต์เนยสด",
    "prompt_en": "posing aesthetic cafe shot holding camera with latte and croissant",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_202",
    "category": "สายกิน & ชวนหิว",
    "caption": "กินเพื่ออยู่หรืออยู่เพื่อกิน",
    "pose": "นอนกอดโดนัทกลมยักษ์แทนหมอน",
    "emotion": "คำถามเชิงปรัชญาสายกิน",
    "props": "ขนมหวานลอยเป็นกาแล็กซี",
    "prompt_en": "pondering meaning of life hugging giant glazed donut like pillow",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_203",
    "category": "สายกิน & ชวนหิว",
    "caption": "ชีสคือความรัก",
    "pose": "ดึงพิซซ่ายืดชีสสูงเหนือหัว",
    "emotion": "ตื่นตาตื่นใจ ว้าวสุดๆ",
    "props": "เส้นชีสสีเหลืองทองยืดหยุ่น",
    "prompt_en": "pulling extra-cheese slice high in the air, mesmerized wide eyes",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_204",
    "category": "สายกิน & ชวนหิว",
    "caption": "กินคลีนวันแรก",
    "pose": "เคี้ยวใบสลัดทำหน้าเอียนขำๆ",
    "emotion": "กล้ำกลืนเพื่อสุขภาพ",
    "props": "ชามสลัดผักใบเขียวล้นๆ",
    "prompt_en": "chewing plain green salad leaf with hilariously forced healthy smile",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_205",
    "category": "สายกิน & ชวนหิว",
    "caption": "ต้มยำกุ้งรสเด็ด",
    "pose": "ซดน้ำซุปต้มยำกุ้งแม่น้ำตัวโต",
    "emotion": "ฟินรสชาติจัดจ้านถึงใจ",
    "props": "พริกขี้หนูและมะนาวลอย",
    "prompt_en": "sipping spicy tom yum kung with giant prawn, mouth watering expression",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_206",
    "category": "สายกิน & ชวนหิว",
    "caption": "กาแฟดำไม่ใส่น้ำตาล",
    "pose": "จิบเอสเปรสโซ่ช็อตเข้มๆ ตาโต",
    "emotion": "ตาสว่าง กระปรี้กระเปร่าทันที",
    "props": "เมล็ดกาแฟคั่วบดหอมกรุ่น",
    "prompt_en": "taking concentrated black espresso shot, eyes snapping wide open awake",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_207",
    "category": "สายกิน & ชวนหิว",
    "caption": "กินคาวไม่กินหวาน",
    "pose": "ทำหน้าไม่ยอมถ้าไม่มีของหวาน",
    "emotion": "เรียกร้องสิทธิ์สายหวาน",
    "props": "ถ้วยบิงซูเกล็ดหิมะยักษ์",
    "prompt_en": "pouting demanding dessert after meal, giant shaved ice bingsu beside",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_208",
    "category": "สายกิน & ชวนหิว",
    "caption": "เนื้อย่างเยียวยาทุกสิ่ง",
    "pose": "คีบเนื้อวากิวลายหินอ่อนลงกระทะ",
    "emotion": "หลงใหลในกลิ่นหอมกรุ่น",
    "props": "ประกายไฟเตาย่างเนื้อ",
    "prompt_en": "grilling marbled wagyu beef on charcoal grill, pure food worship face",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_209",
    "category": "สายกิน & ชวนหิว",
    "caption": "ขอน้ำเย็นแก้ว",
    "pose": "กระดกเหยือกน้ำเย็นเฉียบชื่นใจ",
    "emotion": "ดับกระหาย คลายร้อนสดชื่น",
    "props": "ก้อนน้ำแข็งและหยดน้ำเย็น",
    "prompt_en": "chugging cold iced water pitcher, ultra-refreshed satisfied sigh",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_210",
    "category": "สายกิน & ชวนหิว",
    "caption": "สลัดผักเพื่อเธอ",
    "pose": "จัดจานสลัดผักผลไม้สีสวยงาม",
    "emotion": "ใส่ใจสุขภาพ น่าทาน",
    "props": "ผลไม้อะโวคาโดและส้มสด",
    "prompt_en": "presenting fresh colorful fruit salad plate, wholesome healthy smile",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_211",
    "category": "สายกิน & ชวนหิว",
    "caption": "ของหวานจะเยียวยา",
    "pose": "ตักไอศกรีมสตอเบอรี่เข้าปาก",
    "emotion": "ใจละลาย ฟินสุดหัวใจ",
    "props": "สตรอว์เบอร์รี่สดลูกโต",
    "prompt_en": "eating strawberry ice cream spoonful, melting cheeks in sweetness",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_212",
    "category": "สายกิน & ชวนหิว",
    "caption": "หิวดึกอีกแล้ว",
    "pose": "เปิดตู้เย็นตอนตี 2 แสงส่องหน้า",
    "emotion": "แอบกินเงียบๆ ตลกๆ",
    "props": "แสงสีฟ้าสว่างวาบจากตู้เย็น",
    "prompt_en": "sneaking food from fridge at 2 AM, fridge light illuminating guilty grin",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_213",
    "category": "สายกิน & ชวนหิว",
    "caption": "ก๋วยเตี๋ยวต้มยำ",
    "pose": "คีบเส้นบะหมี่หมูสับลูกชิ้นคำโต",
    "emotion": "อร่อยจนหยุดไม่อยู่",
    "props": "ควันหอมฉุยและพริกป่น",
    "prompt_en": "lifting noodles with chopsticks from Thai spicy noodle bowl, steam rising",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_214",
    "category": "สายกิน & ชวนหิว",
    "caption": "สายบุฟเฟต์",
    "pose": "กางแขนหน้าเคาน์เตอร์อาหารตักไม่อั้น",
    "emotion": "พร้อมฟาดเรียบ ไม่มียั้ง",
    "props": "จานอาหารเรียงซ้อน 10 ชั้น",
    "prompt_en": "standing before lavish buffet spread with glowing eyes, tall plate stack",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_215",
    "category": "สายกิน & ชวนหิว",
    "caption": "ขอซอสเพิ่ม",
    "pose": "บีบขวดซอสมะเขือเทศจนหยดสุดท้าย",
    "emotion": "มุ่งมั่น ไม่ยอมขาดรสชาติ",
    "props": "ขวดซอสคว่ำบีบสุดแรง",
    "prompt_en": "squeezing ketchup bottle upside down intensely for every last drop",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_216",
    "category": "สายกิน & ชวนหิว",
    "caption": "รสชาติแม่ทำ",
    "pose": "ซดแกงจืดเต้าหู้หมูสับยิ้มอุ่น",
    "emotion": "ซาบซึ้ง อิ่มอกอิ่มใจ",
    "props": "หม้อแกงดินเผาควันกรุ่น",
    "prompt_en": "sipping comforting home-cooked soup, nostalgic warm grateful smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_217",
    "category": "สายกิน & ชวนหิว",
    "caption": "ไม่เผ็ดแน่นะวิ",
    "pose": "เหงื่อแตกพลั่กแลบลิ้นพ่นควัน",
    "emotion": "โดนแกง เผ็ดจนหูอื้อ",
    "props": "พริกขี้หนูแดงเผารอบตัว",
    "prompt_en": "sweating buckets from deceptive spicy food, comical steam from ears",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_218",
    "category": "สายกิน & ชวนหิว",
    "caption": "ไอศกรีมคลายร้อน",
    "pose": "ถือโคนไอศกรีม 3 ชั้นหลากสี",
    "emotion": "สดใส ร่าเริง ดับร้อน",
    "props": "เกล็ดน้ำแข็งและไอเย็น",
    "prompt_en": "holding triple-scoop colorful ice cream cone, joyful summer smile",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_219",
    "category": "สายกิน & ชวนหิว",
    "caption": "กินปิ้งย่างกัน",
    "pose": "สวมผ้ากันเปื้อนถือคีมเตรียมย่าง",
    "emotion": "กระตือรือร้น พร้อมลุยปาร์ตี้",
    "props": "เตาถ่านไฟลุกแดง",
    "prompt_en": "wearing chef apron holding tongs ready for BBQ party, eager grin",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_220",
    "category": "สายกิน & ชวนหิว",
    "caption": "ชิมคำเดียว",
    "pose": "ตักจานเพื่อนคำเบ้อเริ่มจนแทบหมด",
    "emotion": "หน้ามึน ทะเล้น แย่งกิน",
    "props": "ช้อนไซส์ยักษ์",
    "prompt_en": "taking a 'tiny bite' that eats half the burger, hilariously cheeky face",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_221",
    "category": "สายกิน & ชวนหิว",
    "caption": "เบเกอรี่อบใหม่",
    "pose": "สูดดมกลิ่นขนมปังอบร้อนจากเตา",
    "emotion": "หอมละมุน ชื่นใจ",
    "props": "ก้อนขนมปังสีทองกรอบนอกนุ่มใน",
    "prompt_en": "inhaling aroma of freshly baked golden bread loaf, blissful expression",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_222",
    "category": "สายกิน & ชวนหิว",
    "caption": "อาหารคลีนรสชาติอร่อย",
    "pose": "ชูจานอกไก่ผักต้มยิ้มมั่นใจ",
    "emotion": "สุขภาพดี รูปร่างเป๊ะ",
    "props": "กล้ามแขนล่ำเล็กๆ แข็งแรง",
    "prompt_en": "holding tasty grilled chicken and veggies, proud fit healthy pose",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_223",
    "category": "สายกิน & ชวนหิว",
    "caption": "บิงซูถ้วยยักษ์",
    "pose": "จ้วงช้อนลงบนยอดภูเขาบิงซู",
    "emotion": "ตาวาว อร่อยเย็นเจี๊ยบ",
    "props": "เกล็ดนมสโนว์นุ่มฟู",
    "prompt_en": "digging spoon into giant snow bingsu mountain, delighted cold chills",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_224",
    "category": "สายกิน & ชวนหิว",
    "caption": "ขอเบิ้ลสอง",
    "pose": "ชูสองนิ้วสั่งแม่ค้าเพิ่มพิเศษ",
    "emotion": "ติดใจ อร่อยไม่หยุด",
    "props": "ชามเปล่า 2 ใบคอนเฟิร์ม",
    "prompt_en": "raising two fingers ordering double portion, completely hooked",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_225",
    "category": "สายกิน & ชวนหิว",
    "caption": "รสชาติในตำนาน",
    "pose": "หลับตาพริ้มยกมือไหว้ขอบคุณเชฟ",
    "emotion": "เคลิบเคลิ้ม อร่อยแสงออกปาก",
    "props": "ลำแสงสีทองพุ่งออกจากปาก",
    "prompt_en": "eyes closed tasting legendary dish, golden rays bursting from mouth",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_226",
    "category": "สายกิน & ชวนหิว",
    "caption": "กินผลไม้กัน",
    "pose": "ถือถาดแตงโมและมะม่วงสุกสีฉ่ำ",
    "emotion": "สดชื่น วิตามินซีเต็มเปี่ยม",
    "props": "แตงโมสีแดงสดฉ่ำน้ำ",
    "prompt_en": "holding platter of juicy watermelon slices, refreshing summer vibe",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_227",
    "category": "สายกิน & ชวนหิว",
    "caption": "หิวแสงหรือหิวข้าว",
    "pose": "ชี้ไปที่ท้องแล้วชี้ไปที่ไฟสปอตไลท์",
    "emotion": "ตลก ล้อเลียน ขี้เล่น",
    "props": "สปอตไลท์ส่องลงที่ท้อง",
    "prompt_en": "pointing at tummy then at spotlight, witty humorous sticker expression",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_228",
    "category": "สายกิน & ชวนหิว",
    "caption": "กาแฟส้มแก้วโปรด",
    "pose": "ถือแก้วกาแฟน้ำส้มสดแยกชั้นสวย",
    "emotion": "สดชื่น ตาสว่าง มีสไตล์",
    "props": "ชิ้นส้มฝานประดับปากแก้ว",
    "prompt_en": "holding stylish orange americano layered coffee, refreshing modern pose",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_229",
    "category": "สายกิน & ชวนหิว",
    "caption": "อาหารบำรุงสมอง",
    "pose": "กินวอลนัทและปลาแซลมอนยิ้มแป้น",
    "emotion": "ฉลาด ปราดเปรียว สดใส",
    "props": "ประกายไอคิวเปล่งปลั่ง",
    "prompt_en": "eating brain-food walnuts and salmon, clever sparkling expression",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_230",
    "category": "สายกิน & ชวนหิว",
    "caption": "น้ำผลไม้ปั่น",
    "pose": "ดูดสมูทตี้ผลไม้รวมผ่านหลอดดูด",
    "emotion": "สดชื่น สุขภาพดี แก้มชมพู",
    "props": "ผลไม้เบอร์รี่สดลอยรอบแก้ว",
    "prompt_en": "sipping colorful mixed berry smoothie, glowing healthy flushed cheeks",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_231",
    "category": "สายกิน & ชวนหิว",
    "caption": "แซ่บจนน้ำตาไหล",
    "pose": "ซับน้ำตาที่ไหลพรากแต่ยังกินต่อ",
    "emotion": "เผ็ดแต่อร่อยหยุดไม่ได้",
    "props": "พริกชี้ฟ้าแดงระเบิด",
    "prompt_en": "crying tears from extreme chili heat but still eating, hooked masochist foodie",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_232",
    "category": "สายกิน & ชวนหิว",
    "caption": "กินเค้กไม่รู้สึกผิด",
    "pose": "ตักชีสเค้กเข้าปากแล้วยักไหล่",
    "emotion": "ปล่อยใจ ปล่อยจอย",
    "props": "มาตรวัดแคลอรี่พังทลาย",
    "prompt_en": "eating cheesecake shrugging carefree, broken calorie meter icon",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_233",
    "category": "สายกิน & ชวนหิว",
    "caption": "ข้าวมันไก่พิเศษ",
    "pose": "ยกจานข้าวมันไก่ตอนเนื้อน่องฉ่ำ",
    "emotion": "น้ำลายสอ พร้อมราดน้ำจิ้ม",
    "props": "ถ้วยน้ำจิ้มเต้าเจี้ยวรสเด็ด",
    "prompt_en": "holding luscious Hainanese chicken rice plate, drooling anticipation",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_234",
    "category": "สายกิน & ชวนหิว",
    "caption": "อร่อยตะโกน",
    "pose": "ป้องปากตะโกนบอกความอร่อยลั่นทุ่ง",
    "emotion": "สุดยอด อร่อยเกินบรรยาย",
    "props": "คลื่นเสียงตัวอักษร 'อร่อย!'",
    "prompt_en": "hands cupped shouting at top of lungs how delicious it is, sound waves",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_235",
    "category": "สายกิน & ชวนหิว",
    "caption": "ค่ำนี้กินอะไร",
    "pose": "นั่งกอดเข่าคิดเมนูมื้อเย็น",
    "emotion": "ลังเล เลือกไม่ถูก น่ารัก",
    "props": "ฟองสบู่รูปก๋วยเตี๋ยวและข้าวผัด",
    "prompt_en": "hugging knees debating dinner choices, thought bubbles of street food",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_236",
    "category": "กวนๆ & มุกตลก",
    "caption": "มองบน",
    "pose": "กลอกตาขึ้นฟ้าจนเห็นตาขาว",
    "emotion": "เอือมระอา กวนประสาท",
    "props": "ลูกศรชี้ขึ้นฟ้าวนๆ",
    "prompt_en": "rolling eyes dramatically upwards, sassy exasperated smirk",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_237",
    "category": "กวนๆ & มุกตลก",
    "caption": "อย่าหาทำ",
    "pose": "ส่ายนิ้วชี้ไปมา ทำหน้าห้ามปราม",
    "emotion": "เตือนสติ ขำแห้ง กวนๆ",
    "props": "ป้ายเตือนสามเหลี่ยมสีเหลือง",
    "prompt_en": "wagging index finger in disapproval, 'don't you dare' sarcastic look",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_238",
    "category": "กวนๆ & มุกตลก",
    "caption": "แล้วไงใครแคร์",
    "pose": "ยักไหล่สองข้าง คว่ำปากเชิดหน้า",
    "emotion": "ไม่แคร์ โนสนโนแคร์ ลอยตัว",
    "props": "สายลมพัดผ่านเบาๆ",
    "prompt_en": "shrugging both shoulders chin tilted up, aloof sassy 'who cares' pose",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_239",
    "category": "กวนๆ & มุกตลก",
    "caption": "ปล่อยจอย",
    "pose": "นอนลอยคอบนแพยางกลางสระน้ำ",
    "emotion": "ชิลล์ไม่สนโลก ปล่อยวาง",
    "props": "แว่นกันแดดและเครื่องดื่มเย็น",
    "prompt_en": "floating effortlessly on pool floatie sunglasses on, pure careless zen",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_240",
    "category": "กวนๆ & มุกตลก",
    "caption": "ช็อตฟีลมาก",
    "pose": "ยืนนิ่งเป็นท่อนไม้ โดนช็อตควันออกหู",
    "emotion": "อึ้ง เสียอารมณ์ ค้างเติ่ง",
    "props": "สายฟ้าเปรี๊ยะๆ ช็อตร่าง",
    "prompt_en": "frozen rigid like statue with comical electric sparks smoking from ears",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_241",
    "category": "กวนๆ & มุกตลก",
    "caption": "ร้องไห้แป๊บ",
    "pose": "น้ำตาพุ่งเป็นสายน้ำตกออกจากตา",
    "emotion": "ดราม่าโอเวอร์แอคติ้ง ขำๆ",
    "props": "น้ำตาท่วมห้องจนต้องใช้ห่วงยาง",
    "prompt_en": "waterfall tears spouting comically from eyes, paddling in rubber dinghy",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_242",
    "category": "กวนๆ & มุกตลก",
    "caption": "หูยยยย",
    "pose": "เอามือทาบอก ทำปากจู๋ตาโต",
    "emotion": "ทึ่ง แซว แซ่บ",
    "props": "ตัวอักษร 'ย' ยืดยาว",
    "prompt_en": "hands on chest mouth shaped in 'Oooo', teasing gossipy reaction",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_243",
    "category": "กวนๆ & มุกตลก",
    "caption": "พักก่อน",
    "pose": "ยกสองมือทำสัญญาณ Timeout ขอเวลานอก",
    "emotion": "เหนื่อยใจ ไม่ไหวจะเคลียร์",
    "props": "นกหวีดกรรมการสีแดง",
    "prompt_en": "making T-sign timeout hand signal, exhausted 'take a break' expression",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_244",
    "category": "กวนๆ & มุกตลก",
    "caption": "พูดเป็นเล่น",
    "pose": "เอานิ้วเคาะหัวเพื่อนเบาๆ ขำๆ",
    "emotion": "หยอกล้อ ไม่เชื่อหรอก",
    "props": "ประกายหัวเราะก๊าก",
    "prompt_en": "tapping temple teasingly laughing out loud, playful banter",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_245",
    "category": "กวนๆ & มุกตลก",
    "caption": "ขอพื้นที่หายใจ",
    "pose": "ใช้พัดลมมือถือจ่อหน้า เป่าผมปลิว",
    "emotion": "ร้อนรน แน่นอก อึดอัด",
    "props": "ลมพัดแรงจนหน้าเบ้",
    "prompt_en": "holding mini electric fan blowing face, hair flying back dramatically",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_246",
    "category": "กวนๆ & มุกตลก",
    "caption": "สภาพพพ",
    "pose": "ส่องกระจกมองตัวเองหัวฟูตาโหล",
    "emotion": "สังเวชตัวเอง ขำขัน ปลง",
    "props": "กระจกสะท้อนคนหมดสภาพ",
    "prompt_en": "looking into mirror at messy hair and dark eye bags, laughing at own state",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_247",
    "category": "กวนๆ & มุกตลก",
    "caption": "ใครถามก่อน",
    "pose": "เอามือป้องหูมองหาคนถาม",
    "emotion": "กวนโอ๊ย หน้านิ่งสนิท",
    "props": "ความเงียบกริบิ้งกิ้งหรีดร้อง",
    "prompt_en": "cupping hand looking around listening for who asked, deadpan troll face",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_248",
    "category": "กวนๆ & มุกตลก",
    "caption": "อย่ามาแซว",
    "pose": "หน้าแดงตัวบิด เอากระเป๋าปิดหน้า",
    "emotion": "เขินหนักมาก แต่แกล้งดุ",
    "props": "ควันความร้อนพุ่งออกจากหัว",
    "prompt_en": "hiding blushing face behind bag, cute embarrassed tsundere pout",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_249",
    "category": "กวนๆ & มุกตลก",
    "caption": "เนียนเลยนะ",
    "pose": "หรี่ตาจับผิด เอานิ้วชี้ชี้หน้า",
    "emotion": "รู้ทัน จับโป๊ะได้",
    "props": "ไฟสปอตไลท์จับผู้ต้องหา",
    "prompt_en": "narrowing eyes pointing finger caught-red-handed, dramatic spotlight",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_250",
    "category": "กวนๆ & มุกตลก",
    "caption": "เกรงใจบ้าง",
    "pose": "เอามือปิดหน้าผาก ส่ายหัวเอือม",
    "emotion": "หนักใจกับพฤติกรรม ขำๆ",
    "props": "เหงื่อหยดติ๋งเม็ดเป้ง",
    "prompt_en": "facepalming with heavy sigh, shaking head at shameless antics",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_251",
    "category": "กวนๆ & มุกตลก",
    "caption": "ล้อเล่นน่า",
    "pose": "หัวเราะเอามือปิดปาก ตบไหล่เพื่อน",
    "emotion": "แซวเล่น หยอกเย้า สนุกสนาน",
    "props": "ฟองหัวเราะฮ่าๆๆ",
    "prompt_en": "laughing clapping friend on shoulder, 'just kidding' playful grin",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_252",
    "category": "กวนๆ & มุกตลก",
    "caption": "อยากกรี๊ด",
    "pose": "สูดหายใจลึก กรี๊ดใส่หมอนนุ่ม",
    "emotion": "อัดอั้น ระบายอารมณ์สุดขีด",
    "props": "คลื่นเสียงสั่นสะเทือน",
    "prompt_en": "screaming muffled into fluffy pillow, comical dramatic vent",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_253",
    "category": "กวนๆ & มุกตลก",
    "caption": "ไม่รู้ไม่ชี้",
    "pose": "เป่านกหวีดมองนกมองไม้ ทำเนียน",
    "emotion": "แกล้งไม่รู้เรื่อง รอดตัว",
    "props": "นกน้อยเกาะหัวร้องเพลง",
    "prompt_en": "whistling looking innocently at the sky, playing dumb brilliantly",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_254",
    "category": "กวนๆ & มุกตลก",
    "caption": "เดี๋ยวตีตายเลย",
    "pose": "หยิบไม้ตีพริกแกว่งไปมา แกล้งดุ",
    "emotion": "ดุแบบน่ารัก ขี้เล่น",
    "props": "ประกายไฟเปรี๊ยะๆ",
    "prompt_en": "waving wooden pestle comically threatening, adorable bossy glare",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_255",
    "category": "กวนๆ & มุกตลก",
    "caption": "แอบมองอยู่นะ",
    "pose": "แอบอยู่หลังเสา ตาโผล่มาข้างเดียว",
    "emotion": "ส่องเงียบๆ ซุ่มดู",
    "props": "กล้องส่องทางไกลคู่ใจ",
    "prompt_en": "peeking from behind pillar with one eye glinting, stealthy stalker fun",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_256",
    "category": "กวนๆ & มุกตลก",
    "caption": "จ๊ะเอ๋",
    "pose": "โผล่พรวดขึ้นมาจากใต้โต๊ะ",
    "emotion": "แกล้งให้ตกใจ ทะเล้น",
    "props": "ประกายตกใจวิ้งๆ",
    "prompt_en": "jumping up from under table shouting peekaboo, mischievous grin",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_257",
    "category": "กวนๆ & มุกตลก",
    "caption": "ตลกร้ายมาก",
    "pose": "หัวเราะแห้งๆ น้ำตาไหลหนึ่งหยด",
    "emotion": "ขำทั้งน้ำตา ชีวิตจริงยิ่งกว่าละคร",
    "props": "หน้ากากยิ้มแต่ข้างในร้องไห้",
    "prompt_en": "laughing dryly with single tear running down, tragic comedy mask",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_258",
    "category": "กวนๆ & มุกตลก",
    "caption": "เงียบกริบ",
    "pose": "ยืนท่ามกลางทุ่งหญ้า มีหรีดร้อง",
    "emotion": "เดดแอร์ ไม่มีใครตอบ",
    "props": "จิ้งหรีดดีดสีไวโอลิน",
    "prompt_en": "standing alone in complete deadpan silence, tumbleweed and cricket",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_259",
    "category": "กวนๆ & มุกตลก",
    "caption": "ขอยาดหัวเราะ",
    "pose": "กุมท้องหัวเราะจนตัวงอ น้ำตาเล็ด",
    "emotion": "ขำขี้แตกขี้แตน ไม่ไหวแล้ว",
    "props": "ตัวอักษร 55555 ลอยท่วม",
    "prompt_en": "clutching stomach bent over in hysterical laughter, tears of joy",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_260",
    "category": "กวนๆ & มุกตลก",
    "caption": "เรื่องมันเศร้า",
    "pose": "หยิบกีตาร์มาดีดเพลงเศร้าคนเดียว",
    "emotion": "ดราม่าเล่นใหญ่ เวอร์วัง",
    "props": "สายฝนตกเฉพาะบนหัวตัวเอง",
    "prompt_en": "strumming acoustic guitar melodramatically, tiny personal raincloud over head",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_261",
    "category": "กวนๆ & มุกตลก",
    "caption": "อารมณ์บ่จอย",
    "pose": "นั่งกอดอก หน้าบึ้ง ปากจู๋",
    "emotion": "หงุดหงิด งอน งี่เง่าเบาๆ",
    "props": "เมฆดำลอยเหนือหัว",
    "prompt_en": "sitting with crossed arms and huge pouty lips, dark storm cloud",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_262",
    "category": "กวนๆ & มุกตลก",
    "caption": "สาธุบุญ",
    "pose": "พนมมือนิ่ง กรวดน้ำขำๆ",
    "emotion": "ปลงในพฤติกรรม แผ่เมตตา",
    "props": "หยดน้ำกรวดลงขันเงิน",
    "prompt_en": "pouring merit water with calm sarcastic prayer hands, halo over head",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_263",
    "category": "กวนๆ & มุกตลก",
    "caption": "เก่งจริงมาเลย",
    "pose": "กวักมือท้าทาย ใส่สนับมือจิ๋ว",
    "emotion": "ท้าดวล กวนประสาท ยียวน",
    "props": "สายฟ้าแลบระหว่างสายตา",
    "prompt_en": "beckoning with hand daring opponent, cocky challenging smirk",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_264",
    "category": "กวนๆ & มุกตลก",
    "caption": "ยอมแพ้ราบคาบ",
    "pose": "โบกธงขาวนอนราบกับพื้น",
    "emotion": "สยบ ยอมแล้วจ้า ยกธงขาว",
    "props": "ธงสีขาวผืนใหญ่",
    "prompt_en": "waving white surrender flag lying flat on stomach, comic submission",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_265",
    "category": "กวนๆ & มุกตลก",
    "caption": "ทำตัวไม่ถูก",
    "pose": "เกาหัวแกรกๆ ขาบิดไปมา",
    "emotion": "เขิน เก้ๆ กังๆ งงงวย",
    "props": "เกลียวคลื่นความเคอะเขิน",
    "prompt_en": "scratching head shuffling feet awkwardly, funny bashful pose",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_266",
    "category": "กวนๆ & มุกตลก",
    "caption": "รู้หมดแต่ไม่พูด",
    "pose": "เอานิ้วชี้แตะริมฝีปาก ขยิบตา",
    "emotion": "กุมความลับ เจ้าเล่ห์",
    "props": "กุญแจล็อคปากสีทอง",
    "prompt_en": "finger on lips winking secretly, tiny golden padlock icon",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_267",
    "category": "กวนๆ & มุกตลก",
    "caption": "เบอร์หนึ่งเรื่องโม้",
    "pose": "ทำท่าเป่าแตรโอ้อวด ปากกว้าง",
    "emotion": "ขี้โม้ ตลก เฮฮา",
    "props": "แตรเป่ามีเสียง 'โม้!'",
    "prompt_en": "blowing giant brass horn bragging loudly, comical boastful expression",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_268",
    "category": "กวนๆ & มุกตลก",
    "caption": "ปวดหัวกับสิ่งนี้",
    "pose": "เอายาดมเสียบจมูกสองข้าง",
    "emotion": "วิงเวียน เป็นลมกับเรื่องไร้สาระ",
    "props": "หลอดยาดมสมุนไพรคู่",
    "prompt_en": "inhalers stuck in both nostrils rolling eyes, dizzy headache swirls",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_269",
    "category": "กวนๆ & มุกตลก",
    "caption": "เอาที่สบายใจเลย",
    "pose": "แบมือสองข้าง ผายมือเชิญตามสบาย",
    "emotion": "ประชดเบาๆ ปลงขั้นสุด",
    "props": "พรมแดงปูทางให้",
    "prompt_en": "extending hands welcoming sarcasm, 'whatever makes you happy' smile",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_270",
    "category": "กวนๆ & มุกตลก",
    "caption": "ขอยาดพักก่อน",
    "pose": "ดึงม่านรูดปิดฉากตัวเอง",
    "emotion": "ชัตดาวน์ ไม่รับรู้อะไรทั้งนั้น",
    "props": "ม่านกำมะหยี่สีแดงปิด",
    "prompt_en": "pulling theater curtain closed on oneself, exit stage left",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_271",
    "category": "กวนๆ & มุกตลก",
    "caption": "ขอพื้นที่ส่วนตัว",
    "pose": "กางเต็นท์กางร่มคลุมตัวเอง",
    "emotion": "โลกส่วนตัวสูง ห้ามเข้า",
    "props": "ป้ายห้ามรบกวนส่วนตัว",
    "prompt_en": "hiding inside mini pop-up tent, private sanctuary funny sign",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_272",
    "category": "กวนๆ & มุกตลก",
    "caption": "มองแรงมาก",
    "pose": "หรี่ตามองจิกแบบตัวแม่",
    "emotion": "จิกกัด ฟาดด้วยสายตา",
    "props": "ประกายไฟเลเซอร์จากดวงตา",
    "prompt_en": "fierce dramatic laser glare, sassy diva squint",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_273",
    "category": "กวนๆ & มุกตลก",
    "caption": "กลั้นขำไม่ไหว",
    "pose": "เอามือปิดปากแน่น แก้มป่องขำจนตัวสั่น",
    "emotion": "พยายามกลั้นแต่หลุดขำกิ๊กน่ารัก",
    "props": "แก้มป่องมีประกายวิ้งค์หยดเหงื่อการ์ตูนขำขัน",
    "prompt_en": "puffing cheeks holding back a burst of giggles, hands over mouth, cute chibi humor",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_274",
    "category": "กวนๆ & มุกตลก",
    "caption": "เหม็นความรัก",
    "pose": "สวมหน้ากากกันแก๊สพิษมองคู่รัก",
    "emotion": "หมั่นไส้คนมีคู่ อิจฉาตลกๆ",
    "props": "หัวใจสีชมพูโดนกักบริเวณ",
    "prompt_en": "wearing gas mask looking at flirting couple, comically repulsed",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_275",
    "category": "กวนๆ & มุกตลก",
    "caption": "มีเรื่องจะเมาท์",
    "pose": "ป้องปากกระซิบ ตาโตตื่นเต้น",
    "emotion": "ข่าวกรองด่วน แซ่บเว่อร์",
    "props": "เครื่องดักฟังและสายฟ้า",
    "prompt_en": "leaning in cupping mouth whispering juicy gossip, wide excited eyes",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_276",
    "category": "กวนๆ & มุกตลก",
    "caption": "ตาสว่างเลย",
    "pose": "เอานิ้วถ่างตา ดื่มกาแฟหม้อต้ม",
    "emotion": "หายง่วงทันควัน ช็อก",
    "props": "ประกายสายฟ้าในลูกตา",
    "prompt_en": "pulling eyelids wide open with fingers, lightning spark in pupils",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_277",
    "category": "กวนๆ & มุกตลก",
    "caption": "พูดไม่ออกบอกไม่ถูก",
    "pose": "เอามือกุมหน้าอก ตาเหม่อลอย",
    "emotion": "จุกอก พูดอะไรไม่ได้",
    "props": "คำพูดละลายกลายเป็นไอ",
    "prompt_en": "holding chest looking spaced out, words dissolving into thin air",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_278",
    "category": "กวนๆ & มุกตลก",
    "caption": "จะเครซี่",
    "pose": "เอามือดึงผมสองข้าง ร้องโวยวาย",
    "emotion": "สติหลุด วุ่นวาย คลั่งแล้ว",
    "props": "วิญญาณสติบินหนี",
    "prompt_en": "tugging hair with both hands screaming comically, sanity flying away",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_279",
    "category": "กวนๆ & มุกตลก",
    "caption": "เล่นใหญ่รัชดาลัย",
    "pose": "เอามือทาบอก ล้มตัวลงพิงโซฟาดราม่า",
    "emotion": "เล่นใหญ่ เบอร์แรง นางเอกละคร",
    "props": "สปอตไลท์ดราม่าส่องเดี่ยว",
    "prompt_en": "fainting dramatically onto velvet couch, theatrical stage diva pose",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_280",
    "category": "กวนๆ & มุกตลก",
    "caption": "นิ่งสงบสยบความเคลื่อนไหว",
    "pose": "นั่งสมาธิลอยตัวเหนือพื้น ยิ้มเย็น",
    "emotion": "นิ่งขรึม เหนือชั้น ปลง",
    "props": "รัศมีธรรมะรอบตัว",
    "prompt_en": "floating in lotus meditation pose serene smile, zen aura",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_281",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ว้าวุ่นเลยทีนี้",
    "pose": "เกาหัวหมุนติ้ว หน้าตาเลิ่กลั่ก",
    "emotion": "สับสน ปั่นป่วน วุ่นวายใจ",
    "props": "เกลียวคลื่นวุ่นวายหมุนรอบหัว",
    "prompt_en": "scratching head bewildered spinning around, chaotic spiral over head",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_282",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ตัวมารดา",
    "pose": "สวมมงกุฎ สวมเสื้อคลุมขนนก เดินสับขา",
    "emotion": "ควีน ตัวแม่ ทรงพลัง เลอค่า",
    "props": "สปอตไลท์และพรมแดงหรู",
    "prompt_en": "strutting fiercely in crown and feather boa, queen diva confidence",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_283",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ฉ่ำมาก",
    "pose": "สะบัดพัดขนนก ผิวกระทบแสงวิ้งๆ",
    "emotion": "เป๊ะ ปัง อิ่มเอม เต็มสิบ",
    "props": "ประกายเพชรระยิบระยับ",
    "prompt_en": "waving feather fan, dewy radiant glowing skin, sparkling diamond glints",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_284",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ฟินเว่อร์",
    "pose": "เอามือกุมแก้ม ตัวลอยขึ้นฟ้า",
    "emotion": "สุขล้นพ้น อิ่มความฟิน",
    "props": "ก้อนเมฆสีชมพูและสายรุ้ง",
    "prompt_en": "floating into air clutching cheeks in absolute ecstasy, pink clouds",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_285",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "นอยด์อ่า",
    "pose": "นั่งคุดคู้กอดเข่ามุมห้อง ปากบึ้ง",
    "emotion": "น้อยใจ เหงา หม่นหมอง",
    "props": "ต้นเห็ดงอกบนหัว เมฆฝนหยด",
    "prompt_en": "curled up hugging knees in corner pouting, tiny mushroom on head",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_286",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ช็อตฟีลตัวพ่อ",
    "pose": "โดนแช่แข็งในก้อนน้ำแข็งโปร่งใส",
    "emotion": "ค้างติ่ง เสียจังหวะ อึ้ง",
    "props": "ก้อนน้ำแข็งไอเย็นแผ่",
    "prompt_en": "frozen solid inside clear ice cube, shocked face locked in ice",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_287",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ใจฟูสุดๆ",
    "pose": "ทำมือรูปมินิฮาร์ทสองข้าง หน้าบาน",
    "emotion": "อบอุ่นหัวใจ มีความสุขเต็มเปี่ยม",
    "props": "หัวใจพองโตเต้นตุบๆ",
    "prompt_en": "making twin mini-heart finger gestures, radiant puffed-up happy smile",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_288",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ปังมากแม่",
    "pose": "ปรบมือรัวๆ สะบัดผม 360 องศา",
    "emotion": "ชื่นชมตัวแม่ ตัวมัม ชนะเลิศ",
    "props": "พลุกระดาษสีทองระเบิด",
    "prompt_en": "clapping enthusiastically whipping hair fabulously, golden confetti popper",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_289",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "คุณน้าาาา",
    "pose": "เอามือป้องปากกระซิบแซว ตื่นเต้น",
    "emotion": "ตื่นเต้น แซวสะบัด สายเม้าท์",
    "props": "ตัวอักษร 'น้า' ลอยสั่น",
    "prompt_en": "cupping mouth shouting 'Khun Naaa!' teasing gossip excitedly",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_290",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "อย่าให้ต้องพูด",
    "pose": "ชี้นิ้วเตือน กัดฟันยิ้มเหี้ยม",
    "emotion": "รู้ความลับนะ อย่าให้แฉ",
    "props": "มีด้ามสับมีดอยู่ข้างหลัง",
    "prompt_en": "wagging finger gritting teeth with sinister sweet smile, tea ready to spill",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_291",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ตะโกนว่าปัง",
    "pose": "ถือโทรโข่งสีสดตะโกนสุดเสียง",
    "emotion": "ภูมิใจ มั่นใจ ดังก้องโลก",
    "props": "คลื่นเสียงตัวอักษร PANG!",
    "prompt_en": "shouting through colorful megaphone at top of voice, soundwaves",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_292",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ฟาดมาก",
    "pose": "สะบัดแส้หรือพัดดังเพียะ โพสท่าโมเดล",
    "emotion": "สับ ละเอียด เผ็ดร้อน",
    "props": "สายฟ้าฟาดผ่าลงมา",
    "prompt_en": "snapping fan sharply posing like supermodel, lightning strike drama",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_293",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ดรอปก่อน",
    "pose": "กดปุ่มหยุดเพลง สวมหูฟังทำหน้านิ่ง",
    "emotion": "เบรกก่อน ไม่ไหวจะเคลียร์",
    "props": "ปุ่ม Pause สีเหลืองกระพริบ",
    "prompt_en": "hitting big pause button putting on headphones, stepping back chill",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_294",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "จึ้งมาก",
    "pose": "ตาเบิกกว้าง เอามือปิดปาก ประทับใจ",
    "emotion": "อัศจรรย์ใจ สวยสะกด ตลึง",
    "props": "แสงแฟลชกล้องถ่ายรูปรัวๆ",
    "prompt_en": "eyes wide hands over mouth amazed, dazzling camera flashes",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_295",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "แกก็แรงเกิน",
    "pose": "ทำท่าหงายหลังเอามือทาบอก",
    "emotion": "แซวเพื่อนที่เล่นแรง ตกใจปนขำ",
    "props": "คลื่นลมพัดแรงจนเซ",
    "prompt_en": "reeling backwards clutching chest at savage roast, dramatic wind blast",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_296",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "เกียมขิต",
    "pose": "นอนทำมือไขว้หน้าอก วิญญาณลอย",
    "emotion": "เหนื่อยจนจะไปสวรรค์ ขำๆ",
    "props": "ปีกนางฟ้าและวงแหวนลอย",
    "prompt_en": "lying down hands crossed over chest, angel halo and wings floating up",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_297",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ตัวตึงประจำซอย",
    "pose": "ใส่แจ็กเก็ตหนังยืนกอดอก เก๊กเข้ม",
    "emotion": "ผู้นำ เจ๋ง มั่นใจ ไม่กลัวใคร",
    "props": "เปลวไฟลุกที่ชายเสื้อ",
    "prompt_en": "standing in cool leather jacket folding arms, neighborhood boss aura",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_298",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ไม่ช็อตแน่นะ",
    "pose": "หรี่ตามองลอดแว่น เช็คความมั่นใจ",
    "emotion": "ระแวง ไม่ไว้ใจ ขำๆ",
    "props": "สายไฟเปลือยประกายไฟ",
    "prompt_en": "peeking over sunglasses suspiciously, checking for incoming plot twists",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_299",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ติดแกลม",
    "pose": "นั่งจิบชานิ้วก้อยกระดก สวมผ้าพันคอ",
    "emotion": "หรูหรา ไฮแฟชั่น ติดหรู",
    "props": "ถ้วยชาเคลือบทองและขนม",
    "prompt_en": "sipping tea with pinky finger up, glamorous diva pose, gold cup",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_300",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ฟิลกู๊ดมาก",
    "pose": "กางแขนรับลมเย็นบนยอดเนินหญ้า",
    "emotion": "อารมณ์ดี เบาสบาย มีความสุข",
    "props": "ดอกหญ้าและผีเสื้อบินวน",
    "prompt_en": "arms outstretched embracing gentle breeze on grassy hill, butterflies",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_301",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ฉ่ำปอด",
    "pose": "สูดหายใจเข้าลึกจนอกผาย",
    "emotion": "สดชื่นเต็มที่ ได้ปลดปล่อย",
    "props": "ละอองออกซิเจนสดใส",
    "prompt_en": "taking deep invigorating breath chest puffed, sparkling fresh air",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_302",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "คุณพี่ก็พูดไป",
    "pose": "เอาพัดตีแขนเพื่อนเบาๆ แก้เขิน",
    "emotion": "เขิน แสร้งดุ ทะเล้น",
    "props": "หัวใจสีชมพูดวงเล็กๆ",
    "prompt_en": "playfully tapping friend with hand fan blushing, sweet coy smile",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_303",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "สู้เขาสิวะอีหญิง",
    "pose": "เขย่าไหล่เพื่อนสองข้าง ปลุกพลัง",
    "emotion": "เชียร์สุดใจ ดึงสติเพื่อน",
    "props": "ประกายไฟสู้รบในตา",
    "prompt_en": "shaking friend's shoulders pumping them up, fiery motivational eyes",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_304",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "เริ่ดเกินคุณน้า",
    "pose": "ยกนิ้วโป้งสองข้าง เอียงคอยิ้มหวาน",
    "emotion": "ยอดเยี่ยม ชื่นชมตัวแม่",
    "props": "ดวงดาวสีทองเปล่งประกาย",
    "prompt_en": "double thumbs up head tilted smiling, sparkling golden stars",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_305",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "นอยด์เวอร์",
    "pose": "นั่งเอาหน้าซุกโต๊ะ ปล่อยผมปิดหน้า",
    "emotion": "งอน น้อยใจ เศร้าขำๆ",
    "props": "หยดฝนตกเปาะแปะ",
    "prompt_en": "face buried on table hair covering face, comical sulking rain cloud",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_306",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "มีใจก็ทักมา",
    "pose": "นั่งท้าวคางเขย่าโทรศัพท์ อมยิ้ม",
    "emotion": "หยอด อ่อยเบาๆ ชวนคุย",
    "props": "ข้อความแชตเด้งดึ๋ง",
    "prompt_en": "leaning on elbow twirling phone, flirty teasing smirk, chat notification",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_307",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ทรงอย่างแบด",
    "pose": "ใส่เสื้อช็อป ทำหน้าเข้ม ร็อคเกอร์",
    "emotion": "เท่ แบดบอย แต่แซดบ่อย",
    "props": "กีตาร์ไฟฟ้าและโน้ตดนตรีร็อค",
    "prompt_en": "rocker leather jacket fierce pose, 'Bad Boy' attitude with secretly soft heart",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_308",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "แซดอย่างบ่อย",
    "pose": "กอดเข่านั่งฟังเพลงฝนตก",
    "emotion": "เศร้าบ่อยแต่ยังไหว อกหักทิพย์",
    "props": "หูฟังและหยดน้ำตา",
    "prompt_en": "hugging knees listening to sad music with headphones, rain streaking window",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_309",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "อย่าให้แมส",
    "pose": "เอานิ้วแตะริมฝีปาก แอบยิ้มมุมปาก",
    "emotion": "เก็บไว้เป็นความลับ กลัวดัง",
    "props": "ปุ่ม Share ติดกุญแจ",
    "prompt_en": "finger on lips smiling slyly, keep it secret, locked share button",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_310",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "เกินต้าน",
    "pose": "เอามือกุมหัวใจ ทรุดตัวลงกับพื้น",
    "emotion": "น่ารักเกินทน รับดาเมจไม่ไหว",
    "props": "หัวใจระเบิดเป็นละอองดาว",
    "prompt_en": "clutching chest dropping to knees from unbearable cuteness overload",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_311",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "อย่าแซวเยอะ",
    "pose": "เอามือปิดหน้าแต่แอบมองรอดนิ้ว",
    "emotion": "เขินจนหูแดง แก้มระเบิด",
    "props": "ควันชมพูพุ่งจากหู",
    "prompt_en": "covering face with fingers peeking through, beet-red blushing ears",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_312",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "เต็มคาราเบล",
    "pose": "นอนแผ่ตัวสลบ เมามันส์เต็มที่",
    "emotion": "สุดทุกทาง เต็มพิกัด สิ้นสภาพ",
    "props": "เกจพลังงานแตะ 100% MAX",
    "prompt_en": "collapsed sprawling comically, lived life to the absolute fullest MAX",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_313",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "พักผ่อนหย่อนใจ",
    "pose": "นอนเปลญวนแกว่งชิลล์ๆ ใต้ต้นไม้",
    "emotion": "สโลว์ไลฟ์ สบายใจสุดๆ",
    "props": "นกร้องเพลงและใบไม้พริ้ว",
    "prompt_en": "lounging on hammock swinging gently under shade, peaceful slow life",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_314",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "อย่าดื้อ",
    "pose": "เอานิ้วเคาะหน้าผากอีกฝ่ายเบาๆ",
    "emotion": "ดุแบบเอ็นดู ตักเตือนน่ารัก",
    "props": "ประกายดาวที่หน้าผาก",
    "prompt_en": "tapping someone's forehead gently with index finger, affectionate scolding",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_315",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "คนสวยขา",
    "pose": "ทำท่ากอดเสา ยื่นมืออ้อนวอน",
    "emotion": "คลั่งรัก อวยยศคนสวย",
    "props": "ดอกกุหลาบสีแดงเต็มพื้น",
    "prompt_en": "clinging to pillar reaching out admiringly, worshipping pretty girl vibes",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_316",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ปังปุริเย่",
    "pose": "หมุนตัวเต้นรำ โปรยกระดาษสี",
    "emotion": "สมบูรณ์แบบ ชัยชนะ ปังสุด",
    "props": "มงกุฎดอกไม้และสายรุ้ง",
    "prompt_en": "twirling happily tossing confetti, fabulous celebratory victory",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_317",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ปังมากแม่นึกว่าดารา",
    "pose": "สวมแว่นตากันแดด โพสท่าพรมแดง",
    "emotion": "เฉิดฉาย โดดเด่น ออร่าพุ่ง",
    "props": "แสงสปอตไลท์และไมโครโฟน",
    "prompt_en": "strutting on red carpet wearing luxury sunglasses, celebrity aura",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_318",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ขอยาดกรี๊ด",
    "pose": "ป้องปากสองข้าง ส่งเสียงกรี๊ดดีใจ",
    "emotion": "ตื่นเต้นขั้นสุด ฟินสลบ",
    "props": "ประกายหัวใจพุ่งเป็นพลุ",
    "prompt_en": "cupping mouth screaming in sheer fangirl excitement, heart fireworks",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_319",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ใจบางหมดแล้ว",
    "pose": "ตัวหดเล็กลงเหลือตัวจิ๋วเดียว",
    "emotion": "แพ้ความน่ารัก อ่อนระทวย",
    "props": "หัวใจเปราะบางติดพลาสเตอร์",
    "prompt_en": "shrinking into tiny chibi form melting from cuteness, fragile heart icon",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_320",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "อย่าแกงเพื่อน",
    "pose": "ยกมือห้ามเพื่อนที่กำลังแกล้ง",
    "emotion": "ขำปนสงสาร ห้ามทัพ",
    "props": "หม้อแกงเดือดปุดๆ",
    "prompt_en": "waving hands stopping friend from pranking, laughing and pleading",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_321",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "จังหวะตกหลุมรัก",
    "pose": "สะดุดตกหลุมหัวใจสีชมพู",
    "emotion": "เคลิ้ม หลงรัก ตกหลุมเสน่ห์",
    "props": "หลุมรูปหัวใจมีแสงเปล่ง",
    "prompt_en": "tripping and falling into heart-shaped pit, head over heels in love",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_322",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ไอ้เราก็เท่ซะด้วย",
    "pose": "เสยผมหันข้างยิ้มมุมปาก",
    "emotion": "เก๊กเท่ มั่นใจในเสน่ห์",
    "props": "แสงเงาแบบภาพยนตร์นัวร์",
    "prompt_en": "flipping hair to side with cool smirk, charismatic cinematic lighting",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_323",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ทีนี้ก็ลำบากว้าวุ่นเลย",
    "pose": "เอามือกุมขมับ ยิ้มแห้งทะเล้น",
    "emotion": "เสน่ห์แรงจนคนรุมจีบ",
    "props": "หัวใจหลายดวงลอยเข้าหา",
    "prompt_en": "holding temple grinning bashfully, overwhelmed by own irresistible charm",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_324",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "ไม่พูดเยอะเจ็บคอ",
    "pose": "จิบน้ำมะนาวอุ่น เอานิ้วชี้ผลงาน",
    "emotion": "โชว์ผลงานชัดเจน ไม่ต้องโม้",
    "props": "ถ้วยน้ำผึ้งมะนาวและถ้วยรางวัล",
    "prompt_en": "sipping warm honey lemon pointing at trophy, deeds speak louder than words",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_325",
    "category": "คำแสลง & วัยรุ่น 2026",
    "caption": "รักนะคะคุณน้า",
    "pose": "ส่งมินิฮาร์ทกระพริบตาสองข้าง",
    "emotion": "อ้อนแฟนคลับ น่ารักน่าเอ็นดู",
    "props": "หัวใจสีรุ้งหมุนวน",
    "prompt_en": "sending mini-hearts batting both eyes, adorable crowd-pleaser pose",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_326",
    "category": "ความรัก & เทคแคร์",
    "caption": "คิดถึงจัง",
    "pose": "กอดหมอนข้างแน่น ซุกหน้าลงไป",
    "emotion": "คิดถึง ออดอ้อน เหงาใจ",
    "props": "หัวใจลอยออกจากหมอน",
    "prompt_en": "hugging bolster tightly burying face, longing affectionate look, heart bubbles",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_327",
    "category": "ความรัก & เทคแคร์",
    "caption": "รักนะ",
    "pose": "ทำมือรูปหัวใจดวงโตเหนือศีรษะ",
    "emotion": "บอกรักจริงใจ ตาหยียิ้มกว้าง",
    "props": "ลูกโป่งรูปหัวใจสีแดงสด",
    "prompt_en": "forming giant heart shape with arms over head, beaming loving smile",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_328",
    "category": "ความรัก & เทคแคร์",
    "caption": "เป็นห่วงนะ",
    "pose": "ยื่นมือจับแก้มเบาๆ สายตาอบอุ่น",
    "emotion": "ห่วงใย ลึกซึ้ง ทะนุถนอม",
    "props": "แสงแดดอุ่นและไออุ่น",
    "prompt_en": "gently touching cheek with tender caring gaze, warm glowing aura",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_329",
    "category": "ความรัก & เทคแคร์",
    "caption": "ขอกำลังใจหน่อย",
    "pose": "เกาะแขนส่งสายตาลูกหมาอ้อน",
    "emotion": "ต้องการพลังใจ ออดอ้อนสุดๆ",
    "props": "หัวใจดวงน้อยกระพริบรอเติม",
    "prompt_en": "clinging to arm with adorable begging puppy eyes, empty heart waiting to fill",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_330",
    "category": "ความรัก & เทคแคร์",
    "caption": "งอนแล้วนะ",
    "pose": "หันหลังกอดอก แก้มป่องพองลม",
    "emotion": "งอนตุ๊บป่อง รอคนมาง้อ",
    "props": "ควันฟู่ออกจากแก้ม",
    "prompt_en": "turning back crossing arms with puffed cheeks, waiting to be pampered",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_331",
    "category": "ความรัก & เทคแคร์",
    "caption": "รออยู่นะ",
    "pose": "นั่งเท้าคางมองนาฬิกาแขวนผนัง",
    "emotion": "รอคอย จดจ่อ ใจเต้น",
    "props": "เข็มนาฬิกาเดินติ๊กต็อก",
    "prompt_en": "resting chin on hand gazing at ticking wall clock, eager anticipation",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_332",
    "category": "ความรัก & เทคแคร์",
    "caption": "จุ๊บๆ",
    "pose": "ยื่นปากจู๋ ส่งรอยลิปสติกสีชมพู",
    "emotion": "ส่งความรัก อ่อนหวาน ขี้เล่น",
    "props": "รอยประทับจูบและหัวใจ",
    "prompt_en": "puckering lips blowing sweet kisses, pink lipstick kiss marks floating",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_333",
    "category": "ความรัก & เทคแคร์",
    "caption": "มีใจให้เสมอนะ",
    "pose": "เอามือล้วงกระเป๋าหยิบหัวใจยื่นให้",
    "emotion": "มอบใจให้ จริงใจ มั่นคง",
    "props": "หัวใจเปล่งแสงสีแดงระเรื่อ",
    "prompt_en": "pulling glowing heart out of chest pocket offering it, sincere devotion",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_334",
    "category": "ความรัก & เทคแคร์",
    "caption": "อย่าลืมคิดถึงเค้านะ",
    "pose": "ชี้นิ้วมาข้างหน้า ขยิบตาวิ้ง",
    "emotion": "อ้อนเตือนความจำ น่ารัก",
    "props": "โน้ตเตือนความจำรูปหัวใจ",
    "prompt_en": "pointing finger smiling playfully, reminder note shaped like heart",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_335",
    "category": "ความรัก & เทคแคร์",
    "caption": "คนดีของใจ",
    "pose": "เอามือกุมมือสองข้างแนบอก",
    "emotion": "ซาบซึ้ง ปลื้มปริ่ม อบอุ่น",
    "props": "ดอกกุหลาบสีชมพูบานสะพรั่ง",
    "prompt_en": "holding both hands over chest with grateful melting eyes, blooming rose",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_336",
    "category": "ความรัก & เทคแคร์",
    "caption": "เค้าอยู่ตรงนี้",
    "pose": "กระโดดโบกมือสองข้าง ยิ้มกว้าง",
    "emotion": "เป็นที่พึ่งให้ สดใส อุ่นใจ",
    "props": "สปอตไลท์ส่องสว่าง",
    "prompt_en": "jumping up and down waving both arms brightly, comforting presence",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_337",
    "category": "ความรัก & เทคแคร์",
    "caption": "หายโกรธนะ",
    "pose": "ยื่นช่อดอกไม้จิ๋ว เอียงคอสำนึกผิด",
    "emotion": "ขอโทษ อ้อนวอน ง้อสุดตัว",
    "props": "สายตาวิงวอนแสนน่ารัก",
    "prompt_en": "offering tiny flower bouquet tilting head apologetically, begging forgiveness",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_338",
    "category": "ความรัก & เทคแคร์",
    "caption": "น่ารักจังเลย",
    "pose": "เอามือป้องปาก ตาเป็นประกายรูปหัวใจ",
    "emotion": "หลงใหล เอ็นดู คลั่งรัก",
    "props": "หัวใจเต้นกระดอนออกจากอก",
    "prompt_en": "hands over mouth, heart-shaped eyes, overwhelmed by sheer cuteness",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_339",
    "category": "ความรัก & เทคแคร์",
    "caption": "แฟนใครเนี่ย",
    "pose": "ชี้มาข้างหน้า ยิ้มปลื้มภูมิใจ",
    "emotion": "อวดแฟน หวานเจี๊ยบ ภูมิใจ",
    "props": "ประกายไฟหวานแหวว",
    "prompt_en": "pointing forward with proud adoring grin, bragging about partner",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_340",
    "category": "ความรัก & เทคแคร์",
    "caption": "ขอบคุณที่อยู่ข้างกัน",
    "pose": "จับมือเดินเคียงข้างบนทางเดิน",
    "emotion": "ซาบซึ้งในความผูกพัน มั่นคง",
    "props": "ใบไม้ร่วงและแสงแดดอบอุ่น",
    "prompt_en": "walking hand in hand on autumn path, deep grateful bond, warm sunlight",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_341",
    "category": "ความรัก & เทคแคร์",
    "caption": "คิดถึงจนใจเจ็บ",
    "pose": "กอดอกแน่น น้ำตาคลอเบ้า",
    "emotion": "คิดถึงมาก เหงาจับใจ",
    "props": "หัวใจมีรอยแตกร้าวเล็กๆ",
    "prompt_en": "hugging chest tightly with misty longing eyes, tiny cracked heart healing",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_342",
    "category": "ความรัก & เทคแคร์",
    "caption": "เป็นของเธอคนเดียว",
    "pose": "ชี้ป้ายชื่อที่อกมีชื่ออีกฝ่าย",
    "emotion": "ซื่อสัตย์ ภักดี มีคนเดียวในใจ",
    "props": "กุญแจล็อคหัวใจสีทอง",
    "prompt_en": "pointing at name badge over heart, faithful devoted smile, heart padlock",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_343",
    "category": "ความรัก & เทคแคร์",
    "caption": "ส่งกอดไปให้นะ",
    "pose": "ทำมือโอบกอดอากาศส่งไปข้างหน้า",
    "emotion": "ส่งความอบอุ่นผ่านทางไกล",
    "props": "กลุ่มก้อนเมฆหัวใจลอยไปหา",
    "prompt_en": "hugging the air sending long-distance embrace, floating heart-clouds",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_344",
    "category": "ความรัก & เทคแคร์",
    "caption": "เหนื่อยก็มากอดกัน",
    "pose": "อ้าแขนรอรับ ยิ้มอบอุ่นที่สุด",
    "emotion": "เป็นที่พักใจ ปลอดภัย สบายใจ",
    "props": "หมอนนุ่มและผ้าห่มอุ่น",
    "prompt_en": "arms open wide offering safe haven hug, soothing comforting smile",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_345",
    "category": "ความรัก & เทคแคร์",
    "caption": "เธอคือรอยยิ้มของเค้า",
    "pose": "ชี้นิ้วไปที่แก้มตัวเองยิ้มแป้น",
    "emotion": "มีความสุขเพราะเธอ สดใส",
    "props": "ดวงอาทิตย์ยิ้มแฉ่ง",
    "prompt_en": "pointing at own big smile, 'you make me smile', cheerful sun icon",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_346",
    "category": "ความรัก & เทคแคร์",
    "caption": "อยากเจอจังเลย",
    "pose": "นั่งเกาะหน้าต่างมองฝนตกนอกบ้าน",
    "emotion": "เฝ้ารอวันพบกัน ตาละห้อย",
    "props": "ปฏิทินกากบาทนับวันรอ",
    "prompt_en": "sitting by rainy window pining to meet, crossed-off waiting calendar",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_347",
    "category": "ความรัก & เทคแคร์",
    "caption": "คนเก่งของเค้าสู้ๆ",
    "pose": "ผูกผ้าพันคอให้ ส่งกำปั้นเชียร์",
    "emotion": "ภรรยา/แฟนที่แสนดี สนับสนุน",
    "props": "เปลวไฟสีส้มแห่งกำลังใจ",
    "prompt_en": "adjusting scarf gently, cheering fist, encouraging devoted partner",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_348",
    "category": "ความรัก & เทคแคร์",
    "caption": "ตกหลุมรักซ้ำๆ",
    "pose": "เอามือกุมแก้ม ตัวเซเหมือนจะล้ม",
    "emotion": "แพ้ทางเธอตลอด หลงเสน่ห์",
    "props": "ลูกศรคิวปิดปักกลางอก",
    "prompt_en": "staggering back clutching heart, Cupid's love arrow struck through",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_349",
    "category": "ความรัก & เทคแคร์",
    "caption": "ฝันถึงเค้าด้วยนะ",
    "pose": "ทำท่าเป่าละอองดาวก่อนนอน",
    "emotion": "ส่งความฝันดี หวานซึ้ง",
    "props": "ละอองดาวสีชมพูวิบวับ",
    "prompt_en": "blowing sparkling dream-dust towards viewer, bedtime romantic wish",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_350",
    "category": "ความรัก & เทคแคร์",
    "caption": "กินยาแล้วนอนนะ",
    "pose": "ยื่นแก้วน้ำและยาเม็ดให้ด้วยรัก",
    "emotion": "ดูแลยามป่วยไข้ ใส่ใจจริง",
    "props": "ปรอทวัดไข้และผ้าประคบ",
    "prompt_en": "handing water glass and medicine pills with tender worried gaze",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_351",
    "category": "ความรัก & เทคแคร์",
    "caption": "ห่มผ้าหนาๆ นะ",
    "pose": "ดึงผ้าห่มขึ้นมาคลุมถึงคอให้",
    "emotion": "ห่วงใยสุขภาพ อบอุ่น",
    "props": "เกล็ดหิมะนอกหน้าต่าง",
    "prompt_en": "tucking blanket up to chin, cozy warm protection from cold draft",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_352",
    "category": "ความรัก & เทคแคร์",
    "caption": "อย่าดื้อกับเค้านะ",
    "pose": "ทำหน้างอชี้นิ้วเตือนเบาๆ",
    "emotion": "แกล้งดุ อ้อนให้อยู่ในโอวาท",
    "props": "ลูกแมวน้อยขู่ฟ่อแบบน่ารัก",
    "prompt_en": "pouting finger wagging, cute kitten bossy warning, sweet affection",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_353",
    "category": "ความรัก & เทคแคร์",
    "caption": "มีเค้าคนเดียวพอนะ",
    "pose": "กอดแขนแน่น เอาคางเกยไหล่",
    "emotion": "หวง หวงแหน อ้อนเจ้าของ",
    "props": "โซ่คล้องแขนรูปหัวใจ",
    "prompt_en": "clinging to arm resting chin on shoulder, possessive adorable snuggle",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_354",
    "category": "ความรัก & เทคแคร์",
    "caption": "รักมากกว่าเมื่อวาน",
    "pose": "วาดหัวใจขนาดใหญ่ขึ้นเรื่อยๆ ในอากาศ",
    "emotion": "รักเพิ่มขึ้นทุกวัน หวานฉ่ำ",
    "props": "หัวใจซ้อนกันหลายชั้น",
    "prompt_en": "drawing expanding layered hearts in air, growing love every day",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_355",
    "category": "ความรัก & เทคแคร์",
    "caption": "ขอหอมแก้มทีนึง",
    "pose": "ยื่นแก้มป่องรอรับการหอม",
    "emotion": "อ้อนขอความรัก น่ารักน่าชัง",
    "props": "ประกายแก้มสีชมพูระเรื่อ",
    "prompt_en": "puffing cheek offering it for a kiss, blushing expectant expression",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_356",
    "category": "ความรัก & เทคแคร์",
    "caption": "แฮปปี้แอนนิเวอร์ซารี่",
    "pose": "ถือเค้กครบรอบปักเลขวันสำคัญ",
    "emotion": "ฉลองความรัก ยิ้มยินดี",
    "props": "ลูกโป่งรูปหัวใจและริบบิ้น",
    "prompt_en": "holding anniversary cake with candles, celebrating milestones together",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_357",
    "category": "ความรัก & เทคแคร์",
    "caption": "ขอบคุณที่รักกัน",
    "pose": "พนมมือไหว้น้ำตาซึมด้วยความรัก",
    "emotion": "ซาบซึ้งในรักแท้ อบอุ่นใจ",
    "props": "แสงเทียนส่องสว่างนุ่มนวล",
    "prompt_en": "hands together in tearful heartfelt gratitude for enduring love",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_358",
    "category": "ความรัก & เทคแคร์",
    "caption": "อยู่ด้วยกันไปนานๆ นะ",
    "pose": "เกี่ยวก้อยสัญญา ยิ้มให้กัน",
    "emotion": "สัญญารัก มั่นคง ตลอดไป",
    "props": "ด้ายแดงผูกนิ้วก้อย",
    "prompt_en": "pinky promise with red string of destiny tied, eternal commitment smile",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_359",
    "category": "ความรัก & เทคแคร์",
    "caption": "สายตาคู่นี้มีให้เธอ",
    "pose": "จ้องตาส่งประกายวิ้งๆ หวานซึ้ง",
    "emotion": "ตาหวานเชื่อม ละลายใจ",
    "props": "ประกายดาวในแววตา",
    "prompt_en": "gazing deeply with melting starry eyes full of tender affection",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_360",
    "category": "ความรัก & เทคแคร์",
    "caption": "เธอคือของขวัญที่ดีที่สุด",
    "pose": "นั่งกอดกล่องของขวัญผูกโบว์โต",
    "emotion": "ยินดีที่มีเธอในชีวิต",
    "props": "โบว์ริบบิ้นสีแดงทอง",
    "prompt_en": "hugging giant gift box, 'you are my best gift', radiant happiness",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_361",
    "category": "ความรัก & เทคแคร์",
    "caption": "เค้าไม่เคยไปไหน",
    "pose": "วางมือทาบอก ยืนหยัดข้างๆ",
    "emotion": "มั่นคง ให้ความปลอดภัย",
    "props": "ต้นไม้ใหญ่ร่มรื่น",
    "prompt_en": "hand on chest standing tall, steady unwavering loyal presence",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_362",
    "category": "ความรัก & เทคแคร์",
    "caption": "อย่าร้องไห้คนดี",
    "pose": "ใช้นิ้วโป้งค่อยๆ เช็ดน้ำตาให้",
    "emotion": "อ่อนโยน ปลอบโยนจากใจ",
    "props": "ทิชชู่ซับน้ำตา",
    "prompt_en": "wiping tears gently with thumbs, soothing loving tenderness",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_363",
    "category": "ความรัก & เทคแคร์",
    "caption": "ยิ้มให้เค้าดูหน่อย",
    "pose": "ดึงมุมปากเพื่อนให้ยิ้มกว้าง",
    "emotion": "อยากให้มีความสุข ทะเล้น",
    "props": "รอยยิ้มสดใสสีเหลือง",
    "prompt_en": "tugging cheek corners smiling wide, wanting to see partner happy",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_364",
    "category": "ความรัก & เทคแคร์",
    "caption": "ตกหลุมรักรอบที่ล้าน",
    "pose": "เอามือทาบอก ตัวบิดเขินอาย",
    "emotion": "เขินซ้ำๆ หลงรักคนเดิม",
    "props": "ลูกศรหัวใจพุ่งปักรัวๆ",
    "prompt_en": "squirming blushing wildly, falling in love all over again, Cupid arrows",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_365",
    "category": "ความรัก & เทคแคร์",
    "caption": "เค้าเป็นของเธอเสมอ",
    "pose": "ชูตราประทับรูปหัวใจที่หน้าอก",
    "emotion": "การันตีความรัก ไม่แปรผัน",
    "props": "ตราประทับสีแดงสด",
    "prompt_en": "pointing to stamped heart on chest, guaranteed unconditional devotion",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_366",
    "category": "ความรัก & เทคแคร์",
    "caption": "คนโปรดของฉัน",
    "pose": "ชูป้ายไฟชื่อเธอ โบกไปมา",
    "emotion": "แฟนคลับนัมเบอร์วัน เชียร์สุดตัว",
    "props": "ป้ายไฟนีออนสว่างจ้า",
    "prompt_en": "waving glowing neon lightboard of partner's name, number one fan",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_367",
    "category": "ความรัก & เทคแคร์",
    "caption": "หวานตัดขา",
    "pose": "ถือโหลน้ำผึ้งที่หกเลอะพื้น",
    "emotion": "หวานเกินไป มดขึ้นจอ",
    "props": "ฝูงมดน้อยเดินเรียงแถว",
    "prompt_en": "holding overflowing honey pot with cute ants swarming, sugary sweetness",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_368",
    "category": "ความรัก & เทคแคร์",
    "caption": "ใจละลายหมดแล้ว",
    "pose": "ตัวเหลวเป็นไอศกรีมละลายบนพื้น",
    "emotion": "ทนความน่ารักไม่ไหว ละลาย",
    "props": "แอ่งน้ำหวานรูปหัวใจ",
    "prompt_en": "melting into puddle on floor from sweet overload, puddle of hearts",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_369",
    "category": "ความรัก & เทคแคร์",
    "caption": "รักที่สุดในโลก",
    "pose": "กางแขนกว้างหมุนรอบตัวเอง",
    "emotion": "รักกว้างใหญ่ไร้ขีดจำกัด",
    "props": "ลูกโลกและวงโคจรดาว",
    "prompt_en": "arms spread wide spinning with world globe, infinite universal love",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_370",
    "category": "ความรัก & เทคแคร์",
    "caption": "มีเธอแล้วชีวิตดี",
    "pose": "นั่งเอนหลังจิบชามองดาวคู่กัน",
    "emotion": "อบอุ่น พอใจ สมบูรณ์แบบ",
    "props": "ดาวตกพาดผ่านฟากฟ้า",
    "prompt_en": "sitting side by side stargazing, peaceful contentment, shooting stars",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_371",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณมากครับ",
    "pose": "ก้มศีรษะคำนับสองมือแนบลำตัว",
    "emotion": "สุภาพ อ่อนน้อม จริงใจ",
    "props": "ประกายแสงดาวสีทอง",
    "prompt_en": "bowing deeply with both hands at sides, sincere respectful gratitude",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_372",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณมากค่ะ",
    "pose": "ย่อตัวถอนสายบัว ยกมือไหว้",
    "emotion": "อ่อนช้อย งดงาม น่ารัก",
    "props": "พวงมาลัยดอกไม้สด",
    "prompt_en": "curtsying gracefully with Thai Wai gesture, delicate floral wreath",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_373",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบพระคุณเป็นอย่างสูง",
    "pose": "นั่งคุกเข่ากราบแนบพื้นอย่างสง่างาม",
    "emotion": "ซาบซึ้งในพระคุณอย่างยิ่งยวด",
    "props": "พานพุ่มดอกบัวหลวง",
    "prompt_en": "kneeling down in deep formal prostration Wai, golden lotus tray",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_374",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ซาบซึ้งใจที่สุด",
    "pose": "เอามือกุมหน้าอก น้ำตาซึมปลาบปลื้ม",
    "emotion": "ตื้นตันใจ ประทับใจอย่างยิ่ง",
    "props": "แสงเรืองรองอบอุ่นในอก",
    "prompt_en": "holding hands over heart with glistening tears of deep gratitude",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_375",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณจากใจจริง",
    "pose": "ยื่นการ์ดขอบคุณเขียนด้วยลายมือ",
    "emotion": "จริงใจ อบอุ่น เป็นกันเอง",
    "props": "ซองจดหมายผูกริบบิ้นทอง",
    "prompt_en": "handing handwritten Thank You card with two hands, ribbon envelope",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_376",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณสำหรับทุกอย่าง",
    "pose": "ชูช่อดอกไม้ช่อใหญ่ส่งให้",
    "emotion": "ขอบคุณในความช่วยเหลือ",
    "props": "ช่อกุหลาบและลิลลี่หลากสี",
    "prompt_en": "presenting magnificent thank-you flower bouquet, bright grateful smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_377",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "เกรงใจจังเลย",
    "pose": "โบกมือปฏิเสธแบบเขินๆ ขอบคุณ",
    "emotion": "นอบน้อม เกรงใจ อ่อนหวาน",
    "props": "เหงื่อหยดเล็กๆ บนแก้ม",
    "prompt_en": "waving hands shyly in polite modesty, touched by generosity",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_378",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขออภัยด้วยครับ",
    "pose": "ยืนก้มศีรษะ 45 องศา สองมือประสาน",
    "emotion": "ยอมรับผิด สำนึกอย่างจริงใจ",
    "props": "เงาโค้งคำนับสุภาพ",
    "prompt_en": "bowing 45 degrees hands clasped, sincere humble apology posture",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_379",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขออภัยด้วยค่ะ",
    "pose": "พนมมือไหว้น้ำตาคลอเบาๆ",
    "emotion": "รู้สึกผิด ขอโทษจากใจ",
    "props": "ดอกกล้วยไม้สีขาวบริสุทธิ์",
    "prompt_en": "apologetic Thai Wai with remorseful pleading eyes, white orchid",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_380",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "เค้าขอโทษนะ",
    "pose": "กอดเข่าคุกเข่า ทำตาละห้อยสำนึกผิด",
    "emotion": "สำนึกผิดอย่างสุดซึ้ง ง้อขอโทษ",
    "props": "หยดน้ำตาและป้าย Sorry",
    "prompt_en": "kneeling on floor with sorrowful puppy eyes, tiny sorry sign",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_381",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ยกโทษให้เค้านะ",
    "pose": "พนมมือไหว้ส่งสายตาอ้อนวอนสุดตัว",
    "emotion": "ขอความเมตตา ไม่ได้ตั้งใจ",
    "props": "หัวใจผูกเชือกขอคืนดี",
    "prompt_en": "pleading desperately for forgiveness with praying hands, mending heart",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_382",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ไม่ได้ตั้งใจจริงๆ",
    "pose": "เอามือปิดหน้า ทำหน้าเสียใจ",
    "emotion": "ไม่ได้เจตนา เสียใจกับสิ่งที่เกิด",
    "props": "จานแก้วแตกที่พยายามต่อ",
    "prompt_en": "covering face with genuine remorse, trying to piece broken cup together",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_383",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ผิดไปแล้ว",
    "pose": "ชูป้าย 'ฉันผิดเอง' คุกเข่ายอมรับ",
    "emotion": "ยอมรับผิดทุกกรณี ไม่เถียง",
    "props": "ป้ายสารภาพบาปสีขาว",
    "prompt_en": "holding up 'My Fault' confession sign kneeling down honestly",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_384",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "อย่าโกรธเค้าเลย",
    "pose": "เอานิ้วสะกิดแขนเบาๆ ทำปากคว่ำ",
    "emotion": "อ้อนวอน ขอคืนดี น่าสงสาร",
    "props": "ลูกแมวน้อยเปียกฝน",
    "prompt_en": "gently poking arm with pouty lips, sad drenched kitten eyes",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_385",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ให้อภัยเค้านะ",
    "pose": "ยื่นตุ๊กตาหมีถือป้ายขอโทษให้",
    "emotion": "ง้อจากใจจริง อยากกลับมาคุย",
    "props": "ตุ๊กตาหมีปักคำว่า Forgive Me",
    "prompt_en": "handing cute teddy bear holding Forgive Me heart, hopeful gaze",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_386",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่เข้าใจ",
    "pose": "ยิ้มโล่งอก ถอนหายใจเบาสบาย",
    "emotion": "ซึ้งในความเข้าใจ สบายใจ",
    "props": "เมฆหมอกสลายเปิดทางให้แดด",
    "prompt_en": "sighing in immense relief, grateful smile, storm clouds parting",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_387",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่เตือนนะ",
    "pose": "พยักหน้ารับฟัง จดคำแนะนำ",
    "emotion": "เปิดใจรับฟัง มีสติ น้อมรับ",
    "props": "สมุดบันทึกและรอยยิ้ม",
    "prompt_en": "nodding attentively taking note of advice, receptive humble smile",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_388",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่ช่วยเหลือ",
    "pose": "จับมือสองข้างเขย่าขอบคุณ",
    "emotion": "รอดพ้นวิกฤตได้เพราะเธอ",
    "props": "เชือกกู้ภัยและห่วงชูชีพ",
    "prompt_en": "two-handed heartfelt handshake of rescue gratitude, lifebuoy beside",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_389",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "เป็นพระคุณอย่างยิ่ง",
    "pose": "กราบลงบนหมอนขวานลายไทย",
    "emotion": "ซาบซึ้งในความกรุณา ล้นพ้น",
    "props": "ดอกมะลิร้อยมาลัย",
    "prompt_en": "bowing to traditional Thai triangle pillow, supreme graceful gratitude",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_390",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอโอกาสแก้ตัว",
    "pose": "กำหมัดมุ่งมั่น ขอแก้ไขข้อผิดพลาด",
    "emotion": "ตั้งใจปรับปรุง ไม่ให้เกิดซ้ำ",
    "props": "นาฬิกาทรายหมุนกลับ",
    "prompt_en": "clenched fist determined to do better, turning hourglass around",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_391",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "จะไม่ทำอีกแล้ว",
    "pose": "ชูสามนิ้วปฏิญาณตน ตาแน่วแน่",
    "emotion": "สัญญาจากใจจริง จะเป็นคนดี",
    "props": "ตราสัญลักษณ์คำสัญญา",
    "prompt_en": "raising three fingers in solemn promise, resolute earnest vow",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_392",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "สำนึกผิดแล้วจ้า",
    "pose": "นั่งคุกเข่าบนเมล็ดถั่วทำโทษตัวเอง",
    "emotion": "ยอมรับบทลงโทษ สำนึกแล้ว",
    "props": "ป้ายสารภาพผิดสีแดง",
    "prompt_en": "kneeling on floor in comic self-punishment, remorseful big eyes",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_393",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณสำหรับคำแนะนำ",
    "pose": "โค้งรับคำแนะนำ ถือสมุดบันทึก",
    "emotion": "กระตือรือร้นพัฒนาตนเอง",
    "props": "หลอดไฟปัญญาและแว่นตา",
    "prompt_en": "bowing receiving guidance with notebook, enlightened lightbulb spark",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_394",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขออภัยในความไม่สะดวก",
    "pose": "ยืนโค้งคำนับสุภาพหน้าแผงกั้น",
    "emotion": "มืออาชีพ สุภาพ อ่อนน้อม",
    "props": "ป้ายขออภัยสีเหลืองดำ",
    "prompt_en": "professional polite bow in front of maintenance barrier, caution sign",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_395",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณน้ำใจ",
    "pose": "รับของสองมือ สายตาซาบซึ้งใจ",
    "emotion": "สัมผัสได้ถึงความอบอุ่น",
    "props": "ถ้วยน้ำใจใสสะอาด",
    "prompt_en": "receiving gift with both hands, touching gratitude in eyes",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_396",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอโทษที่รบกวน",
    "pose": "ย่อตัวเดินผ่านอย่างสุภาพ",
    "emotion": "มีมารยาท เกรงใจ น่ารัก",
    "props": "ทางเดินเงียบสงบ",
    "prompt_en": "crouching low walking past politely, considerate courteous gesture",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_397",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่รอ",
    "pose": "วิ่งกระหืดกระหอบมาถึง ยกมือไหว้",
    "emotion": "ขอบคุณที่อดทนรอ เกรงใจ",
    "props": "นาฬิกาหยุดเดินและผ้าเช็ดเหงื่อ",
    "prompt_en": "arriving panting with hands raised in Wai, thanking for waiting patiently",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_398",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขออภัยที่ตอบช้า",
    "pose": "พนมมือไหว้น้ำตาซึมข้างโทรศัพท์",
    "emotion": "รู้สึกผิด ติดภารกิจด่วน",
    "props": "หน้าจอแชตมีข้อความรอ",
    "prompt_en": "apologizing with hands clasped over phone for late reply, guilty face",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_399",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่รับฟัง",
    "pose": "นั่งคุยข้ามโต๊ะ ส่งยิ้มอบอุ่นใจ",
    "emotion": "สบายใจที่ได้ระบาย ขอบคุณ",
    "props": "ถ้วยชาอุ่นสองใบ",
    "prompt_en": "smiling warmly across cafe table, grateful for compassionate listener",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_400",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอโทษจากก้นบึ้งหัวใจ",
    "pose": "ก้มกราบแนบพื้นด้วยความจริงใจ",
    "emotion": "สำนึกผิดขั้นสูงสุด ขออภัย",
    "props": "หยดน้ำตาหยดลงพื้น",
    "prompt_en": "prostrating flat to floor in absolute heartfelt repentance",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_401",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณมิตรภาพดีๆ",
    "pose": "กอดคอเพื่อนสองคน ยิ้มกว้าง",
    "emotion": "ผูกพัน มีค่า เหนียวแน่น",
    "props": "สร้อยข้อมือมิตรภาพ",
    "prompt_en": "arms around friends laughing warmly, cherished friendship bracelets",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_402",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ซาบซึ้งจนพูดไม่ออก",
    "pose": "กุมอก น้ำตาแห่งความสุขไหลอาบแก้ม",
    "emotion": "ตื้นตันใจ ประทับใจล้นพ้น",
    "props": "แสงออร่าแห่งความปิติ",
    "prompt_en": "clutching chest speechless with tears of overwhelming gratitude",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_403",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่เชื่อใจกัน",
    "pose": "จับมือประสานสายตามั่นคง",
    "emotion": "ไว้ใจ ไม่ทำให้ผิดหวัง",
    "props": "ตราประทับเกียรติยศ",
    "prompt_en": "firm handshake with unwavering eye contact, honoring trust given",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_404",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "กราบขออภัย",
    "pose": "หมอบกราบกราบงามๆ บนพรม",
    "emotion": "สุภาพสูงสุด สำนึกผิด",
    "props": "พวงมาลัยดอกมะลิสด",
    "prompt_en": "prostrating respectfully in formal Thai apology on elegant carpet",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_405",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่เตือนสติ",
    "pose": "ยกมือทาบหน้าผาก เข้าใจแจ่มแจ้ง",
    "emotion": "ตาสว่าง ได้สติ ขอบคุณ",
    "props": "น้ำเย็นประพรมใบหน้า",
    "prompt_en": "splashing face waking up to reality, thankful for grounding advice",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_406",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอโทษที่ทำให้ผิดหวัง",
    "pose": "ยืนคอตก สำนึกในความผิดพลาด",
    "emotion": "เสียใจ มุ่งมั่นจะแก้ไข",
    "props": "หยดฝนตกกระทบร่ม",
    "prompt_en": "head hung low with deep sorrow, determined to redeem oneself",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_407",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่ให้โอกาส",
    "pose": "โค้งรับโอกาสใหม่ สองมือกำหมัด",
    "emotion": "ซาบซึ้งใจ มุ่งมั่นทำเต็มที่",
    "props": "ประตูบานใหม่เปิดรับแสง",
    "prompt_en": "bowing deeply receiving second chance, fists clenched to prove worth",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_408",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบใจนะเพื่อน",
    "pose": "ตบไหล่เพื่อนเบาๆ ยิ้มกวนๆ อบอุ่น",
    "emotion": "ซี้ปึ้ก มิตรภาพแน่นแฟ้น",
    "props": "แก้วน้ำชนกันดังเอี๊ยด",
    "prompt_en": "clapping buddy on shoulder, warm brotherhood fist bump, clinking mugs",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_409",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอโทษที่เอาแต่ใจ",
    "pose": "นั่งพับเพียบ ก้มหน้าสำนึกผิด",
    "emotion": "รู้ตัวว่างี่เง่า ง้อขอคืนดี",
    "props": "ดอกไม้ขอโทษสีขาว",
    "prompt_en": "sitting politely looking down contrite, admitting stubborn fault",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_410",
    "category": "ขอโทษ & ขอบคุณ",
    "caption": "ขอบคุณที่รักและเมตตา",
    "pose": "ยกมือไหว้จรดหว่างคิ้ว งดงาม",
    "emotion": "ซาบซึ้งในความเมตตาผู้ใหญ่",
    "props": "แสงบุญสีขาวบริสุทธิ์",
    "prompt_en": "graceful Thai Wai touching eyebrows, deep reverence for elder kindness",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_411",
    "category": "วันหยุด & พักผ่อน",
    "caption": "วันหยุดแล้วโว้ย",
    "pose": "กระโดดตีลังกาโยนกระเป๋าทำงานทิ้ง",
    "emotion": "สะใจ ดีใจ หลุดพ้นพันธะ",
    "props": "ปฏิทินบินว่อนและดาวกระจาย",
    "prompt_en": "backflipping joyfully tossing briefcase in air, weekend freedom roar",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_412",
    "category": "วันหยุด & พักผ่อน",
    "caption": "นอนทั้งวัน",
    "pose": "มุดผ้าห่มนุ่มเป็นดักแด้กลมดิ๊ก",
    "emotion": "ขี้เกียจขั้นสุด สบายอารมณ์",
    "props": "หมอนนุ่ม 4 ใบและตุ๊กตา",
    "prompt_en": "swaddled into cozy burrito blanket like caterpillar, ultimate lazy weekend",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_413",
    "category": "วันหยุด & พักผ่อน",
    "caption": "เที่ยวกันเถอะ",
    "pose": "สะพายกล้อง สวมหมวกปีกกว้างพร้อมลุย",
    "emotion": "ตื่นเต้น กระตือรือร้น รักอิสระ",
    "props": "กระเป๋าเดินทางล้อลากและตั๋วบิน",
    "prompt_en": "wearing sun hat and camera slung over neck with luggage, ready to travel",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_414",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ชาร์จแบตให้ตัวเอง",
    "pose": "นอนอาบแดด จิบค็อกเทลริมชายหาด",
    "emotion": "ผ่อนคลาย รีเฟรชพลัง 100%",
    "props": "ต้นมะพร้าว คลื่นทะเลสีคราม",
    "prompt_en": "lounging on beach chair sipping tropical drink, turquoise ocean waves",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_415",
    "category": "วันหยุด & พักผ่อน",
    "caption": "นอนดูซีรีส์",
    "pose": "นอนบนโซฟากอดถังป๊อปคอร์นดูจอ",
    "emotion": "เพลิดเพลิน อินกับเนื้อเรื่อง",
    "props": "กล่องทิชชู่และแก้วน้ำอัดลม",
    "prompt_en": "curled on couch hugging popcorn bucket watching TV series, binge mode",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_416",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ไม่อยากตื่นเลย",
    "pose": "ดึงหมอนมาปิดหู กดปิดนาฬิกาปลุก",
    "emotion": "ง่วงนอน ขอนอนต่ออีก 5 นาที",
    "props": "นาฬิกาปลุกร้องลั่นกริ๊งๆ",
    "prompt_en": "smothering head under pillow slapping snooze button, '5 more minutes'",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_417",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ตั้งแคมป์รับลมหนาว",
    "pose": "นั่งผิงไฟหน้าเต็นท์ จิบโกโก้ร้อน",
    "emotion": "อบอุ่น ชิลล์ ท่ามกลางธรรมชาติ",
    "props": "กองไฟแคมป์ปิ้งและดวงดาว",
    "prompt_en": "sitting by crackling campfire sipping cocoa outside tent, starry night",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_418",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ปาร์ตี้หมูกระทะ",
    "pose": "คีบหมูสามชั้นย่างรอบเตากับแก๊ง",
    "emotion": "เฮฮา บันเทิง อิ่มสำราญ",
    "props": "ควันหอมกรุ่นและเสียงหัวเราะ",
    "prompt_en": "grilling pork around charcoal stove with friends laughing, BBQ party joy",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_419",
    "category": "วันหยุด & พักผ่อน",
    "caption": "สูดอากาศบริสุทธิ์",
    "pose": "ยืนกางแขนบนยอดดอยรับลมหมอก",
    "emotion": "สดชื่น ปลอดโปร่ง เต็มปอด",
    "props": "ทะเลหมอกสีขาวและทิวเขา",
    "prompt_en": "standing on misty mountain peak arms spread wide, fresh crisp morning breeze",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_420",
    "category": "วันหยุด & พักผ่อน",
    "caption": "เล่นเกมยันเช้า",
    "pose": "สวมหูฟังเกมมิ่ง กดยิ๊กๆ จอสะท้อนตา",
    "emotion": "อินจัด มีสมาธิ สะใจ",
    "props": "คอนโซลจอยเกมส์และขนมขบเคี้ยว",
    "prompt_en": "wearing gaming headset furiously pressing controller buttons, neon RGB glow",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_421",
    "category": "วันหยุด & พักผ่อน",
    "caption": "สโลว์ไลฟ์",
    "pose": "รดน้ำกระถางแคคตัส จิบกาแฟดริป",
    "emotion": "เรียบง่าย สงบ ผ่อนคลาย",
    "props": "ต้นไม้กระถางและกาแฟดริป",
    "prompt_en": "slow-living watering bonsai plants while brewing pour-over coffee, zen smile",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_422",
    "category": "วันหยุด & พักผ่อน",
    "caption": "วันพักผ่อนของฉัน",
    "pose": "แช่น้ำอุ่นในอ่างฟองสบู่ฟูฟ่อง",
    "emotion": "หรูหรา ผ่อนคลายกล้ามเนื้อ",
    "props": "เป็ดยางสีเหลืองและเทียนหอม",
    "prompt_en": "soaking in bubble bath with yellow rubber ducky, luxury spa relaxation",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_423",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ไปทะเลกัน",
    "pose": "ใส่กางเกงฮาวาย ถือกระดานโต้คลื่น",
    "emotion": "พร้อมลุยแดด เล่นคลื่น",
    "props": "คลื่นทะเลและนกนางนวล",
    "prompt_en": "wearing hawaiian shirt holding surfboard, beach vacation excitement",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_424",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ปีนเขารับลม",
    "pose": "สะพายเป้เดินป่า ถือไม้เท้าก้าวเดิน",
    "emotion": "ท้าทาย มุ่งมั่น แข็งแรง",
    "props": "ทิวเขาสลับซับซ้อน",
    "prompt_en": "hiking up rocky trail with trekking poles and sturdy backpack, explorer spirit",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_425",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ปั่นจักรยานรับลม",
    "pose": "ปั่นจักรยานตะกร้าดอกไม้ริมสวน",
    "emotion": "สดใส ร่าเริง สุขภาพดี",
    "props": "ผีเสื้อและลมพัดใบไม้ปลิว",
    "prompt_en": "riding vintage bicycle with flower basket through scenic park, happy breeze",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_426",
    "category": "วันหยุด & พักผ่อน",
    "caption": "นอนอืดอยู่บ้าน",
    "pose": "นอนเกลือกกลิ้งบนพรมเหมือนแมว",
    "emotion": "ขี้เกียจตัวเป็นขน ไร้กังวล",
    "props": "ของกินวางเกลื่อนรอบตัว",
    "prompt_en": "rolling on fluffy carpet like lazy cat, snacks scattered all around",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_427",
    "category": "วันหยุด & พักผ่อน",
    "caption": "อ่านหนังสือเล่มโปรด",
    "pose": "นั่งริมหน้าต่าง จิบชาอ่านนิยาย",
    "emotion": "สุขุม จินตนาการกว้างไกล",
    "props": "กองหนังสือและแมวหลับข้างๆ",
    "prompt_en": "reading novel by sunlit window sipping tea with sleeping cat beside",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_428",
    "category": "วันหยุด & พักผ่อน",
    "caption": "พักผ่อนจิตใจ",
    "pose": "นั่งใต้ร่มไม้ใหญ่ ฟังเสียงนก",
    "emotion": "สงบ นิ่ง ปราศจากเรื่องวุ่นวาย",
    "props": "ใบไม้ร่วงและแสงแดดรำไร",
    "prompt_en": "sitting peacefully under giant shady oak tree listening to birdsong, zen",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_429",
    "category": "วันหยุด & พักผ่อน",
    "caption": "เที่ยวคาเฟ่สวยๆ",
    "pose": "โพสท่าถ่ายรูปคู่แก้วมัทฉะลาเต้",
    "emotion": "น่ารัก ชิค อินสตาแกรมเมเบิล",
    "props": "เค้กมินิมอลและมุมถ่ายรูป",
    "prompt_en": "posing aesthetic cafe portrait with iced matcha latte, pastel bakery vibe",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_430",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ช้อปปิ้งวันหยุด",
    "pose": "เดินช้อปปิ้งมอลล์หิ้วถุงแบรนด์เนม",
    "emotion": "ฟินกับของขวัญให้ตัวเอง",
    "props": "แสงไฟห้างหรูระยิบระยับ",
    "prompt_en": "strolling through gleaming luxury mall with designer bags, retail therapy",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_431",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ไปไหว้พระทำบุญ",
    "pose": "ถือพวงมาลัยดอกดาวเรือง จุดธูป",
    "emotion": "อิ่มบุญ จิตใจผ่องใส สงบ",
    "props": "ควันธูปหอมและองค์พระพุทธรูป",
    "prompt_en": "holding marigold garland offering incense at Thai temple, serene merit smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_432",
    "category": "วันหยุด & พักผ่อน",
    "caption": "นวดแผนไทยฟินๆ",
    "pose": "นอนนวดคอบ่าไหล่สบายตัว",
    "emotion": "คลายเส้น หายเมื่อย ปลิดทิ้ง",
    "props": "ลูกประคบสมุนไพรและน้ำมันหอม",
    "prompt_en": "relaxing under Thai herbal massage, relieved happy melting expression",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_433",
    "category": "วันหยุด & พักผ่อน",
    "caption": "กินของอร่อยทั้งวัน",
    "pose": "เดินตลาดนัดกลางคืนสองมือถือสตรีทฟู้ด",
    "emotion": "ตะลุยกิน เพลิดเพลินใจ",
    "props": "โคมไฟตลาดและควันของปิ้งย่าง",
    "prompt_en": "eating street food skewers browsing bustling night market, pure foodie bliss",
    "color": "#F97316",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_434",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ดูพระอาทิตย์ตก",
    "pose": "นั่งบนโขดหินมองขอบฟ้าเปลี่ยนสี",
    "emotion": "โรแมนติก ซาบซึ้ง สงบสุข",
    "props": "ท้องฟ้าทไวไลท์สีชมพูส้ม",
    "prompt_en": "watching sunset on coastal rocks, serene silhouette against twilight sky",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_435",
    "category": "วันหยุด & พักผ่อน",
    "caption": "นอนดูดาวกลางดอย",
    "pose": "นอนดูดาวบนหลังคารถ สวมเสื้อกันหนาว",
    "emotion": "ตื่นตากับความกว้างใหญ่",
    "props": "ทางช้างเผือกส่องแสงระยิบ",
    "prompt_en": "stargazing from car rooftop bundled in sweater, milky way galaxy glowing",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_436",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ไปดำน้ำดูปะการัง",
    "pose": "ใส่แว่นตาดำน้ำ คาบท่อหายใจ โบกมือ",
    "emotion": "ตื่นเต้นกับโลกใต้ทะเล",
    "props": "ปลาการ์ตูนและปะการังหลากสี",
    "prompt_en": "snorkeling with mask and breathing tube waving, colorful clownfish swimming",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_437",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ขับรถกินลมชมวิว",
    "pose": "เปิดกระจกรถรับลม ฮัมเพลงสบายๆ",
    "emotion": "อิสระ ปลอดโปร่ง ฮีลใจ",
    "props": "ถนนเลียบชายหาดและต้นมะพร้าว",
    "prompt_en": "driving convertible along coastal highway letting breeze ruffle hair, singing",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_438",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ว่ายน้ำคลายร้อน",
    "pose": "กระโดดพุ่งหลาวลงสระว่ายน้ำสีฟ้า",
    "emotion": "กระปรี้กระเปร่า สดชื่นสุดขีด",
    "props": "ละอองน้ำกระจายตูม",
    "prompt_en": "diving gracefully into sparkling turquoise swimming pool, water splashing",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_439",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ร้องคาราโอเกะหลุดโลก",
    "pose": "ถือไมค์แหกปากร้องเพลงสุดเสียง",
    "emotion": "ปลดปล่อยพลัง สนุกสุดเหวี่ยง",
    "props": "ลูกบอลดิสโก้หมุนสะท้อนแสง",
    "prompt_en": "singing loudly into microphone dancing wildly, spinning disco ball flashes",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_440",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ทำอาหารกินเอง",
    "pose": "สวมหมวกกุ๊ก โยนกระทะผัดสไตล์เชฟ",
    "emotion": "ภูมิใจ สนุกกับการเข้าครัว",
    "props": "ไฟลุกในกระทะและกลิ่นหอม",
    "prompt_en": "tossing stir-fry in wok wearing chef hat, sizzling pan flames, proud smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_441",
    "category": "วันหยุด & พักผ่อน",
    "caption": "จัดห้องใหม่รับพลังบวก",
    "pose": "ถือไม้กวาดจัดแจกันดอกไม้สด",
    "emotion": "สดใส สะอาด ปลอดโปร่ง",
    "props": "ประกายสะอาดวิ้งๆ ในห้อง",
    "prompt_en": "sweeping and organizing bedroom placing fresh flowers, tidy sparkling room",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_442",
    "category": "วันหยุด & พักผ่อน",
    "caption": "นอนกลิ้งไปมา",
    "pose": "กลิ้งซ้ายกลิ้งขวาบนเตียงนุ่ม",
    "emotion": "ขี้เกียจอย่างมีความสุข",
    "props": "หมอนข้างและผ้าห่มฟู",
    "prompt_en": "rolling left and right lazily across plush mattress, blissful carefree chuckles",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_443",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ไปปิคนิคในสวน",
    "pose": "ปูเสื่อลายสก็อต วางตะกร้าแซนด์วิช",
    "emotion": "อบอุ่น ชิลล์ท่ามกลางธรรมชาติ",
    "props": "ตะกร้าสานและผลไม้สด",
    "prompt_en": "sitting on picnic gingham blanket in park with sandwich basket, breezy sun",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_444",
    "category": "วันหยุด & พักผ่อน",
    "caption": "เดินเล่นรับลมเย็น",
    "pose": "สวมเสื้อคลุมเดินทอดน่องริมแม่น้ำ",
    "emotion": "ผ่อนคลาย คิดอะไรเรื่อยเปื่อย",
    "props": "แสงไฟริมน้ำสะท้อนระยิบระยับ",
    "prompt_en": "strolling along riverside promenade in cozy cardigan, reflective peaceful gaze",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_445",
    "category": "วันหยุด & พักผ่อน",
    "caption": "นอนดูการ์ตูนทั้งวัน",
    "pose": "กอดถุงขนมขบเคี้ยวนอนดูจอ",
    "emotion": "ย้อนวัย สบายใจ ไร้ภาระ",
    "props": "ตัวการ์ตูนลอยออกมาจากจอ",
    "prompt_en": "watching cartoons all day hugging snack bag, innocent carefree childlike smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_446",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ฮีลใจด้วยธรรมชาติ",
    "pose": "ยืนโอบกอดต้นไม้ใหญ่กลางป่า",
    "emotion": "รับพลังธรรมชาติ ฟื้นฟูจิตใจ",
    "props": "ละอองหมอกและแสงแดดส่องร่มไม้",
    "prompt_en": "hugging ancient tree in lush forest, absorbing healing earth energy, sunlight beams",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_447",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ไปล่องแก่งผจญภัย",
    "pose": "ใส่ชูชีพ พายเรือยางฝ่าแก่งน้ำ",
    "emotion": "มันส์ สนุก กรี๊ดสนั่น",
    "props": "คลื่นน้ำเชี่ยวกรากสาดกระเซ็น",
    "prompt_en": "whitewater rafting in life jacket paddling vigorously, adrenaline thrill smile",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_448",
    "category": "วันหยุด & พักผ่อน",
    "caption": "ชื่นชมดอกไม้บาน",
    "pose": "โน้มตัวลงดมกลิ่นดอกกุหลาบในสวน",
    "emotion": "อ่อนโยน ดื่มด่ำความงาม",
    "props": "ผึ้งน้อยและละอองเกสร",
    "prompt_en": "gently sniffing blooming garden rose, delicate serene romantic expression",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_449",
    "category": "วันหยุด & พักผ่อน",
    "caption": "จิบชาบ่ายสไตล์ผู้ดี",
    "pose": "ประคองถ้วยชาอังกฤษ กัดสโคน",
    "emotion": "หรูหรา ผู้ดี มีระดับ",
    "props": "หอคอยขนม 3 ชั้นสไตล์อังกฤษ",
    "prompt_en": "afternoon high tea holding fine porcelain cup biting scone, elegant poise",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_450",
    "category": "วันหยุด & พักผ่อน",
    "caption": "วันหยุดผ่านไปไวเหมือนโกหก",
    "pose": "กอดเสาไม่อยากให้ถึงวันจันทร์",
    "emotion": "อาลัยอาวรณ์ ตลก ร้องไห้แงๆ",
    "props": "ปฏิทินวันจันทร์ขยับเข้ามาใกล้",
    "prompt_en": "clinging desperately to doorpost terrified of Monday, comic weeping face",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_451",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อย่าให้ถึงตาฉันบ้างนะ",
    "pose": "กอดอกกัดฟัน หรี่ตามองคาดโทษ",
    "emotion": "แค้นฝังหุ่น รอวันเอาคืน",
    "props": "ประกายไฟแค้นลุกในตา",
    "prompt_en": "glaring with crossed arms gritting teeth plotting revenge, comic fiery eyes",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_452",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "หมดคำจะพูด",
    "pose": "อ้าปากค้างเอามือกุมขมับ ถอนหายใจ",
    "emotion": "เอือมระอา เกินจะบรรยาย",
    "props": "ฟองอากาศว่างเปล่า '...'",
    "prompt_en": "jaw dropped rubbing temples, completely speechless exasperated sigh",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_453",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "โกรธแล้วนะ",
    "pose": "กระทืบเท้า หน้าแดงควันออกหู",
    "emotion": "โกรธจัด งอนแรง ไม่คุยด้วย",
    "props": "ควันไอน้ำพ่นจากหูสองข้าง",
    "prompt_en": "stomping foot face red with steam hissing from ears, furious adorable pout",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_454",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ใจเย็นก่อนโยม",
    "pose": "ทำท่ายกมือห้าม ยิ้มเย็นแบบสงบ",
    "emotion": "เตือนสติ ดึงสติคนที่กำลังเดือด",
    "props": "หยดน้ำค้างดับเปลวไฟ",
    "prompt_en": "holding up calming palm serene smile, putting out flames with cool water",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_455",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "เครียดเลย",
    "pose": "ขยำกระดาษจนยับ กุมหัวสองมือ",
    "emotion": "เครียดตึ้บ แก้ปัญหาไม่ตก",
    "props": "เส้นเลือดเต้นตุบๆ ที่ขมับ",
    "prompt_en": "crumpling paper clutching head tightly, throbbing stress vein on temple",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_456",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ปวดหัวตึ้บ",
    "pose": "เอามือกุมหน้าผาก หมุนวนขมับ",
    "emotion": "ปวดหัว ไมเกรนขึ้นทันที",
    "props": "สายฟ้าแลบในสมอง",
    "prompt_en": "rubbing throbbing forehead with grimace, lightning bolt migraine icon",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_457",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "จะร้องไห้แล้วนะ",
    "pose": "เบะปาก น้ำตาเอ่อล้นคลอสองเบ้า",
    "emotion": "ทนไม่ไหวแล้ว น้อยใจ เสียใจ",
    "props": "หยดน้ำตาเม็ดเป้งเกาะขนตา",
    "prompt_en": "trembling lower lip with massive tear pools welling up, ready to burst",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_458",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ใครทำเธอ บอกมา",
    "pose": "ม้วนแขนเสื้อ ถือท่อนไม้เตรียมลุย",
    "emotion": "ปกป้องเพื่อน โมโหแทน เอาเรื่อง",
    "props": "เปลวไฟลุกท่วมฉากหลัง",
    "prompt_en": "rolling up sleeves brandishing club, ready to defend friend angrily",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_459",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ไม่อยากคุยด้วยแล้ว",
    "pose": "หันหลังหนี เอาหูฟังอุดหูสองข้าง",
    "emotion": "ตัดขาด งอน ไม่ฟังคำแก้ตัว",
    "props": "กำแพงอิฐก่อขึ้นกั้นกลาง",
    "prompt_en": "turning back plugging ears with headphones, brick wall rising between",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_460",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "เจ็บกระดองใจ",
    "pose": "เอามือกุมอก ล้มตัวลงคุกเข่า",
    "emotion": "ช้ำใจ เจ็บแปลบ โดนแทงข้างหลัง",
    "props": "มีดของเล่นปักกลางหลัง",
    "prompt_en": "collapsing to knees clutching chest in dramatic heartbreak, toy dagger in back",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_461",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ทำไมทำแบบนี้",
    "pose": "ชี้หน้าถาม แววตาตัดพ้อรุนแรง",
    "emotion": "ผิดหวัง เสียความรู้สึกอย่างยิ่ง",
    "props": "กระจกแตกร้าวตรงกลาง",
    "prompt_en": "pointing finger asking in deep hurt betrayal, cracked mirror reflection",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_462",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "เสียความรู้สึกมาก",
    "pose": "ยืนหันข้างกอดอก น้ำตาหยดลงแก้ม",
    "emotion": "เศร้าลึก เสียใจ หมดศรัทธา",
    "props": "หัวใจแตกสลายเป็นเสี่ยงๆ",
    "prompt_en": "standing side-profile crossing arms silent tear falling, shattered heart",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_463",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ขอเวลาอยู่คนเดียว",
    "pose": "นั่งกอดเข่าปิดไฟในห้องมืด",
    "emotion": "ต้องการความสงบ ถอยมาพักใจ",
    "props": "โคมไฟดวงเดียวส่องสลัว",
    "prompt_en": "hugging knees sitting in dimly lit room, needing solitary healing space",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_464",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "โมโหร้าย",
    "pose": "กัดผ้าเช็ดหน้าดึงสุดแรง ตาโต",
    "emotion": "แค้นใจ กัดฟันกรอด ข่มอารมณ์",
    "props": "ประกายไฟสปาร์ค",
    "prompt_en": "biting handkerchief tugging fiercely in sheer comic rage, sparking eyes",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_465",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อย่ามาแตะต้อง",
    "pose": "กางแขนตั้งการ์ดปัดมือออก",
    "emotion": "หวงตัว รังเกียจ ไม่ให้ยุ่ง",
    "props": "กำแพงหนามกั้นล้อมรอบ",
    "prompt_en": "swatting hand away setting defensive guard, barbed wire boundary",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_466",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "เกลียดคนโกหก",
    "pose": "หรี่ตาจับผิด หน้าตาคมกริบ",
    "emotion": "เกลียดการหลอกลวง เด็ดขาด",
    "props": "จมูกพิน็อกคิโอยาวเหยียด",
    "prompt_en": "sharp piercing glare discerning lies, long Pinocchio nose growing on shadow",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_467",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ทำดีไม่ได้ดี",
    "pose": "ยืนตากฝนแบมือถามฟ้า",
    "emotion": "ท้อแท้ โชคชะตากลั่นแกล้ง",
    "props": "ฝนตกฟ้าร้องผ่าเปรี้ยง",
    "prompt_en": "standing in pouring rain questioning destiny, thunderstorm clouds",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_468",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "พูดแล้วจะร้อง",
    "pose": "เอามือปิดปาก กลืนก้อนสะอื้น",
    "emotion": "กลั้นน้ำตาสุดชีวิต ตื้นตัน/เศร้า",
    "props": "หยดน้ำตาเอ่อล้นขอบตา",
    "prompt_en": "hand over mouth swallowing sob, holding back flood of tears bravely",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_469",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ทำไมใจร้ายจัง",
    "pose": "กอดตุ๊กตาร้องไห้ตาแดงก่ำ",
    "emotion": "น้อยใจ ทำไมต้องทำร้ายจิตใจ",
    "props": "ตุ๊กตาหมีหน้าเศร้ากอดตอบ",
    "prompt_en": "hugging teddy bear with red teary eyes, asking why so cruel, sad sniffles",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_470",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "พอกันที",
    "pose": "โยนเอกสารทุกอย่างทิ้ง เดินหนี",
    "emotion": "เด็ดขาด เลิกทน ปลดแอก",
    "props": "ประตูบานใหญ่ปิดกระแทกปัง",
    "prompt_en": "throwing all papers in air turning back walking away, slamming door shut",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_471",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อย่าท้าทายระบบ",
    "pose": "สวมแว่นตาดำ ถือไม้เรียวเคาะโต๊ะ",
    "emotion": "มีอำนาจ เด็ดขาด อย่าลองดี",
    "props": "สายฟ้าแลบแปลบปลาบ",
    "prompt_en": "wearing dark glasses tapping pointer stick on desk, intimidating authority",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_472",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ความจริงมันเจ็บปวด",
    "pose": "ยืนรับลูกธนูความจริงปักอก",
    "emotion": "ยอมรับความจริงที่โหดร้าย",
    "props": "ลูกศรคำพูดปักกลางอก",
    "prompt_en": "standing taking arrow of bitter truth straight to chest, tragic comic pose",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_473",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อย่าให้หมดความอดทน",
    "pose": "กำหมัดสั่นระริก เส้นเลือดปูด",
    "emotion": "ความอดทนใกล้หมดขีดจำกัด",
    "props": "หม้อต้มน้ำเดือดปุดๆ พ่นไอ",
    "prompt_en": "clenched fist trembling with popping vein, boiling kettle ready to whistle",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_474",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "พูดไม่คิด",
    "pose": "เอามือฟาดหน้าผากตัวเองแรงๆ",
    "emotion": "เอือมระอาคำพูดไร้สติ",
    "props": "เครื่องหมายคำพูดบินกระจัดกระจาย",
    "prompt_en": "facepalming hard at thoughtless words, scattered careless speech bubbles",
    "color": "#94A3B8",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_475",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "น้อยใจอยู่นะ",
    "pose": "นั่งกอดเข่าเขียนพื้นดินด้วยกิ่งไม้",
    "emotion": "งอน เรียกร้องความสนใจเบาๆ",
    "props": "รูปหัวใจวาดบนดินทราย",
    "prompt_en": "drawing broken heart in dirt with stick, pouting waiting for comfort",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_476",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "แทงข้างหลังทะลุถึงหัวใจ",
    "pose": "กุมหน้าอกด้านหน้า ลูกศรทะลุหลัง",
    "emotion": "โดนหักหลัง ทรยศ เจ็บแสบ",
    "props": "ลูกธนูหักหลังปักแน่น",
    "prompt_en": "dramatic anime betrayal pose clutching chest with arrow piercing through",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_477",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ทำไมต้องเป็นฉัน",
    "pose": "คุกเข่าชูมือขึ้นฟ้าถามสวรรค์",
    "emotion": "ตัดพ้อโชคชะตา เล่นใหญ่",
    "props": "แสงสปอตไลท์ส่องลงคนเดียว",
    "prompt_en": "kneeling hands raised to heaven asking why me, dramatic opera spotlight",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_478",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "เกลียดความอยุติธรรม",
    "pose": "ทุบโต๊ะดังปัง ลุกขึ้นประท้วง",
    "emotion": "เรียกร้องความถูกต้อง ดุดัน",
    "props": "ค้อนตุลาการหักสองท่อน",
    "prompt_en": "slamming fist on desk standing up to protest, broken judge gavel",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_479",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อารมณ์บูด",
    "pose": "ทำหน้าเหม็นเบื่อ ปากเบ้ไปข้าง",
    "emotion": "หงุดหงิด อารมณ์เสีย ไร้สาเหตุ",
    "props": "นมเปรี้ยวบูดมีกลิ่นเหม็น",
    "prompt_en": "sour foul mood with mouth twisted sideways, spoiled curdled milk icon",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_480",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อย่ามาจุดชนวน",
    "pose": "ยืนเท้าสะเอวชี้ป้ายเตือนการ์ตูนอิโมจิหน้าบึ้งพ่นควัน",
    "emotion": "เตือนเล่นๆ ว่าอย่าแหย่ เดี๋ยวอารมณ์ขึ้น",
    "props": "ป้ายเตือนการ์ตูนอิโมจิหน้าแดงพ่นควันน่ารัก",
    "prompt_en": "standing with hand on hip pointing at cute cartoon steaming angry face warning sign, playful stern chibi pout, 100% wholesome kid-friendly",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_481",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ปรี๊ดแตก",
    "pose": "ทำแก้มป่องหน้าแดงมีควันการ์ตูนปุ๋งๆ ออกจากหู",
    "emotion": "งอนน่ารัก อารมณ์ปรี๊ดแบบการ์ตูน",
    "props": "เอฟเฟกต์ควันการ์ตูนสีขาวลอยน่ารัก",
    "prompt_en": "puffed red cheeks with cute cartoon steam puffs from ears, playful anime tantrum, cute harmless chibi",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_482",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ช่างมันเถอะ",
    "pose": "ปัดมือทิ้ง ส่ายหน้าเบื่อหน่าย",
    "emotion": "ปลง ตัดรำคาญ ไม่สนใจแล้ว",
    "props": "ฝุ่นละอองปลิวหายไป",
    "prompt_en": "swatting hand dismissively shaking head, brush it off careless sigh",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_483",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อย่ามาเล่นกับไฟ",
    "pose": "จุดไฟแช็ค ดีดนิ้วมีไฟลุก",
    "emotion": "เตือนด้วยความมั่นใจ อันตราย",
    "props": "กำแพงเปลวไฟสีส้มแดง",
    "prompt_en": "flicking lighter snapping fiery fingers, dangerous fiery confidence",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_484",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ทนไม่ไหวแล้วโว้ย",
    "pose": "ฉีกกระดาษเป็นชิ้นๆ ตะโกนลั่น",
    "emotion": "ระเบิดอารมณ์ ปลดปล่อยสุดขีด",
    "props": "กระดาษขาดปลิวว่อน",
    "prompt_en": "ripping paper to shreds roaring in fury, paper scraps flying everywhere",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_485",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ผิดหวังที่สุด",
    "pose": "หันหลังเดินจากไป ทิ้งเงาดำมืด",
    "emotion": "สิ้นหวัง ตัดขาด ไม่หันหลังกลับ",
    "props": "ดอกกุหลาบเหี่ยวแห้งร่วงโรย",
    "prompt_en": "walking away into shadowy darkness, wilting black rose dropping petals",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_486",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "หน้าไหว้หลังหลอก",
    "pose": "ถอดหน้ากากยิ้มออกเผยหน้าจริง",
    "emotion": "แฉคนสองหน้า รังเกียจ",
    "props": "หน้ากากสองหน้าขาวดำ",
    "prompt_en": "peeling off smiling mask to reveal cold stare, two-faced deceit theme",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_487",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "อย่ามายุ่งกับฉัน",
    "pose": "วาดวงกลมรอบตัวเอง ถือป้ายห้ามเข้า",
    "emotion": "ต้องการระยะห่าง ไม่รับแขก",
    "props": "กรวยจราจรและเชือกกั้น",
    "prompt_en": "drawing chalk boundary circle around self, barricade cones, do not cross",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_488",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "เจ็บแล้วจำคือคน",
    "pose": "เอามือจับรอยแผลเป็นที่หัวใจ",
    "emotion": "เข้มแข็งขึ้นจากบาดแผล เรียนรู้",
    "props": "โล่เหล็กกำบังหัวใจ",
    "prompt_en": "touching heart scar with hardened resolute expression, steel shield",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_489",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "ไม่อยากมองหน้า",
    "pose": "เอากระดาษหนังสือพิมพ์มาบังหน้า",
    "emotion": "ไม่อยากเห็น ไม่ชอบใจ ขำๆ",
    "props": "หนังสือพิมพ์เจาะรูตาแอบมอง",
    "prompt_en": "holding newspaper in front of face with two peepholes, silent boycott",
    "color": "#64748B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_490",
    "category": "ดราม่า & อารมณ์เหวี่ยง",
    "caption": "จบลบเลิก",
    "pose": "เคาะค้อนตุลาการลงแท่นไม้ ปิดคดี",
    "emotion": "เด็ดขาด สิ้นสุด ไม่ต่อรอง",
    "props": "ตราประทับ CLOSED สีแดงฉาน",
    "prompt_en": "slamming gavel down decisively closing case, big red CLOSED stamp",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_491",
    "category": "อวยพร & มงคล",
    "caption": "ร่ำรวยเงินทอง",
    "pose": "นั่งบนกองเงินกองทอง โปรยเหรียญ",
    "emotion": "มั่งคั่ง เบิกบาน หน้าตามีสุข",
    "props": "ก้อนทองตำลึงจีนและเหรียญทอง",
    "prompt_en": "sitting atop treasure trove tossing gold coins, prosperous radiant smile",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_492",
    "category": "อวยพร & มงคล",
    "caption": "เฮงๆ ปังๆ",
    "pose": "ถือป้ายอักษรจีนมงคล 'ฮก' สวมชุดกี่เพ้า",
    "emotion": "โชคดี รุ่งเรือง ฉลองตรุษจีน",
    "props": "ประทัดสีแดงและส้มมงคล",
    "prompt_en": "holding golden Chinese blessing plaque in festive silk robe, firecrackers",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_493",
    "category": "อวยพร & มงคล",
    "caption": "สุขภาพแข็งแรง",
    "pose": "เบ่งกล้ามแขนสองข้าง ตาเป็นประกาย",
    "emotion": "แข็งแรง กระปรี้กระเปร่า อายุยืน",
    "props": "หัวใจสีแดงเต้นแข็งแรง",
    "prompt_en": "flexing strong muscular bicep with energetic beaming grin, vigorous health",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_494",
    "category": "อวยพร & มงคล",
    "caption": "โชคดีมีชัย",
    "pose": "ถือธงชัยชนะสีทองโบกสะบัด",
    "emotion": "อวยพรให้มีชัยชนะทุกสมรภูมิ",
    "props": "ม้าศึกสีขาววิ่งทะยาน",
    "prompt_en": "waving golden victory flag wishing triumph, galloping noble white steed",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_495",
    "category": "อวยพร & มงคล",
    "caption": "มีความสุขมากๆ นะ",
    "pose": "ปล่อยนกพิราบขาวบินสู่ท้องฟ้า",
    "emotion": "จิตใจบริสุทธิ์ ส่งต่อความสุข",
    "props": "นกพิราบขาวและสายรุ้งงาม",
    "prompt_en": "releasing white dove into bright blue sky, pure joyous loving blessing",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_496",
    "category": "อวยพร & มงคล",
    "caption": "สมปรารถนาทุกประการ",
    "pose": "อธิษฐานต่อดาวตกสองมือประสาน",
    "emotion": "ความฝันเป็นจริงทุกประการ",
    "props": "ดวงดาวประกายแสงวิบวับ",
    "prompt_en": "making wish on falling shooting star with hands clasped, stardust aura",
    "color": "#6366F1",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_497",
    "category": "อวยพร & มงคล",
    "caption": "ค้าขายร่ำรวย",
    "pose": "กวักมือเรียกลูกค้าเหมือนแมวกวัก",
    "emotion": "ดึงดูดทรัพย์ กิจการเจริญรุ่งเรือง",
    "props": "แมวกวักนำโชคสีทองและพานทอง",
    "prompt_en": "beckoning customers like lucky golden Maneki-neko cat, booming shop vibes",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_498",
    "category": "อวยพร & มงคล",
    "caption": "เงินไหลกองทองไหลมา",
    "pose": "เปิดหีบสมบัติแสงสีทองส่องประกาย",
    "emotion": "ทรัพย์สมบัติเนืองนอง ไร้ขีดจำกัด",
    "props": "ประกายแสงเพชรพลอยระยิบระยับ",
    "prompt_en": "opening magical chest overflowing with jewels and gold, brilliant luminescence",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_499",
    "category": "อวยพร & มงคล",
    "caption": "แคล้วคลาดปลอดภัย",
    "pose": "ยืนมีเกราะแก้วใสล้อมรอบตัว",
    "emotion": "คุ้มครอง ปกป้อง รอดพ้นอันตราย",
    "props": "ยันต์มงคลและแสงคุ้มภัยสีฟ้า",
    "prompt_en": "shielded inside protective crystal orb barrier, divine safe blessing",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_500",
    "category": "อวยพร & มงคล",
    "caption": "สุขสันต์วันสงกรานต์",
    "pose": "ถือขันน้ำอบไทยพรมน้ำยิ้มสดใส",
    "emotion": "เย็นชุ่มฉ่ำ รื่นเริง ต้อนรับปีใหม่ไทย",
    "props": "ขันเงินลายไทยและดอกมะลิ",
    "prompt_en": "holding traditional Thai silver water bowl sprinkling perfumed water, Songkran",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_501",
    "category": "อวยพร & มงคล",
    "caption": "สุขสันต์วันปีใหม่",
    "pose": "เป่าลิ้นกระดาษปาร์ตี้ จุดพลุฉลอง",
    "emotion": "สดชื่น ต้อนรับสิ่งใหม่ๆ โชคดี",
    "props": "พลุปีใหม่หลากสีและลูกโป่ง 2026",
    "prompt_en": "blowing party horn celebrating New Year countdown, dazzling midnight fireworks",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_502",
    "category": "อวยพร & มงคล",
    "caption": "สุขสันต์วันลอยกระทง",
    "pose": "ประคองกระทงใบตองจุดเทียนสว่าง",
    "emotion": "ขอขมาพระแม่คงคา งดงาม อ่อนหวาน",
    "props": "กระทงดอกบัวลอยบนผิวน้ำสะท้อนแสงจันทร์",
    "prompt_en": "gently holding lit banana leaf Krathong on moonlit water, serene floating festival",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_503",
    "category": "อวยพร & มงคล",
    "caption": "ขอให้โชคดี",
    "pose": "ชูใบโคลเวอร์ 4 แฉกสีเขียวมรกต",
    "emotion": "นำพาความโชคดีมาสู่เธอ",
    "props": "เกือกม้าทองคำนำโชค",
    "prompt_en": "presenting emerald 4-leaf clover with sparkling hopeful smile, lucky horseshoe",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_504",
    "category": "อวยพร & มงคล",
    "caption": "สาธุ อนุโมทนาบุญ",
    "pose": "พนมมือนิ่ง แววตาเปี่ยมบุญบารมี",
    "emotion": "อิ่มบุญ จิตใจผ่องใส สว่างไสว",
    "props": "ดอกบัวหลวงสีชมพูบานสะพรั่ง",
    "prompt_en": "hands together in reverent Thai Sadhu merit gesture, blooming pink lotus",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_505",
    "category": "อวยพร & มงคล",
    "caption": "อายุยืนหมื่นปี",
    "pose": "ถือผลท้อสวรรค์สองมือมอบให้",
    "emotion": "อายุยืนยาว แข็งแรง ไร้โรคา",
    "props": "ผลท้อมงคลสีชมพูแดง",
    "prompt_en": "presenting celestial longevity peach with respectful deep bow, eternal vitality",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_506",
    "category": "อวยพร & มงคล",
    "caption": "การงานก้าวหน้า",
    "pose": "ก้าวขึ้นบันไดทองคำสู่ยอดตึกสูง",
    "emotion": "เลื่อนขั้น เลื่อนตำแหน่ง รุ่งเรือง",
    "props": "บันไดทองคำและดวงดาว",
    "prompt_en": "climbing upward on shining golden staircase, career promotion success",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_507",
    "category": "อวยพร & มงคล",
    "caption": "สอบผ่านฉลุย",
    "pose": "ถือใบเกรด A+ ชูนิ้วโป้งยิ้มแป้น",
    "emotion": "สำเร็จดั่งใจ คว้าเกียรตินิยม",
    "props": "หมวกปริญญาและใบปริญญาบัตร",
    "prompt_en": "waving report card with straight A+ grades, graduation mortarboard tossing",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_508",
    "category": "อวยพร & มงคล",
    "caption": "เดินทางโดยสวัสดิภาพ",
    "pose": "โบกผ้าพันคออวยพรข้างขบวนรถไฟ",
    "emotion": "ปลอดภัยทุกการเดินทาง ราบรื่น",
    "props": "เครื่องบินบินผ่านก้อนเมฆ",
    "prompt_en": "waving scarf wishing peaceful safe travel journey, airplane soaring",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_509",
    "category": "อวยพร & มงคล",
    "caption": "บารมีคุ้มครอง",
    "pose": "ยืนในวงล้อมแสงธรรมสีทองสว่าง",
    "emotion": "คุ้มกันภัย เมตตามหานิยม",
    "props": "รัศมีพระธรรมจักรสีทอง",
    "prompt_en": "standing within protective golden aura of divine grace, spiritual safety",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_510",
    "category": "อวยพร & มงคล",
    "caption": "ชนะทุกอุปสรรค",
    "pose": "ชูดาบแสงแห่งความกล้าหาญฟันเมฆดำ",
    "emotion": "เกรียงไกร ไร้พ่าย พิชิตทุกสิ่ง",
    "props": "ดาบแสงประกายเพชร",
    "prompt_en": "raising glowing sword of courage banishing dark storm, triumphant hero",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_511",
    "category": "อวยพร & มงคล",
    "caption": "ขอให้ถูกหวยรางวัลที่ 1",
    "pose": "ถือสลากกินแบ่งรัฐบาล 6 ตัวตรง",
    "emotion": "ลุ้นรวย เบิกบาน เป็นเศรษฐีใหม่",
    "props": "ถุงทองและลูกแก้วเสี่ยงทาย",
    "prompt_en": "holding lucky lottery ticket with beaming expectant grin, winning jackpot",
    "color": "#EF4444",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_512",
    "category": "อวยพร & มงคล",
    "caption": "มีกินมีใช้ไม่ขาดมือ",
    "pose": "ถือตะกร้าผลไม้และอาหารพูนล้น",
    "emotion": "อุดมสมบูรณ์ มั่งคั่ง มั่นคง",
    "props": "รวงข้าวสีทองสุกอร่าม",
    "prompt_en": "holding overflowing horn of plenty harvest basket, golden ripe rice stalks",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_513",
    "category": "อวยพร & มงคล",
    "caption": "สุขกายสบายใจ",
    "pose": "นอนอมยิ้มบนเก้าอี้หวายโยกเยก",
    "emotion": "ผาสุก ไร้ความกังวล สบายตัว",
    "props": "ชามะลิหอมกรุ่นควันลอย",
    "prompt_en": "rocking gently on wicker chair with serene blissful smile, jasmine tea aroma",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_514",
    "category": "อวยพร & มงคล",
    "caption": "ชีวิตราบรื่น",
    "pose": "แล่นเรือใบสีขาวบนผิวน้ำเรียบดั่งกระจก",
    "emotion": "ไร้อุปสรรค ราบรื่น ไหลลื่น",
    "props": "สายลมอ่อนและปลาโลมากระโดด",
    "prompt_en": "sailing white sailboat on mirror-calm crystal water, smooth sailing journey",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_515",
    "category": "อวยพร & มงคล",
    "caption": "มิตรภาพยั่งยืน",
    "pose": "จับมือเพื่อนผูกริบบิ้นสีทองสองมือ",
    "emotion": "ผูกพัน กลมเกลียว ตลอดกาล",
    "props": "ต้นไม้แห่งมิตรภาพแตกกิ่งก้าน",
    "prompt_en": "tying golden ribbon around intertwined hands of true friendship, enduring bond",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_516",
    "category": "อวยพร & มงคล",
    "caption": "กิจการรุ่งเรือง",
    "pose": "ตัดริบบิ้นเปิดร้านใหม่ ป้ายทองส่องแสง",
    "emotion": "เจริญก้าวหน้า ลูกค้าแน่นร้าน",
    "props": "พรรณไม้ดอกฉลองเปิดร้าน",
    "prompt_en": "cutting ceremonial grand opening ribbon, thriving booming business entrance",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_517",
    "category": "อวยพร & มงคล",
    "caption": "ครอบครัวอบอุ่น",
    "pose": "กอดรวมสมาชิกในบ้านพร้อมหน้า",
    "emotion": "เปี่ยมรัก กลมเกลียว มีสุข",
    "props": "บ้านหลังน้อยมีควันลอยจากปล่อง",
    "prompt_en": "whole family warm group hug, glowing cozy fireplace cottage in background",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_518",
    "category": "อวยพร & มงคล",
    "caption": "คิดสิ่งใดสมความปรารถนา",
    "pose": "ลูบตะเกียงวิเศษมีควันยักษ์ใจดีลอย",
    "emotion": "สมหวังดั่งเวทมนตร์ ปาฏิหาริย์",
    "props": "ตะเกียงทองคำและประกายเวทย์",
    "prompt_en": "rubbing golden magic lamp with friendly genie vapor granting wishes",
    "color": "#8B5CF6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_519",
    "category": "อวยพร & มงคล",
    "caption": "ไร้โรคภัยไข้เจ็บ",
    "pose": "โยนขวดยาทิ้ง ยืนสูดหายใจโล่งอก",
    "emotion": "หายป่วย ปลอดโรค ร่างกายสดชื่น",
    "props": "ผีเสื้อโบยบินรอบตัวแข็งแรง",
    "prompt_en": "tossing away medicine bottles taking deep healthy breath, vibrant vitality",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_520",
    "category": "อวยพร & มงคล",
    "caption": "มีเสน่ห์ดึงดูดใจ",
    "pose": "โปรยเสน่ห์ขยิบตา รอยยิ้มพิมพ์ใจ",
    "emotion": "เมตตามหานิยม ใครเห็นใครรัก",
    "props": "ละอองเกสรดอกไม้หอมฟุ้ง",
    "prompt_en": "winking charmingly with radiant charismatic smile, captivating magnetic aura",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_521",
    "category": "อวยพร & มงคล",
    "caption": "อายุ วรรณะ สุขะ พละ",
    "pose": "พนมมือน้อมรับพรพระอย่างสงบ",
    "emotion": "พร 4 ประการแห่งความเจริญ",
    "props": "พระพุทธรูปปางสมาธิสีทอง",
    "prompt_en": "bowing peacefully receiving Buddhist four blessings of life, golden Buddha halo",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_522",
    "category": "อวยพร & มงคล",
    "caption": "เจริญในหน้าที่การงาน",
    "pose": "จับมือแสดงความยินดีในห้องทำงานหรู",
    "emotion": "ก้าวหน้า มั่นคง เป็นผู้บริหาร",
    "props": "ป้ายชื่อตำแหน่งใหม่บนโต๊ะไม้",
    "prompt_en": "congratulatory professional handshake in executive corner office, success",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_523",
    "category": "อวยพร & มงคล",
    "caption": "พบเจอแต่สิ่งดีๆ",
    "pose": "เปิดประตูรับแสงสว่างจ้าต้อนรับสิ่งใหม่",
    "emotion": "โชคชะตาเปิดรับ มงคลยิ่ง",
    "props": "ประตูบานใหญ่เปิดสู่ทุ่งดอกไม้",
    "prompt_en": "opening grand doorway into bright golden paradise meadow of blessings",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_524",
    "category": "อวยพร & มงคล",
    "caption": "จิตใจแจ่มใส",
    "pose": "นั่งสมาธิบนโขดหินริมน้ำตกใส",
    "emotion": "สงบนิ่ง ผ่องแผ้ว มีปัญญา",
    "props": "หยดน้ำตกและดอกบัวขาว",
    "prompt_en": "meditating beside crystalline waterfall, calm enlightened clarity",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_525",
    "category": "อวยพร & มงคล",
    "caption": "ศัตรูพ่ายแพ้",
    "pose": "ยืนกอดอกสง่างาม มีโล่ศักดิ์สิทธิ์",
    "emotion": "ชนะอุปสรรคทั้งปวง ปลอดภัย",
    "props": "โล่ทองคำสะท้อนแสงขับไล่สิ่งชั่วร้าย",
    "prompt_en": "standing regal with sacred divine shield reflecting away all negativity",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_526",
    "category": "อวยพร & มงคล",
    "caption": "สมรสสมรัก",
    "pose": "สวมมงคลแฝด รดน้ำสังข์คู่รัก",
    "emotion": "คู่สร้างคู่สม รักนิรันดร์",
    "props": "หอยสังข์รดน้ำและดอกรัก",
    "prompt_en": "wedding holy water pouring ceremony with twin flower crowns, eternal romance",
    "color": "#EC4899",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_527",
    "category": "อวยพร & มงคล",
    "caption": "บ้านนี้ร่มเย็นเป็นสุข",
    "pose": "แขวนโมบายกระดิ่งลมหน้าบ้านยิ้มสุข",
    "emotion": "สงบ อบอุ่น ร่มรื่น มั่นคง",
    "props": "กระดิ่งลมกรุ๊งกริ๊งและต้นไม้ใหญ่",
    "prompt_en": "hanging melodic windchime at home entrance, peaceful flourishing household",
    "color": "#10B981",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_528",
    "category": "อวยพร & มงคล",
    "caption": "โชคลาภไม่ขาดสาย",
    "pose": "ตักน้ำทองคำจากบ่อน้ำทิพย์ไม่รู้หมด",
    "emotion": "มีโชคตลอดเวลา ลาภลอย",
    "props": "บ่อน้ำศักดิ์สิทธิ์เปล่งแสง",
    "prompt_en": "scooping golden water from endless wishing well, continuous windfall wealth",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_529",
    "category": "อวยพร & มงคล",
    "caption": "มีความสุขในทุกวัน",
    "pose": "ยิ้มกว้างกางแขนต้อนรับทุกเช้า",
    "emotion": "มองโลกในแง่ดี เปี่ยมสุข",
    "props": "ปฏิทินยิ้มและแสงตะวัน",
    "prompt_en": "smiling wide with open arms greeting each new day, optimistic sunny disposition",
    "color": "#F59E0B",
    "stroke": "#FFFFFF"
  },
  {
    "id": "LINE_CAP_530",
    "category": "อวยพร & มงคล",
    "caption": "สวัสดีปีใหม่ไทย",
    "pose": "สาดน้ำสงกรานต์ขันเงิน สนุกสนาน",
    "emotion": "ชุ่มฉ่ำ เบิกบานใจ รื่นเริง",
    "props": "สายน้ำสาดกระจายประกายแดด",
    "prompt_en": "joyfully splashing festive Songkran water with silver bowl, sparkling water arcs",
    "color": "#3B82F6",
    "stroke": "#FFFFFF"
  }
]

def get_all_captions():
    """Return all 530 captions."""
    return CAPTIONS_DATABASE

def get_categories():
    """Return list of all unique category names."""
    cats = []
    for it in CAPTIONS_DATABASE:
        if it["category"] not in cats:
            cats.append(it["category"])
    return cats

def get_captions_by_category(category_name):
    """Filter captions by category."""
    return [it for it in CAPTIONS_DATABASE if it["category"] == category_name]

def search_captions(keyword):
    """Search captions by text or pose."""
    kw = keyword.strip().lower()
    if not kw:
        return CAPTIONS_DATABASE
    return [
        it for it in CAPTIONS_DATABASE
        if kw in it["caption"].lower() or kw in it["pose"].lower() or kw in it["category"].lower()
    ]

NO_CAPTION_POSES = [
    {
        "id": "NOCAP_01",
        "category": "Main & Tab (ไม่มีแคปชั่น)",
        "caption": "[ไม่มีข้อความ - แนะนำทำรูป Main ปก]",
        "pose": "ยืนตรง แอ็กท่าเท่/น่ารัก ยิ้มแย้มสดใส โบกมือทักทายอย่างมั่นใจ",
        "emotion": "ยิ้มหวาน มีเสน่ห์ อารมณ์ดีมาก",
        "props": "ประกายวิบวับรอบตัว",
        "prompt_en": "hero character presentation, facing forward waving hand cheerfully with sparkling eyes and sweet smile, no text, no words, clean character art",
        "color": "#000000",
        "stroke": "#FFFFFF"
    },
    {
        "id": "NOCAP_02",
        "category": "Main & Tab (ไม่มีแคปชั่น)",
        "caption": "[ไม่มีข้อความ - แนะนำทำรูป Tab ไอคอน]",
        "pose": "โคลสอัพท่อนบน ชูสองนิ้วกระพริบตาข้างเดียว แก้มแดงสดใส",
        "emotion": "ขี้เล่น ทะเล้น น่ารักสุดๆ",
        "props": "หัวใจดวงเล็กๆ ลอยข้างแก้ม",
        "prompt_en": "compact upper body bust shot, flashing cute peace sign with a playful wink and blushed cheeks, no text, no words, clean icon art",
        "color": "#000000",
        "stroke": "#FFFFFF"
    },
    {
        "id": "NOCAP_03",
        "category": "Main & Tab (ไม่มีแคปชั่น)",
        "caption": "[ไม่มีข้อความ - แอ็กชันส่งความรัก]",
        "pose": "ถือหัวใจดวงโตด้วยสองมือข้างลำตัว ส่งสายตาหวานซึ้ง",
        "emotion": "อบอุ่น เต็มเปี่ยมด้วยความรัก",
        "props": "ออร่าหัวใจสีชมพูอ่อน",
        "prompt_en": "holding a big glowing heart with both hands, warm sweet expression, charming character art, no text, no words",
        "color": "#000000",
        "stroke": "#FFFFFF"
    },
    {
        "id": "NOCAP_04",
        "category": "Main & Tab (ไม่มีแคปชั่น)",
        "caption": "[ไม่มีข้อความ - แอ็กชันแอบมองน่ารัก]",
        "pose": "เกาะขอบมอง ชะเง้อหน้าออกมา ตาแป๋วสุดน่ารัก",
        "emotion": "สงสัย ขี้เล่น ไร้เดียงสา",
        "props": "เครื่องหมายคำถามและดอกไม้เล็กๆ",
        "prompt_en": "cute peeking head and shoulders over border, curious big round shining eyes, adorable expression, no text, no words",
        "color": "#000000",
        "stroke": "#FFFFFF"
    }
]

def get_preset_48_stickers(selected_caption_ids=None):
    """
    Get 48 sticker items:
    - 44 items with Thai captions
    - 4 items WITHOUT captions (pure character poses for Main cover, Tab icon, and action stickers)
    """
    if selected_caption_ids and len(selected_caption_ids) >= 44:
        lookup = {it["id"]: it for it in CAPTIONS_DATABASE}
        chosen_44 = [lookup[cid] for cid in selected_caption_ids if cid in lookup][:44]
        if len(chosen_44) < 44:
            remain = [it for it in CAPTIONS_DATABASE if it not in chosen_44]
            chosen_44.extend(random.sample(remain, 44 - len(chosen_44)))
    else:
        chosen_44 = random.sample(CAPTIONS_DATABASE, 44)

    return {
        "caption_stickers": chosen_44,     # 44 stickers with captions
        "no_caption_poses": list(NO_CAPTION_POSES) # 4 stickers without captions
    }

# Backward compatibility alias
def get_preset_42_stickers(selected_ids=None):
    p48 = get_preset_48_stickers(selected_ids)
    return {
        "main": p48["no_caption_poses"][0],
        "tab": p48["no_caption_poses"][1],
        "stickers": p48["caption_stickers"][:40]
    }

COMMON_MODIFIERS_AND_PARTICLES = [
    # คำสร้อย/คำลงท้าย/คำบอกน้ำเสียง/คำขยาย
    'นะครับ', 'นะคะ', 'นะจ๊ะ', 'ด้วยนะ', 'ด้วยครับ', 'ด้วยค่ะ', 'ก่อนนะ',
    'แป๊บนึง', 'แป๊บนะ', 'จังเลย', 'มากเลย', 'มากๆ', 'ที่สุด', 'กันเถอะ',
    'จนใจเจ็บ', 'ก้นบึ้งหัวใจ', 'ทุกสิ่ง', 'ทุกวัน', 'แท้ๆ', 'แท้', 'ไปเลย',
    'วันอาทิตย์', 'วันจันทร์', 'วันอังคาร', 'วันพุธ', 'วันพฤหัส', 'วันศุกร์', 'วันเสาร์',
    'กริบ', 'จ้า', 'จ้ะ', 'ค่ะ', 'ครับ', 'อ่ะ', 'เนอะ', 'น้า', 'หน่อย',
    'เสมอ', 'แล้ว', 'เลย', 'มาก', 'จัง', 'ดิ', 'เหรอ', 'ไหม', 'มั้ย', 'สิ', 'นะ', 'มั้ง', 'ปะเนี่ย'
]


def analyze_typography_hierarchy(caption: str) -> dict:
    """
    วิเคราะห์ลำดับความสำคัญของข้อความ (Visual Hierarchy & Word Emphasis):
    - แยกคำหลักเด่น (Hero Word / Action / Emotion) ให้ตัวใหญ่เด่น (130-150%)
    - แยกคำขยาย/คำลงท้าย (Subtext / Particle / Modifier) ให้ตัวเล็กกะทัดรัด (70-80%)
    - ป้องกันการตัดผ่ากลางคำหรือแยกพยางค์ 100%
    """
    caption = caption.strip()
    if not caption:
        return {
            "has_hierarchy": False,
            "hero_word": "",
            "hero_size": "100% UNIFORM STANDARD FONT",
            "sub_word": "",
            "sub_size": "",
            "lines": [caption],
            "layout_description": "Single uniform line"
        }

    # 1. กรณีมีช่องว่างธรรมชาติ (เช่น 'เนื้อย่าง เยียวยาทุกสิ่ง')
    if ' ' in caption:
        parts = [p.strip() for p in caption.split(' ') if p.strip()]
        if len(parts) >= 2:
            hero = parts[0]
            sub = ' '.join(parts[1:])
            return {
                "has_hierarchy": True,
                "hero_word": hero,
                "hero_size": "130-150% LARGE DOMINANT FONT",
                "sub_word": sub,
                "sub_size": "70-80% COMPACT SUBTEXT FONT",
                "lines": [hero, sub],
                "layout_description": f"Line 1 (HERO, BIG 140%): '{hero}' | Line 2 (SUB, SMALL 75%): '{sub}' (or inline size contrast with '{hero}' dominating)"
            }

    # 2. กรณีลงท้ายด้วยคำสร้อย คำลงท้าย หรือคำขยายที่พบบ่อย (เช่น 'เงียบกริบ', 'รับทราบค่ะ', 'พร้อมเปย์เสมอ')
    for p in sorted(COMMON_MODIFIERS_AND_PARTICLES, key=len, reverse=True):
        if caption.endswith(p) and len(caption) > len(p):
            hero = caption[:-len(p)].strip()
            sub = p.strip()
            # ตรวจสอบความปลอดภัยทางไวยากรณ์: hero ต้องไม่ทิ้งสระหน้าลอย และ sub ต้องไม่ตัดสระบน/ล่าง/วรรณยุกต์
            if len(hero) >= 2 and hero[-1] not in 'เแโใไ' and sub[0] not in '่้๊๋์ฯๆะัิีึืุู':
                return {
                    "has_hierarchy": True,
                    "hero_word": hero,
                    "hero_size": "130-150% LARGE DOMINANT FONT",
                    "sub_word": sub,
                    "sub_size": "70-80% COMPACT SUBTEXT FONT",
                    "lines": [hero, sub],
                    "layout_description": f"Line 1 (HERO, BIG 140%): '{hero}' | Line 2 (SUB, SMALL 75%): '{sub}' (or inline size contrast with '{hero}' dominating)"
                }

    # 3. ถ้าข้อความยาวเกิน 11 ตัวอักษร ให้ใช้ pythainlp ตัดคำตามหลักภาษาศาสตร์
    try:
        from pythainlp import word_tokenize
        tokens = word_tokenize(caption, engine='newmm')
    except Exception:
        tokens = [caption]

    merged = []
    for t in tokens:
        if merged and (len(t) == 1 and t in "่้๊๋์ฯๆะัิีึืุู"):
            merged[-1] += t
        else:
            merged.append(t)
    tokens = merged

    if len(tokens) >= 2 and sum(len(t) for t in tokens) > 11:
        total_len = sum(len(t) for t in tokens)
        best_split = 1
        min_diff = float('inf')
        cum_len = 0
        for i in range(len(tokens) - 1):
            cum_len += len(tokens[i])
            rest_len = total_len - cum_len
            diff = abs(cum_len - rest_len)
            if diff < min_diff:
                min_diff = diff
                best_split = i + 1
        line1 = "".join(tokens[:best_split]).strip()
        line2 = "".join(tokens[best_split:]).strip()
        if line1 and line2 and line1[-1] not in 'เแโใไ' and line2[0] not in '่้๊๋์ฯๆะัิีึืุู':
            return {
                "has_hierarchy": True,
                "hero_word": line1,
                "hero_size": "120-130% PROMINENT FONT",
                "sub_word": line2,
                "sub_size": "80-90% SECONDARY FONT",
                "lines": [line1, line2],
                "layout_description": f"Line 1 (PROMINENT): '{line1}' | Line 2: '{line2}' (Stacked balanced layout)"
            }

    # ข้อความเดี่ยวหรือคำสั้นที่ไม่มีคำขยาย ให้ใช้ขนาดมาตรฐาน 1 บรรทัด
    return {
        "has_hierarchy": False,
        "hero_word": caption,
        "hero_size": "100% UNIFORM STANDARD FONT",
        "sub_word": "",
        "sub_size": "",
        "lines": [caption],
        "layout_description": f"Single uniform horizontal line: '{caption}'"
    }


def suggest_thai_stacked_lines(caption: str) -> list:
    """
    แบ่งคำในแคปชั่นภาษาไทยออกเป็น 1-2 บรรทัดโดยยึดตามหลักไวยากรณ์และความหมายของคำ 100%
    พร้อมคำนึงถึงลำดับความสำคัญของคำ (Visual Hierarchy)
    """
    hierarchy = analyze_typography_hierarchy(caption)
    return hierarchy.get("lines", [caption])


TEXT_LAYOUT_STYLES = {
    "Corner Straight": {
        "name_th": "มุมบนซ้ายจัดเรียงแนวนอน (Top-Left Straight)",
        "prompt_template": 'Single unified text block placed cleanly in top-left open negative space. Horizontal 1-2 stacked lines with hero word "[BIG_WORD]" dominant. 100% visible, no overlap.'
    },
    "Left-Right": {
        "name_th": "ตัวละครฝั่งขวา ตัวหนังสือฝั่งซ้าย (Left-Right Framing)",
        "prompt_template": 'Character framed on right half, single unified text block placed in open left half. Horizontal stacked lines with hero word "[BIG_WORD]" prominent.'
    },
    "Right-Left": {
        "name_th": "ตัวละครฝั่งซ้าย ตัวหนังสือฝั่งขวา (Right-Left Framing)",
        "prompt_template": 'Character framed on left half, single unified text block placed in open right half. Horizontal stacked lines with hero word "[BIG_WORD]" prominent.'
    },
    "Speech Bubble": {
        "name_th": "บอลลูนคำพูดน่ารัก (Cute Speech Bubble)",
        "prompt_template": 'Single cute speech bubble floating in open negative space above character. Text neatly formatted inside horizontally with hero word "[BIG_WORD]" bold.'
    },
    "Cute Badge": {
        "name_th": "ป้ายป๊อปการ์ตูน (Pop-Art Badge)",
        "prompt_template": 'Single unified pop-art badge in open upper space containing horizontal text with hero word "[BIG_WORD]" prominent, safe margin from edges.'
    },
    "Ribbon Banner": {
        "name_th": "ริบบิ้นแนวนอนน่ารัก (Cute Horizontal Banner)",
        "prompt_template": 'Single neat horizontal ribbon banner floating in open negative space above character. Text printed straight horizontally with hero word "[BIG_WORD]" bold.'
    },
    "Pop Emblem": {
        "name_th": "ตราป้ายป๊อปกลม (Pop Emblem)",
        "prompt_template": 'Single round pop emblem floating in open upper corner space, containing straight horizontal text with hero word "[BIG_WORD]" bold.'
    },
    "Top Centered": {
        "name_th": "กึ่งกลางด้านบน (Top Centered)",
        "prompt_template": 'Character sitting/crouching in lower half, single unified text block floating centered in upper open space with clear gap above head.'
    },
    "Shadow Pop": {
        "name_th": "เอฟเฟกต์เงาป๊อป 3D (Shadow Pop)",
        "prompt_template": 'Single text block in open negative space with crisp 3D bubble depth, horizontal stacked lines with hero word "[BIG_WORD]" prominent.'
    },
    "Lively Bounce": {
        "name_th": "ตัวอักษรจังหวะน่ารัก (Lively Bounce)",
        "prompt_template": 'Single text block in open negative space with cheerful rhythmic baseline, straight horizontal reading with hero word "[BIG_WORD]" prominent.'
    },
    "Layered Stack": {
        "name_th": "ซ้อนเลเยอร์บน-ล่าง (Layered Stack)",
        "prompt_template": 'Single text block neatly stacked in 2 horizontal lines in open space: Line 1 hero word "[BIG_WORD]" bold 140%, Line 2 subtext compact below.'
    },
    "Comic Starburst": {
        "name_th": "ประกายดาวการ์ตูนป๊อป (Comic Starburst Pop)",
        "prompt_template": 'Single cartoon starburst pop badge floating in open negative space beside character, bold 3D bubble text straight inside.'
    },
    "Heart Accents": {
        "name_th": "ประดับมินิหัวใจ (Heart Accents)",
        "prompt_template": 'Single text block in open negative space accented by cute tiny floating heart doodles, straight horizontal lines with hero word "[BIG_WORD]" prominent.'
    },
    "Glossy Bubble": {
        "name_th": "ฟองสบู่ป่องใส (Glossy Bubble)",
        "prompt_template": 'Single text block in open negative space styled with glossy inflated candy bubble lettering, straight horizontal lines with hero word "[BIG_WORD]" prominent.'
    },
    "Sparkle Accent": {
        "name_th": "ประกายวิ้งค์สดใส (Sparkle Accent)",
        "prompt_template": 'Single text block in open negative space with subtle cute sparkle twinkle accents, straight horizontal lines with hero word "[BIG_WORD]" prominent.'
    },
    "Pop Art Doodles": {
        "name_th": "ป๊อปอาร์ตการ์ตูน (Pop Art Doodles)",
        "prompt_template": 'Single text block in open negative space surrounded by small cute chibi doodles like stars and music notes, straight horizontal lines.'
    },
    "Highlight Focus": {
        "name_th": "เน้นคำเด่นไฮไลต์ (Highlight Focus)",
        "prompt_template": 'Single text block in open space with vibrant contrast highlight on hero word "[BIG_WORD]", straight horizontal lines, zero occlusion.'
    },
    "Compact Stack": {
        "name_th": "บล็อกกะทัดรัดด้านขวา (Compact Right Stack)",
        "prompt_template": 'Single compact text block formatted as 2 short stacked horizontal lines in open right space, hero word "[BIG_WORD]" prominent.'
    },
    "Cloud Bubble": {
        "name_th": "ก้อนเมฆคำพูดน่ารัก (Cute Cloud Bubble)",
        "prompt_template": 'Single fluffy cute cloud thought bubble floating in open space above character, straight horizontal text inside.'
    },
    "Spacious Top": {
        "name_th": "เปิดกว้างด้านบน (Spacious Top)",
        "prompt_template": 'Character in lower half, single wide text block spanning upper negative space with strict 12% padding from all canvas borders.'
    },
}

TEXT_LAYOUT_STYLE_KEYS = list(TEXT_LAYOUT_STYLES.keys())

AVAILABLE_FONT_STYLES = [
    "Glossy 3D puffy bubble pop typography with subtle glossy shine, heavy thick contrasting outline contour border, stacked horizontal lines in open space, zero character occlusion, 100% visible and unblocked in foreground",
    "Bold cute round 3D bubble typography, straight block placement",
    "Handwritten playful kawaii brush script, stacked block placement",
    "Bold clean modern comic display font, block placement"
]

def apply_text_layout_style(style_key: str, caption: str, hero_word: str = "", sub_word: str = "") -> str:
    style_info = TEXT_LAYOUT_STYLES.get(style_key, TEXT_LAYOUT_STYLES.get("Corner Straight", list(TEXT_LAYOUT_STYLES.values())[0]))
    template = style_info["prompt_template"]

    big_word = hero_word.strip() if hero_word else caption.strip()
    small_word = sub_word.strip() if sub_word else ""

    formatted = template.replace("[TEXT]", caption).replace("[BIG_WORD]", big_word)
    if "[SMALL_WORD]" in formatted:
        if small_word:
            formatted = formatted.replace("[SMALL_WORD]", small_word)
        else:
            formatted = formatted.replace(', word "[SMALL_WORD]" smaller below aligned left', '')
            formatted = formatted.replace(', word "[SMALL_WORD]" huge bottom half', '')
            formatted = formatted.replace(', word "[SMALL_WORD]" small offset overlapping bottom right with shadow', '')
            formatted = formatted.replace(', word "[SMALL_WORD]" below vertical', '')
            formatted = formatted.replace('[SMALL_WORD]', '')

    return formatted


def build_line_sticker_prompt_json(
    character_description="Cute cartoon character based on attached image reference",
    font_style="Glossy 3D puffy bubble pop typography with heavy thick white outline border",
    text_color="#000000",
    stroke_color="#FFFFFF",
    selected_items_48=None,
    custom_title_hint="น่ารัก สดใส ใช้งานได้ทุกวัน",
    batch_index=None,
    batch_size=8,
    text_layout_style="DYNAMIC_VARIETY"
):
    """
    Builds the structured prompt containing 48 items in JSON format:
    - 44 items with Thai captions (Items 01 - 44)
    - 4 items WITHOUT captions for Main cover and Tab icon (Items 45 - 48)
    - Supports batch mode: 8 images per batch x 6 batches (batch_index=1..6)
    - Pure magenta background (#FF00FF) for effortless 1-click transparency keying
    - Zero character occlusion rule: Typography placed exclusively in wide open negative space
    """
    if not selected_items_48:
        selected_items_48 = get_preset_48_stickers()

    caption_items = selected_items_48.get("caption_stickers", [])
    if len(caption_items) < 44:
        remain = [it for it in CAPTIONS_DATABASE if it not in caption_items]
        caption_items = (caption_items + random.sample(remain, 44 - len(caption_items)))[:44]

    no_caption_items = selected_items_48.get("no_caption_poses", NO_CAPTION_POSES)

    # Dynamic color mapping for both English and Thai
    color_names_en = {
        "#FFFFFF": "pure-white",
        "#FEF08A": "vibrant bright-yellow",
        "#FFFF00": "vibrant sunny-yellow",
        "#FDE047": "warm canary-yellow",
        "#000000": "solid pitch-black",
        "#2563EB": "vibrant royal-blue",
        "#EC4899": "vibrant hot-pink",
        "#F97316": "vibrant bright-orange",
        "#10B981": "vibrant emerald-green",
        "#8B5CF6": "vibrant deep-purple",
        "#F59E0B": "glossy golden-amber",
    }
    color_names_th = {
        "#FFFFFF": "ขาว",
        "#FEF08A": "เหลืองสดใส",
        "#FFFF00": "เหลืองสว่าง",
        "#FDE047": "เหลืองคานารี",
        "#000000": "ดำสนิท",
        "#2563EB": "น้ำเงินสด",
        "#EC4899": "ชมพูสดใส",
        "#F97316": "ส้มสดใส",
        "#10B981": "เขียวมรกต",
        "#8B5CF6": "ม่วงเข้ม",
        "#F59E0B": "ทองเงางาม",
    }
    stroke_clean = (stroke_color or "#FFFFFF").strip().upper()
    stroke_name_en = color_names_en.get(stroke_clean, f"contrasting {stroke_clean}")
    stroke_name_th = color_names_th.get(stroke_clean, stroke_clean)

    text_clean = (text_color or "#000000").strip().upper()
    text_name_en = color_names_en.get(text_clean, f"solid {text_clean}")
    text_name_th = color_names_th.get(text_clean, text_clean)

    items_payload = []

    # Items 01 to 44 (With Captions)
    for idx, s in enumerate(caption_items, start=1):
        hierarchy_info = analyze_typography_hierarchy(s["caption"])
        lines = hierarchy_info["lines"]
        line_preview = " / ".join(lines)

        # Determine Text Layout Style for this sticker from the 20 styles
        if not text_layout_style or text_layout_style == "DYNAMIC_VARIETY":
            # Automatically cycle through all 20 text placement styles
            style_key = TEXT_LAYOUT_STYLE_KEYS[(idx - 1) % len(TEXT_LAYOUT_STYLE_KEYS)]
        else:
            style_key = text_layout_style if text_layout_style in TEXT_LAYOUT_STYLES else "Speech Bubble"

        style_meta = TEXT_LAYOUT_STYLES[style_key]
        layout_prompt = apply_text_layout_style(
            style_key=style_key,
            caption=s["caption"],
            hero_word=hierarchy_info.get("hero_word", ""),
            sub_word=hierarchy_info.get("sub_word", "")
        )

        # Orthography Safeguards: Provide pure positive geometric anatomical instructions for AI typography
        # Avoid reverse-priming negative tokens (e.g. avoid mentioning forbidden letters like ซ or ฃ which diffusion attention inadvertently renders)
        glyph_warnings = []
        cap_text = s["caption"]
        if "ข" in cap_text:
            glyph_warnings.append(
                "CRITICAL THAI UNICODE U+0E02 (ข, THAI CHARACTER KHO KHAI): "
                "The head loop must be a continuous single smooth circle with zero notch, zero indentation, zero crease. "
                "Smooth circle head only!"
            )
        if "ช" in cap_text:
            glyph_warnings.append(
                "CRITICAL THAI UNICODE U+0E0A (ช, THAI CHARACTER CHO CHANG): "
                f"In caption '{cap_text}', consonant 'ช' (U+0E0A) begins with a 100% perfectly smooth unbroken circular starting head loop (identical circular head to 'ข' U+0E02) with an upward-swept tail. "
                "The head loop is a seamless, continuous, smooth circular ring with zero notch and zero crease. Clean modern Thai round-head typography!"
            )
        if "ค" in cap_text:
            glyph_warnings.append(
                "CRITICAL THAI UNICODE U+0E04 (ค, THAI CHARACTER KHO KHWAI): "
                "Head must be a smooth outward circular loop."
            )
        if "ด" in cap_text:
            glyph_warnings.append(
                "CRITICAL THAI UNICODE U+0E14 (ด, THAI CHARACTER DO DEK): "
                "Smooth rounded arch head with inward circular loop."
            )
        glyph_note_en = (" Typography Unicode Safeguard: " + " ".join(glyph_warnings)) if glyph_warnings else ""

        consistency_suffix = (
            "Same Character identity from reference image (face features, hairstyle, clothing style, colors). "
            "DYNAMIC EXPRESSIONS & POSES: Highly expressive facial emotions (eyes, eyebrows, mouth) and active, animated body gestures matching the Thai caption. Do NOT make the character stiff, static, or repetitive! "
            "Clean borderless 2D illustration directly on a flat uniform solid magenta (#FF00FF) background. "
            "ABSOLUTELY NO white die-cut border, NO white outline, NO sticker contour around character body, hair, clothing, or props. "
            "Zero shadows. No magenta in character."
        )
        action_prompt = (
            f"Vibrant expressive sticker pose matching '{s['caption']}': {s['prompt_en']}. "
            f"Active dynamic body language, exaggerated cute anime emotion, natural props. "
            f"Composition: {layout_prompt}. Single text instance only (do NOT duplicate text). "
            f"ABSOLUTELY NO English words, NO 'Sticker' text, NO item numbers or labels on canvas.{glyph_note_en} {consistency_suffix}"
        )

        if len(lines) == 1:
            layout_desc = f"Horizontal text formatted strictly as 1 single line: '{lines[0]}'."
        else:
            layout_desc = (
                f"Horizontal text formatted strictly as 2 stacked lines: "
                f"Line 1 (HERO WORD, BIGGER 140%): '{lines[0]}' / "
                f"Line 2 (SUBTEXT, SMALLER 75%): '{lines[1]}' "
                f"(or inline size contrast with '{lines[0]}' distinctly dominating)."
            )

        item_typography = {
            "has_text": True,
            "single_text_instance_rule": "MANDATORY: Render this exact Thai caption strictly ONCE on the entire canvas. Absolutely NO duplicate text, NO repeating at both top and bottom.",
            "text_content": s["caption"],
            "text_placement_style": style_key,
            "text_placement_instruction": layout_prompt,
            "visual_hierarchy": {
                "has_hierarchy": hierarchy_info["has_hierarchy"],
                "hero_keyword": hierarchy_info["hero_word"],
                "hero_font_scale": hierarchy_info["hero_size"],
                "supporting_subtext": hierarchy_info["sub_word"],
                "supporting_font_scale": hierarchy_info["sub_size"],
                "hierarchy_instruction": hierarchy_info["layout_description"]
            },
            "text_fill_color": f"Solid glossy {text_name_en} ({text_clean}) with 3D puffy bubble depth and subtle highlight",
            "stroke_color": f"Heavy thick bold {stroke_name_en} outline border ({stroke_clean}) applied EXCLUSIVELY to Thai letters (STRICTLY FORBIDDEN on character body)",
            "layout": f"{layout_desc} NEVER break or split words mid-syllable across lines. Render caption ONCE in single unified block.",
            "spelling_instruction": f"Render exact Thai caption '{s['caption']}' verbatim with zero spelling mistakes, zero repeated characters, zero hallucinated vowels.{glyph_note_en}"
        }
        if glyph_warnings:
            item_typography["glyph_orthography_safeguards"] = glyph_warnings

        items_payload.append({
            "sticker_number": idx,
            "type": "sticker_with_caption",
            "thai_caption": s["caption"],
            "single_caption_rule": "MANDATORY: Print the Thai caption strictly ONCE on the image canvas. DO NOT duplicate text.",
            "canvas_elements_rule": "Render ONLY the character illustration and the single Thai caption. ABSOLUTELY FORBIDDEN: DO NOT render any English words, titles, labels, or numbers onto the canvas. The only text permitted anywhere on the entire image canvas is the specified Thai caption.",
            "suggested_horizontal_lines": lines,
            "text_layout_style": {
                "style_key": style_key,
                "placement_rule": layout_prompt
            },
            "character_framing": "Sized to fit comfortably in frame with at least 12% pure magenta padding from frame edges. Borderless illustration directly on magenta (STRICTLY NO white die-cut border around character).",
            "pose_and_emotion": s["pose"] + " (" + s["emotion"] + ")",
            "props_and_visuals": s["props"],
            "english_action_prompt": action_prompt,
            "consistency_rule": consistency_suffix,
            "typography": item_typography
        })

    # Items 45 to 48 (NO Captions - For Main, Tab, and Action Stickers)
    for idx, s in enumerate(no_caption_items, start=45):
        slot_role = "Main Cover & Action" if idx == 45 else ("Tab Icon & Action" if idx == 46 else "Special Action Sticker")
        items_payload.append({
            "sticker_number": idx,
            "type": "pure_character_pose_no_text",
            "recommended_usage": slot_role,
            "thai_caption": "NONE (ไม่มีข้อความตัวอักษร)",
            "canvas_elements_rule": "Render ONLY the character illustration. ABSOLUTELY FORBIDDEN: DO NOT render any English words, letters, labels, or numbers onto the image canvas. Pure character illustration only.",
            "character_framing": "Character centered in frame, sized to fill 75-80% height with a strict 12% safe margin from all outer borders (NEVER touch frame edges). Borderless illustration directly on magenta (STRICTLY NO white die-cut border around character).",
            "pose_and_emotion": s["pose"] + " (" + s["emotion"] + ")",
            "props_and_visuals": s["props"],
            "english_action_prompt": f"{s['prompt_en']}, 12% safe margin from canvas borders, clean magenta background. ABSOLUTELY NO words, NO labels, NO numbers on canvas. {consistency_suffix}",
            "consistency_rule": consistency_suffix,
            "typography": {
                "has_text": False,
                "note": "STRICTLY NO TEXT, NO LETTERS, NO WORDS. Pure character illustration only."
            }
        })

    if batch_index is not None and 1 <= batch_index <= 6:
        start_idx = (batch_index - 1) * batch_size
        end_idx = min(batch_index * batch_size, len(items_payload))
        selected_batch_items = items_payload[start_idx:end_idx]
        start_num = start_idx + 1
        end_num = end_idx

        payload = {
            "project": f"LINE Sticker 48 Set Generator - Batch {batch_index}/6 (Images {start_num:02d} to {end_num:02d})",
            "batch_information": {
                "current_batch": batch_index,
                "total_batches": 6,
                "batch_size": len(selected_batch_items),
                "image_range": f"Images {start_num:02d} - {end_num:02d}",
                "instruction": f"Generate ONLY Images {start_num:02d} through {end_num:02d} ({len(selected_batch_items)} images) in this single run. Generate strictly 1 master image per item (NO duplicate or alternative versions). Do not generate other batches now."
            },
            "canvas_rules": {
                "aspect_ratio": "1:1 Square (perfect square canvas, equal width and height, strictly NOT vertical 9:16 and NOT horizontal 16:9).",
                "do_not_render_labels": "CRITICAL: Absolutely DO NOT paint any English words, sequence numbers, labels, 'Sticker', 'Sticker 01', 'Item', or '01' on the image canvas. The canvas must contain ONLY the character illustration and the single Thai caption.",
                "single_text_instance": "CRITICAL: Render the Thai caption strictly ONCE per image. Absolutely DO NOT duplicate text at both top and bottom.",
                "no_character_outline": f"CRITICAL: The character illustration MUST NOT have any white or colored sticker outline, die-cut silhouette border, or glow around the character body, hair, clothes, limbs, or props. The character drawing must be rendered cleanly with normal illustration lineart directly placed onto the pure magenta background (#FF00FF). The {stroke_name_en} outline contour stroke is applied EXCLUSIVELY to the Thai typography letters, NEVER to the character body.",
                "background": "Solid pure magenta background (#FF00FF, RGB 255, 0, 255, chroma key fuchsia), absolutely flat single color, zero shadows, zero gradients, zero noise, high contrast against character edges for perfect 1-click transparency keying.",
                "single_version_per_item": "Generate strictly ONE single image per item. Do NOT generate alternative or backup versions."
            },
            "character_consistency": {
                "reference": "Strictly preserve the character identity, facial design, hairstyle, and outfit from the reference image, BUT grant MAXIMUM CREATIVE FREEDOM for dynamic poses and dramatic facial expressions matching each sticker's context.",
                "character_description": character_description,
                "dynamic_poses_and_acting": "MANDATORY DRAMATIC EXPRESSIONS & ACTIVE POSES: Absolutely DO NOT keep the character static or merely tilted! Change the whole body pose, arm gestures, hand signs, jumping/sitting/running actions, and exaggerated facial emotions (tears, laugh, shock, heart eyes, energetic grin, shy blush) to perfectly act out each Thai caption. Every sticker must feel like a unique lively mini-scene."
            },
            "typography_rules": {
                "style": f"{font_style}: Japanese-LINE-sticker typography with solid {text_name_en} inner fill ({text_clean}) and an ultra-thick bold {stroke_name_en} outer contour stroke border ({stroke_clean}) for maximum legibility and pop against the background.",
                "word_emphasis_and_hierarchy": {
                    "rule": "DYNAMIC FONT SIZING & WORD EMPHASIS: Create authentic, high-impact LINE Creators Market typography by emphasizing the primary hero keyword. In captions with multiple words or ending particles (e.g., 'เงียบกริบ', 'รับทราบค่ะ', 'พร้อมเปย์เสมอ'), render the primary action/emotion keyword in a noticeably LARGER, bolder font (130-150% scale), while rendering supporting particles, modifiers, or subtext in a smaller, compact font (70-80% scale). The smaller word may sit on Line 2 directly underneath or inline beside the hero word, giving the sticker vibrant commercial appeal and instant readability.",
                    "example_positive": "For 'เงียบกริบ': Line 1 'เงียบ' (HUGE 140% BUBBLE FONT), Line 2 'กริบ' (SMALLER 75% SUBTEXT underneath) - or inline size contrast. For 'รับทราบค่ะ': 'รับทราบ' (LARGE) + 'ค่ะ' (SMALL COMPACT).",
                    "example_forbidden": "DO NOT make all words flat and uniformly same-sized if there is an obvious hero keyword, and NEVER split words mid-syllable."
                },
                "thai_word_breaking_rules": "CRITICAL ZERO SYLLABLE SPLITTING: NEVER split a Thai word mid-syllable or separate a leading/trailing vowel (เ, แ, โ, ใ, ไ, ะ, า) or tone mark (่, ้, ๊, ๋, ์) onto another line. If suggested_horizontal_lines has 1 line, render it on exactly ONE horizontal line. If it has 2 lines, break ONLY at the natural word boundary specified in suggested_horizontal_lines. NEVER wrap or break letters mid-word (FORBIDDEN: 'รับทร/าบค่ะ', 'พร้อมเ/ปย์เสมอ', 'สวัสดีวั/นอาทิตย์', 'คิดถึงจ/นใจเจ็บ').",
                "visual_layering": "CRITICAL ZERO OCCLUSION: Text MUST be placed strictly in OPEN NEGATIVE SPACE and 100% UNOBSCURED. The character MUST NEVER stand in front of the text or hide any part of the text behind its head, body, or props. Text must NEVER cover or overlap the character's face, hair, or eyes. Face, hair, and eyes must remain 100% visible and unobstructed.",
                "text_fill_color": f"Solid {text_name_en} ({text_clean}). STRICTLY {text_name_en} inside every Thai character. NO other fill colors permitted.",
                "outline_border": f"Heavy thick bold {stroke_name_en} outline border ({stroke_clean}) applied ONLY to the Thai text characters for legibility (STRICTLY DO NOT put outline or border around the character).",
                "composition_and_placement": {
                    "aspect_ratio": "Strict 1:1 square canvas (width == height). Absolutely NO vertical 9:16 or widescreen 16:9 orientation.",
                    "dynamic_asymmetrical_framing": "The character MUST NOT always be in the dead center. Use asymmetrical framing (Rule of Thirds): position character either on the left half (X: 15-45%), on the right half (X: 55-85%), or in a compact sitting/crouching pose in the lower 45% of the frame. This intentionally creates an expansive, vacant negative space on the opposite side specifically dedicated to hosting the stacked typography cleanly without crowding.",
                    "text_layout_rules": "Text is formatted into 1 to 2 short horizontal stacked lines (like a neat text bubble or paragraph). The text block sits entirely inside the open negative space beside or above the character, with a distinct clear gap separating character and text. No words are bent along a curve or split into vertical columns.",
                    "strict_safe_margin_rule": "CRITICAL: Character and text MUST NEVER TOUCH OR BE FLUSH AGAINST ANY CANVAS EDGE. Always maintain at least 12-15% pure magenta (#FF00FF) padding/margin around all 4 sides (top, bottom, left, right). Do not bleed or crop off character limbs, hair, or text outline.",
                    "strictly_forbidden_elements": [
                        "FORBIDDEN: Drawing the words 'Sticker', 'Item', or any numbers/labels (e.g. 'Sticker 01', 'Sticker 06', 'Item 27', '01') anywhere on the canvas",
                        "FORBIDDEN: Drawing any English text, sequence tags, or title badges on the image",
                        "FORBIDDEN: Duplicating the Thai text (e.g. printing it at both top and bottom)",
                        "FORBIDDEN: Drawing a white sticker die-cut border, white outline, or silhouette contour around character body, hair, clothes, limbs, furniture, or props",
                        "FORBIDDEN: Generating multiple images or 'safe alternative versions' for a single item (strictly generate 1 master image per item)",
                        "FORBIDDEN: Splitting Thai words mid-syllable or separating vowels/tone marks across lines",
                        "FORBIDDEN: Text placed directly over the character's head, face, hair, or body (occlusion)",
                        "FORBIDDEN: Canvas aspect ratio other than 1:1 square (FORBIDDEN: vertical portrait 9:16 or horizontal landscape 16:9)"
                    ]
                },
                "thai_glyph_anatomy_rules": {
                    "rule_khor_khai_smooth_head": "CRITICAL FOR 'ข' (UNICODE U+0E02): The consonant 'ข' MUST have a perfectly smooth, continuous circular head loop with zero indentation and zero crease. Modern Thai smooth circular loop head.",
                    "rule_chor_chang_smooth_head": "CRITICAL GEOMETRIC ANATOMY FOR 'ช' (UNICODE U+0E0A, CHO CHANG): The consonant 'ช' (U+0E0A) MUST begin with a 100% completely smooth, continuous, round circular head loop (identical circular head to 'ข' U+0E02), followed by a bottom curve and an upward tail on the right. The circular head loop is a single seamless unbroken ring with zero notch and zero crease in modern Thai typography.",
                    "rule_do_dek_smooth_head": "The letter 'ด' (U+0E14) has a smooth arched head with an inward circular loop.",
                    "rule_3d_bubble_loops": "Do not let 3D bubble highlights or shadows mimic notches or creases on letter heads. All circular heads must remain distinctly smooth, unbroken, and clean."
                },
                "spelling_accuracy": "Strict verbatim reproduction of Thai captions. Thai vowels, tone marks (วรรณยุกต์), and consonants must be perfectly formed and attached.",
                "rule_caption_items": f"Bold horizontal stacked Thai typography ({font_style}) with solid {text_name_en} fill ({text_clean}), thick {stroke_name_en} border ({stroke_clean}), and dynamic hero word sizing placed in open space above or beside character with ZERO occlusion. Character has no body outline.",
                "rule_no_caption_items": "STRICTLY NO TEXT! Pure character illustrations with zero words or letters, and zero body outlines."
            },
            f"sticker_items_batch_{batch_index}": selected_batch_items
        }

        json_str = json.dumps(payload, ensure_ascii=False, indent=2)

        prompt_text = (
            f"กรุณาสร้างชุดสติกเกอร์ LINE [ชุดที่ {batch_index}/6: รายการที่ {start_num:02d} - {end_num:02d}] จำนวน {len(selected_batch_items)} รูป (จากชุดเต็ม 48 รูป) "
            f"สไตล์ฟอนต์: {font_style} (สีข้อความ: {text_name_th} {text_clean}, สีขอบ: {stroke_name_th} {stroke_clean}) "
            f"โดยรักษาเอกลักษณ์ตัวละคร ลายเส้น เสื้อผ้า และสีสันให้ตรงกับรูปต้นแบบที่แนบอย่างเคร่งครัด 100%\n\n"
            f"=== 🛑 กฎเหล็กข้อห้ามเด็ดขาด 5 ประการ (CRITICAL MUST-FOLLOW RULES) ===\n"
            f"1. 🛑 ห้ามมีคำว่า 'Sticker', 'Item', ตัวหนังสือภาษาอังกฤษ หรือหมายเลขลำดับติดในภาพเด็ดขาด (ABSOLUTELY NO 'Sticker' OR 'Item' LABELS, ENGLISH WORDS, OR NUMBERS):\n"
            f"   - ห้ามพิมพ์คำว่า 'Sticker', 'Sticker 01', 'Sticker 06', 'Item', 'Item 27', '01' หรือตัวเลขกำกับลำดับใดๆ ลงบนผืนผ้าใบภาพเด็ดขาด 100%! ห้ามมีตัวหนังสือภาษาอังกฤษทุกชนิดในภาพ!\n"
            f"   - ผืนผ้าใบต้องมีเฉพาะ 'ตัวหนังสือภาษาไทยที่ระบุ' และ 'ภาพวาดตัวละคร' เท่านั้น ห้ามใส่ Title, Label, ป้ายชื่อสติกเกอร์ หรือ Metadata ใดๆ ลงในรูปภาพเด็ดขาด\n\n"
            f"2. 🛑 ห้ามพิมพ์ข้อความซ้ำซ้อนในภาพเดียวกันเด็ดขาด (SINGLE TEXT INSTANCE ONLY):\n"
            f"   - ข้อความภาษาไทยต้องปรากฏเพียง 'จุดเดียว ครั้งเดียว' ต่อ 1 รูปภาพเท่านั้น!\n"
            f"   - ห้ามพิมพ์ข้อความซ้ำทั้งข้างบนและข้างล่าง ห้ามใส่ข้อความเบิ้ล 2 ที่ในรูปเดียวกันเด็ดขาด ให้เลือกวางในพื้นที่ว่างจุดเดียวตามความเหมาะสม\n\n"
            f"3. 🛑 ห้ามมีขอบขาวรอบตัวละครและสิ่งของเด็ดขาด (STRICTLY NO WHITE DIE-CUT BORDER AROUND CHARACTER):\n"
            f"   - ห้ามวาดเส้นขอบขาว (White Die-Cut Contour / Sticker Silhouette Border / White Halo) ล้อมรอบตัวละคร เส้นผม เสื้อผ้า แขน ขา เก้าอี้ พร็อพ หรือสิ่งของเด็ดขาด!\n"
            f"   - ตัวละครและสิ่งของต้องเป็นภาพวาดประกอบ 2D สไตล์อนิเมะ ลายเส้นปกติ วาดสัมผัสแนบกับพื้นหลังสีชมพู (#FF00FF) โดยตรง 100% ไม่มีขอบขาวรอบตัว\n"
            f"   - เส้นขอบสี{stroke_name_th}หนา ({stroke_clean}) อนุญาตให้ใส่ได้ 'เฉพาะที่ตัวหนังสือภาษาไทยเท่านั้น' เพื่อให้อ่านง่าย ห้ามมีขอบขาวที่ตัวละครเด็ดขาด\n\n"
            f"4. 🛑 กฎลักษณะพยัญชนะ 'ช' (Unicode U+0E0A) และ 'ข' (Unicode U+0E02) หัวกลมมนเรียบเนียน 100% (MANDATORY SMOOTH CIRCULAR HEAD LOOPS):\n"
            f"   - หัวของพยัญชนะ 'ช' (Unicode U+0E0A: ช.ช้าง) ทุกคำ (เช่น ธรรมชาติ, เช็ค, ชวน, ชิล, ชอบ, ใช่, ชื่นใจ, ชาร์จ, ช่วย) ต้องเป็น 'ห่วงวงกลมกลมเกลี้ยงเรียบเนียน 100% ชิ้นเดียวต่อเนื่อง' โครงสร้างตัวอักษรเหมือน ข.ไข่ (U+0E02) ที่มีหางตวัดขึ้นทางขวา เส้นรอบหัวต้องโค้งมนสม่ำเสมอ ไร้รอยบาก ไร้รอยหยัก ไร้รอยพับใดๆ ทั้งสิ้น\n"
            f"   - หัวของพยัญชนะ 'ข' (Unicode U+0E02: ข.ไข่) ทุกคำ (เช่น ขอ, ขอบคุณ, เข้าใจ, ข้าว) ต้องเป็น 'ห่วงวงกลมกลมเกลี้ยง 100%' เส้นโค้งมนเรียบระดับเวกเตอร์โมเดิร์นฟอนต์\n\n"
            f"5. 🛑 สร้างเพียง 1 รูปภาพต่อ 1 รายการเท่านั้น (ห้ามสร้าง 2 เวอร์ชั่น หรือเวอร์ชันสำรองปลอดภัย):\n"
            f"   - ในแต่ละรายการ ให้สร้างเฉพาะภาพหลักภาพเดียวที่สมบูรณ์แบบเท่านั้น ห้ามสร้างภาพซ้ำสอง หรือสร้าง 'เวอร์ชันสำรองปลอดภัย' (Safe Alternative Version) ออกมาคู่กัน\n"
            f"   - เนื้อหาและพร็อพทั้งหมดเป็นแนว Chibi น่ารัก สดใส ไร้ความรุนแรง ปลอดภัย 100%\n\n"
            f"6. 🌟 ท่าทางและอารมณ์ต้องมีมิติหลากหลายตามแคปชั่น (DRAMATIC EXPRESSIONS & ACTIVE POSES):\n"
            f"   - ห้ามใช้ท่าเดิมแล้วแค่เอียงตัวเล็กน้อยเด็ดขาด! ให้เปลี่ยนท่าทางของทั้งตัว ท่าทางมือ แขน ขา การเคลื่อนไหว (วิ่ง, นั่ง, กระโดด, กอด, กุมขมับ, ชูนิ้ว)\n"
            f"   - สีหน้าและแววตาต้องแสดงอารมณ์แบบการ์ตูนญี่ปุ่นอย่างชัดเจน (ยิ้มกว้าง, หัวเราะลั่น, ร้องไห้กระซิก, ตกใจตาโต, ตาเป็นประกายหัวใจ, เขินแก้มแดง) ให้เข้ากับความหมายของแคปชั่นแต่ละรูป 100%\n\n"
            f"=== ข้อกำหนดด้านสัดส่วนและองค์ประกอบ ===\n"
            f"- สัดส่วนภาพสี่เหลี่ยมจัตุรัส 1:1 เท่านั้น (Square Canvas 1:1 Aspect Ratio): ความกว้างเท่ากับความสูง 100% ห้ามวาดเป็นแนวตั้ง 9:16 หรือแนวนอน 16:9 เด็ดขาด\n"
            f"- พื้นหลังสีชมพูมาเจนต้าล้วน (#FF00FF, Chroma Key Magenta): สะอาดตา เรียบสนิท ไม่มีเงา ไม่มีเกรเดียนท์\n"
            f"- ห้ามตัดคำหรือแยกพยางค์ข้ามบรรทัดเด็ดขาด (Zero Syllable Splitting): คำภาษาไทยต้องสมบูรณ์ 100% ในแต่ละบรรทัด ห้ามผ่ากลางคำเด็ดขาด\n"
            f"- ห้ามข้อความทับหรือบังหน้าตัวละครเด็ดขาด (Zero Face/Head Occlusion): ตัวหนังสือต้องอยู่บน 'พื้นที่ว่าง' (Negative Space) เท่านั้น ใบหน้า ตา รอยยิ้ม ต้องเปิดโล่ง 100%\n"
            f"- ห้ามตัวละครและตัวหนังสือชิดขอบภาพเด็ดขาด (Strict Safe Margin): เว้นระยะปลอดภัยอย่างน้อย 12-15% จากขอบทั้ง 4 ด้าน\n\n"
            f"```json\n{json_str}\n```\n\n"
            f"⚠️ กฎการสร้างชุดนี้ (CRITICAL BATCH INSTRUCTION):\n"
            f"กรุณาสร้างรูปภาพชุดนี้จำนวน {len(selected_batch_items)} รูปเท่านั้น (เฉพาะรายการที่ {start_num:02d} ถึง {end_num:02d}) ตามรายละเอียดใน JSON ด้านบนให้ครบถ้วนทุกรูปบนสัดส่วนสี่เหลี่ยมจัตุรัส 1:1 สร้างเพียง 1 รูปต่อรายการ (ห้ามมีเวอร์ชันสำรอง)\n\n"
        )
        if batch_index == 6:
            prompt_text += (
                f"สำคัญมาก: ในชุดสติกเกอร์ชุดสุดท้ายนี้ ให้วิเคราะห์คาแรคเตอร์แล้วส่งข้อมูลสำหรับลงทะเบียน LINE Creators Market ตอบกลับมาในแชตนี้ทันที:\n"
                f"- 🛑 ห้ามระบุจำนวนตัวเลขสติกเกอร์ (เช่น ห้ามใส่คำว่า '48 รูป', '48 ท่า', '48 อารมณ์', '48 stickers') ลงในชื่อชุดหรือคำอธิบายเด็ดขาด เพื่อความยืดหยุ่นในการคัดเลือกภาพ\n"
                f"- 🛑 ให้ตอบกลับเฉพาะบล็อกข้อมูลด้านล่างนี้เท่านั้น ปิดท้ายด้วยเครื่องหมาย ##### ทันที และห้ามพิมพ์ข้อความสรุปหรือข้อความสนทนาใดๆ ต่อท้ายเครื่องหมาย ##### เด็ดขาด:\n\n"
                f"=== ข้อมูลสำหรับลงทะเบียน LINE Creators Market ===\n"
                f"ชื่อชุดสติกเกอร์ (ไทย): [ชื่อชุดภาษาไทยที่ดึงดูด น่ารัก จำง่าย โดยไม่มีการระบุตัวเลขจำนวนภาพ]\n"
                f"ชื่อชุดสติกเกอร์ (อังกฤษ): [English Title without any number count]\n"
                f"คำอธิบายสติกเกอร์ (ไทย): [คำอธิบายชุดสติกเกอร์ภาษาไทยความยาวไม่เกิน 500 ตัวอักษร สื่ออารมณ์น่ารักใช้งานง่าย โดยไม่ระบุตัวเลขจำนวนภาพ]\n"
                f"คำอธิบายสติกเกอร์ (อังกฤษ): [English description expressing daily cute emotions for chatting without any number count]\n"
                f"#####\n"
            )
        else:
            prompt_text += (
                f"หมายเหตุ: รักษาความต่อเนื่องของเอกลักษณ์ตัวละคร ลายเส้น สไตล์ และสัดส่วนสี่เหลี่ยมจัตุรัส 1:1 ตามชุดก่อนหน้าอย่างสมบูรณ์แบบ\n"
            )
    else:
        payload = {
            "project": "LINE Sticker 48 Set Generator (44 Captions + 4 No-Caption Poses)",
            "canvas_rules": {
                "aspect_ratio": "1:1 Square (perfect square canvas, equal width and height, strictly NOT vertical 9:16 and NOT horizontal 16:9).",
                "do_not_render_labels": "CRITICAL: Absolutely DO NOT paint any English words, sequence numbers, labels, 'Sticker', 'Sticker 01', 'Item', or '01' on the image canvas. The canvas must contain ONLY the Thai caption and the character illustration.",
                "single_text_instance": "CRITICAL: Render the Thai caption strictly ONCE per image. Absolutely DO NOT duplicate text at both top and bottom.",
                "no_character_outline": f"CRITICAL: The character illustration MUST NOT have any white or colored sticker outline, die-cut silhouette border, or glow around the character body, hair, clothes, limbs, or props. The character drawing must be rendered cleanly with normal illustration lineart directly placed onto the pure magenta background (#FF00FF). The {stroke_name_en} outline contour stroke is applied EXCLUSIVELY to the Thai typography letters, NEVER to the character body.",
                "background": "Solid pure magenta background (#FF00FF, RGB 255, 0, 255, chroma key fuchsia), absolutely flat single color, zero shadows, zero gradients, zero noise, high contrast against character edges for perfect 1-click transparency keying.",
                "single_version_per_item": "Generate strictly ONE single image per item. Do NOT generate alternative or backup versions."
            },
            "character_consistency": {
                "reference": "Strictly keep the exact same character features, face, hair, clothing style, colors, and art line style from the attached image reference in every single image.",
                "character_description": character_description
            },
            "typography_rules": {
                "style": f"Glossy 3D puffy bubble pop-art sticker font: Rounded cute Japanese-LINE-sticker typography with solid {text_name_en} inner fill ({text_clean}), glossy specular shine highlights, and an ultra-thick bold {stroke_name_en} outer contour stroke border ({stroke_clean}) for maximum legibility and pop against the background.",
                "word_emphasis_and_hierarchy": {
                    "rule": "DYNAMIC FONT SIZING & WORD EMPHASIS: Create authentic, high-impact LINE Creators Market typography by emphasizing the primary hero keyword. In captions with multiple words or ending particles (e.g., 'เงียบกริบ', 'รับทราบค่ะ', 'พร้อมเปย์เสมอ'), render the primary action/emotion keyword in a noticeably LARGER, bolder font (130-150% scale), while rendering supporting particles, modifiers, or subtext in a smaller, compact font (70-80% scale). The smaller word may sit on Line 2 directly underneath or inline beside the hero word, giving the sticker vibrant commercial appeal and instant readability.",
                    "example_positive": "For 'เงียบกริบ': Line 1 'เงียบ' (HUGE 140% BUBBLE FONT), Line 2 'กริบ' (SMALLER 75% SUBTEXT underneath) - or inline size contrast. For 'รับทราบค่ะ': 'รับทราบ' (LARGE) + 'ค่ะ' (SMALL COMPACT).",
                    "example_forbidden": "DO NOT make all words flat and uniformly same-sized if there is an obvious hero keyword, and NEVER split words mid-syllable."
                },
                "thai_word_breaking_rules": "CRITICAL ZERO SYLLABLE SPLITTING: NEVER split a Thai word mid-syllable or separate a leading/trailing vowel (เ, แ, โ, ใ, ไ, ะ, า) or tone mark (่, ้, ๊, ๋, ์) onto another line. If suggested_horizontal_lines has 1 line, render it on exactly ONE horizontal line. If it has 2 lines, break ONLY at the natural word boundary specified in suggested_horizontal_lines. NEVER wrap or break letters mid-word (FORBIDDEN: 'รับทร/าบค่ะ', 'พร้อมเ/ปย์เสมอ', 'สวัสดีวั/นอาทิตย์', 'คิดถึงจ/นใจเจ็บ').",
                "visual_layering": "CRITICAL ZERO OCCLUSION: Text MUST be placed strictly in OPEN NEGATIVE SPACE and 100% UNOBSCURED. The character MUST NEVER stand in front of the text or hide any part of the text behind its head, body, or props. Text must NEVER cover or overlap the character's face, hair, or eyes. Face, hair, and eyes must remain 100% visible and unobstructed.",
                "text_fill_color": f"Solid glossy {text_name_en} ({text_clean}) with subtle glossy surface shine. STRICTLY {text_name_en} inside every Thai character. NO other fill colors permitted.",
                "outline_border": f"Heavy thick bold {stroke_name_en} outline border ({stroke_clean}) applied ONLY to the Thai text characters for legibility (STRICTLY DO NOT put outline or border around the character).",
                "composition_and_placement": {
                    "aspect_ratio": "Strict 1:1 square canvas (width == height). Absolutely NO vertical 9:16 or widescreen 16:9 orientation.",
                    "dynamic_asymmetrical_framing": "The character MUST NOT always be in the dead center. Use asymmetrical framing (Rule of Thirds): position character either on the left half (X: 15-45%), on the right half (X: 55-85%), or in a compact sitting/crouching pose in the lower 45% of the frame. This intentionally creates an expansive, vacant negative space on the opposite side specifically dedicated to hosting the stacked typography cleanly without crowding.",
                    "text_layout_rules": "Text is formatted into 1 to 2 short horizontal stacked lines (like a neat text bubble or paragraph). The text block sits entirely inside the open negative space beside or above the character, with a distinct clear gap separating character and text. No words are bent along a curve or split into vertical columns.",
                    "strict_safe_margin_rule": "CRITICAL: Character and text MUST NEVER TOUCH OR BE FLUSH AGAINST ANY CANVAS EDGE. Always maintain at least 12-15% pure magenta (#FF00FF) padding/margin around all 4 sides (top, bottom, left, right). Do not bleed or crop off character limbs, hair, or text outline.",
                    "strictly_forbidden_elements": [
                        "FORBIDDEN: Drawing the words 'Sticker', 'Item', or any numbers/labels (e.g. 'Sticker 01', 'Sticker 06', 'Item 27', '01') anywhere on the canvas",
                        "FORBIDDEN: Drawing any English text, sequence tags, or title badges on the image",
                        "FORBIDDEN: Duplicating the Thai text (e.g. printing it at both top and bottom)",
                        "FORBIDDEN: Drawing a white sticker die-cut border, white outline, or silhouette contour around character body, hair, clothes, limbs, furniture, or props",
                        "FORBIDDEN: Generating multiple images or 'safe alternative versions' for a single item (strictly generate 1 master image per item)",
                        "FORBIDDEN: Splitting Thai words mid-syllable or separating vowels/tone marks across lines",
                        "FORBIDDEN: Text placed directly over the character's head, face, hair, or body (occlusion)",
                        "FORBIDDEN: Canvas aspect ratio other than 1:1 square (FORBIDDEN: vertical portrait 9:16 or horizontal landscape 16:9)"
                    ]
                },
                "thai_glyph_anatomy_rules": {
                    "rule_khor_khai_smooth_head": "CRITICAL FOR 'ข' (UNICODE U+0E02): The consonant 'ข' MUST have a perfectly smooth, continuous circular head loop with zero indentation and zero crease. Modern Thai smooth circular loop head.",
                    "rule_chor_chang_smooth_head": "CRITICAL GEOMETRIC ANATOMY FOR 'ช' (UNICODE U+0E0A, CHO CHANG): The consonant 'ช' (U+0E0A) MUST begin with a 100% completely smooth, continuous, round circular head loop (identical circular head to 'ข' U+0E02), followed by a bottom curve and an upward tail on the right. The circular head loop is a single seamless unbroken ring with zero notch and zero crease in modern Thai typography.",
                    "rule_do_dek_smooth_head": "The letter 'ด' (U+0E14) has a smooth arched head with an inward circular loop.",
                    "rule_3d_bubble_loops": "Do not let 3D bubble highlights or shadows mimic notches or creases on letter heads. All circular heads must remain distinctly smooth, unbroken, and clean."
                },
                "spelling_accuracy": "Strict verbatim reproduction of Thai captions. Thai vowels, tone marks (วรรณยุกต์), and consonants must be perfectly formed and attached.",
                "rule_caption_items": f"Bold horizontal stacked Thai typography with solid {text_name_en} fill ({text_clean}), thick {stroke_name_en} border ({stroke_clean}), and dynamic hero word sizing placed in open space above or beside character with ZERO occlusion. Character has no body outline.",
                "rule_no_caption_items": "STRICTLY NO TEXT! Pure character illustrations with zero words or letters, and zero body outlines."
            },
            "batch_generation_schedule": {
                "batch_size": 8,
                "total_batches": 6,
                "schedule": [
                    "Batch 1: Images 01 - 08 (8 images)",
                    "Batch 2: Images 09 - 16 (8 images)",
                    "Batch 3: Images 17 - 24 (8 images)",
                    "Batch 4: Images 25 - 32 (8 images)",
                    "Batch 5: Images 33 - 40 (8 images)",
                    "Batch 6: Images 41 - 48 (8 images: 4 captions + 4 Main/Tab)"
                ],
                "total_images": 48
            },
            "sticker_items_48": items_payload
        }

        json_str = json.dumps(payload, ensure_ascii=False, indent=2)

        prompt_text = (
            f"กรุณาสร้างชุดสติกเกอร์ LINE จำนวนทั้งหมด 48 รูป (44 รูปมีข้อความแคปชั่น + 4 รูปไม่มีข้อความสำหรับทำ Main และ Tab) "
            f"โดยรักษาเอกลักษณ์ตัวละคร ลายเส้น เสื้อผ้า และสีสันให้ตรงกับรูปต้นแบบที่แนบอย่างเคร่งครัด 100%\n\n"
            f"=== 🛑 กฎเหล็กข้อห้ามเด็ดขาด 5 ประการ (CRITICAL MUST-FOLLOW RULES) ===\n"
            f"1. 🛑 ห้ามมีคำว่า 'Sticker', 'Item', ตัวหนังสือภาษาอังกฤษ หรือหมายเลขลำดับติดในภาพเด็ดขาด (ABSOLUTELY NO 'Sticker' OR 'Item' LABELS, ENGLISH WORDS, OR NUMBERS):\n"
            f"   - ห้ามพิมพ์คำว่า 'Sticker', 'Sticker 01', 'Sticker 06', 'Item', 'Item 27', '01' หรือตัวเลขกำกับลำดับใดๆ ลงบนผืนผ้าใบภาพเด็ดขาด 100%! ห้ามมีตัวหนังสือภาษาอังกฤษทุกชนิดในภาพ!\n"
            f"   - ผืนผ้าใบต้องมีเฉพาะ 'ตัวหนังสือภาษาไทยที่ระบุ' และ 'ภาพวาดตัวละคร' เท่านั้น ห้ามใส่ Title, Label, ป้ายชื่อสติกเกอร์ หรือ Metadata ใดๆ ลงในรูปภาพเด็ดขาด\n\n"
            f"2. 🛑 ห้ามพิมพ์ข้อความซ้ำซ้อนในภาพเดียวกันเด็ดขาด (SINGLE TEXT INSTANCE ONLY):\n"
            f"   - ข้อความภาษาไทยต้องปรากฏเพียง 'จุดเดียว ครั้งเดียว' ต่อ 1 รูปภาพเท่านั้น!\n"
            f"   - ห้ามพิมพ์ข้อความซ้ำทั้งข้างบนและข้างล่าง ห้ามใส่ข้อความเบิ้ล 2 ที่ในรูปเดียวกันเด็ดขาด ให้เลือกวางในพื้นที่ว่างจุดเดียวตามความเหมาะสม\n\n"
            f"3. 🛑 ห้ามมีขอบขาวรอบตัวละครและสิ่งของเด็ดขาด (STRICTLY NO WHITE DIE-CUT BORDER AROUND CHARACTER):\n"
            f"   - ห้ามวาดเส้นขอบขาว (White Die-Cut Contour / Sticker Silhouette Border / White Halo) ล้อมรอบตัวละคร เส้นผม เสื้อผ้า แขน ขา เก้าอี้ พร็อพ หรือสิ่งของเด็ดขาด!\n"
            f"   - ตัวละครและสิ่งของต้องเป็นภาพวาดประกอบ 2D สไตล์อนิเมะ ลายเส้นปกติ วาดสัมผัสแนบกับพื้นหลังสีชมพู (#FF00FF) โดยตรง 100% ไม่มีขอบขาวรอบตัว\n"
            f"   - เส้นขอบสี{stroke_name_th}หนา ({stroke_clean}) อนุญาตให้ใส่ได้ 'เฉพาะที่ตัวหนังสือภาษาไทยเท่านั้น' เพื่อให้อ่านง่าย ห้ามมีขอบขาวที่ตัวละครเด็ดขาด\n\n"
            f"4. 🛑 กฎลักษณะพยัญชนะ 'ช' (Unicode U+0E0A) และ 'ข' (Unicode U+0E02) หัวกลมมนเรียบเนียน 100% (MANDATORY SMOOTH CIRCULAR HEAD LOOPS):\n"
            f"   - หัวของพยัญชนะ 'ช' (Unicode U+0E0A: ช.ช้าง) ทุกคำ (เช่น ธรรมชาติ, เช็ค, ชวน, ชิล, ชอบ, ใช่, ชื่นใจ, ชาร์จ, ช่วย) ต้องเป็น 'ห่วงวงกลมกลมเกลี้ยงเรียบเนียน 100% ชิ้นเดียวต่อเนื่อง' โครงสร้างตัวอักษรเหมือน ข.ไข่ (U+0E02) ที่มีหางตวัดขึ้นทางขวา เส้นรอบหัวต้องโค้งมนสม่ำเสมอ ไร้รอยบาก ไร้รอยหยัก ไร้รอยพับใดๆ ทั้งสิ้น\n"
            f"   - หัวของพยัญชนะ 'ข' (Unicode U+0E02: ข.ไข่) ทุกคำ (เช่น ขอ, ขอบคุณ, เข้าใจ, ข้าว) ต้องเป็น 'ห่วงวงกลมกลมเกลี้ยง 100%' เส้นโค้งมนเรียบระดับเวกเตอร์โมเดิร์นฟอนต์\n\n"
            f"5. 🛑 สร้างเพียง 1 รูปภาพต่อ 1 รายการเท่านั้น (ห้ามสร้าง 2 เวอร์ชั่น หรือเวอร์ชันสำรองปลอดภัย):\n"
            f"   - ในแต่ละรายการ ให้สร้างเฉพาะภาพหลักภาพเดียวที่สมบูรณ์แบบเท่านั้น ห้ามสร้างภาพซ้ำสอง หรือสร้าง 'เวอร์ชันสำรองปลอดภัย' (Safe Alternative Version) ออกมาคู่กัน\n"
            f"   - เนื้อหาและพร็อพทั้งหมดเป็นแนว Chibi น่ารัก สดใส ไร้ความรุนแรง ปลอดภัย 100%\n\n"
            f"6. 🌟 ท่าทางและอารมณ์ต้องมีมิติหลากหลายตามแคปชั่น (DRAMATIC EXPRESSIONS & ACTIVE POSES):\n"
            f"   - ห้ามใช้ท่าเดิมแล้วแค่เอียงตัวเล็กน้อยเด็ดขาด! ให้เปลี่ยนท่าทางของทั้งตัว ท่าทางมือ แขน ขา การเคลื่อนไหว (วิ่ง, นั่ง, กระโดด, กอด, กุมขมับ, ชูนิ้ว)\n"
            f"   - สีหน้าและแววตาต้องแสดงอารมณ์แบบการ์ตูนญี่ปุ่นอย่างชัดเจน (ยิ้มกว้าง, หัวเราะลั่น, ร้องไห้กระซิก, ตกใจตาโต, ตาเป็นประกายหัวใจ, เขินแก้มแดง) ให้เข้ากับความหมายของแคปชั่นแต่ละรูป 100%\n\n"
            f"=== ข้อกำหนดด้านสัดส่วนและองค์ประกอบ ===\n"
            f"- สัดส่วนภาพสี่เหลี่ยมจัตุรัส 1:1 เท่านั้น (Square Canvas 1:1 Aspect Ratio): ความกว้างเท่ากับความสูง 100% ห้ามวาดเป็นแนวตั้ง 9:16 หรือแนวนอน 16:9 เด็ดขาด\n"
            f"- พื้นหลังสีชมพูมาเจนต้าล้วน (#FF00FF, Chroma Key Magenta): สะอาดตา เรียบสนิท ไม่มีเงา ไม่มีเกรเดียนท์\n"
            f"- ห้ามตัดคำหรือแยกพยางค์ข้ามบรรทัดเด็ดขาด (Zero Syllable Splitting): คำภาษาไทยต้องสมบูรณ์ 100% ในแต่ละบรรทัด ห้ามผ่ากลางคำเด็ดขาด\n"
            f"- ห้ามข้อความทับหรือบังหน้าตัวละครเด็ดขาด (Zero Face/Head Occlusion): ตัวหนังสือต้องอยู่บน 'พื้นที่ว่าง' (Negative Space) เท่านั้น ใบหน้า ตา รอยยิ้ม ต้องเปิดโล่ง 100%\n"
            f"- ห้ามตัวละครและตัวหนังสือชิดขอบภาพเด็ดขาด (Strict Safe Margin): เว้นระยะปลอดภัยอย่างน้อย 12-15% จากขอบทั้ง 4 ด้าน\n\n"
            f"```json\n{json_str}\n```\n\n"
            f"⚠️ กฎการสร้างแบบแบ่งชุด (CRITICAL BATCH INSTRUCTION):\n"
            f"กรุณาสร้างรูปภาพรอบละ 8 รูป x 6 รอบ รวมจะได้ครบ 48 รูปพอดี สร้างเพียง 1 รูปต่อรายการ (ห้ามมีเวอร์ชันสำรอง)\n\n"
            f"สำคัญมาก: เมื่อเริ่มสร้างหรือสร้างชุดสติกเกอร์นี้ ให้วิเคราะห์คาแรคเตอร์แล้วส่งข้อมูลสำหรับลงทะเบียน LINE Creators Market ตอบกลับมาในแชตนี้ทันที:\n"
            f"- 🛑 ห้ามระบุจำนวนตัวเลขสติกเกอร์ (เช่น ห้ามใส่คำว่า '48 รูป', '48 ท่า', '48 อารมณ์', '48 stickers') ลงในชื่อชุดหรือคำอธิบายเด็ดขาด\n"
            f"- 🛑 ให้ตอบกลับเฉพาะบล็อกข้อมูลด้านล่างนี้เท่านั้น ปิดท้ายด้วยเครื่องหมาย ##### ทันที และห้ามพิมพ์ข้อความสรุปหรือข้อความสนทนาใดๆ ต่อท้ายเครื่องหมาย ##### เด็ดขาด:\n\n"
            f"=== ข้อมูลสำหรับลงทะเบียน LINE Creators Market ===\n"
            f"ชื่อชุดสติกเกอร์ (ไทย): [ชื่อชุดภาษาไทยที่ดึงดูด น่ารัก จำง่าย โดยไม่มีการระบุตัวเลขจำนวนภาพ]\n"
            f"ชื่อชุดสติกเกอร์ (อังกฤษ): [English Title without any number count]\n"
            f"คำอธิบายสติกเกอร์ (ไทย): [คำอธิบายชุดสติกเกอร์ภาษาไทยความยาวไม่เกิน 500 ตัวอักษร สื่ออารมณ์น่ารักใช้งานง่าย โดยไม่ระบุตัวเลขจำนวนภาพ]\n"
            f"คำอธิบายสติกเกอร์ (อังกฤษ): [English description expressing daily cute emotions for chatting without any number count]\n"
            f"#####\n"
        )

    return prompt_text, payload
 

def extract_clean_line_market_info(text: str) -> str:
    """
    สกัดเฉพาะบล็อกมาร์กดาวน์สำหรับลงทะเบียน LINE Creators Market จากข้อความตอบกลับของ AI
    โดยเริ่มต้นเก็บที่ '=== ข้อมูลสำหรับลงทะเบียน LINE Creators Market ==='
    และตัดจบที่ '#####' เพื่อให้ได้เฉพาะข้อมูลลงทะเบียนแท้จริงสำหรับไฟล์ info.txt 100%
    """
    if not text:
        return ""

    # 1. ละเว้นโค้ดบล็อก json (Prompt ต้นฉบับ) เพื่อไม่ให้ชนกับข้อความในคำสั่งของผู้ใช้
    text_no_json = re.sub(r'```json[\s\S]*?```', '', text)

    # 2. หากอยู่ใน markdown code block (```markdown ... ``` หรือ ```text ... ``` หรือ ``` ... ```)
    code_match = re.search(r'```(?:markdown|text)?\s*([\s\S]*?LINE Creators Market[\s\S]*?)```', text_no_json, re.IGNORECASE)
    search_target = code_match.group(1) if code_match else text_no_json

    # ปรับจูนคำผิดจาก AI/OCR เบื้องต้น
    search_target = re.sub(r'คำอ[ธิฐิ]บายสติกเกอร์', 'คำอธิบายสติกเกอร์', search_target)
    search_target = re.sub(r'(?:อังกรูษ|อังกฤษ|English)', 'อังกฤษ', search_target, flags=re.IGNORECASE)

    # 3. ค้นหาจุดเริ่มต้นของหัวข้อลงทะเบียน
    header_m = re.search(
        r'(={2,}\s*ข้อมูลสำหรับลง(?:ทะ|ฒะ)เบียน\s*LINE Creators Market\s*={2,}|[#*]+\s*ข้อมูลสำหรับลง(?:ทะ|ฒะ)เบียน\s*LINE Creators Market|ข้อมูลสำหรับลง(?:ทะ|ฒะ)เบียน\s*LINE Creators Market)',
        search_target,
        re.IGNORECASE
    )
    if not header_m:
        header_m = re.search(r'(=* ?.*?LINE Creators Market ?=*)', search_target, re.IGNORECASE)
        if not header_m:
            return ""

    start_pos = header_m.start()
    sub_text = search_target[start_pos:]

    # 4. ค้นหาจุดสิ้นสุดที่ ##### หรือตัดจบหลังคำอธิบายภาษาอังกฤษทันที
    end_hash_m = re.search(r'#{3,}', sub_text)
    if end_hash_m:
        raw_block = sub_text[:end_hash_m.start()].strip()
    else:
        desc_en_m = re.search(r'(?:คำอธิบายสติกเกอร์\s*\((?:อังกฤษ|English)\)|Description\s*\(?English\)?)\s*[:：]', sub_text, re.IGNORECASE)
        if desc_en_m:
            pos_after_label = desc_en_m.end()
            rest = sub_text[pos_after_label:]
            # ตัดจบเมื่อเจอการขึ้นย่อหน้าใหม่ที่มีข้อความพูดคุย/สรุป เช่น "ตอนนี้ชุดเต็ม", "หวังว่า", "พร้อมส่งตรวจ", ฯลฯ
            end_m = re.search(r'(\n\s*(?:ตอนนี้|ชุดเต็ม|พร้อมส่ง|thumb_up|thumb_down|content_copy|flag|See all|```|คุณสามารถ|หากต้องการ|หวังว่า|Hope you|Enjoy|Let me know|All \d+|\d+\s*stickers)|\Z)', rest, re.IGNORECASE)
            if end_m:
                raw_block = sub_text[:pos_after_label + end_m.start()].strip()
            else:
                raw_block = sub_text.strip()
        else:
            raw_block = sub_text.split('\n\n\n')[0].strip()

    # 5. กรองข้อความขยะ/ปุ่ม UI หรือข้อความคุยท้ายประโยคออกทีละบรรทัด
    clean_lines = []
    for l in raw_block.splitlines():
        st = l.strip()
        if st in ['thumb_up', 'thumb_down', 'content_copy', 'flag', 'See all', 'ดูน้อยลง', 'ดูเพิ่มเติม']:
            continue
        if st.startswith('```') or st.startswith('#####'):
            continue
        if any(st.startswith(prefix) for prefix in ['ตอนนี้ชุดเต็ม', 'พร้อมส่งตรวจ', 'ครบ 6 แบทช์', 'หวังว่าจะชอบ', 'หากต้องการปรับ']):
            break
        clean_lines.append(l)

    res = '\n'.join(clean_lines).strip()

    # 6. ลบตัวเลขจำนวนสติกเกอร์ (เช่น 48 รูป, 48 ท่า, 48 อารมณ์, 48 stickers) ออกจากชื่อชุดและคำอธิบาย
    # เพื่อป้องกันปัญหาการระบุจำนวนตายตัว เพราะผู้ใช้จะนำไปคัดเหลือ 40 รูป
    res = re.sub(r'[-\s,]*\b48\s*(?:รูป|ท่าทาง|ท่า|อารมณ์|แบบ|stickers?|emotions?)\b', '', res, flags=re.IGNORECASE)
    res = re.sub(r'\b48\s*(?:รูป|ท่าทาง|ท่า|อารมณ์|แบบ)\b', '', res, flags=re.IGNORECASE)

    # 7. จัดระเบียบการขึ้นบรรทัดใหม่และการสะกดของแต่ละหัวข้อให้สวยงามมาตรฐาน 100%
    res = re.sub(r'^[#*=\s]*ข้อมูลสำหรับลง(?:ทะ|ฒะ)เบียน\s*LINE Creators Market[#*=\s]*\n*', '=== ข้อมูลสำหรับลงทะเบียน LINE Creators Market ===\n\n', res)
    res = re.sub(r'^[^\n]*?ชุดสติกเกอร์\s*\((?:ไทย|Thai)\)', 'ชื่อชุดสติกเกอร์ (ไทย)', res, flags=re.MULTILINE)
    res = re.sub(r'([^\n])\s*(?:ช[ิืำ][^\s]*?ชุดสติกเกอร์|ชื่อชุดสติกเกอร์)\s*\((?:อังกฤษ|English)\)', r'\1\nชื่อชุดสติกเกอร์ (อังกฤษ)', res)
    res = re.sub(r'([^\n])\s*คำอ[ธิฐิ]บายสติกเกอร์\s*\((?:ไทย|Thai)\)', r'\1\n\nคำอธิบายสติกเกอร์ (ไทย)', res)
    res = re.sub(r'([^\n])\s*คำอ[ธิฐิ]บายสติกเกอร์\s*\((?:อังกฤษ|English)\)', r'\1\n\nคำอธิบายสติกเกอร์ (อังกฤษ)', res)
    res = re.sub(r'คำอ[ธิฐิ]บายสติกเกอร์', 'คำอธิบายสติกเกอร์', res)

    # ตัดช่องว่างซ้ำซ้อน
    res = re.sub(r'[ \t]+', ' ', res)
    res = re.sub(r'\n{3,}', '\n\n', res)
    res = res.strip()

    if "[" in res and ("ชื่อชุดภาษาไทย" in res or "คำอธิบายชุดสติกเกอร์" in res):
        return ""  # เป็นเพียงตัวอย่างเทมเพลตในคำสั่ง ไม่ใช่คำตอบจริงจาก AI

    return res

