"""
Final PhD-Level Equation Bank for digits 0-9.
This version has been fully curated to contain only graduate-level, purely
symbolic equations, with at least 25 templates per digit where appropriate.
"""

import logging
import logging.handlers
import random
import os
import uuid
import sys


# --- Robust Logger Setup ---
class ContextFilter(logging.Filter):
	def __init__(self, session_id):
		super().__init__()
		self.session_id = session_id

	def filter(self, record):
		record.session_id = self.session_id
		return True


class ColoredFormatter(logging.Formatter):
	GREY, YELLOW, RED, BOLD_RED, RESET = "\x1b[38;20m", "\x1b[33;20m", "\x1b[31;20m", "\x1b[31;1m", "\x1b[0m"

	def __init__(self, fmt):
		super().__init__()
		self.fmt = fmt
		self.FORMATS = {
			logging.DEBUG: self.GREY + self.fmt + self.RESET,
			logging.INFO: self.GREY + self.fmt + self.RESET,
			logging.WARNING: self.YELLOW + self.fmt + self.RESET,
			logging.ERROR: self.RED + self.fmt + self.RESET,
			logging.CRITICAL: self.BOLD_RED + self.fmt + self.RESET
		}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


def setup_logging(session_id, log_level=logging.DEBUG, log_file="equation_bank.log"):
	logger_obj = logging.getLogger(__name__)
	logger_obj.setLevel(log_level)
	logger_obj.addFilter(ContextFilter(session_id))
	if logger_obj.hasHandlers():
		logger_obj.handlers.clear()
	console_handler = logging.StreamHandler(sys.stdout)
	console_format = "[%(levelname)-8s] %(message)s (%(filename)s:%(lineno)d)"
	console_handler.setFormatter(ColoredFormatter(console_format))
	console_handler.setLevel(logging.INFO)
	logger_obj.addHandler(console_handler)
	file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
	file_format = "%(asctime)s - %(session_id)s - %(name)s [%(levelname)s] %(funcName)s: %(message)s"
	file_handler.setFormatter(logging.Formatter(file_format))
	file_handler.setLevel(log_level)
	logger_obj.addHandler(file_handler)

	def handle_exception(exc_type, exc_value, exc_traceback):
		if issubclass(exc_type, KeyboardInterrupt):
			sys.__excepthook__(exc_type, exc_value, exc_traceback)
			return
		logger_obj.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

	sys.excepthook = handle_exception
	return logger_obj


SESSION_ID = str(uuid.uuid4())[:8]
logger = setup_logging(session_id=SESSION_ID)


# --- Helper Functions ---
def get_rand_int(min_val=1, max_val=10):
	return random.randint(min_val, max_val)


# --- Core Symbol and Fallback Generators ---
def eq_plus():
	logger.debug("Generating LaTeX for plus symbol")
	return r"\mathbf{+}"


def eq_placeholder(digit_char):
	logger.warning(f"eq_placeholder called for digit: '{digit_char}' - specific function missing or error.")
	return rf"\mathbf{{\textit{{({digit_char})}}}}"


# --- Digit Equation Template Provider Functions ---

