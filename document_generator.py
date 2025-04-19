#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import qrcode
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Paths to assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")

# Create temp directory if it doesn't exist
os.makedirs(TEMP_DIR, exist_ok=True)

# Default font paths - will be initialized in init_resources()
FONT_REGULAR = None
FONT_BOLD = None

# Default logos - will be initialized in init_resources()
LOGO_RUQSAT = None
LOGO_QOLDAU = None

def init_resources():
    """Initialize resources like fonts and logos."""
    global FONT_REGULAR, FONT_BOLD, LOGO_RUQSAT, LOGO_QOLDAU
    
    # Check if fonts directory exists, create if not
    os.makedirs(FONT_DIR, exist_ok=True)
    
    # Use default system fonts if custom fonts not available
    try:
        FONT_REGULAR = ImageFont.truetype(os.path.join(FONT_DIR, "regular.ttf"), 16)
    except IOError:
        # Fallback to default font
        FONT_REGULAR = ImageFont.load_default()
    
    try:
        FONT_BOLD = ImageFont.truetype(os.path.join(FONT_DIR, "bold.ttf"), 18)
    except IOError:
        # Fallback to default font
        FONT_BOLD = ImageFont.load_default()
    
    # Create simple placeholder logos if not available
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    # Create RUQSAT logo if not exists
    ruqsat_path = os.path.join(ASSETS_DIR, "ruqsat_logo.png")
    if not os.path.exists(ruqsat_path):
        create_placeholder_logo(ruqsat_path, "CARGO RUQSAT", (0, 150, 100))
    
    # Load logo with error handling
    try:
        LOGO_RUQSAT = Image.open(ruqsat_path).convert("RGBA")
        # Use LANCZOS if available, otherwise use BICUBIC (more compatible with older PIL)
        resample_method = getattr(Image, "LANCZOS", Image.BICUBIC)
        LOGO_RUQSAT = LOGO_RUQSAT.resize((100, 50), resample_method)
    except Exception as e:
        print(f"Warning: Could not load RUQSAT logo: {e}")
        # Create a simple placeholder on the fly
        LOGO_RUQSAT = Image.new("RGBA", (100, 50), (0, 150, 100, 255))
    
    # Create QOLDAU logo if not exists
    qoldau_path = os.path.join(ASSETS_DIR, "qoldau_logo.png")
    if not os.path.exists(qoldau_path):
        create_placeholder_logo(qoldau_path, "QOLDAU.KZ", (150, 150, 150))
    
    # Load logo with error handling
    try:
        LOGO_QOLDAU = Image.open(qoldau_path).convert("RGBA")
        # Use LANCZOS if available, otherwise use BICUBIC
        resample_method = getattr(Image, "LANCZOS", Image.BICUBIC)
        LOGO_QOLDAU = LOGO_QOLDAU.resize((100, 50), resample_method)
    except Exception as e:
        print(f"Warning: Could not load QOLDAU logo: {e}")
        # Create a simple placeholder on the fly
        LOGO_QOLDAU = Image.new("RGBA", (100, 50), (150, 150, 150, 255))

def create_placeholder_logo(path, text, color):
    """Create a simple placeholder logo."""
    logo = Image.new("RGBA", (200, 100), (255, 255, 255, 0))
    draw = ImageDraw.Draw(logo)
    font = ImageFont.load_default()
    
    # Draw a circle
    draw.ellipse((10, 10, 90, 90), fill=color)
    
    # Add text
    draw.text((100, 40), text, fill=(50, 50, 50), font=font)
    
    logo.save(path)

