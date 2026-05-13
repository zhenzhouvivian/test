from PIL import Image, ImageDraw, ImageFont

# Canvas: 3:4 ratio, high resolution for social media
W, H = 1080, 1440

# Color palette — warm, trustworthy, homey
BG_TOP   = (255, 248, 240)   # warm cream
BG_BOT   = (255, 238, 220)   # soft peach
CARD_CLR = (255, 255, 255)   # white cards
SHADOW   = (218, 198, 180)   # subtle shadow

ACCENT1  = (218, 88,  56)    # coral/terracotta — 工作内容
ACCENT2  = (45,  140, 190)   # sky blue          — 任职要求
ACCENT3  = (60,  165, 105)   # mint green        — 薪酬福利
GOLD     = (210, 155,  40)   # warm gold (accents)

TEXT_DARK = (45,  35,  30)
TEXT_MID  = (105, 88,  75)
WHITE     = (255, 255, 255)

FONT_REG  = "/workspace/fonts/NotoSansSC-Regular.otf"
FONT_BOLD = "/workspace/fonts/NotoSansSC-Bold.otf"


# ── Helpers ────────────────────────────────────────────────────────────────

def make_gradient(w, h, top, bot):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def shadow_card(draw, x0, y0, x1, y1, radius=18, offset=6):
    draw.rounded_rectangle([x0+offset, y0+offset, x1+offset, y1+offset],
                            radius=radius, fill=SHADOW)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=CARD_CLR)


