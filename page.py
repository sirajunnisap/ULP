from __future__ import annotations

from typing import Dict, Optional, Tuple

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font as tkfont


def get_page_dimensions(page_size: str) -> Optional[Tuple[int, int]]:
    """Return (height_mm, width_mm) for a given page size.

    Keys are normalized to upper-case. Dimensions are in millimeters.
    """
    sizes: Dict[str, Tuple[int, int]] = {
        "A4": (297, 210),
        "A5": (210, 148),
        "LETTER": (279, 216),
        "LEGAL": (356, 216),
    }
    normalized_key = page_size.strip().upper()
    return sizes.get(normalized_key)


def get_line_height(handwriting: str) -> Optional[int]:
    """Return line height in millimeters for a handwriting size key."""
    styles: Dict[str, int] = {
        "small": 5,
        "medium": 7,
        "large": 10,
    }
    normalized_key = handwriting.strip().lower()
    return styles.get(normalized_key)


def calculate_lines(page_height_mm: float, line_height_mm: float) -> int:
    """Return floored number of lines that fit into the given height."""
    if line_height_mm <= 0:
        return 0
    return int(page_height_mm // line_height_mm)


def run_cli() -> None:
    print("📝 Line Estimator Program 📝")

    page_size = input("Enter page size (A4, A5, Letter, Legal): ").strip()
    dimensions = get_page_dimensions(page_size)
    if not dimensions:
        print("❌ Invalid page size.")
        return

    handwriting = input("Enter handwriting size (small, medium, large): ").strip()
    line_height = get_line_height(handwriting)
    if not line_height:
        print("❌ Invalid handwriting size.")
        return

    orientation = input("Orientation (portrait/landscape) [portrait]: ").strip().lower() or "portrait"
    page_height = dimensions[0] if orientation == "portrait" else dimensions[1]

    try:
        top_margin = float(input("Top margin in mm [0]: ") or 0)
        bottom_margin = float(input("Bottom margin in mm [0]: ") or 0)
    except ValueError:
        print("❌ Margins must be numbers.")
        return

    usable_height = max(0.0, page_height - (top_margin + bottom_margin))
    num_lines = calculate_lines(usable_height, float(line_height))
    print(
        f"\n✅ Approximately {num_lines} lines on a {page_size.upper()} page "
        f"({orientation}) with {handwriting.lower()} handwriting."
    )


def run_gui() -> None:
    """Launch an enhanced GUI for the line estimator using Tkinter."""
    root = tk.Tk()
    root.title("Line Estimator")

    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass

    # Configure default application font via Tk named font API
    try:
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
    except Exception:
        pass

    style = ttk.Style()
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("Section.TLabelframe", padding=12)
    style.configure("Section.TLabelframe.Label", font=("Segoe UI", 10, "bold"))
    style.configure("Result.TLabel", font=("Segoe UI", 11))
    style.configure("Accent.TButton", padding=6)

    container = ttk.Frame(root, padding=16)
    container.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # State variables
    page_size_var = tk.StringVar(value="A4")
    handwriting_var = tk.StringVar(value="medium")
    orientation_var = tk.StringVar(value="portrait")
    top_margin_var = tk.StringVar(value="8")
    bottom_margin_var = tk.StringVar(value="8")
    result_var = tk.StringVar(value="")
    meta_var = tk.StringVar(value="")

    # Title
    header = ttk.Frame(container)
    header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
    ttk.Label(header, text="📝 Line Estimator", style="Title.TLabel").grid(
        row=0, column=0, sticky="w"
    )

    # Left: Controls
    controls = ttk.Labelframe(container, text="Inputs", style="Section.TLabelframe")
    controls.grid(row=1, column=0, sticky="nsew", padx=(0, 12))

    ttk.Label(controls, text="Page size").grid(row=0, column=0, sticky="w")
    page_sizes_display = ["A4", "A5", "Letter", "Legal"]
    page_size_combo = ttk.Combobox(
        controls,
        textvariable=page_size_var,
        values=page_sizes_display,
        state="readonly",
        width=14,
    )
    page_size_combo.grid(row=0, column=1, sticky="w", padx=(8, 0))

    ttk.Label(controls, text="Orientation").grid(row=1, column=0, sticky="w", pady=(8, 0))
    orientation_frame = ttk.Frame(controls)
    orientation_frame.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
    ttk.Radiobutton(
        orientation_frame, text="Portrait", value="portrait", variable=orientation_var
    ).grid(row=0, column=0, sticky="w")
    ttk.Radiobutton(
        orientation_frame, text="Landscape", value="landscape", variable=orientation_var
    ).grid(row=0, column=1, sticky="w", padx=(8, 0))

    ttk.Label(controls, text="Handwriting").grid(row=2, column=0, sticky="w")
    handwriting_combo = ttk.Combobox(
        controls,
        textvariable=handwriting_var,
        values=["small", "medium", "large"],
        state="readonly",
        width=14,
    )
    handwriting_combo.grid(row=2, column=1, sticky="w", padx=(8, 0))

    ttk.Label(controls, text="Top margin").grid(row=3, column=0, sticky="w", pady=(8, 0))
    top_margin_entry = ttk.Entry(controls, textvariable=top_margin_var, width=10)
    top_margin_entry.grid(row=3, column=1, sticky="w", padx=(8, 4), pady=(8, 0))
    ttk.Label(controls, text="mm").grid(row=3, column=1, sticky="e", padx=(0, 0), pady=(8, 0))

    ttk.Label(controls, text="Bottom margin").grid(row=4, column=0, sticky="w")
    bottom_margin_entry = ttk.Entry(controls, textvariable=bottom_margin_var, width=10)
    bottom_margin_entry.grid(row=4, column=1, sticky="w", padx=(8, 4))
    ttk.Label(controls, text="mm").grid(row=4, column=1, sticky="e")

    action_btn = ttk.Button(controls, text="Calculate", style="Accent.TButton")
    action_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    # Right: Preview and results
    right = ttk.Labelframe(container, text="Preview", style="Section.TLabelframe")
    right.grid(row=1, column=1, sticky="nsew")

    canvas = tk.Canvas(right, width=260, height=360, highlightthickness=0, bg="#f7f8fa")
    canvas.grid(row=0, column=0, sticky="nsew")

    result_label = ttk.Label(right, textvariable=result_var, style="Result.TLabel")
    result_label.grid(row=1, column=0, sticky="w", pady=(8, 0))

    meta_label = ttk.Label(right, textvariable=meta_var)
    meta_label.grid(row=2, column=0, sticky="w")

    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    controls.columnconfigure(1, weight=1)
    right.columnconfigure(0, weight=1)
    right.rowconfigure(0, weight=1)

    def parse_margins() -> Optional[Tuple[float, float]]:
        try:
            return float(top_margin_var.get() or 0), float(bottom_margin_var.get() or 0)
        except ValueError:
            return None

    def draw_preview(dimensions: Tuple[int, int], orientation: str, top_mm: float, bottom_mm: float, line_h_mm: int, lines: int) -> None:
        canvas.delete("all")

        page_h = dimensions[0] if orientation == "portrait" else dimensions[1]
        page_w = dimensions[1] if orientation == "portrait" else dimensions[0]

        pad = 12
        max_w = canvas.winfo_width() - pad * 2
        max_h = canvas.winfo_height() - pad * 2

        scale = min(max_w / page_w, max_h / page_h)
        scaled_w = page_w * scale
        scaled_h = page_h * scale

        x0 = (canvas.winfo_width() - scaled_w) / 2
        y0 = (canvas.winfo_height() - scaled_h) / 2
        x1 = x0 + scaled_w
        y1 = y0 + scaled_h

        canvas.create_rectangle(x0, y0, x1, y1, fill="#ffffff", outline="#cfd6e4")

        tm = max(0.0, top_mm) * scale
        bm = max(0.0, bottom_mm) * scale
        # Top margin band
        canvas.create_rectangle(x0, y0, x1, y0 + tm, fill="#eef2fb", outline="")
        # Bottom margin band
        canvas.create_rectangle(x0, y1 - bm, x1, y1, fill="#eef2fb", outline="")

        content_top = y0 + tm
        content_bottom = y1 - bm
        content_height = max(0.0, content_bottom - content_top)

        if content_height > 0 and line_h_mm > 0 and lines > 0:
            px_per_line = content_height / lines
            y = content_top
            for _ in range(lines):
                canvas.create_line(x0 + 8, y, x1 - 8, y, fill="#d7deea")
                y += px_per_line

    def calculate_and_update(event: Optional[tk.Event] = None) -> None:
        dims = get_page_dimensions(page_size_var.get())
        line_height_mm = get_line_height(handwriting_var.get())
        margins = parse_margins()

        if not dims or not line_height_mm or margins is None:
            result_var.set("Enter valid inputs to see results.")
            meta_var.set("")
            canvas.delete("all")
            return

        top_mm, bottom_mm = margins
        page_height = dims[0] if orientation_var.get() == "portrait" else dims[1]
        usable_height = max(0.0, page_height - (top_mm + bottom_mm))
        lines = calculate_lines(usable_height, float(line_height_mm))

        result_var.set(f"≈ {lines} lines")
        human_page = page_size_var.get().upper()
        human_orient = orientation_var.get()
        meta_var.set(
            f"{human_page} ({human_orient}) • Page: {dims[0]}×{dims[1]} mm • Usable height: {usable_height:.1f} mm"
        )

        draw_preview(dims, orientation_var.get(), top_mm, bottom_mm, int(line_height_mm), lines)

    # Bind interactions
    action_btn.configure(command=calculate_and_update)
    page_size_combo.bind("<<ComboboxSelected>>", calculate_and_update)
    handwriting_combo.bind("<<ComboboxSelected>>", calculate_and_update)
    orientation_frame.bind_all("<Return>", calculate_and_update)
    top_margin_entry.bind("<KeyRelease>", calculate_and_update)
    bottom_margin_entry.bind("<KeyRelease>", calculate_and_update)

    # Initial layout sizing and first draw
    root.update_idletasks()
    root.minsize(680, 460)
    calculate_and_update()

    root.mainloop()


if __name__ == "__main__":
    # Default to GUI for a better user experience. Use run_cli() if preferred.
    run_gui()
