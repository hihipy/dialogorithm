"""
dialogorithm.py — Dialogorithm GUI application.

Provides a Tkinter-based interface for selecting a country, entering a
local phone number, choosing a signature line, and generating a PNG image
where each digit of the number is replaced by a PhD-level mathematical
expression via ``latex_processor``.

Run directly::

    python dialogorithm.py
"""

import os
import shutil
import sys

# Modules live in support_files/
_HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(_HERE, "support_files"))

# --- Logging: off by default, user can enable via GUI checkbox ---
import logging

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.NullHandler())

_log_file_handler = None  # Created on first enable, reused on subsequent toggles


class _ColorFormatter(logging.Formatter):
	"""Compact colored formatter for terminal output."""
	RESET = "\x1b[0m"
	STYLES = {
		logging.DEBUG: "\x1b[38;5;240m",  # dark gray
		logging.INFO: "\x1b[97m",  # bright white
		logging.WARNING: "\x1b[93m",  # yellow
		logging.ERROR: "\x1b[91m",  # bright red
		logging.CRITICAL: "\x1b[1;91m",  # bold bright red
	}

	def format(self, record):
		color = self.STYLES.get(record.levelno, self.RESET)
		time = self.formatTime(record, "%H:%M:%S")
		level = f"{record.levelname:<8}"
		return f"{color}{time}  {level}  {record.getMessage()}{self.RESET}"


_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.DEBUG)
_console_handler.setFormatter(_ColorFormatter())
logging.getLogger().addHandler(_console_handler)


def _toggle_logging(*_) -> None:
	"""Attach or detach the file log handler based on the checkbox state."""
	global _log_file_handler
	root_logger = logging.getLogger()
	if logging_var.get():
		if _log_file_handler is None:
			_log_file_handler = logging.FileHandler(
				os.path.join(Path.home(), "Downloads", "dialogorithm.log"),
				mode="a", encoding="utf-8"
			)
			_log_file_handler.setLevel(logging.DEBUG)
			_log_file_handler.setFormatter(logging.Formatter(
				fmt="%(asctime)s  %(name)-28s  %(levelname)-8s  %(funcName)s: %(message)s",
				datefmt="%Y-%m-%d %H:%M:%S"
			))
		if _log_file_handler not in root_logger.handlers:
			root_logger.addHandler(_log_file_handler)
	else:
		if _log_file_handler and _log_file_handler in root_logger.handlers:
			root_logger.removeHandler(_log_file_handler)


import threading
import tkinter as tk
from tkinter import messagebox, ttk
import latex_processor
import logging
import random
from pathlib import Path
import traceback

# Suppress macOS GUI warnings
if sys.platform == "darwin":  # macOS
	os.environ['TK_SILENCE_DEPRECATION'] = '1'

from phone_formats import (
	ALL_COUNTRIES,
	extract_country_code_from_label,
	get_digit_limit,
	format_display_number,
	validate_digit_input,
	get_countries_by_continent_and_subregion,
	get_continent_structure,
	get_special_prefixes,
)

# --- SOPHISTICATED DEBUG SYSTEM ---

logger = logging.getLogger("dialogorithm")


# --- Signature Line Generator ---
def get_signature_line() -> str:
	"""Return a random signature line for use above the phone number equations."""
	options = [
		"Please call me at:", "Contact me:", "Reach out via:", "Phone:", "Business line:",
		"Available at:", "You can reach me at:", "My direct line:", "Telephone:", "Feel free to call:",
		"For further assistance:", "Professional contact:", "Main line:", "Office line:", "Direct dial:",
		"Kindly reach out at:", "Primary contact:", "Call for inquiries:", "Reach my desk at:",
		"Client services line:"
	]
	return random.choice(options)


def get_downloads_dir() -> Path:
	"""Return the path to the current user's Downloads folder."""
	home = Path.home()
	return home / "Downloads"


# --- GUI Logic ---
def on_continent_select(_event) -> None:
	"""Populate the subregion dropdown when a continent is chosen."""
	continent = continent_var.get()
	subregion_combo['values'] = []
	country_combo['values'] = []
	subregion_var.set("")
	country_var.set("")
	entry_local.config(state='disabled')
	format_label.config(text="Choose a subregion below")
	country_code_label.config(text="+")
	formatted_display.config(text="")
	local_number_var.set("")

	if continent == "All Continents":
		all_subregions = sorted({
			sub for sublist in get_continent_structure().values() for sub in sublist
		})
		subregion_combo['values'] = all_subregions
	else:
		subregions = get_continent_structure().get(continent, [])
		subregion_combo['values'] = subregions