def _get_0_templates():
	n = get_rand_int(1, 3)

	templates = [
		# --- Differential & Algebraic Geometry ---
		r"\left( d^2\omega \right)",
		r"\left( H^1(\mathbb{P}^2, \mathcal{O}(-" + str(n) + r")) \right)",
		r"\left( \text{ch}_0(\mathcal{E} \otimes \mathcal{F}) - \text{ch}_0(\mathcal{E}) \cdot \text{ch}_0(\mathcal{F}) \right)",
		r"\left( c_1(SU(n)) \right)",
		r"\left( p_1(M^3) \right)",

		# --- Homological Algebra & Topology ---
		r"\left( \partial_n \circ \partial_{n+1} \right)",
		r"\left( H_n(\text{pt}), n>0 \right)",
		r"\left( \operatorname{Ext}^1_{\mathbb{Z}}(\mathbb{Z}/n\mathbb{Z}, \mathbb{Q}) \right)",
		r"\left( \chi(SU(n)) \right)",
		r"\left( \operatorname{Tor}_1^{\mathbb{Z}}(\mathbb{Z}/n\mathbb{Z}, \mathbb{Q}) \right)",
		r"\left( \sigma(\partial W) \right)",
		r"\left( \hat{A}(\partial W) \right)",

		# --- Lie Theory & Representation Theory ---
		r"\left( [\mathbf{X}, \mathbf{X}] \right)",
		r"\left( [X, [Y, Z]] + [Y, [Z, X]] + [Z, [X, Y]] \right)",
		r"\left( \operatorname{Tr}(T^a), T^a \in \mathfrak{su}(n) \right)",
		r"\left( \langle \chi_i, \chi_j \rangle_{i \neq j} \right)",
		r"\left( \text{index}(D_{\text{odd dim}}) \right)",

		# --- Advanced Number Theory & Analysis ---
		r"\left( \sum_{N=1}^{\infty} \frac{\mu(N)}{N} \right)",
		r"\left( \Gamma(z)\Gamma(1-z)\sin(\pi z) - \pi \right)",
		r"\left( \lim_{\tau \to i\infty} f(\tau) \text{ for } f \in S_k(\Gamma_0(N)) \right)",
		r"\left( \operatorname{rank}_{an}(E) - \operatorname{rank}_{alg}(E) \right)",

		# --- Theoretical & Mathematical Physics ---
		rf"\left( J_{{{n}}}(z) Y_{{{n}-1}}(z) - J_{{{n}-1}}(z) Y_{{{n}}}(z) + \frac{{2}}{{\pi z}} \right)",
		r"\left( \langle[\hat{x}, \hat{p}_x]\rangle - i\hbar \right)",
		r"\left( \nabla_\mu g^{\alpha \beta} \right)",
	]
	return templates


def _get_1_templates():
	s_val = get_rand_int(2, 4)
	A_sym = 'A'

	templates = [
		# --- Abstract Algebra & Representation Theory ---
		r"\left( \text{rk}(\text{Pic}(\mathbb{P}^1)) \right)",
		r"\left( \text{dim}(\mathfrak{so}(2)) \right)",
		r"\left( \text{rank}(\text{K}_0(\text{Spec}(\mathbb{Z}))) \right)",
		rf"\left( \frac{{\det(e^{{{A_sym}}})}}{{e^{{\operatorname{{Tr}}({A_sym})}}}} \right)",
		r"\left( \text{rank}(\mathfrak{su}(2)) \right)",
		r"\left( \chi_V(e) / \dim(V) \right)",
		r"\left( |Z(S_3)| \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{dim}_{\mathbb{C}} H^{0,0}(X) \right)",
		r"\left( h^{1,1}(\mathbb{P}^1) \right)",
		r"\left( \chi(\text{Spec}(\mathbb{C})) \right)",
		r"\left( \frac{1}{2}\chi(\mathbb{S}^{0}) \right)",
		r"\left( \text{dim}(H^0(\mathbb{P}^1, \mathcal{O}(0))) \right)",
		r"\left( \text{genus}(\mathbb{P}^1) + 1 \right)",
		r"\left( \deg(\mathbb{P}^0) \right)",
		r"\left( \frac{(d-1)(d-2)}{2}|_{d=3} \right)",
		r"\left( \text{lk}(L2a1) \right)",
		r"\left( b_0(\mathbb{T}^n) \right)",

		# --- Advanced Number Theory & Special Functions ---
		r"\left( \zeta(0) + \frac{3}{2} \right)",
		r"\left( \lim_{s \to 1} (s-1)\zeta(s) \right)",
		r"\left( \prod_p \left(1 + \frac{1}{p(p-1)}\right) / \left(\frac{\zeta(2)\zeta(3)}{\zeta(6)}\right) \right)",
		r"\left( \sum_{idx=1}^{\infty} \frac{\mu(idx)}{idx} + 1 \right)",
		r"\left( h(-4) \right)",

		# --- Analysis & Measure Theory ---
		r"\left( \lambda([0,1]) \right)",
		rf"\left( \int_0^{{\infty}} \frac{{x^{{{s_val}-1}}}}{{e^x - 1}} \,dx \cdot \frac{{1}}{{\Gamma({s_val})\zeta({s_val})}} \right)",
	]
	return templates


