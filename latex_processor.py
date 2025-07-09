import logging
import os
import shutil
import subprocess
import tempfile
import random
import sys
import traceback
from pathlib import Path
from typing import Optional, Tuple, Set
from datetime import datetime

# Import your custom equation bank module
import equation_bank

MAX_UNIQUE_ATTEMPTS = 15
DEFAULT_DPI = 2400
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class RobustLogger:
	def __init__(self, name: str = __name__, log_level: int = logging.INFO,
	             log_file: Optional[str] = None, console_output: bool = True):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(log_level)

		if self.logger.handlers:
			self.logger.handlers.clear()

		formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

		if console_output:
			console_handler = logging.StreamHandler(sys.stdout)
			console_handler.setLevel(log_level)
			console_handler.setFormatter(formatter)
			self.logger.addHandler(console_handler)

		if log_file is None:
			timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
			log_file = f"latex_generator_{timestamp}.log"

		try:
			log_path = Path(log_file)
			log_path.parent.mkdir(parents=True, exist_ok=True)
			file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
			file_handler.setLevel(logging.DEBUG)
			file_handler.setFormatter(formatter)
			self.logger.addHandler(file_handler)
		except Exception as e:
			print(f"Error setting up logger: {e}", file=sys.stderr)

	def get_logger(self) -> logging.Logger:
		return self.logger


def setup_logger(debug_mode: bool = False) -> logging.Logger:
	log_level = logging.DEBUG if debug_mode else logging.INFO
	robust_logger = RobustLogger(__name__, log_level, console_output=False)
	return robust_logger.get_logger()


logger = setup_logger()


def log_function_entry_exit(func):
	def wrapper(*args, **kwargs):
		logger.debug(f"ENTER {func.__name__} with args={args}, kwargs={kwargs}")
		try:
			result = func(*args, **kwargs)
			logger.debug(f"EXIT {func.__name__} successfully")
			return result
		except Exception as e:
			logger.error(f"EXIT {func.__name__} with exception: {e}")
			logger.debug(traceback.format_exc())
			raise

	return wrapper


def create_verification_output(full_number_str: str, latex_parts: list, used_formulas: set,
                               signature_text: str, output_dir: str) -> str:
	"""
	Creates a comprehensive verification file for GenAI evaluation.
	"""
	logger.info("Creating verification output for GenAI evaluation")

	# Parse the phone number to extract expected digits
	clean_number = "".join(filter(str.isdigit, full_number_str))
	has_plus = full_number_str.strip().startswith('+')

	# Build expected sequence
	expected_sequence = []
	if has_plus:
		expected_sequence.append("+")

	# Add country code if present
	if has_plus and len(clean_number) == 11 and clean_number.startswith('1'):
		expected_sequence.extend(list('1'))  # US country code
		expected_sequence.extend(list(clean_number[1:]))  # Rest of number
	elif has_plus and len(clean_number) > 10:
		# International number - figure out country code
		cc_len = len(clean_number) - 10 if len(clean_number) > 10 else 1
		country_code = clean_number[:cc_len]
		main_number = clean_number[cc_len:]
		expected_sequence.extend(list(country_code))
		expected_sequence.extend(list(main_number))
	else:
		expected_sequence.extend(list(clean_number))

	# Create verification data
	verification_data = {
		"metadata": {
			"timestamp": datetime.now().isoformat(),
			"original_input": full_number_str,
			"clean_digits": clean_number,
			"has_plus_sign": has_plus,
			"signature_text": signature_text,
			"total_expressions": len(latex_parts),
			"expected_sequence": expected_sequence
		},
		"expressions_to_verify": []
	}

	# Process each expression
	for i, latex_expr in enumerate(latex_parts):
		# Skip formatting elements
		if latex_expr in [r"\quad", r"\;", r"\text{---}", r"\boldsymbol{(}", r"\boldsymbol{)}"]:
			continue

		expected_value = None
		expression_type = "unknown"

		# Determine expected value based on position
		expr_index = len(verification_data["expressions_to_verify"])
		if expr_index < len(expected_sequence):
			expected_value = expected_sequence[expr_index]
			if expected_value == "+":
				expression_type = "plus_symbol"
			elif expected_value.isdigit():
				expression_type = f"digit_{expected_value}"
				expected_value = int(expected_value)

		expr_data = {
			"index": expr_index,
			"latex_expression": latex_expr,
			"expected_value": expected_value,
			"expression_type": expression_type,
			"verification_question": f"Does this expression evaluate to {expected_value}?",
			"clean_latex": latex_expr.replace(r"\left(", "").replace(r"\right)", "").strip()
		}

		verification_data["expressions_to_verify"].append(expr_data)

	# Create human-readable verification file
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	verification_filename = f"verification_{timestamp}.txt"
	verification_path = os.path.join(output_dir, verification_filename)

	try:
		with open(verification_path, 'w', encoding='utf-8') as f:
			f.write("=" * 80 + "\n")
			f.write("DIALOGORITHM EQUATION VERIFICATION FILE\n")
			f.write("=" * 80 + "\n\n")

			f.write(f"🔍 VERIFICATION REQUEST\n")
			f.write(f"Generated: {verification_data['metadata']['timestamp']}\n")
			f.write(f"Original Input: {full_number_str}\n")
			f.write(f"Expected Sequence: {' '.join(map(str, expected_sequence))}\n")
			f.write(f"Signature: {signature_text}\n\n")

			f.write("📝 TASK FOR AI EVALUATOR:\n")
			f.write("Please verify that each mathematical expression below evaluates to its expected value.\n")
			f.write("Respond with ✅ if correct, ❌ if incorrect, and briefly explain any errors.\n\n")

			f.write("🧮 EXPRESSIONS TO VERIFY:\n")
			f.write("-" * 60 + "\n\n")

			for i, expr in enumerate(verification_data["expressions_to_verify"]):
				f.write(f"Expression #{i + 1}:\n")
				f.write(f"LaTeX: {expr['latex_expression']}\n")
				f.write(f"Expected Value: {expr['expected_value']}\n")
				f.write(f"Question: {expr['verification_question']}\n")
				f.write(f"Type: {expr['expression_type']}\n")
				f.write("\nVerification Result: [ ] ✅ Correct  [ ] ❌ Incorrect\n")
				f.write("Notes: ________________________________\n")
				f.write("\n" + "-" * 40 + "\n\n")

			f.write("📊 SUMMARY CHECK:\n")
			f.write(f"Total expressions verified: _____ / {len(verification_data['expressions_to_verify'])}\n")
			f.write(f"Phone number reconstruction: ________________\n")
			f.write(f"Overall assessment: [ ] ✅ All correct  [ ] ❌ Issues found\n\n")

			f.write("=" * 80 + "\n")
			f.write("END OF VERIFICATION FILE\n")
			f.write("=" * 80 + "\n")

		logger.info(f"✅ Verification file created: {verification_path}")
		return verification_path

	except Exception as e:
		logger.error(f"Failed to create verification file: {e}")
		return None


