"""
Shared UI styling constants.
Change values here to restyle the whole app at once.
"""

# Color palette - medical/professional theme
COLORS = {
    "bg":          "#F5F7FA",   # main background (soft gray-blue)
    "surface":     "#FFFFFF",   # card backgrounds
    "primary":     "#1E5F8E",   # deep medical blue
    "primary_hover": "#164a70",
    "accent":      "#2E8B97",   # teal accent
    "success":     "#27AE60",
    "warning":     "#E67E22",
    "danger":      "#C0392B",
    "text":        "#2C3E50",
    "text_muted":  "#7F8C8D",
    "border":      "#DDE3EA",
}

# Fonts (Tkinter accepts (family, size, style))
FONTS = {
    "title":     ("Helvetica", 26, "bold"),
    "heading":   ("Helvetica", 18, "bold"),
    "subheading":("Helvetica", 14, "bold"),
    "body":      ("Helvetica", 12),
    "body_bold": ("Helvetica", 12, "bold"),
    "small":     ("Helvetica", 10),
    "button":    ("Helvetica", 12, "bold"),
}

# Spacing
PAD_S = 5
PAD_M = 10
PAD_L = 20
PAD_XL = 30

# Window
APP_TITLE = "Hospital Medical Staff Management System"
WINDOW_W = 1100
WINDOW_H = 700