def _get_2_templates():
	n = get_rand_int(1, 3)
	s_val = get_rand_int(2, 4)

	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{rank}(\mathfrak{sl}_3(\mathbb{C})) \right)",
		r"\left( \dim H^1(S_3, \mathbb{C}^*) \right)",
		r"\left( \text{dim}(\mathfrak{u}(1)) \cdot 2 \right)",
		r"\left( \text{dim}(\mathfrak{so}(3)) - 1 \right)",
		r"\left( \text{rank}(\mathfrak{so}(4)) \right)",
		r"\left( \dim(\mathfrak{sl}_2(\mathbb{C}))-1 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{rk}(\text{Pic}(\mathbb{P}^1)) + 1 \right)",
		r"\left( \text{dim}(H^0(\mathbb{P}^1, \mathcal{O}(1))) \right)",
		r"\left( b_0(\mathbb{S}^1) + b_1(\mathbb{S}^1) \right)",
		r"\left( b_1(\mathbb{T}^2) \right)",
		r"\left( \deg(Q \subset \mathbb{P}^3) \right)",
		r"\left( \chi(\mathbb{CP}^2) - 1 \right)",
		r"\left( \sum_i b_{2i}(\mathbb{CP}^1) \right)",
		r"\left( \deg(\mathbb{V}(x_0x_2 - x_1^2)) \right)",

		# --- Advanced Number Theory ---
		r"\left( \zeta(0) + \frac{5}{2} \right)",
		r"\left( \lim_{s \to 1} 2(s-1)\zeta(s) \right)",
		r"\left( h(-15) \right)",
		r"\left( \phi(\phi(5)) \right)",
		r"\left( h(-23) - 1 \right)",
		r"\left( |\{\mathfrak{p} \subset \mathbb{Z}[i] \mid \mathfrak{p} | (5)\}| \right)",
		r"\left( \phi(4) \right)",
		r"\left( |\text{Aut}(S_3)| - 4 \right)",

		# --- Analysis & K-Theory ---
		r"\left( \text{rank}(\text{K}_0(\mathbb{P}^1)) \right)",
		r"\left( \text{rank}(\mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2\mathbb{Z}) \right)",
		rf"\left( \left(\int_0^{{\infty}} \frac{{x^{{{s_val}-1}}}}{{e^x - 1}} \,dx \cdot \frac{{1}}{{\Gamma({s_val})\zeta({s_val})}}\right) \cdot 2 \right)",
	]
	return templates


def _get_3_templates():
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{dim}(\mathfrak{sl}_2(\mathbb{C})) \right)",
		r"\left( \text{dim}(\mathfrak{su}(2)) \right)",
		r"\left( \text{dim}(\text{SO}(3)) \right)",
		r"\left( \dim(\text{ad}(\mathfrak{su}(2))) \right)",
		r"\left( |W(A_2)| - 3 \right)",
		r"\left( \text{rank}(\mathfrak{so}(7)) \right)",
		r"\left( |Irr(S_3)| \right)",
		r"\left( \dim(\mathfrak{g}_2) - 11 \right)",
		r"\left( \dim(\mathfrak{f}_4) - 49 \right)",
		r"\left( \text{rank}(\mathfrak{e}_7) - 4 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{dim}(H^0(\mathbb{P}^2, \mathcal{O}(1))) \right)",
		r"\left( \chi(\mathbb{CP}^2) \right)",
		r"\left( [\mathbb{Q}(\sqrt[3]{2}) : \mathbb{Q}] \right)",
		r"\left( b_1(\mathbb{T}^3) \right)",
		r"\left( c(3_1) \right)",
		r"\left( \dim(k[x,y,z]) \right)",
		r"\left( \deg(\nu_3(\mathbb{P}^1)) \right)",
		r"\left( c_1(T_{\mathbb{P}^2}) \cdot H \right)",
		r"\left( \sigma(E_8) - 5 \right)",

		# --- Advanced Number Theory ---
		r"\left( \zeta(-1) + \frac{37}{12} \right)",
		r"\left( h(-23) \right)",
		r"\left( \omega(30) \right)",
		r"\left( |\mathbb{A}_3| \right)",

		# --- Templated Expressions ---
		r"\left( \text{rank}(\mathfrak{e}_8) - 5 \right)",
		r"\left( \frac{\Gamma(4)\Gamma(2)}{\Gamma(3)} \right)",
	]
	return templates