def on_subregion_select(_event) -> None:
	"""Populate the country dropdown when a subregion is chosen."""
	continent = continent_var.get()
	subregion = subregion_var.get()
	country_var.set("")
	entry_local.config(state='disabled')
	format_label.config(text="Choose a country below")
	country_code_label.config(text="+")
	formatted_display.config(text="")
	local_number_var.set("")

	countries = get_countries_by_continent_and_subregion(continent=continent, subregion=subregion)
	country_combo['values'] = countries


def on_country_select(_event) -> None:
	"""Update the country code label, enable the phone entry, and populate number type options."""
	country = country_var.get()
	if not country:
		return

	format_example = ALL_COUNTRIES.get(country, "")
	format_label.config(text=f"Format: {format_example}")

	code, region = extract_country_code_from_label(country)
	if code is not None:
		country_code_label.config(text=f"+{code}")
		local_number_var.set("")
		entry_local.config(state='normal')
		entry_local.icursor(0)
		entry_local.focus_set()
		formatted_display.config(text="")

		# Populate number type dropdown if special prefixes exist
		prefixes = get_special_prefixes(code)
		if prefixes:
			type_options = ["Standard (no prefix)"] + list(prefixes.keys())
			number_type_combo.config(state='readonly')
			number_type_combo['values'] = type_options
			number_type_var.set("Standard (no prefix)")
			number_type_frame.pack(pady=(5, 0))
		else:
			number_type_var.set("")
			number_type_combo['values'] = []
			number_type_combo.config(state='disabled')
			number_type_frame.pack_forget()

		limit = get_digit_limit(code)
		logger.debug("Selected %s: +%s, max %d local digits", country, code, limit)
	else:
		country_code_label.config(text="+")
		local_number_var.set("")
		entry_local.config(state='disabled')
		formatted_display.config(text="")
		number_type_var.set("")
		number_type_combo['values'] = []
		number_type_frame.pack_forget()


def create_validation():
	"""Return a Tkinter validation callback that enforces per-country digit limits.

	The inner function reads the actual field content directly (rather than
	relying on Tkinter's ``%P`` proposed-value parameter, which can be
	unreliable) and rejects any character that would push the digit count
	above the country's local maximum.
	"""
	"""Create validation function that uses ACTUAL field content instead of Tkinter's misleading parameter"""

	def validate(char, proposed_value):
		try:
			# Empty char means a deletion (backspace/delete) — always allow
			if not char:
				return True

			actual_current = entry_local.get() if 'entry_local' in globals() else ""

			# Only allow digits for insertions
			if not char.isdigit():
				logger.debug("Validation REJECT: non-digit '%s'", char)
				return False

			# Get country code from label
			country_code_text = country_code_label['text']
			if country_code_text == '+':
				return len(actual_current + char) <= 15

			try:
				country_code = int(country_code_text.replace('+', ''))
				max_digits = get_digit_limit(country_code)
				new_length = len(actual_current + char)  # Use ACTUAL current content
				will_accept = new_length <= max_digits

				decision = "ACCEPT" if will_accept else "REJECT"
				logger.debug(
					f"Validation {decision}: '{char}' → '{actual_current + char}' ({new_length}/{max_digits}) +{country_code}")
				return will_accept

			except Exception as parse_err:
				logger.error(f"Validation parse error: {parse_err}")
				return len(actual_current + char) <= 15

		except Exception as validation_err:
			logger.error(f"Validation error: {validation_err}")
			return False

	return validate


def on_number_change(*_) -> None:
	"""Format and display the phone number as the user types."""
	try:
		country = country_var.get()
		if not country:
			return

		code, region = extract_country_code_from_label(country)
		raw_number = local_number_var.get()

		clean_number = "".join(filter(str.isdigit, raw_number))

		if clean_number != raw_number:
			local_number_var.set(clean_number)
			return

		if code and clean_number:
			format_template = ALL_COUNTRIES.get(country, "")
			formatted = format_display_number(clean_number, code, format_template)
			formatted_display.config(text=f"+{code} {formatted}")

			current_length = len(clean_number)
			max_length = get_digit_limit(code)
			logger.debug("Input: %d/%d digits  '%s' → '%s'",
			             current_length, max_length, clean_number, formatted)

			try:
				entry_local.icursor(tk.END)
				entry_local.xview_moveto(1.0)
			except Exception:
				pass
		else:
			formatted_display.config(text="")

	except Exception as err:
		logger.error("Number change error: %s", err)