def generate_qr_code(data):
    """Generate a QR code image."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    return qr.make_image(fill_color="black", back_color="white")

def create_document(data):
    """Create a document with the given data."""
    # Initialize resources if not already done
    if FONT_REGULAR is None:
        init_resources()
    
    # Create a new image
    width, height = 1000, 800
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # Current date and time for the printout
    now = datetime.now()
    print_datetime = now.strftime("%d.%m.%Y %H:%M")
    
    # Generate a QR code
    qr_text = f"Бронирование {data['booking_number']} для {data['vehicle_number']} на {data['date']} {data['time']}"
    qr_img = generate_qr_code(qr_text)
    
    # Use LANCZOS if available, otherwise use BICUBIC (more compatible with older PIL)
    resample_method = getattr(Image, "LANCZOS", Image.BICUBIC)
    qr_img = qr_img.resize((400, 400), resample_method)
    
    # Paste the QR code
    image.paste(qr_img, (50, 100))
    
    # Add "1 of 1" text above QR
    draw.rectangle((75, 30, 175, 70), fill=(200, 200, 200), outline=None)
    draw.text((95, 40), "1 of 1", fill="black", font=FONT_BOLD)
    
    # Add document title and content
    # Use a larger font for title if possible
    try:
        # Try to use a bigger font for the title - more compatible approach
        title_font = ImageFont.load_default()
        title_size = 24
    except Exception:
        # Fallback to regular font if can't create larger one
        title_font = FONT_BOLD
        title_size = 18
        
    draw.text((550, 100), "ВЫПИСКА ИЗ СИСТЕМЫ", fill="black", font=title_font)
    draw.text((550, 130), "ЭЛЕКТРОННОЙ ОЧЕРЕДИ", fill="black", font=title_font)
    
    # Add print date and time
    draw.text((550, 170), f"Дата и время распечатки: {print_datetime}", fill="black", font=FONT_REGULAR)
    
    # Add "БРОНИРОВАНИЕ" section
    draw.text((550, 220), "БРОНИРОВАНИЕ", fill="black", font=FONT_BOLD)
    
    # Add status
    draw.text((550, 250), "Статус", fill="gray", font=FONT_REGULAR)
    draw.rectangle((850, 245, 950, 265), fill=(130, 90, 220), outline=None)
    draw.text((860, 250), "В очереди", fill="white", font=FONT_REGULAR)
    
    # Add booking details
    draw.text((550, 290), "№ бронирования", fill="gray", font=FONT_REGULAR)
    draw.text((850, 290), data["booking_number"], fill="black", font=FONT_REGULAR)
    
    draw.text((550, 330), "Пункт пропуска", fill="gray", font=FONT_REGULAR)
    draw.text((850, 330), data["checkpoint"], fill="black", font=FONT_REGULAR)
    
    draw.text((550, 370), "Дата", fill="gray", font=FONT_REGULAR)
    draw.text((850, 370), data["date"], fill="black", font=FONT_REGULAR)
    
    draw.text((550, 410), "Ориентировочное время", fill="gray", font=FONT_REGULAR)
    draw.text((850, 410), data["time"], fill="black", font=FONT_REGULAR)
    
    draw.text((550, 450), "Тип очереди", fill="gray", font=FONT_REGULAR)
    draw.text((850, 450), "Выбранное время", fill="black", font=FONT_REGULAR)
    
    # Add "ТРАНСПОРТ" section
    draw.text((550, 520), "ТРАНСПОРТ", fill="black", font=FONT_BOLD)
    
    draw.text((550, 550), "Номерной знак транспорта", fill="gray", font=FONT_REGULAR)
    draw.text((850, 550), data["vehicle_number"], fill="black", font=FONT_REGULAR)
    
    draw.text((550, 590), "Номерной знак прицепа", fill="gray", font=FONT_REGULAR)
    draw.text((850, 590), data["trailer_number"], fill="black", font=FONT_REGULAR)
    
    draw.text((550, 630), "Страна регистрации", fill="gray", font=FONT_REGULAR)
    draw.text((850, 630), data["country"], fill="black", font=FONT_REGULAR)
    
    # Add instruction text
    instr_text = "Для подтверждения бронирования предъявите QR для сканирования на пункте пропуска"
    draw.text((50, 530), instr_text, fill="black", font=FONT_REGULAR)
    
    # Add logos
    image.paste(LOGO_RUQSAT, (70, 600), LOGO_RUQSAT)
    image.paste(LOGO_QOLDAU, (70, 670), LOGO_QOLDAU)
    
    # Add "Цифровая платформа для бизнеса" text
    draw.text((180, 680), "Цифровая платформа для бизнеса", fill="gray", font=FONT_REGULAR)
    
    # Save to temporary file
    temp_filename = f"{uuid.uuid4()}.png"
    temp_path = os.path.join(TEMP_DIR, temp_filename)
    image.save(temp_path)
    
    return temp_path

def create_document_from_defaults():
    """Create a document using default values for testing."""
    default_data = {
        "date": "04.03.2025",
        "time": "21:00-22:00",
        "booking_number": "A334BECF0368C",
        "checkpoint": "Нур Жолы - Хоргос",
        "vehicle_number": "931AFY13",
        "trailer_number": "97AGJ13",
        "country": "Казахстан",
    }
    
    return create_document(default_data)

if __name__ == "__main__":
    # Test functionality
    test_doc_path = create_document_from_defaults()
    print(f"Test document created: {test_doc_path}")