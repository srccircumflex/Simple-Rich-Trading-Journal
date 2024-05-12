from src.config import color_theme, rc

notepaper = {
    "fontSize": "13px",
    "fontFamily": "monospace",
    "color": color_theme.notepaper_fg,
    "backgroundColor": color_theme.notepaper_bg + (color_theme.notepaper_def_transparency if rc.notePaperDefaultTransparency else ""),
    "border": "1px solid " + color_theme.notepaper_border
}