def _get_4_templates():
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{dim}(\mathfrak{so}(5)) - 6 \right)",
		r"\left( \text{rank}(\mathfrak{so}(8)) \right)",
		r"\left( \dim(\text{spinor rep of } SO(5)) \right)",
		r"\left( \dim(\mathfrak{g}_2) - 10 \right)",
		r"\left( \text{rank}(\mathfrak{e}_7) - 3 \right)",
		r"\left( |W(A_2)| - 2 \right)",
		r"\left( \dim(\text{ad}(\mathfrak{sl}_2(\mathbb{C}))) + 1 \right)",
		r"\left( \dim(\mathfrak{su}(3)) - 4 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{dim}(H^0(\mathbb{P}^3, \mathcal{O}(1))) \right)",
		r"\left( \chi(\mathbb{P}^2) + 1 \right)",
		r"\left( \text{dim}(\text{End}(\mathbb{C}^2)) \right)",
		r"\left( \deg(\nu_2(\mathbb{P}^2)) \right)",
		r"\left( \sum_i b_i(\mathbb{T}^2) \right)",
		r"\left( \text{rank}(\pi_1(\Sigma_2)) \right)",
		r"\left( c_1(T_{\mathbb{P}^1 \times \mathbb{P}^1})^2 - 4 \right)",
		r"\left( \deg(K_{\mathbb{P}^2}) + 7 \right)",

		# --- Advanced Number Theory ---
		r"\left( \zeta(-3) + \frac{479}{120} \right)",
		r"\left( h(-39) \right)",
		r"\left( h(-51) \right)",
		r"\left( h(-52) \right)",
		r"\left( |\{\mathfrak{p} \subset \mathbb{Z}[i] \mid \mathfrak{p} | (13)\}| + 2 \right)",

		# --- Commutative Algebra & K-Theory ---
		r"\left( \text{depth}(k[[w,x,y,z]]) \right)",
		r"\left( \text{rank}(K_0(\mathbb{P}^1)) + 2 \right)",

		# --- Complex Analysis & Physics ---
		r"\left( \operatorname{Res}_{z=0} \frac{4\cos(z)}{z} \right)",
		r"\left( \sigma(E_8) - 4 \right)",
	]
	return templates


def _get_5_templates():
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{dim}(\mathfrak{sp}(4,\mathbb{C})) - 5 \right)",
		r"\left( \dim(\text{U}(2)) + 1 \right)",
		r"\left( |Irr(D_4)| \right)",
		r"\left( \text{rank}(\mathfrak{so}(11)) \right)",
		r"\left( \dim(\mathfrak{g}_2) - 9 \right)",
		r"\left( \text{rank}(\mathfrak{e}_8) - 3 \right)",
		r"\left( \sigma(E_8) - 3 \right)",
		r"\left( |W(A_2)| - 1 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{dim}(\text{Symp}^5(\mathbb{C}^2)) - 1 \right)",
		r"\left( \text{dim}(H^0(\mathbb{P}^4, \mathcal{O}(1))) \right)",
		r"\left( \chi(\mathbb{P}^2) + 2 \right)",
		r"\left( \chi(K_5) \right)",
		r"\left( c_1(T_{\mathbb{P}^2})^2 - 4 \right)",
		r"\left( b_1(\mathbb{T}^2) \cdot 2 + 1 \right)",
		r"\left( \deg(\nu_4(\mathbb{P}^1)) + 1 \right)",

		# --- Advanced Number Theory ---
		r"\left( h(-47) \right)",
		r"\left( v_2(40) \right)",
		r"\left( h(-23) + 2 \right)",
		r"\left( \zeta(-3) \cdot 120 + 4 \right)",

		# --- Templated & Combined ---
		r"\left( \text{dim}(\mathfrak{sl}_2(\mathbb{C})) + 2 \right)",
		r"\left( \text{rank}(\mathfrak{e}_6) - 1 \right)",
		r"\left( \text{rank}(\mathfrak{e}_7) - 2 \right)",
		r"\left( \dim(\mathfrak{so}(4)) + \zeta(0) + 1/2 \right)",
		r"\left( \dim(\Lambda^2(\mathbb{C}^4)) - 1 \right)",
	]
	return templates


