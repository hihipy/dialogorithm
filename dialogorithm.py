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
	get_continent_structure
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
	"""Update the country code label and enable the phone entry when a country is chosen."""
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

		# Show the digit limit for this country
		limit = get_digit_limit(code)
		logger.debug(f"Selected {country}: +{code}, max {limit} local digits")
	else:
		country_code_label.config(text="+")
		local_number_var.set("")
		entry_local.config(state='disabled')
		formatted_display.config(text="")


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
			# CRITICAL FIX: Use actual field content instead of Tkinter's parameter
			actual_current = entry_local.get() if 'entry_local' in globals() else ""

			# Only allow digits
			if not char.isdigit():
				logger.debug(f"Validation REJECT: non-digit '{char}'")
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
	"""Simplified number change handler"""
	try:
		country = country_var.get()
		if not country:
			return

		code, region = extract_country_code_from_label(country)
		raw_number = local_number_var.get()

		# Clean the raw number to only digits
		clean_number = "".join(filter(str.isdigit, raw_number))

		# If the cleaned number is different from raw, update it
		if clean_number != raw_number:
			local_number_var.set(clean_number)
			return

		if code and clean_number:
			formatted = format_display_number(clean_number, code)
			formatted_display.config(text=f"+{code} {formatted}")

			# Show progress
			current_length = len(clean_number)
			max_length = get_digit_limit(code)
			logger.debug(f"Input: {current_length}/{max_length} digits  '{clean_number}' → '{formatted}'")

			# Ensure field shows the end
			try:
				entry_local.icursor(tk.END)
				entry_local.xview_moveto(1.0)
			except Exception:
				pass
		else:
			formatted_display.config(text="")

	except Exception as err:
		logger.error(f"Number change error: {err}")


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


def _on_generation_success(output_path: str) -> None:
	"""Re-enable the generate button and show the success status."""
	"""Called on the main thread after successful generation."""
	generate_button.config(state='normal', text="🎯 Generate LaTeX Image")
	status_label.config(text=f"✅ Saved to: {output_path}", fg="#006600")


def _on_generation_error(error_msg: str) -> None:
	"""Re-enable the generate button and report the error to the user."""
	"""Called on the main thread after a generation failure."""
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
format_label.pack(pady=(2, 10))

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
entry_local = tk.Entry(phone_input_frame, width=60, font=("Arial", 12), textvariable=local_number_var, state='disabled',
                       validate='key', validatecommand=vcmd)
entry_local.grid(row=1, column=1, sticky="w")

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
generate_button.pz1ack()

# --- STATUS LABEL ---
status_label = tk.Label(root, text="Ready.", font=("Arial", 10), fg="gray", wraplength=650)
status_label.pack(pady=(0, 15))

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