def on_number_type_select(_event) -> None:
	"""Pre-fill the phone entry with the selected number type prefix."""
	country = country_var.get()
	if not country:
		return
	code, _ = extract_country_code_from_label(country)
	if not code:
		return

	selected_type = number_type_var.get()
	if selected_type == "Standard (no prefix)" or not selected_type:
		local_number_var.set("")
		entry_local.focus_set()
		return

	prefixes = get_special_prefixes(code)
	prefix_list = prefixes.get(selected_type, [])
	if prefix_list:
		# Pre-fill with the first (most common) prefix for this type
		local_number_var.set(prefix_list[0])
		entry_local.icursor(tk.END)
		entry_local.focus_set()
		logger.debug("Pre-filled prefix '%s' for type '%s'", prefix_list[0], selected_type)


def clear_number() -> None:
	"""Clear the phone entry field and reset the number type selector."""
	local_number_var.set("")
	number_type_var.set("Standard (no prefix)")
	formatted_display.config(text="")
	entry_local.focus_set()


def on_paste(event) -> str:
	"""Intercept paste events and strip non-digit characters before inserting.

	Handles any clipboard format: (786) 212-6394, 786-212-6394,
	+1 786 212 6394, etc.  Only the digit characters are inserted.
	"""
	try:
		raw = root.clipboard_get()
		digits_only = "".join(filter(str.isdigit, raw))
		if digits_only:
			entry_local.delete(0, tk.END)
			entry_local.insert(0, digits_only)
			logger.debug("Paste cleaned: '%s' → '%s'", raw[:40], digits_only)
	except Exception as err:
		logger.error("Paste handler error: %s", err)
	return "break"  # prevent Tkinter's default paste from also firing