def _get_6_templates():
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{dim}(\mathfrak{so}(4,\mathbb{R})) \right)",
		r"\left( \text{rank}(\mathfrak{e}_6) \right)",
		r"\left( |W(A_2)| \right)",
		r"\left( \dim(\mathfrak{so}(5)) - \text{rank}(\mathfrak{so}(8)) \right)",
		r"\left( \dim(\Lambda^2(\mathbb{C}^4)) \right)",
		r"\left( \dim(\mathfrak{su}(3)) - 2 \right)",
		r"\left( \dim(\mathfrak{sp}(4,\mathbb{C})) - 4 \right)",
		r"\left( \dim(\mathfrak{g}_2) - 8 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{dim}(\text{Symp}^6(\mathbb{C}^2)) - 1 \right)",
		r"\left( e_0(Q, R)|_{R=k[x], Q=(x^6)} \right)",
		r"\left( -2 \deg(K_{\mathbb{P}^2}) \right)",
		r"\left( b_1(\mathbb{T}^2) \cdot 3 \right)",
		r"\left( h^{2,0}(\text{K3 surface}) + 5 \right)",
		r"\left( \chi(\mathbb{CP}^2) \cdot 2 \right)",
		r"\left( c_1^2(\mathbb{P}^2) - 3 \right)",

		# --- Advanced Number Theory ---
		r"\left( \zeta(-5) + \frac{1513}{252} \right)",
		r"\left( h(-87) \right)",
		r"\left( h(-23) \cdot 2 \right)",
		r"\left( -v_p(p^3!) + 3p+1 |_{p=2} \right)",
		r"\left( |\text{Aut}(V_4)| \right)",

		# --- Complex Analysis ---
		r"\left( \operatorname{Res}_{z=0} \frac{e^{6z}-1}{z^2} \right)",

		# --- Templated & Combined ---
		r"\left( \dim(\mathfrak{sl}_2(\mathbb{C})) \cdot 2 \right)",
		r"\left( \zeta(0) \cdot (-12) \right)",
		r"\left( \text{rank}(\mathfrak{e}_8) - 2 \right)",
	]
	return templates


def _get_7_templates():
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{rank}(\mathfrak{e}_7) \right)",
		r"\left( \dim(V_7) \right)",
		r"\left( \dim(\text{ad}(\mathfrak{su}(3))) - 1 \right)",
		r"\left( \dim(L(6\omega_1)_0) \text{ for } A_1 \right)",
		r"\left( \dim(\text{Hom}_{A_1}(V_{5}, V_{1} \otimes V_{5})) \right)",
		r"\left( |W(A_2)| + 1 \right)",
		r"\left( \dim(\mathfrak{sp}(4,\mathbb{C})) - 3 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{mult}_0(\mathbb{C}[x_1..x_7]/(x_1..x_7)) \right)",
		r"\left( \text{dim}(\text{Symp}^7(\mathbb{C}^2)) - 1 \right)",
		r"\left( c_2(T_{\mathbb{P}^3}) \cdot H - 5 \right)",
		r"\left( h^{1,1}(X) - h^{2,1}(X) + 6 |_{X=\text{quintic}} \right)",
		r"\left( \chi(\text{dP}_2) + 5 \right)",
		r"\left( \deg(\nu_6(\mathbb{P}^1)) + 1 \right)",
		r"\left( c(4_1) + 2 \right)",

		# --- Advanced Number Theory ---
		r"\left( h(-71) \right)",
		r"\left( (x^2+7=2^n)|_{n=5} \rightarrow x \right)",
		r"\left( \sum_{k=1}^5 p(5,k) \right)",
		r"\left( \phi(14) + 1 \right)",
		r"\left( \zeta(-3) \cdot 120 + 6 \right)",
		r"\left( h(-47) + 2 \right)",

		# --- Physics & Combined ---
		r"\left( \dim(\text{M-Theory}) - 4 \right)",
		r"\left( \sigma(E_8) - 1 \right)",
		r"\left( \dim(\mathfrak{g}_2) - 7 \right)",
		r"\left( \text{rank}(\mathfrak{e}_6) + 1 \right)",
		r"\left( \left(\int_{-\infty}^{\infty} \frac{dx}{(1+x^2)^4}\right) \cdot \frac{112}{5\pi} \right)",
	]
	return templates


