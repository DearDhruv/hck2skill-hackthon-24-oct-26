import os
from PIL import Image, ImageDraw, ImageFont
from fractions import Fraction

def embed_gps_exif(img: Image.Image, lat: float, lng: float) -> Image.Exif:
    """Embeds GPS coordinates into image EXIF data using PIL."""
    exif = img.getexif()
    gps_ifd = exif.get_ifd(0x8825)

    lat_ref = "N" if lat >= 0 else "S"
    lng_ref = "E" if lng >= 0 else "W"
    lat_abs = abs(lat)
    lng_abs = abs(lng)

    lat_deg = int(lat_abs)
    lat_min = int((lat_abs - lat_deg) * 60)
    lat_sec = round(((lat_abs - lat_deg) * 60 - lat_min) * 60, 2)

    lng_deg = int(lng_abs)
    lng_min = int((lng_abs - lng_deg) * 60)
    lng_sec = round(((lng_abs - lng_deg) * 60 - lng_min) * 60, 2)

    gps_ifd[1] = lat_ref
    gps_ifd[2] = (Fraction(lat_deg, 1), Fraction(lat_min, 1), Fraction(int(lat_sec * 100), 100))
    gps_ifd[3] = lng_ref
    gps_ifd[4] = (Fraction(lng_deg, 1), Fraction(lng_min, 1), Fraction(int(lng_sec * 100), 100))

    return exif

