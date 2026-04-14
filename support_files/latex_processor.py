"""
latex_processor.py — LaTeX document assembly and PNG rendering for Dialogorithm.

Assembles a complete LaTeX standalone document from per-digit equation
expressions, compiles it to PDF via ``pdflatex``, and converts the result
to a PNG image via ``pdftoppm``. Also logs a verification table that maps
each expression to its expected digit value.
"""

import logging
import os
import random
import shutil
import subprocess
import tempfile
import traceback
from pathlib import Path
from typing import Optional, Set, Tuple

import equation_bank

MAX_UNIQUE_ATTEMPTS: int = 15
DEFAULT_DPI: int = 2400

logger = logging.getLogger(__name__)


def log_function_entry_exit(func):
	"""Decorator that logs entry and exit of the wrapped function at DEBUG level."""

	def wrapper(*args, **kwargs):
		logger.debug("ENTER %s args=%s kwargs=%s", func.__name__, args, kwargs)
		try:
			result = func(*args, **kwargs)
			logger.debug("EXIT %s OK", func.__name__)
			return result
		except Exception as exc:
			logger.error("EXIT %s with exception: %s", func.__name__, exc)
			logger.debug(traceback.format_exc())
			raise

	return wrapper


def log_verification(full_number_str: str, latex_parts: list, signature_text: str) -> None:
	"""Log a verification table mapping each LaTeX expression to its expected digit.

	Args:
		full_number_str: The full international phone number string (e.g. '+1 (202) 285-1684').
		latex_parts: Ordered list of LaTeX fragments produced by the generator.
		signature_text: The signature line used in the document.
	"""
	clean_number = "".join(filter(str.isdigit, full_number_str))
	has_plus = full_number_str.strip().startswith('+')

	expected_sequence = []
	if has_plus:
		expected_sequence.append("+")
	if has_plus and len(clean_number) == 11 and clean_number.startswith('1'):
		expected_sequence.extend(list('1'))
		expected_sequence.extend(list(clean_number[1:]))
	elif has_plus and len(clean_number) > 10:
		cc_len = len(clean_number) - 10 if len(clean_number) > 10 else 1
		expected_sequence.extend(list(clean_number[:cc_len]))
		expected_sequence.extend(list(clean_number[cc_len:]))
	else:
		expected_sequence.extend(list(clean_number))

	logger.info(f"--- VERIFICATION: {full_number_str} | Signature: {signature_text} ---")
	logger.info(f"Expected sequence: {' '.join(map(str, expected_sequence))}")

	expr_index = 0
	for latex_expr in latex_parts:
		if latex_expr in [r"\quad", r"\;", r"\text{---}", r"\boldsymbol{(}", r"\boldsymbol{)}"]:
			continue
		expected = expected_sequence[expr_index] if expr_index < len(expected_sequence) else "?"
		logger.debug(f"  [{expr_index + 1}] expected={expected!r:>3}  latex={latex_expr}")
		expr_index += 1

	logger.info(f"--- END VERIFICATION ({expr_index} expressions) ---")


@log_function_entry_exit
def _get_unique_latex_for_digit(digit_char: str, used_formulas: Set[str]) -> str:
	"""Return a LaTeX expression for *digit_char* not already in *used_formulas*.

	Tries up to ``MAX_UNIQUE_ATTEMPTS`` times to find a fresh template.
	Falls back to a random (possibly repeated) choice if the pool is exhausted.
	"""
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
def generate_latex_for_number(
		full_number_str: str,
		signature_text: str = "Please call me at:",
) -> str:
	"""Build a LaTeX document for *full_number_str* and render it to PNG.

	Args:
		full_number_str: International phone number (e.g. '+1 (202) 285-1684').
		signature_text: Header line displayed above the equations.

	Returns:
		Absolute path to the generated PNG file in ~/Downloads.

	Raises:
		ValueError: If *full_number_str* contains no digits.
		RuntimeError: If LaTeX compilation or PNG conversion fails.
	"""
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

	math_line = format_equation_single_line(latex_parts)

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
		"\\begin{minipage}{70cm}",
		"\\centering",
		f"{{\\Large \\textbf{{{escaped_signature}}}}}\\\\[0.2cm]",
		"\\[",
		f"\\LARGE {math_line}",
		"\\]",
		"\\end{minipage}",
		"\\end{document}"
	])

	output_dir = os.path.join(str(Path.home()), "Downloads")
	os.makedirs(output_dir, exist_ok=True)

	# Log verification data
	log_verification(full_number_str=full_number_str, latex_parts=latex_parts, signature_text=signature_text)

	# Render PNG from LaTeX
	image_path, msg = render_latex_to_png(latex_doc.strip(), output_dir=output_dir, dpi=150)
	if not image_path:
		raise RuntimeError(msg)

	logger.info(f"Image saved: {image_path}")
	return image_path


def format_equation_single_line(latex_parts: list) -> str:
	"""Join all LaTeX fragments into a single display-math line.

	Args:
		latex_parts: Ordered list of LaTeX strings (expressions + separators).

	Returns:
		A single space-joined string suitable for use inside ``\\[ ... \\]``.
	"""
	return " ".join(latex_parts)


@log_function_entry_exit
def render_latex_to_png(
		latex_doc_str: str,
		output_dir: str,
		dpi: int = DEFAULT_DPI,
) -> Tuple[Optional[str], str]:
	"""Compile *latex_doc_str* to PDF then convert to PNG.

	Args:
		latex_doc_str: Complete LaTeX document source.
		output_dir: Directory where the final PNG will be saved.
		dpi: Resolution for the PNG output.

	Returns:
		A ``(path, message)`` tuple.  *path* is the absolute PNG path on
		success, or ``None`` on failure.  *message* is ``"Success"`` or a
		human-readable error description.
	"""
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