def _get_8_templates():
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{dim}(\mathfrak{sl}(3,\mathbb{C})) \right)",
		r"\left( \text{dim}(\mathfrak{so}(5)) - 2 \right)",
		r"\left( \text{dim}(\text{SU}(3)) \right)",
		r"\left( \text{rank}(\mathfrak{e}_8) \right)",
		r"\left( \dim(\text{ad}(\mathfrak{sl}_3(\mathbb{C}))) \right)",
		r"\left( |\Delta(\mathfrak{sp}_4)| \right)",
		r"\left( \dim(\mathfrak{f}_4) - 44 \right)",
		r"\left( \dim(\mathfrak{g}_2) - 6 \right)",
		r"\left( \dim(\mathfrak{e}_7) - 125 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{dim}(\text{Symp}^8(\mathbb{C}^2)) - 1 \right)",
		r"\left( \sigma(E_8) \right)",
		r"\left( c_1(T_{\mathbb{P}^1 \times \mathbb{P}^1})^2 \right)",
		r"\left( h^{2,1}(\text{quintic}) - 93 \right)",
		r"\left( b_1(\mathbb{T}^2) \cdot 4 \right)",
		r"\left( \chi(\mathbb{CP}^3) + 4 \right)",

		# --- Advanced Number Theory ---
		r"\left( \tau(24) \right)",
		r"\left( \phi(15) \right)",
		r"\left( h(-47) + 3 \right)",
		r"\left( |W(A_2)| + 2 \right)",

		# --- Complex Analysis & Physics ---
		r"\left( \left(\int_{-\infty}^{\infty} \frac{dx}{(1+x^2)^4}\right) \cdot \frac{128}{5\pi} \right)",
		r"\left( \operatorname{Res}_{z=0} \frac{8\cosh(z)}{z} \right)",
		r"\left( \operatorname{Res}_{z=0} \frac{\sinh(8z)}{z^2} \right)",

		# --- Templated & Combined ---
		r"\left( \text{rank}(\mathfrak{e}_6) + 2 \right)",
		r"\left( \chi(\mathbb{CP}^2) \cdot 3 - 1 \right)",
	]
	return templates


def _get_9_templates():
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \text{dim}(\mathfrak{so}(3) \otimes \mathfrak{so}(3)) \right)",
		r"\left( \dim(\mathfrak{sl}(3,\mathbb{C})) + 1 \right)",
		r"\left( \text{rank}(\mathfrak{e}_8) + 1 \right)",
		r"\left( \sigma(E_8) + 1 \right)",
		r"\left( |W(A_2)| + 3 \right)",
		r"\left( \dim(\mathfrak{g}_2) - 5 \right)",
		r"\left( \dim(\mathfrak{f}_4) - 43 \right)",
		r"\left( \dim(\mathfrak{e}_7) - 124 \right)",
		r"\left( \dim(\text{ad}(\mathfrak{su}(3))) + 1 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \text{dim}(\text{Symp}^9(\mathbb{C}^2)) - 1 \right)",
		r"\left( c_1(T_{\mathbb{P}^2})^2 \right)",
		r"\left( h^{1,1}(\text{K3 surface}) - 11 \right)",
		r"\left( b_1(\mathbb{T}^3) \cdot 3 \right)",
		r"\left( c(5_1) + 4 \right)",

		# --- Advanced Number Theory ---
		r"\left( h(-199) \right)",
		r"\left( \tau(36) \right)",
		r"\left( v_3(3^4!) \right)",
		r"\left( h(-87) + 3 \right)",
		r"\left( h(-47) + 4 \right)",
		r"\left( \deg(\nu_8(\mathbb{P}^1)) + 1 \right)",

		# --- Complex Analysis ---
		r"\left( \left(\int_{-\infty}^{\infty} \frac{dx}{(1+x^2)^5}\right) \cdot \frac{1152}{35\pi} \right)",
		r"\left( \operatorname{Res}_{z=0} \frac{9-z^2}{z(1-z)} \right)",

		# --- Templated & Combined ---
		r"\left( \text{rank}(\mathfrak{e}_7) + 2 \right)",
		r"\left( \text{rank}(\mathfrak{e}_6) + 3 \right)",
		r"\left( \dim(\mathfrak{so}(5)) - 1 \right)",
	]
	return templates


