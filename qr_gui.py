#!/usr/bin/env python3
"""Simple Tkinter GUI for the SVG QR Code generator.

This wraps `SVGQRGenerator` from `qr_generator.py` and provides
file choosers for output and logo, color inputs, and a Generate button.
"""

import threading
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from qr_generator import SVGQRGenerator
except Exception as e:
    # Will raise at runtime if imports fail; keep module importable for tests
    SVGQRGenerator = None


class QRGui(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=12)
        self.master = master
        self.master.title('QR Code Generator')
        self.grid(sticky='nsew')

        self.generator = SVGQRGenerator() if SVGQRGenerator else None

        # Variables
        self.data_var = tk.StringVar(value='https://example.com')
        self.output_var = tk.StringVar(value='qr_output.svg')
        self.logo_var = tk.StringVar(value='')
        self.fill_var = tk.StringVar(value='black')
        self.back_var = tk.StringVar(value='white')
        self.box_size_var = tk.IntVar(value=10)
        self.border_var = tk.IntVar(value=4)
        self.logo_size_var = tk.DoubleVar(value=0.2)
        self.format_var = tk.StringVar(value='SVG')
        self.format_var.trace_add('write', self._on_format_change)

        self._build_ui()

    def _build_ui(self):
        # Data
        ttk.Label(self, text='Data:').grid(column=0, row=0, sticky='w')
        ttk.Entry(self, textvariable=self.data_var, width=60).grid(column=1, row=0, columnspan=3, sticky='ew')

        # Output
        ttk.Label(self, text='Output file:').grid(column=0, row=1, sticky='w')
        ttk.Entry(self, textvariable=self.output_var, width=48).grid(column=1, row=1, sticky='ew')
        ttk.Button(self, text='Browse', command=self.browse_output).grid(column=2, row=1, sticky='w')

        # Logo
        ttk.Label(self, text='Logo (optional):').grid(column=0, row=2, sticky='w')
        ttk.Entry(self, textvariable=self.logo_var, width=48).grid(column=1, row=2, sticky='ew')
        ttk.Button(self, text='Browse', command=self.browse_logo).grid(column=2, row=2, sticky='w')

        # Colors
        ttk.Label(self, text='Fill color:').grid(column=0, row=3, sticky='w')
        ttk.Entry(self, textvariable=self.fill_var, width=20).grid(column=1, row=3, sticky='w')
        ttk.Label(self, text='Background:').grid(column=2, row=3, sticky='w')
        ttk.Entry(self, textvariable=self.back_var, width=20).grid(column=3, row=3, sticky='w')

        # Box size / border / logo size
        ttk.Label(self, text='Box size:').grid(column=0, row=4, sticky='w')
        ttk.Spinbox(self, from_=1, to=100, textvariable=self.box_size_var, width=8).grid(column=1, row=4, sticky='w')
        ttk.Label(self, text='Border:').grid(column=2, row=4, sticky='w')
        ttk.Spinbox(self, from_=0, to=20, textvariable=self.border_var, width=8).grid(column=3, row=4, sticky='w')

        ttk.Label(self, text='Logo size ratio:').grid(column=0, row=5, sticky='w')
        ttk.Spinbox(self, from_=0.05, to=0.5, increment=0.01, format='%.2f', textvariable=self.logo_size_var, width=8).grid(column=1, row=5, sticky='w')

        # Format
        ttk.Label(self, text='Format:').grid(column=0, row=6, sticky='w')
        fmt_frame = ttk.Frame(self)
        fmt_frame.grid(column=1, row=6, sticky='w', columnspan=3)
        ttk.Radiobutton(fmt_frame, text='SVG', variable=self.format_var, value='SVG').pack(side='left', padx=(0, 10))
        ttk.Radiobutton(fmt_frame, text='PNG', variable=self.format_var, value='PNG').pack(side='left')

        # Generate button and status
        self.generate_btn = ttk.Button(self, text='Generate', command=self.on_generate)
        self.generate_btn.grid(column=1, row=7, sticky='w', pady=(8,0))

        self.open_btn = ttk.Button(self, text='Open Output', command=self.open_output)
        self.open_btn.grid(column=2, row=7, sticky='w', pady=(8,0))

        self.status_var = tk.StringVar(value='Ready')
        ttk.Label(self, textvariable=self.status_var).grid(column=0, row=8, columnspan=4, sticky='w', pady=(8,0))

        for i in range(4):
            self.columnconfigure(i, weight=1)

    def _on_format_change(self, *_):
        """Auto-update the output file extension when the format changes."""
        current = self.output_var.get().strip()
        if not current:
            return
        p = Path(current)
        new_ext = '.svg' if self.format_var.get() == 'SVG' else '.png'
        if p.suffix.lower() in ('.svg', '.png'):
            self.output_var.set(str(p.with_suffix(new_ext)))

    def browse_output(self):
        is_svg = self.format_var.get() == 'SVG'
        ext = '.svg' if is_svg else '.png'
        ftypes = [('SVG files', '*.svg'), ('All files', '*.*')] if is_svg else [('PNG files', '*.png'), ('All files', '*.*')]
        path = filedialog.asksaveasfilename(defaultextension=ext, filetypes=ftypes)
        if path:
            self.output_var.set(path)

    def browse_logo(self):
        path = filedialog.askopenfilename(filetypes=[('Image files','*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.svg'),('All files','*.*')])
        if path:
            self.logo_var.set(path)

    def set_status(self, text):
        self.status_var.set(text)
        self.master.update_idletasks()

    def on_generate(self):
        if not self.generator:
            messagebox.showerror('Error', 'SVGQRGenerator could not be imported. Check dependencies.')
            return

        data = self.data_var.get().strip()
        output = self.output_var.get().strip()
        logo = self.logo_var.get().strip() or None

        if not data:
            messagebox.showwarning('Missing data', 'Please provide data to encode in the QR code.')
            return

        # Disable UI while generating
        self.generate_btn.config(state='disabled')
        self.set_status('Generating...')

        def worker():
            try:
                common = dict(
                    data=data,
                    output_path=output if output else None,
                    logo_path=logo,
                    fill_color=self.fill_var.get().strip() or 'black',
                    back_color=self.back_var.get().strip() or 'white',
                    box_size=int(self.box_size_var.get()),
                    border=int(self.border_var.get()),
                    logo_size_ratio=float(self.logo_size_var.get())
                )
                if self.format_var.get() == 'PNG':
                    self.generator.generate_qr_png(**common)
                else:
                    self.generator.generate_qr_svg(**common)

                self.set_status(f'Saved: {output}')
                # Offer to open the file
                try:
                    if output:
                        os.startfile(output)
                except Exception:
                    pass

            except Exception as e:
                messagebox.showerror('Error', f'Failed to generate QR: {e}')
                self.set_status('Error')
            finally:
                self.generate_btn.config(state='normal')

        threading.Thread(target=worker, daemon=True).start()

    def open_output(self):
        out = self.output_var.get().strip()
        if not out or not Path(out).exists():
            messagebox.showinfo('Not found', 'Output file not found. Generate first or choose a valid file.')
            return
        try:
            os.startfile(out)
        except Exception as e:
            messagebox.showerror('Error', f'Cannot open file: {e}')


def main():
    root = tk.Tk()
    root.geometry('760x370')
    app = QRGui(master=root)
    root.mainloop()


if __name__ == '__main__':
    # Quick CLI path for automated checks: `python -c "import qr_gui; print('ok')"`
    main()