def open_preview_popout(temp_path: str) -> None:
	"""Open a popout window showing the generated image with Save / Discard options.

	Includes a filename entry field and optional Browse button to change the
	save location.  The preview is shown at the image's native resolution,
	scrollable if wider than the screen.

	Args:
		temp_path: Path to the PNG in the system temp directory.
	"""
	from PIL import Image, ImageTk
	import tkinter.filedialog as filedialog

	popout = tk.Toplevel(root)
	popout.title("Dialogorithm — Preview")
	popout.resizable(True, True)
	popout.configure(bg="#1e1e2e")
	popout.grab_set()

	# ── Image — scaled to fit window, full-res saved separately ──────────────
	try:
		img = Image.open(temp_path)
		w, h = img.size

		# Scale down to fit comfortably on screen — max 1200px wide
		max_w = min(1200, root.winfo_screenwidth() - 100)
		if w > max_w:
			scale = max_w / w
			display_w = int(w * scale)
			display_h = int(h * scale)
			display_img = img.resize((display_w, display_h), Image.Resampling.LANCZOS)
		else:
			display_img = img
			display_w, display_h = w, h

		canvas_frame = tk.Frame(popout, bg="#1e1e2e")
		canvas_frame.pack(fill="both", expand=True, padx=15, pady=(15, 5))

		canvas = tk.Canvas(canvas_frame, width=display_w, height=display_h + 4,
		                   bg="white", highlightthickness=0)

		photo = ImageTk.PhotoImage(display_img)
		canvas.create_image(0, 0, anchor="nw", image=photo)
		canvas.image = photo
		canvas.configure(scrollregion=(0, 0, display_w, display_h))
		canvas.pack(side="top")

	except Exception as err:
		tk.Label(popout, text=f"Could not load preview:\n{err}",
		         font=("Arial", 11), fg="#ff6b6b", bg="#1e1e2e",
		         padx=20, pady=20).pack()

	# ── Filename + save location ──────────────────────────────────────────────
	save_frame = tk.Frame(popout, bg="#1e1e2e", pady=8)
	save_frame.pack(fill="x", padx=15)

	tk.Label(save_frame, text="Filename:", font=("Arial", 11),
	         fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=0, sticky="e", padx=(0, 6))

	filename_var = tk.StringVar(value="Dialogorithm_Contact")
	filename_entry = tk.Entry(save_frame, textvariable=filename_var,
	                          font=("Arial", 11), width=28)
	filename_entry.grid(row=0, column=1, sticky="w")

	tk.Label(save_frame, text=".png", font=("Arial", 11),
	         fg="#a6adc8", bg="#1e1e2e").grid(row=0, column=2, sticky="w", padx=(2, 16))

	save_dir_var = tk.StringVar(value=str(Path.home() / "Downloads"))

	tk.Label(save_frame, text="Save to:", font=("Arial", 11),
	         fg="#cdd6f4", bg="#1e1e2e").grid(row=1, column=0, sticky="e", padx=(0, 6), pady=(6, 0))

	dir_label = tk.Label(save_frame, textvariable=save_dir_var,
	                     font=("Arial", 10), fg="#89b4fa", bg="#1e1e2e",
	                     anchor="w", width=32)
	dir_label.grid(row=1, column=1, sticky="w", pady=(6, 0))

	def browse_dir():
		chosen = filedialog.askdirectory(initialdir=save_dir_var.get(),
		                                 title="Choose save folder")
		if chosen:
			save_dir_var.set(chosen)

	tk.Button(save_frame, text="Browse…", command=browse_dir,
	          font=("Arial", 10, "bold"),
	          highlightbackground="#89b4fa", highlightthickness=2,
	          cursor="hand2").grid(row=1, column=2, sticky="w",
	                               padx=(2, 0), pady=(6, 0))

	# ── Action buttons ────────────────────────────────────────────────────────
	btn_frame = tk.Frame(popout, bg="#1e1e2e", pady=14)
	btn_frame.pack()

	def save_and_close():
		"""Copy the temp PNG to the chosen location and close the popout."""
		raw_name = filename_var.get().strip() or "Dialogorithm_Contact"
		fname = raw_name if raw_name.lower().endswith(".png") else raw_name + ".png"
		dest = os.path.join(save_dir_var.get(), fname)
		try:
			shutil.copy(temp_path, dest)
			_cleanup_temp(temp_path)
			status_label.config(text=f"✅  Saved: {dest}", fg="#a6e3a1")
			logger.info("Saved: %s", dest)
		except Exception as err:
			messagebox.showerror("Save failed", str(err))
			logger.error("Save failed: %s", err)
			return
		popout.destroy()

	def discard_and_close():
		"""Delete the temp PNG and close without saving."""
		_cleanup_temp(temp_path)
		status_label.config(text="Discarded — nothing saved.", fg="#a6adc8")
		logger.debug("Preview discarded.")
		popout.destroy()

	tk.Button(
		btn_frame, text="Save", command=save_and_close,
		font=("Arial", 13, "bold"), width=14, height=2,
		highlightbackground="#2ecc71", highlightthickness=3,
		cursor="hand2",
	).grid(row=0, column=0, padx=14)

	tk.Button(
		btn_frame, text="Discard", command=discard_and_close,
		font=("Arial", 13, "bold"), width=14, height=2,
		highlightbackground="#e74c3c", highlightthickness=3,
		cursor="hand2",
	).grid(row=0, column=1, padx=14)

	popout.protocol("WM_DELETE_WINDOW", discard_and_close)


def _cleanup_temp(path: str) -> None:
	"""Delete the temp PNG and its parent directory if it was ours."""
	try:
		parent = os.path.dirname(path)
		if os.path.exists(path):
			os.remove(path)
		if os.path.isdir(parent) and "dialogorithm_" in os.path.basename(parent):
			os.rmdir(parent)
	except Exception as err:
		logger.warning("Temp cleanup failed: %s", err)


def on_generate() -> None:
	"""Validate input and kick off background LaTeX generation."""
	country = country_var.get()
	if not country:
		messagebox.showwarning("Input Error", "Please select a country first.")
		return

	code, region = extract_country_code_from_label(country)
	local_part = "".join(filter(str.isdigit, local_number_var.get()))

	if not local_part or len(local_part) < 4:
		messagebox.showwarning("Input Error", "Please enter a valid local number with at least 4 digits.")
		return
	if not code:
		messagebox.showwarning("Input Error", "Please select a country and enter a phone number.")
		return

	max_digits = get_digit_limit(code)
	if len(local_part) > max_digits:
		messagebox.showwarning("Input Error",
		                       f"Phone number too long. {country} allows maximum {max_digits} local digits.")
		return

	formatted_local = format_display_number(local_part, code)
	full_international = f"+{code} {formatted_local}"

	signature_option = signature_var.get()
	if signature_option == "Random":
		signature_text = get_signature_line()
	elif signature_option == "Custom":
		signature_text = custom_signature_var.get().strip() or "Please call me at:"
	else:
		signature_text = signature_option

	# Lock the UI and kick off background generation
	generate_button.config(state='disabled', text="⏳ Generating...")
	status_label.config(text="Compiling LaTeX — this takes a few seconds...", fg="#886600")
	root.update_idletasks()

	logger.info(f"Generating LaTeX for {full_international} with signature: {signature_text}")
	thread = threading.Thread(
		target=_generation_worker,
		args=(full_international, signature_text),
		daemon=True
	)
	thread.start()


