import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import latex_processor
import logging
import random
from pathlib import Path
import traceback
import time

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
class DebugTracker:
	def __init__(self):
		self.validation_calls = []
		self.field_states = []
		self.last_successful_input = ""

	def log_validation(self, char, current_value, country_code, max_digits, result, field_content=None):
		timestamp = time.time()
		call_info = {
			'timestamp': timestamp,
			'char': char,
			'current_value': current_value,
			'current_length': len(current_value),
			'country_code': country_code,
			'max_digits': max_digits,
			'result': result,
			'field_content': field_content,
			'field_length': len(field_content) if field_content else None,
			'stack_trace': ''.join(traceback.format_stack()[-3:-1])  # Last 2 stack frames
		}
		self.validation_calls.append(call_info)

		# Keep only last 20 calls to prevent memory issues
		if len(self.validation_calls) > 20:
			self.validation_calls = self.validation_calls[-20:]

	def log_field_state(self, source, field_content, var_content):
		timestamp = time.time()
		state_info = {
			'timestamp': timestamp,
			'source': source,
			'field_content': field_content,
			'var_content': var_content,
			'field_length': len(field_content),
			'var_length': len(var_content),
			'cursor_pos': None
		}

		try:
			# Try to get cursor position
			if hasattr(entry_local, 'index'):
				state_info['cursor_pos'] = entry_local.index(tk.INSERT)
		except:
			pass

		self.field_states.append(state_info)

		# Keep only last 20 states
		if len(self.field_states) > 20:
			self.field_states = self.field_states[-20:]

	def print_analysis(self):
		print("\n" + "=" * 80)
		print("🔍 COMPREHENSIVE DEBUG ANALYSIS")
		print("=" * 80)

		print(f"\n📊 VALIDATION CALLS ({len(self.validation_calls)} total):")
		for i, call in enumerate(self.validation_calls[-5:]):  # Last 5 calls
			print(
				f"  [{i + 1}] Char: '{call['char']}' | Current: '{call['current_value']}' (len={call['current_length']})")
			print(f"      Country: +{call['country_code']} | Max: {call['max_digits']} | Result: {call['result']}")
			if call['field_content'] is not None:
				print(f"      Field: '{call['field_content']}' (len={call['field_length']})")
			print()

		print(f"\n📋 FIELD STATES ({len(self.field_states)} total):")
		for i, state in enumerate(self.field_states[-3:]):  # Last 3 states
			print(f"  [{i + 1}] Source: {state['source']}")
			print(f"      Field: '{state['field_content']}' (len={state['field_length']})")
			print(f"      Var:   '{state['var_content']}' (len={state['var_length']})")
			if state['cursor_pos'] is not None:
				print(f"      Cursor: {state['cursor_pos']}")
			print()

		# Check for discrepancies
		if self.validation_calls and self.field_states:
			last_validation = self.validation_calls[-1]
			last_state = self.field_states[-1]

			print("🚨 DISCREPANCY ANALYSIS:")
			if last_validation['current_value'] != last_state['field_content']:
				print(
					f"  ❌ MISMATCH: Validation sees '{last_validation['current_value']}' but field contains '{last_state['field_content']}'")
			else:
				print(f"  ✅ MATCH: Validation and field agree on content")

			if last_state['field_content'] != last_state['var_content']:
				print(
					f"  ❌ VAR MISMATCH: Field shows '{last_state['field_content']}' but StringVar has '{last_state['var_content']}'")
			else:
				print(f"  ✅ VAR MATCH: Field and StringVar agree")

		print("=" * 80)


debug_tracker = DebugTracker()