def generate_samples():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "app", "static", "samples")
    video_dir = os.path.join(output_dir, "video")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)

    samples = [
        {
            "name": "pothole_cg_road.jpg",
            "title": "POTHOLE ON ARTERIAL ROAD",
            "location": "CG Road, Navrangpura, Ahmedabad",
            "lat": 23.0375,
            "lng": 72.5583,
            "bg_color": (55, 60, 68),
            "accent_color": (239, 68, 68),
            "hazard_type": "pothole",
            "detail": "Deep asphalt crater (18cm depth), two-wheeler rim hazard"
        },
        {
            "name": "garbage_overflow_kankaria.jpg",
            "title": "SOLID WASTE OVERFLOW",
            "location": "Near Gate 3, Kankaria Lake, Maninagar",
            "lat": 22.9978,
            "lng": 72.6033,
            "bg_color": (60, 50, 45),
            "accent_color": (245, 158, 11),
            "hazard_type": "garbage",
            "detail": "Commercial bin spillover onto pedestrian footpath"
        },
        {
            "name": "broken_streetlight_vastrapur.jpg",
            "title": "UNLIT BROKEN STREETLIGHT",
            "location": "Lake Periphery, Vastrapur, Bodakdev",
            "lat": 23.0421,
            "lng": 72.5117,
            "bg_color": (25, 30, 42),
            "accent_color": (168, 85, 247),
            "hazard_type": "streetlight",
            "detail": "Twin overhead LED luminaire fixture blackout"
        },
        {
            "name": "waterlogging_stadium.jpg",
            "title": "MONSOON WATERLOGGING",
            "location": "Near Sardar Patel Stadium, Navrangpura",
            "lat": 23.0450,
            "lng": 72.5620,
            "bg_color": (30, 58, 82),
            "accent_color": (6, 182, 212),
            "hazard_type": "waterlogging",
            "detail": "Stormwater backup spanning 40m carriageway (22cm depth)"
        }
    ]

    for item in samples:
        width, height = 800, 500
        img = Image.new("RGB", (width, height), color=item["bg_color"])
        draw = ImageDraw.Draw(img)

        # Draw road / environmental texture
        if item["hazard_type"] == "pothole":
            draw.line([(0, 250), (800, 250)], fill=(220, 220, 220), width=6)
            draw.ellipse([(220, 180), (580, 360)], fill=(25, 27, 30), outline=(239, 68, 68), width=5)
            draw.ellipse([(270, 210), (530, 330)], fill=(15, 16, 18), outline=(180, 40, 40), width=3)
            draw.line([(220, 270), (160, 290)], fill=(120, 120, 120), width=2)
            draw.line([(580, 260), (660, 240)], fill=(120, 120, 120), width=2)
            draw.line([(400, 360), (420, 420)], fill=(120, 120, 120), width=2)
            draw.rectangle([(200, 160), (600, 380)], outline=(239, 68, 68), width=3)

        elif item["hazard_type"] == "garbage":
            draw.rectangle([(0, 300), (800, 500)], fill=(80, 75, 70))
            draw.rectangle([(250, 160), (550, 420)], fill=(40, 90, 60), outline=(20, 50, 30), width=4)
            draw.polygon([(200, 420), (320, 260), (480, 270), (600, 420)], fill=(160, 120, 60), outline=(245, 158, 11), width=4)
            draw.ellipse([(180, 370), (280, 450)], fill=(200, 80, 60))
            draw.ellipse([(520, 360), (640, 440)], fill=(220, 180, 50))
            draw.rectangle([(160, 140), (660, 460)], outline=(245, 158, 11), width=3)

        elif item["hazard_type"] == "streetlight":
            draw.rectangle([(0, 350), (800, 500)], fill=(20, 22, 28))
            draw.line([(400, 80), (400, 450)], fill=(160, 165, 175), width=10)
            draw.line([(320, 100), (480, 100)], fill=(160, 165, 175), width=8)
            draw.ellipse([(300, 95), (340, 125)], fill=(50, 55, 65), outline=(168, 85, 247), width=4)
            draw.ellipse([(460, 95), (500, 125)], fill=(50, 55, 65), outline=(168, 85, 247), width=4)
            draw.ellipse([(280, 75), (520, 145)], outline=(239, 68, 68), width=3)

        elif item["hazard_type"] == "waterlogging":
            draw.rectangle([(0, 200), (800, 500)], fill=(25, 75, 110))
            for y_off in range(230, 480, 40):
                draw.arc([(50, y_off), (400, y_off + 30)], start=0, end=180, fill=(90, 180, 230), width=3)
                draw.arc([(420, y_off), (750, y_off + 30)], start=0, end=180, fill=(90, 180, 230), width=3)
            draw.rectangle([(380, 280), (420, 360)], fill=(220, 180, 40), outline=(239, 68, 68), width=3)
            draw.rectangle([(80, 180), (720, 460)], outline=(6, 182, 212), width=3)

        # Draw HUD Overlay Banner
        draw.rectangle([(0, 0), (800, 70)], fill=(15, 23, 42))
        draw.rectangle([(0, 430), (800, 500)], fill=(15, 23, 42))

        # Text labels
        draw.text((25, 15), f"AMC CITIZEN VISION FEED: {item['title']}", fill=item["accent_color"])
        draw.text((25, 38), f"Location: {item['location']} | GPS: {item['lat']}, {item['lng']}", fill=(203, 213, 225))
        draw.text((25, 445), f"AI Feature Diagnostic: {item['detail']}", fill=(241, 245, 249))
        draw.text((25, 468), "AMC Autonomous Civic Complaint Agent · Live Ground Sensor Verification", fill=(148, 163, 184))

        exif = embed_gps_exif(img, item["lat"], item["lng"])
        out_path = os.path.join(output_dir, item["name"])
        img.save(out_path, "JPEG", quality=92, exif=exif)
        print(f"Generated sample with GPS EXIF: {out_path}")

    # Generate the 5 road video frame images
    video_frames = [
        {"file": "frame_1_t0s.jpg", "sec": 0, "loc": "CG Road, Near Stadium Circle", "hazard": False},
        {"file": "frame_2_t3s.jpg", "sec": 3, "loc": "CG Road, Opp. Municipal Market", "hazard": True, "bbox": (240, 220, 560, 380)},
        {"file": "frame_3_t6s.jpg", "sec": 6, "loc": "CG Road, Bodyline Crossroads", "hazard": False},
        {"file": "frame_4_t9s.jpg", "sec": 9, "loc": "CG Road, Near Navrangpura Bus Stop", "hazard": True, "bbox": (200, 240, 580, 400)},
        {"file": "frame_5_t12s.jpg", "sec": 12, "loc": "CG Road, Law Garden Junction", "hazard": False}
    ]

    for vf in video_frames:
        w, h = 640, 360
        fimg = Image.new("RGB", (w, h), color=(48, 52, 60))
        fdraw = ImageDraw.Draw(fimg)

        # Perspective road lines
        fdraw.polygon([(260, 140), (380, 140), (600, 360), (40, 360)], fill=(35, 38, 44))
        fdraw.line([(320, 140), (320, 360)], fill=(220, 220, 220), width=3)

        # Road horizon
        fdraw.rectangle([(0, 0), (w, 140)], fill=(20, 25, 35))

        if vf["hazard"]:
            bx1, by1, bx2, by2 = vf["bbox"]
            # Scale to 640x360
            bx1, bx2 = int(bx1 * w / 800), int(bx2 * w / 800)
            by1, by2 = int(by1 * h / 500), int(by2 * h / 500)
            fdraw.ellipse([(bx1 + 20, by1 + 10), (bx2 - 20, by2 - 10)], fill=(18, 19, 22), outline=(239, 68, 68), width=3)
            fdraw.rectangle([(bx1, by1), (bx2, by2)], outline=(239, 68, 68), width=2)
            fdraw.rectangle([(bx1, by1 - 20), (bx1 + 140, by1)], fill=(239, 68, 68))
            fdraw.text((bx1 + 4, by1 - 16), "HAZARD: POTHOLE (95%)", fill=(255, 255, 255))

        # Dashcam HUD
        fdraw.rectangle([(0, 0), (w, 32)], fill=(15, 23, 42))
        fdraw.text((12, 8), f"AMC DASHCAM SURVEILLANCE · t={vf['sec']}s · {vf['loc']}", fill=(226, 232, 240))
        status_text = "ALERT: ROAD CAVITY DETECTED" if vf["hazard"] else "CLEAR ROAD SURFACE"
        status_color = (239, 68, 68) if vf["hazard"] else (16, 185, 129)
        fdraw.text((w - 240, 8), status_text, fill=status_color)

        frame_path = os.path.join(video_dir, vf["file"])
        fimg.save(frame_path, "JPEG", quality=88)
        print(f"Generated video frame: {frame_path}")

if __name__ == "__main__":
    generate_samples()