def _generation_worker(full_international: str, signature_text: str) -> None:
	"""Run LaTeX generation in a background thread.

	Uses ``root.after`` to push GUI updates back to the main thread on
	completion or failure.
	"""
	"""Runs in a background thread. Uses root.after to push GUI updates back to the main thread."""
	try:
		output_path = latex_processor.generate_latex_for_number(full_international, signature_text)
		root.after(0, _on_generation_success, output_path)
	except Exception as err:
		logger.exception("Generation failed")
		root.after(0, _on_generation_error, str(e))


def _on_generation_success(temp_path: str) -> None:
	"""Re-enable the generate button and open the preview popout."""
	generate_button.config(state='normal', text="🎯 Generate LaTeX Image")
	status_label.config(text="Preview ready — save or discard below.", fg="#004488")
	open_preview_popout(temp_path)


def _on_generation_error(error_msg: str) -> None:
	"""Re-enable the generate button and report the error to the user."""
	generate_button.config(state='normal', text="🎯 Generate LaTeX Image")
	status_label.config(text=f"❌ Generation failed — check the log for details.", fg="#cc0000")
	messagebox.showerror("Error", f"Failed to generate image:\n{error_msg}")


def on_signature_change(*_) -> None:
	"""Enable or disable the custom signature entry based on the dropdown value."""
	try:
		if signature_var.get() == "Custom":
			custom_signature_entry.config(state='normal')
			custom_signature_entry.focus_set()
		else:
			custom_signature_entry.config(state='disabled')
			custom_signature_var.set("")
	except NameError:
		pass


# --- GUI Setup ---
root = tk.Tk()
root.geometry("700x820")
root.resizable(True, True)
root.title("📞 Dialogorithm: LaTeX Phone Generator (UN Geoscheme)")