# --- Logger Setup ---
logger = logging.getLogger("dialogorithm_gui")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("dialogorithm_gui.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# --- Signature Line Generator ---
def get_signature_line():
	options = [
		"Please call me at:", "Contact me:", "Reach out via:", "Phone:", "Business line:",
		"Available at:", "You can reach me at:", "My direct line:", "Telephone:", "Feel free to call:",
		"For further assistance:", "Professional contact:", "Main line:", "Office line:", "Direct dial:",
		"Kindly reach out at:", "Primary contact:", "Call for inquiries:", "Reach my desk at:",
		"Client services line:"
	]
	return random.choice(options)


def get_downloads_dir():
	home = Path.home()
	return home / "Downloads"


# --- Fixed Validation Function ---
def validate_phone_input_fixed(char, current_value, country_code_text):
	"""
	FIXED: Validate phone input ensuring only LOCAL digits are counted (not country code)
	"""
	# Only allow digits
	if not char.isdigit():
		return False

	# Extract country code from the label text (e.g., "+1" -> 1)
	try:
		if country_code_text == '+':
			return len(current_value + char) <= 15  # Default fallback
		country_code = int(country_code_text.replace('+', ''))
	except (ValueError, AttributeError):
		return len(current_value + char) <= 15  # Default fallback

	# Get the maximum LOCAL digits allowed for this country
	max_local_digits = get_digit_limit(country_code)

	# Check if adding this character would exceed the limit
	new_length = len(current_value + char)

	# Debug when rejection happens
	if new_length > max_local_digits:
		print(
			f"VALIDATION REJECT: trying to add '{char}' to '{current_value}' (len={len(current_value)}) would make {new_length} > {max_local_digits}")
	else:
		print(
			f"VALIDATION ACCEPT: adding '{char}' to '{current_value}' (len={len(current_value)}) makes {new_length} <= {max_local_digits}")

	return new_length <= max_local_digits


# --- GUI Logic ---
def on_continent_select(event):
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


def on_subregion_select(event):
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


def on_country_select(event):
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
		print(f"Selected {country}: +{code} allows {limit} LOCAL digits")
	else:
		country_code_label.config(text="+")
		local_number_var.set("")
		entry_local.config(state='disabled')
		formatted_display.config(text="")


def create_validation():
	"""Create validation function that uses ACTUAL field content instead of Tkinter's misleading parameter"""

	def validate(char, proposed_value):
		try:
			# CRITICAL FIX: Use actual field content instead of Tkinter's parameter
			actual_current = entry_local.get() if 'entry_local' in globals() else ""

			# Only allow digits
			if not char.isdigit():
				print(f"🚫 REJECT: Non-digit character '{char}'")
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

				print(f"\n🔍 FIXED VALIDATION:")
				print(f"  📝 Adding: '{char}'")
				print(f"  📱 ACTUAL current: '{actual_current}' (len={len(actual_current)})")
				print(f"  🗑️  Ignoring Tkinter param: '{proposed_value}' (misleading)")
				print(f"  🌍 Country: +{country_code} (max {max_digits} LOCAL digits)")
				print(f"  📏 REAL new length: {new_length}")
				print(f"  🎯 Decision: {'✅ ACCEPT' if will_accept else '❌ REJECT'}")

				return will_accept

			except Exception as e:
				print(f"⚠️  Error parsing country code: {e}")
				return len(actual_current + char) <= 15

		except Exception as e:
			print(f"💥 VALIDATION ERROR: {e}")
			return False

	return validate


def on_number_change(*args):
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
			print(f"📱 {current_length}/{max_length} digits: '{clean_number}' → '{formatted}'")

			# Ensure field shows the end
			try:
				entry_local.icursor(tk.END)
				entry_local.xview_moveto(1.0)
			except:
				pass
		else:
			formatted_display.config(text="")

	except Exception as e:
		print(f"💥 NUMBER CHANGE ERROR: {e}")


def on_generate():
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

	# Use our robust phone_formats.py validation instead of phonenumbers library
	max_digits = get_digit_limit(code)
	if len(local_part) > max_digits:
		messagebox.showwarning("Input Error",
		                       f"Phone number too long. {country} allows maximum {max_digits} local digits.")
		return

	# Format the number using our system
	formatted_local = format_display_number(local_part, code)
	full_international = f"+{code} {formatted_local}"

	signature_option = signature_var.get()
	if signature_option == "Random":
		signature_text = get_signature_line()
	elif signature_option == "Custom":
		signature_text = custom_signature_var.get().strip() or "Please call me at:"
	else:
		signature_text = signature_option

	try:
		logger.info(f"Generating LaTeX for {full_international} with signature: {signature_text}")
		output_path = latex_processor.generate_latex_for_number(full_international, signature_text)
		messagebox.showinfo("Success", f"LaTeX image saved to:\n{output_path}")
	except Exception as e:
		logger.exception("Failed to generate image")
		messagebox.showerror("Error", f"Failed to generate image:\n{e}")


def on_signature_change(*args):
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
root.geometry("700x520")
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
local_number_var.trace('w', on_number_change)

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
signature_var.trace('w', on_signature_change)

# --- GENERATE BUTTON ---
button_frame = tk.Frame(root)
button_frame.pack(pady=(20, 20))
generate_button = tk.Button(button_frame, text="🎯 Generate LaTeX Image", command=on_generate,
                            font=("Arial", 14, "bold"), width=25, height=2)
generate_button.pack()

# --- DEBUG: Print initial state ---
print("=== Dialogorithm Started ===")
print("🔧 Sophisticated debugging enabled")
print("📞 Phone number validation system ready")

# Test phone_formats.py integration
try:
	test_limit = get_digit_limit(1)
	test_format = format_display_number("5551234567", 1)
	print(f"✅ phone_formats.py integration test passed")
	print(f"   US limit: {test_limit}, Format test: '{test_format}'")
except Exception as e:
	print(f"❌ phone_formats.py integration test FAILED: {e}")
	traceback.print_exc()

root.mainloop()