@log_function_entry_exit
def _get_unique_latex_for_digit(digit_char: str, used_formulas: Set[str]) -> str:
	if not digit_char.isdigit():
		return equation_bank.eq_placeholder(digit_char)

	func_name = f"_get_{digit_char}_templates"
	if not hasattr(equation_bank, func_name):
		return equation_bank.eq_placeholder(digit_char)

	get_templates = getattr(equation_bank, func_name)

	for _ in range(MAX_UNIQUE_ATTEMPTS):
		all_templates = get_templates()
		latex_str = random.choice(all_templates)
		if latex_str not in used_formulas:
			used_formulas.add(latex_str)
			return latex_str

	return random.choice(get_templates())


# CRITICAL FIX 1: Replace the generate_latex_for_number function in latex_processor.py

@log_function_entry_exit
def generate_latex_for_number(full_number_str: str, signature_text: str = "Please call me at:") -> str:
	if not full_number_str.strip():
		raise ValueError("Phone number cannot be empty")

	clean_number = ''.join(filter(str.isdigit, full_number_str))
	has_plus = full_number_str.strip().startswith('+')

	if not clean_number:
		raise ValueError("Phone number must contain at least one digit")

	country_code, main_number = "", clean_number
	if has_plus and len(clean_number) == 11 and clean_number.startswith('1'):
		country_code, main_number = '1', clean_number[1:]
	elif has_plus and len(clean_number) > 10:
		country_code, main_number = clean_number[:-10], clean_number[-10:]

	used_formulas = set()
	latex_parts = []

	if has_plus:
		latex_parts.append(equation_bank.eq_plus())
	if country_code:
		for digit in country_code:
			latex_parts.append(_get_unique_latex_for_digit(digit, used_formulas))
		latex_parts.append(r"\quad")

	if len(main_number) == 10:
		area, exch, line = main_number[:3], main_number[3:6], main_number[6:]
		latex_parts.append(r"\boldsymbol{(}")
		latex_parts.extend([_get_unique_latex_for_digit(d, used_formulas) for d in area])
		latex_parts.append(r"\boldsymbol{)}")
		latex_parts.append(r"\;")
		latex_parts.extend([_get_unique_latex_for_digit(d, used_formulas) for d in exch])
		latex_parts.append(r"\text{---}")
		latex_parts.extend([_get_unique_latex_for_digit(d, used_formulas) for d in line])
	else:
		latex_parts.extend([_get_unique_latex_for_digit(d, used_formulas) for d in main_number])

	# 🔧 CRITICAL FIX: Break long equations into multiple lines
	math_lines = format_equation_with_line_breaks(latex_parts)

	escaped_signature = signature_text.translate(str.maketrans({
		'\\': '\\textbackslash{}', '&': '\\&', '%': '\\%', '$': '\\$', '#': '\\#',
		'_': '\\_', '{': '\\{', '}': '\\}'
	}))

	latex_doc = "\n".join([
		"\\documentclass[border=10pt]{standalone}",
		"\\usepackage{amsmath, amssymb, amsfonts, graphicx, xcolor}",
		"\\usepackage[T1]{fontenc}",
		"\\usepackage{helvet}",
		"\\renewcommand{\\familydefault}{\\sfdefault}",
		"\\begin{document}",
		"\\begin{center}",
		"\\begin{minipage}{0.95\\linewidth}",  # Slightly narrower
		"\\centering",
		f"{{\\Large \\textbf{{{escaped_signature}}}}}\\\\[0.5cm]",
		"\\begin{align*}",
		f"{math_lines}",
		"\\end{align*}",
		"\\end{minipage}",
		"\\end{center}",
		"\\end{document}"
	])

	output_dir = os.path.join(str(Path.home()), "Downloads")
	os.makedirs(output_dir, exist_ok=True)

	# Create verification file
	verification_path = None
	try:
		verification_path = create_verification_output(
			full_number_str=full_number_str,
			latex_parts=latex_parts,
			used_formulas=used_formulas,
			signature_text=signature_text,
			output_dir=output_dir
		)
		if verification_path:
			logger.info(f"📋 Verification file ready for AI evaluation: {verification_path}")
	except Exception as e:
		logger.warning(f"Could not create verification file: {e}")

	# Render PNG from LaTeX
	image_path, msg = render_latex_to_png(latex_doc.strip(), output_dir=output_dir, dpi=600)
	if not image_path:
		raise RuntimeError(msg)

	logger.info(f"🎯 LaTeX image saved: {image_path}")
	if verification_path:
		logger.info(f"📋 Verification file: {verification_path}")

	return image_path


