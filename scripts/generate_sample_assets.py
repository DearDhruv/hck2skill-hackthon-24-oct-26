import os
from PIL import Image, ImageDraw, ImageFont

def generate_samples():
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "static", "samples")
    os.makedirs(output_dir, exist_ok=True)

    samples = [
        {
            "name": "pothole_cg_road.jpg",
            "title": "POTHOLE ON ARTERIAL ROAD",
            "location": "CG Road, Navrangpura, Ahmedabad",
            "bg_color": (55, 60, 68),
            "accent_color": (239, 68, 68),
            "hazard_type": "pothole",
            "detail": "Deep asphalt crater (18cm depth), two-wheeler rim hazard"
        },
        {
            "name": "garbage_overflow_kankaria.jpg",
            "title": "SOLID WASTE OVERFLOW",
            "location": "Near Gate 3, Kankaria Lake, Maninagar",
            "bg_color": (60, 50, 45),
            "accent_color": (245, 158, 11),
            "hazard_type": "garbage",
            "detail": "Commercial bin spillover onto pedestrian footpath"
        },
        {
            "name": "broken_streetlight_vastrapur.jpg",
            "title": "UNLIT BROKEN STREETLIGHT",
            "location": "Lake Periphery, Vastrapur, Bodakdev",
            "bg_color": (25, 30, 42),
            "accent_color": (168, 85, 247),
            "hazard_type": "streetlight",
            "detail": "Twin overhead LED luminaire fixture blackout"
        },
        {
            "name": "waterlogging_stadium.jpg",
            "title": "MONSOON WATERLOGGING",
            "location": "Near Sardar Patel Stadium, Navrangpura",
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
            # Road lines
            draw.line([(0, 250), (800, 250)], fill=(220, 220, 220), width=6)
            # Pothole crater simulation
            draw.ellipse([(220, 180), (580, 360)], fill=(25, 27, 30), outline=(239, 68, 68), width=5)
            draw.ellipse([(270, 210), (530, 330)], fill=(15, 16, 18), outline=(180, 40, 40), width=3)
            # Cracked asphalt lines
            draw.line([(220, 270), (160, 290)], fill=(120, 120, 120), width=2)
            draw.line([(580, 260), (660, 240)], fill=(120, 120, 120), width=2)
            draw.line([(400, 360), (420, 420)], fill=(120, 120, 120), width=2)
            # Bounding box tag
            draw.rectangle([(200, 160), (600, 380)], outline=(239, 68, 68), width=3)

        elif item["hazard_type"] == "garbage":
            # Footpath pavement
            draw.rectangle([(0, 300), (800, 500)], fill=(80, 75, 70))
            # Dumpster
            draw.rectangle([(250, 160), (550, 420)], fill=(40, 90, 60), outline=(20, 50, 30), width=4)
            # Overflow trash pile
            draw.polygon([(200, 420), (320, 260), (480, 270), (600, 420)], fill=(160, 120, 60), outline=(245, 158, 11), width=4)
            draw.ellipse([(180, 370), (280, 450)], fill=(200, 80, 60))
            draw.ellipse([(520, 360), (640, 440)], fill=(220, 180, 50))
            draw.rectangle([(160, 140), (660, 460)], outline=(245, 158, 11), width=3)

        elif item["hazard_type"] == "streetlight":
            # Night sky with road horizon
            draw.rectangle([(0, 350), (800, 500)], fill=(20, 22, 28))
            # Mast pole
            draw.line([(400, 80), (400, 450)], fill=(160, 165, 175), width=10)
            # Crossbar & luminaires
            draw.line([(320, 100), (480, 100)], fill=(160, 165, 175), width=8)
            draw.ellipse([(300, 95), (340, 125)], fill=(50, 55, 65), outline=(168, 85, 247), width=4)
            draw.ellipse([(460, 95), (500, 125)], fill=(50, 55, 65), outline=(168, 85, 247), width=4)
            # Defect warning ring
            draw.ellipse([(280, 75), (520, 145)], outline=(239, 68, 68), width=3)

        elif item["hazard_type"] == "waterlogging":
            # Submerged road with water waves
            draw.rectangle([(0, 200), (800, 500)], fill=(25, 75, 110))
            for y_off in range(230, 480, 40):
                draw.arc([(50, y_off), (400, y_off + 30)], start=0, end=180, fill=(90, 180, 230), width=3)
                draw.arc([(420, y_off), (750, y_off + 30)], start=0, end=180, fill=(90, 180, 230), width=3)
            # Submerged road divider
            draw.rectangle([(380, 280), (420, 360)], fill=(220, 180, 40), outline=(239, 68, 68), width=3)
            draw.rectangle([(80, 180), (720, 460)], outline=(6, 182, 212), width=3)

        # Draw HUD Overlay Banner
        draw.rectangle([(0, 0), (800, 70)], fill=(15, 23, 42))
        draw.rectangle([(0, 430), (800, 500)], fill=(15, 23, 42))

        # Text labels
        draw.text((25, 15), f"AMC CITIZEN VISION FEED: {item['title']}", fill=item["accent_color"])
        draw.text((25, 38), f"Location: {item['location']} | AMC Ward Telemetry", fill=(203, 213, 225))
        draw.text((25, 445), f"AI Feature Diagnostic: {item['detail']}", fill=(241, 245, 249))
        draw.text((25, 468), "AMC Autonomous Civic Complaint Agent · Live Ground Sensor Verification", fill=(148, 163, 184))

        out_path = os.path.join(output_dir, item["name"])
        img.save(out_path, "JPEG", quality=92)
        print(f"Generated sample: {out_path}")

if __name__ == "__main__":
    generate_samples()
