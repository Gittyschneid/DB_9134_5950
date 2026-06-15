"""
Shared UI styling constants.
Change values here to restyle the whole app at once.
"""

# Color palette — Enterprise Medical Dashboard
COLORS = {
    # Backgrounds
    "bg":            "#F8FAFC",   # slate 50 — main window background
    "surface":       "#FFFFFF",   # pure white — cards and panels
    "surface_alt":   "#F1F5F9",   # slate 100 — subtle alternate surface
    "sidebar":       "#0F172A",   # slate 900 — dark sidebar

    # Brand
    "primary":       "#2563EB",   # blue 600 — corporate, trustworthy
    "primary_hover": "#1D4ED8",   # blue 700
    "primary_light": "#EFF6FF",   # blue 50 — tinted backgrounds
    "accent":        "#0F172A",   # slate 900 — secondary actions
    "accent_hover":  "#1E293B",   # slate 800

    # Semantic
    "success":       "#16A34A",   # green 600
    "success_light": "#DCFCE7",   # green 50
    "warning":       "#D97706",   # amber 600
    "warning_light": "#FFFBEB",   # amber 50
    "danger":        "#DC2626",   # red 600
    "danger_light":  "#FEF2F2",   # red 50

    # Text
    "text":          "#0F172A",   # slate 900 — primary text
    "text_secondary":"#475569",   # slate 600 — secondary text
    "text_muted":    "#64748B",   # slate 500 — muted labels
    "text_on_primary":"#FFFFFF",  # white text on primary bg
    "text_sidebar":  "#F8FAFC",   # white text on dark sidebar

    # Borders & Dividers
    "border":        "#E2E8F0",   # slate 200
    "border_light":  "#F1F5F9",   # slate 100
    "divider":       "#CBD5E1",   # slate 300

    # Input
    "input_bg":      "#FFFFFF",
    "input_border":  "#94A3B8",   # slate 400
    "input_focus":   "#2563EB",   # blue 600
}

# Fonts — Larger, clearer, sophisticated
_FONT_FAMILY = "Helvetica" 

FONTS = {
    "title":      (_FONT_FAMILY, 28, "bold"),      # Increased from 24
    "heading":    (_FONT_FAMILY, 20, "bold"),      # Increased from 17
    "subheading": (_FONT_FAMILY, 16, "bold"),      # Increased from 13
    "body":       (_FONT_FAMILY, 14),              # Increased from 12
    "body_bold":  (_FONT_FAMILY, 14, "bold"),      # Increased from 12
    "small":      (_FONT_FAMILY, 12),              # Increased from 10
    "small_bold": (_FONT_FAMILY, 12, "bold"),      # Increased from 10
    "button":     (_FONT_FAMILY, 13, "bold"),      # Increased from 11
    "mono":       ("Menlo", 12),                   # Increased from 11
}

# Spacing scale (4px base)
PAD_XS = 6
PAD_S  = 12
PAD_M  = 20
PAD_L  = 32
PAD_XL = 48

# Window
APP_TITLE = "Hospital Management System"
WINDOW_W = 1280
WINDOW_H = 850

# Border radius simulation (for label-based buttons)
BTN_PADY = 10
BTN_PADX = 18