def format_equation_with_line_breaks(latex_parts: list) -> str:
	"""Break long equations into multiple lines for LaTeX compilation."""

	lines = []
	current_line = []
	MAX_LINE_LENGTH = 3  # Max equations per line

	# Manually step through parts to handle structure
	i = 0
	while i < len(latex_parts):
		part = latex_parts[i]

		# Start of area code
		if part == r"\boldsymbol{(}":
			# Add area code and its contents as one block
			area_code_parts = [r"\boldsymbol{(}"]
			i += 1
			# Gather the 3 digits of the area code
			for _ in range(3):
				if i < len(latex_parts):
					area_code_parts.append(latex_parts[i])
					i += 1
			if i < len(latex_parts) and latex_parts[i] == r"\boldsymbol{)}":
				area_code_parts.append(r"\boldsymbol{)} ")
				i += 1
			current_line.append(" ".join(area_code_parts))

		# Other parts
		else:
			current_line.append(part)
			i += 1

		# Check if line is full
		if len(current_line) >= MAX_LINE_LENGTH:
			lines.append(" ".join(current_line))
			current_line = []

	# Add any remaining parts
	if current_line:
		lines.append(" ".join(current_line))

	# Format for the align* environment
	return " \\\\\n".join([f"& {line}" for line in lines])


@log_function_entry_exit
def render_latex_to_png(latex_doc_str: str, output_dir: str, dpi: int = DEFAULT_DPI) -> Tuple[Optional[str], str]:
	if not latex_doc_str.strip():
		return None, "Empty LaTeX document."

	with tempfile.TemporaryDirectory() as temp_dir:
		base = os.path.join(temp_dir, "phone_formula")
		tex_path = base + ".tex"
		pdf_path = base + ".pdf"

		try:
			with open(tex_path, "w", encoding="utf-8") as f:
				f.write(latex_doc_str)
		except Exception as e:
			return None, f"Failed to write .tex: {e}"

		try:
			result = subprocess.run(
				["pdflatex", "-interaction=nonstopmode", f"-output-directory={temp_dir}", tex_path],
				capture_output=True, timeout=30, text=True
			)
			if result.returncode != 0:
				# Log the LaTeX error details
				logger.error(f"pdflatex failed with return code: {result.returncode}")
				logger.error(f"pdflatex stdout: {result.stdout}")
				logger.error(f"pdflatex stderr: {result.stderr}")

				# Also log the LaTeX source for debugging
				try:
					with open(tex_path, 'r', encoding='utf-8') as f:
						latex_content = f.read()
					logger.error(f"LaTeX content that failed:\n{latex_content}")
				except:
					pass

				return None, f"LaTeX compile error. Check logs for details. Return code: {result.returncode}"
		except Exception as e:
			return None, f"LaTeX compile error: {e}"

		if not os.path.exists(pdf_path):
			return None, "PDF not generated."

		try:
			subprocess.run(
				["pdftoppm", "-png", "-singlefile", "-r", str(dpi), pdf_path, base],
				capture_output=True, timeout=20, check=True
			)
		except Exception as e:
			return None, f"pdftoppm error: {e}"

		png_path = base + ".png"
		if not os.path.exists(png_path):
			return None, "PNG not generated."

		final_path = os.path.join(output_dir, "Dialogorithm_Contact.png")
		shutil.copy(png_path, final_path)
		return final_path, "Success"