# --- Public Equation Functions (Wrappers) ---
def eq_0():
	logger.debug("Generating true PhD-level formula for digit 0")
	all_templates = _get_0_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_0 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_1():
	logger.debug("Generating true PhD-level formula for digit 1")
	all_templates = _get_1_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_1 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_2():
	logger.debug("Generating true PhD-level formula for digit 2")
	all_templates = _get_2_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_2 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_3():
	logger.debug("Generating true PhD-level formula for digit 3")
	all_templates = _get_3_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_3 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_4():
	logger.debug("Generating true PhD-level formula for digit 4")
	all_templates = _get_4_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_4 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_5():
	logger.debug("Generating true PhD-level formula for digit 5")
	all_templates = _get_5_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_5 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_6():
	logger.debug("Generating true PhD-level formula for digit 6")
	all_templates = _get_6_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_6 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_7():
	logger.debug("Generating true PhD-level formula for digit 7")
	all_templates = _get_7_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_7 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_8():
	logger.debug("Generating true PhD-level formula for digit 8")
	all_templates = _get_8_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_8 PhD-level choice: {chosen[:60]}...")
	return chosen


def eq_9():
	logger.debug("Generating true PhD-level formula for digit 9")
	all_templates = _get_9_templates()
	chosen = random.choice(all_templates)
	logger.debug(f"eq_9 PhD-level choice: {chosen[:60]}...")
	return chosen


# --- Main Execution Block ---
if __name__ == "__main__":
	provider_functions = {
		0: _get_0_templates, 1: _get_1_templates, 2: _get_2_templates,
		3: _get_3_templates, 4: _get_4_templates, 5: _get_5_templates,
		6: _get_6_templates, 7: _get_7_templates, 8: _get_8_templates,
		9: _get_9_templates,
	}

	total_equations = 0
	counts = {}
	print("-" * 40)
	print("Equation Bank Inventory:")
	print("-" * 40)
	for digit, get_templates_func in provider_functions.items():
		try:
			count = len(get_templates_func())  # Call to get list and count
			counts[digit] = count
			total_equations += count
			print(f"Digit {digit}: {count} equations")
		except Exception as e:
			logger.error(f"Error counting templates for digit {digit}: {e}")
			counts[digit] = "Error"

	print("-" * 40)
	print(f"Total Equations: {total_equations}")
	print("-" * 40)

	output_path = os.path.join(os.path.dirname(__file__), "equation_bank_output_full.txt")
	logger.info(f"Starting FULL equation generation for validation. Target: {output_path}")

	with open(output_path, "w", encoding="utf-8") as f:
		f.write(f"FULL PHD-LEVEL EQUATION BANK (Session: {SESSION_ID})\n")
		f.write("This file contains ALL templates for validation.\n")
		f.write("Each list of templates is generated with a fresh set of random parameters.\n")
		f.write("=" * 60 + "\n\n")

		for digit, get_templates_func in provider_functions.items():
			f.write(f"=== DIGIT {digit} (Found {counts.get(digit, 'N/A')} templates) ===\n")
			logger.info(f"Writing full template list for digit {digit}")

			try:
				all_equations = get_templates_func()  # Get full list with evaluated randoms
				for i, equation in enumerate(all_equations):
					f.write(f"{i + 1:02d}: $$ {equation} $$\n")
			except Exception as e:
				logger.error(f"Error generating full list for digit {digit}: {e}", exc_info=True)
				f.write(f"[ERROR generating list for digit {digit} - See log]\n")
			f.write("\n")

		f.write("=" * 60 + "\n")
		f.write("End of full equation bank.\n")

	logger.info(f"✅ Exported FULL equation bank to: {output_path}")