# --- CONTINENT ---
tk.Label(root, text="Choose UN continent:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
tk.Label(root, text="Based on UN Statistics Division (M49 geoscheme)", font=("Arial", 9), fg="gray").pack()

continent_var = tk.StringVar()
continent_options = ["All Continents"] + list(get_continent_structure().keys())
continent_combo = ttk.Combobox(root, textvariable=continent_var, values=continent_options, font=("Arial", 12), width=45,
                               state='readonly')
continent_combo.set("All Continents")
continent_combo.pack()
continent_combo.bind("<<ComboboxSelected>>", on_continent_select)

# --- SUBREGION ---
tk.Label(root, text="Choose UN subregion:", font=("Arial", 12)).pack(pady=(10, 2))
subregion_var = tk.StringVar()
subregion_combo = ttk.Combobox(root, textvariable=subregion_var, values=[], font=("Arial", 12), width=45,
                               state='readonly')
subregion_combo.pack()
subregion_combo.bind("<<ComboboxSelected>>", on_subregion_select)

# --- COUNTRY ---
tk.Label(root, text="Choose country:", font=("Arial", 12)).pack(pady=(10, 2))
country_var = tk.StringVar()
country_combo = ttk.Combobox(root, textvariable=country_var, values=[], font=("Arial", 12), width=45, state='readonly')
country_combo.pack()
country_combo.bind("<<ComboboxSelected>>", on_country_select)

# --- FORMAT LABEL ---
format_label = tk.Label(root, text="Format: Choose continent, subregion, and country", font=("Arial", 10), fg="gray")
format_label.pack(pady=(2, 5))

# --- NUMBER TYPE (shown only for countries with special prefixes) ---
number_type_frame = tk.Frame(root)
# Not packed yet — on_country_select shows/hides it dynamically
tk.Label(number_type_frame, text="Number type:", font=("Arial", 11)).pack(anchor="w")
number_type_var = tk.StringVar()
number_type_combo = ttk.Combobox(number_type_frame, textvariable=number_type_var,
                                 values=[], font=("Arial", 11), width=35, state='disabled')
number_type_combo.pack(pady=(3, 0))
number_type_combo.bind("<<ComboboxSelected>>", on_number_type_select)

# --- PHONE ENTRY ---
phone_input_frame = tk.Frame(root)
phone_input_frame.pack(pady=(10, 10))
tk.Label(phone_input_frame, text="Enter phone number:", font=("Arial", 12)).grid(row=0, column=0, columnspan=2,
                                                                                 sticky="w")

country_code_label = tk.Label(phone_input_frame, text="+", font=("Arial", 12), width=6, anchor="e")
country_code_label.grid(row=1, column=0, sticky="e", padx=(0, 2))

local_number_var = tk.StringVar()
local_number_var.trace_add('write', on_number_change)

# FIXED: Use entry field wide enough for longest possible phone numbers
# Longest numbers can be up to 15 digits + country code display + formatting
vcmd = (root.register(create_validation()), '%S', '%P')
entry_local = tk.Entry(phone_input_frame, width=50, font=("Arial", 12), textvariable=local_number_var, state='disabled',
                       validate='key', validatecommand=vcmd)
entry_local.grid(row=1, column=1, sticky="w")
entry_local.bind("<<Paste>>", on_paste)

clear_button = tk.Button(phone_input_frame, text="✕ Clear", command=clear_number,
                         font=("Arial", 10), width=7)
clear_button.grid(row=1, column=2, padx=(6, 0))

formatted_display = tk.Label(phone_input_frame, text="", font=("Arial", 11), fg="#0066CC")
formatted_display.grid(row=2, column=0, columnspan=2, pady=(5, 0))

# --- SIGNATURE OPTIONS ---
signature_frame = tk.Frame(root)
signature_frame.pack(pady=(15, 10))
tk.Label(signature_frame, text="Signature line:", font=("Arial", 12)).pack(anchor="w")

signature_var = tk.StringVar()
signature_options = [
	"Random", "Please call me at:", "Contact me:", "Reach out via:", "Phone:", "Business line:",
	"Available at:", "You can reach me at:", "My direct line:", "Feel free to call:",
	"Professional contact:", "Custom"
]
signature_combo = ttk.Combobox(signature_frame, textvariable=signature_var, values=signature_options,
                               font=("Arial", 11), width=30, state='readonly')
signature_combo.set("Random")
signature_combo.pack(pady=(5, 5))

custom_signature_frame = tk.Frame(signature_frame)
custom_signature_frame.pack(pady=(5, 0))
tk.Label(custom_signature_frame, text="Custom text:", font=("Arial", 10)).pack(anchor="w")
custom_signature_var = tk.StringVar()
custom_signature_entry = tk.Entry(custom_signature_frame, textvariable=custom_signature_var, font=("Arial", 11),
                                  width=40, state='disabled')
custom_signature_entry.pack()
signature_var.trace_add('write', on_signature_change)

# --- LOGGING TOGGLE ---
logging_var = tk.BooleanVar(value=False)
logging_check = ttk.Checkbutton(root, text="Enable logging to file (Downloads/dialogorithm.log)",
                                variable=logging_var, command=_toggle_logging)
logging_check.pack(pady=(10, 0))

# --- GENERATE BUTTON ---
button_frame = tk.Frame(root)
button_frame.pack(pady=(20, 5))
generate_button = tk.Button(button_frame, text="🎯 Generate LaTeX Image", command=on_generate,
                            font=("Arial", 14, "bold"), width=25, height=2)
generate_button.pack()

# --- STATUS LABEL ---
status_label = tk.Label(root, text="Ready.", font=("Arial", 10), fg="gray", wraplength=700)
status_label.pack(pady=(0, 5))

# --- DEBUG: Print initial state ---
logger.info("=== Dialogorithm started ===")
logger.info("Phone number validation system ready")

try:
	test_limit = get_digit_limit(1)
	test_format = format_display_number("5551234567", 1)
	logger.info(f"phone_formats integration OK — US limit: {test_limit}, sample: '{test_format}'")
except Exception as err:
	logger.error(f"phone_formats integration FAILED: {err}")
	traceback.print_exc()

root.mainloop()