def section_header(draw, x, y, w, h, color, label_char, title):
    """Colored banner with circle icon and title."""
    draw.rounded_rectangle([x, y, x+w, y+h], radius=14, fill=color)
    # White circle badge
    cx, cy = x + 44, y + h // 2
    r = 22
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=WHITE)
    # Icon character (Chinese ideogram — guaranteed in font)
    icon_f = ImageFont.truetype(FONT_BOLD, 20)
    bb = icon_f.getbbox(label_char)
    iw, ih = bb[2]-bb[0], bb[3]-bb[1]
    draw.text((cx - iw//2 - bb[0], cy - ih//2 - bb[1]), label_char,
              font=icon_f, fill=color)
    # Title text
    tf = ImageFont.truetype(FONT_BOLD, 28)
    draw.text((x + 82, y + h//2 - 15), title, font=tf, fill=WHITE)


def wrap_text(text, font, max_w):
    """Character-level wrap (works for Chinese + mixed text)."""
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        if font.getbbox(test)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_items(draw, items, x, y, max_w, dot_color, font, line_h=38, indent=28):
    cy = y
    for item in items:
        # Filled circle bullet
        draw.ellipse([x+2, cy+11, x+12, cy+21], fill=dot_color)
        lines = wrap_text(item, font, max_w - indent)
        for line in lines:
            draw.text((x + indent, cy), line, font=font, fill=TEXT_DARK)
            cy += line_h
        cy += 5
    return cy


def tag_pill(draw, x, y, text, bg, font, pad_x=18, pad_h=10):
    """Draw a pill-shaped tag and return its width."""
    bb = font.getbbox(text)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    pw, ph = tw + pad_x*2, th + pad_h*2
    draw.rounded_rectangle([x, y, x+pw, y+ph], radius=ph//2, fill=bg)
    draw.text((x + pad_x, y + pad_h - bb[1]), text, font=font, fill=WHITE)
    return pw


# ── Build image ────────────────────────────────────────────────────────────

img = make_gradient(W, H, BG_TOP, BG_BOT)
draw = ImageDraw.Draw(img)

# Triple-color top stripe
bar_h = 10
for i, col in enumerate([ACCENT1, ACCENT2, ACCENT3]):
    draw.rectangle([i * W//3, 0, (i+1)*W//3, bar_h], fill=col)

# ── TITLE SECTION ──────────────────────────────────────────────────────────
f_big   = ImageFont.truetype(FONT_BOLD, 52)
f_sub   = ImageFont.truetype(FONT_BOLD, 26)
f_body  = ImageFont.truetype(FONT_REG,  25)
f_small = ImageFont.truetype(FONT_REG,  21)
f_tag   = ImageFont.truetype(FONT_BOLD, 20)

ty = bar_h + 36

# Main title
title = "家庭助理招聘"
bb = f_big.getbbox(title)
draw.text(((W - (bb[2]-bb[0])) // 2, ty), title, font=f_big, fill=ACCENT1)

ty += bb[3] - bb[1] + 14

# Subtitle tags
tags = [("温馨家庭", ACCENT1), ("长期稳定", ACCENT2), ("月薪7000", ACCENT3)]
total_w = sum(f_tag.getbbox(t)[2] + 36 + 12 for t, _ in tags) - 12
sx = (W - total_w) // 2
for text, col in tags:
    pw = tag_pill(draw, sx, ty, text, col, f_tag, pad_x=18, pad_h=8)
    sx += pw + 12

ty += 44 + 16

# Decorative divider with diamond
dline_y = ty
draw.rectangle([80, dline_y+8, W-80, dline_y+11], fill=ACCENT1)
# Central diamond
cx = W // 2
pts = [(cx, dline_y), (cx+12, dline_y+9), (cx, dline_y+18), (cx-12, dline_y+9)]
draw.polygon(pts, fill=ACCENT1)

ty += 30

# ── CARD SETTINGS ──────────────────────────────────────────────────────────
CX    = 44
CW    = W - 88
PAD   = 30
LH    = 38
HDR_H = 58

# ── SECTION 1: 工作内容 ────────────────────────────────────────────────────
items1 = [
    "工作时间：09:00 – 18:30，午休 1.5 小时",
    "排班：做六休一（可协商做五休二）",
    "地点：泰欣嘉园（地铁 3/4/7 号线镇平路站上盖）",
    "职责：每日遛狗两次、烹饪三餐、陪同就医",
]
lines1 = sum(len(wrap_text(it, f_body, CW-PAD*2-28)) for it in items1)
h1 = HDR_H + PAD + lines1*LH + len(items1)*5 + PAD

shadow_card(draw, CX, ty, CX+CW, ty+h1)
section_header(draw, CX, ty, CW, HDR_H, ACCENT1, "工", "工作内容")
cy = draw_items(draw, items1, CX+PAD, ty+HDR_H+PAD, CW-PAD, ACCENT1, f_body, LH)

ty += h1 + 26

# ── SECTION 2: 任职要求 ────────────────────────────────────────────────────
items2 = [
    "性格温和、情绪稳定，善于维护家庭和谐氛围",
    "喜爱动物，擅长烹饪者优先",
    "熟练乘坐地铁，会用手机导航（需陪同就医）",
    "乐于学习新型家电：扫地机器人、厨师机等",
    "上班专注工作，午休外不沉迷手机",
    "年龄 35–50 岁，男女不限，初中及以上学历",
]
lines2 = sum(len(wrap_text(it, f_body, CW-PAD*2-28)) for it in items2)
h2 = HDR_H + PAD + lines2*LH + len(items2)*5 + PAD

shadow_card(draw, CX, ty, CX+CW, ty+h2)
section_header(draw, CX, ty, CW, HDR_H, ACCENT2, "求", "任职要求")
cy = draw_items(draw, items2, CX+PAD, ty+HDR_H+PAD, CW-PAD, ACCENT2, f_body, LH)

ty += h2 + 26

# ── SECTION 3: 薪酬福利 ────────────────────────────────────────────────────
items3 = [
    "月薪 7000 元（做六休一）；五休二可协商",
    "上岗前体检，费用由主家承担",
    "地铁直达，通勤极为便利",
    "家庭氛围和睦，工作环境舒心",
]
lines3 = sum(len(wrap_text(it, f_body, CW-PAD*2-28)) for it in items3)
h3 = HDR_H + PAD + lines3*LH + len(items3)*5 + PAD

shadow_card(draw, CX, ty, CX+CW, ty+h3)
section_header(draw, CX, ty, CW, HDR_H, ACCENT3, "福", "薪酬福利")
cy = draw_items(draw, items3, CX+PAD, ty+HDR_H+PAD, CW-PAD, ACCENT3, f_body, LH)

ty += h3 + 26

# ── SALARY HIGHLIGHT BANNER ────────────────────────────────────────────────
rem = H - 10 - ty  # remaining space above bottom bar
ban_h = max(66, min(80, rem - 20))
draw.rounded_rectangle([CX, ty, CX+CW, ty+ban_h], radius=16, fill=ACCENT1)
# Inner lighter rectangle for depth
draw.rounded_rectangle([CX+4, ty+4, CX+CW-4, ty+ban_h-4], radius=13,
                        fill=(232, 100, 65))
sal_f = ImageFont.truetype(FONT_BOLD, 30)
sal_t = "月薪 7000 元  ·  长期稳定  ·  真诚相邀"
bb = sal_f.getbbox(sal_t)
draw.text(((W-(bb[2]-bb[0]))//2, ty+(ban_h-(bb[3]-bb[1]))//2 - bb[1]),
          sal_t, font=sal_f, fill=WHITE)

ty += ban_h + 16

# ── FOOTER ─────────────────────────────────────────────────────────────────
foot_t = "地址：泰欣嘉园  |  镇平路地铁站（3/4/7号线）上盖  |  一狗两人  温馨之家"
bb = f_small.getbbox(foot_t)
draw.text(((W-(bb[2]-bb[0]))//2, ty), foot_t, font=f_small, fill=TEXT_MID)

# Bottom triple stripe
for i, col in enumerate([ACCENT3, ACCENT2, ACCENT1]):
    draw.rectangle([i * W//3, H-10, (i+1)*W//3, H], fill=col)

# ── SAVE ───────────────────────────────────────────────────────────────────
out = "/workspace/job_poster.png"
img.save(out, "PNG", dpi=(300, 300))
print(f"Saved {out}  size={img.size}")
print(f"Content ends at y={ty},  canvas H={H},  slack={H-ty-30} px")
