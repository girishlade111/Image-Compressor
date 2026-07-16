from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, os, struct

SIZES = {
    "android-chrome-192x192.png": 192,
    "android-chrome-512x512.png": 512,
    "apple-touch-icon.png": 180,
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "symbol-192x192.png": 192,
}

OUT = r"C:\mazanoke\assets\images"

def gradient(draw, xy, colors, steps=256):
    x0, y0, x1, y1 = xy
    for i in range(steps):
        t = i / (steps - 1)
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * t)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * t)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * t)
        y = int(y0 + (y1 - y0) * t)
        draw.line([(x0, y), (x1, y)], fill=(r, g, b))

def radial_gradient(draw, cx, cy, radius, inner_color, outer_color):
    for r in range(radius, 0, -1):
        t = r / radius
        col = tuple(int(inner_color[i] + (outer_color[i] - inner_color[i]) * (1 - t)) for i in range(3))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

def gaussian_noise_layer(size, intensity=20):
    import random
    noise = Image.new("RGBA", size, (0, 0, 0, 0))
    px = noise.load()
    for x in range(size[0]):
        for y in range(size[1]):
            v = random.randint(-intensity, intensity)
            px[x, y] = (v + 128, v + 128, v + 128, 30)
    return noise

def create_logo(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size
    p = int(s * 0.08)
    inner = s - 2 * p

    shadow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([p + 2, p + 4, p + inner + 2, p + inner + 4], radius=int(s * 0.12), fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=s * 0.05))

    bg_grad = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bgd = ImageDraw.Draw(bg_grad)
    gradient(bgd, [p, p, p + inner, p + inner],
             [(25, 30, 50), (55, 65, 100)])
    mask = Image.new("L", (s, s), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([p, p, p + inner, p + inner], radius=int(s * 0.12), fill=255)
    bg_grad = ImageChops.composite(bg_grad, Image.new("RGBA", (s, s), (0, 0, 0, 0)), mask)

    accent = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ad = ImageDraw.Draw(accent)
    accent_grad = [(70, 130, 255), (100, 200, 255)]
    gradient(ad, [p + 2, p + 2, p + inner - 2, int(p + inner * 0.5)],
             accent_grad)
    am = Image.new("L", (s, s), 0)
    amd = ImageDraw.Draw(am)
    amd.rounded_rectangle([p, p, p + inner, p + inner], radius=int(s * 0.12), fill=255)
    accent = ImageChops.composite(accent, Image.new("RGBA", (s, s), (0, 0, 0, 0)), am)
    accent = accent.filter(ImageFilter.GaussianBlur(radius=s * 0.03))

    ic = int(s * 0.45)
    iy = int(s * 0.28)

    img_mtn = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    imd = ImageDraw.Draw(img_mtn)

    sun_cx = p + int(inner * 0.35)
    sun_cy = p + int(inner * 0.35)
    sun_r = int(s * 0.07)
    radial_gradient(imd, sun_cx, sun_cy, sun_r, (255, 220, 100), (255, 180, 50))

    mtn_color = (200, 220, 255)
    mtn_points = []
    base_y = p + int(inner * 0.7)
    mtn_points = [
        (p + int(inner * 0.05), base_y),
        (p + int(inner * 0.25), p + int(inner * 0.35)),
        (p + int(inner * 0.40), p + int(inner * 0.50)),
        (p + int(inner * 0.55), p + int(inner * 0.25)),
        (p + int(inner * 0.75), p + int(inner * 0.45)),
        (p + int(inner * 0.95), base_y),
    ]
    imd.polygon(mtn_points, fill=mtn_color)

    mtn2_color = (160, 190, 230)
    mtn2_points = [
        (p + int(inner * 0.30), base_y + int(s * 0.02)),
        (p + int(inner * 0.45), p + int(inner * 0.45)),
        (p + int(inner * 0.60), p + int(inner * 0.55)),
        (p + int(inner * 0.85), p + int(inner * 0.40)),
        (p + int(inner * 0.95), base_y + int(s * 0.02)),
    ]
    imd.polygon(mtn2_points, fill=mtn2_color)

    img_mtn = img_mtn.filter(ImageFilter.SMOOTH)

    cx = p + int(inner * 0.5)
    cy = p + int(inner * 0.5)

    arrow_layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ald = ImageDraw.Draw(arrow_layer)

    arrow_color = (255, 255, 255, 220)
    arrow_w = int(s * 0.04)
    arrow_h = int(s * 0.18)
    arrow_gap = int(s * 0.02)
    ax_center = cx

    top_arrow_y1 = p + int(inner * 0.15)
    top_arrow_y2 = top_arrow_y1 - arrow_h
    ald.polygon([
        (ax_center - arrow_w * 2, top_arrow_y1),
        (ax_center, top_arrow_y2),
        (ax_center + arrow_w * 2, top_arrow_y1),
    ], fill=(255, 255, 255, 180))
    ald.rectangle([
        ax_center - int(arrow_w * 0.4), top_arrow_y1,
        ax_center + int(arrow_w * 0.4), top_arrow_y1 + int(s * 0.08)
    ], fill=(255, 255, 255, 200))

    bot_arrow_y1 = p + int(inner * 0.85)
    bot_arrow_y2 = bot_arrow_y1 + arrow_h
    ald.polygon([
        (ax_center - arrow_w * 2, bot_arrow_y1),
        (ax_center, bot_arrow_y2),
        (ax_center + arrow_w * 2, bot_arrow_y1),
    ], fill=(255, 255, 255, 180))
    ald.rectangle([
        ax_center - int(arrow_w * 0.4), bot_arrow_y1 - int(s * 0.08),
        ax_center + int(arrow_w * 0.4), bot_arrow_y1
    ], fill=(255, 255, 255, 200))

    img.paste(shadow, (0, 0), shadow)
    img.paste(bg_grad, (0, 0), bg_grad)
    img.paste(accent, (0, 0), accent)
    img.paste(img_mtn, (0, 0), img_mtn)
    img.paste(arrow_layer, (0, 0), arrow_layer)

    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle([p, p, p + inner, p + inner], radius=int(s * 0.12), outline=(150, 200, 255, 60), width=max(1, int(s * 0.01)))
    img.paste(glow, (0, 0), glow)

    return img

def create_favicon(size=32):
    return create_logo(size)

def save_png(img, path):
    if path.endswith(".ico"):
        img_resized = img.resize((32, 32), Image.LANCZOS)
        img_rgba = img_resized.convert("RGBA")
        with open(path, "wb") as f:
            w, h = img_rgba.size
            data = img_rgba.tobytes()
            xor_data = []
            and_data = []
            for y in range(h):
                row = []
                for x in range(w):
                    r, g, b, a = img_rgba.getpixel((x, y))
                    row.extend([b, g, r])
                    if a < 128:
                        and_data.append(1)
                    else:
                        and_data.append(0)
                xor_data.extend(row)
            and_row_size = ((w + 31) // 32) * 4
            and_bytes = []
            for y in range(h):
                for x in range(0, w, 8):
                    byte = 0
                    for bit in range(8):
                        if x + bit < w:
                            idx = y * w + x + bit
                            byte |= (and_data[idx] << (7 - bit))
                    and_bytes.append(byte)
            xor_row_size = ((w * 3 + 3) // 4) * 4
            xor_size = xor_row_size * h
            and_size = and_row_size * h
            data_size = 40 + xor_size + and_size
            f.write(struct.pack('<HHH', 0, 1, 1))
            f.write(struct.pack('<I', 16))
            f.write(struct.pack('<I', data_size))
            f.write(struct.pack('<iiHH', w, h * 2, 1, 32))
            f.write(struct.pack('<I', 0))
            f.write(struct.pack('<I', xor_size))
            f.write(struct.pack('<I', 0))
            f.write(struct.pack('<I', 0))
            f.write(struct.pack('<I', 0))
            f.write(struct.pack('<I', 0))
            f.write(bytes(xor_data))
            f.write(bytes(and_bytes))
    else:
        img.save(path, "PNG")

def create_ico():
    img = create_logo(32)
    save_png(img, r"C:\mazanoke\favicon.ico")

create_ico()

for name, size in SIZES.items():
    path = os.path.join(OUT, name)
    img = create_logo(size)
    save_png(img, path)
    print(f"Created {path} ({size}x{size})")

print("Done!")
