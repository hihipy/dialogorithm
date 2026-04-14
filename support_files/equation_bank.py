"""
equation_bank.py — Dialogorithm equation template library.

Provides randomised, PhD-level LaTeX expressions for each digit (0–9)
and the '+' symbol. Each public ``eq_N()`` function draws randomly from
a curated pool of graduate-level expressions spanning Lie theory,
algebraic geometry, topology, number theory, complex analysis, and
mathematical physics. All expressions in a given pool evaluate to the
digit they represent.
"""

import logging
import os
import random

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_rand_int(min_val: int = 1, max_val: int = 10) -> int:
	"""Return a random integer in the closed interval [min_val, max_val]."""
	return random.randint(min_val, max_val)


# ---------------------------------------------------------------------------
# Symbol generators
# ---------------------------------------------------------------------------

def eq_plus() -> str:
	"""Return the LaTeX representation of the '+' symbol."""
	logger.debug("eq_plus: Generating LaTeX for plus symbol")
	return r"\mathbf{+}"


def eq_placeholder(digit_char: str) -> str:
	"""Return a fallback LaTeX expression for an unrecognised digit character.

	Logs a warning so missing templates are easy to spot during development.
	"""
	logger.warning(
		"eq_placeholder called for digit: '%s' — no template found.", digit_char
	)
	return rf"\mathbf{{\textit{{({digit_char})}}}}"


# ---------------------------------------------------------------------------
# Template pools  (private — one function per digit)
# ---------------------------------------------------------------------------
# --- Digit Equation Template Provider Functions ---

def _get_0_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 0."""
	n = get_rand_int(1, 3)

	templates = [
		# --- Differential & Algebraic Geometry ---
		r"\left( d^2\omega \right)",
		r"\left( H^1(\mathbb{P}^2, \mathcal{O}(-" + str(n) + r")) \right)",
		r"\left( \operatorname{ch}_0(\mathcal{E} \otimes \mathcal{F}) - \operatorname{ch}_0(\mathcal{E}) \cdot \operatorname{ch}_0(\mathcal{F}) \right)",
		r"\left( c_1(SU(n)) \right)",
		r"\left( p_1(M^3) \right)",

		# --- Homological Algebra & Topology ---
		r"\left( \partial_n \circ \partial_{n+1} \right)",
		r"\left( H_1(\mathbb{S}^2; \mathbb{Z}) \right)",
		r"\left( \operatorname{Ext}^1_{\mathbb{Z}}(\mathbb{Z}/n\mathbb{Z}, \mathbb{Q}) \right)",
		r"\left( \chi(SU(n)) \right)",
		r"\left( \operatorname{Tor}_1^{\mathbb{Z}}(\mathbb{Z}/n\mathbb{Z}, \mathbb{Q}) \right)",
		r"\left( \sigma(\partial W) \right)",
		r"\left( \hat{A}(\partial W) \right)",

		# --- Lie Theory & Representation Theory ---
		r"\left( [\mathbf{X}, \mathbf{X}] \right)",
		r"\left( [X, [Y, Z]] + [Y, [Z, X]] + [Z, [X, Y]] \right)",
		r"\left( \operatorname{Tr}(T^a_{\mathfrak{su}(n)}) \right)",
		r"\left( \langle \chi_i, \chi_j \rangle_{i \neq j} \right)",
		r"\left( \operatorname{index}(D_{\text{odd dim}}) \right)",

		# --- Advanced Number Theory & Analysis ---
		r"\left( \sum_{N=1}^{\infty} \frac{\mu(N)}{N} \right)",
		r"\left( \Gamma(z)\Gamma(1-z)\sin(\pi z) - \pi \right)",
		r"\left( \chi(\mathbb{S}^3) \right)",
		r"\left( \sum_{k=0}^{6} e^{2\pi i k/7} \right)",

		# --- Theoretical & Mathematical Physics ---
		rf"\left( J_{{{n}}}(z) Y_{{{n}-1}}(z) - J_{{{n}-1}}(z) Y_{{{n}}}(z) + \frac{{2}}{{\pi z}} \right)",
		r"\left( \langle[\hat{x}, \hat{p}_x]\rangle - i\hbar \right)",
		r"\left( \nabla_\mu g^{\alpha \beta} \right)",
	]
	return templates


def _get_1_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 1."""
	s_val = get_rand_int(2, 4)
	A_sym = 'A'

	templates = [
		# --- Abstract Algebra & Representation Theory ---
		r"\left( \operatorname{rk}(\operatorname{Pic}(\mathbb{P}^1)) \right)",
		r"\left( \operatorname{dim}(\mathfrak{so}(2)) \right)",
		r"\left( \operatorname{rank}(\operatorname{K}_0(\operatorname{Spec}(\mathbb{Z}))) \right)",
		rf"\left( \frac{{\det(e^{{{A_sym}}})}}{{e^{{\operatorname{{Tr}}({A_sym})}}}} \right)",
		r"\left( \operatorname{rank}(\mathfrak{su}(2)) \right)",
		r"\left( \frac{\chi_V(e)}{\operatorname{dim}(V)} \right)",
		r"\left( |Z(S_3)| \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{dim}_{\mathbb{C}} H^{0,0}(X) \right)",
		r"\left( h^{1,1}(\mathbb{P}^1) \right)",
		r"\left( \chi(\operatorname{Spec}(\mathbb{C})) \right)",
		r"\left( \frac{1}{2}\chi(\mathbb{S}^{0}) \right)",
		r"\left( \operatorname{dim}(H^0(\mathbb{P}^1, \mathcal{O}(0))) \right)",
		r"\left( \operatorname{genus}(\mathbb{P}^1) + 1 \right)",
		r"\left( \deg(\mathbb{P}^0) \right)",
		r"\left( h(-3) \right)",
		r"\left( \operatorname{lk}(L2a1) \right)",
		r"\left( b_0(\mathbb{T}^n) \right)",

		# --- Advanced Number Theory & Special Functions ---
		r"\left( \zeta(0) + \frac{3}{2} \right)",
		r"\left( \lim_{s \to 1} (s-1)\zeta(s) \right)",
		r"\left( \chi(\mathbb{D}^2) \right)",
		r"\left( \sum_{idx=1}^{\infty} \frac{\mu(idx)}{idx} + 1 \right)",
		r"\left( h(-4) \right)",

		# --- Analysis & Measure Theory ---
		r"\left( \lambda([0,1]) \right)",
		rf"\left( \int_0^{{\infty}} \frac{{x^{{{s_val}-1}}}}{{e^x - 1}} \,dx \cdot \frac{{1}}{{\Gamma({s_val})\zeta({s_val})}} \right)",
	]
	return templates


def _get_2_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 2."""
	n = get_rand_int(1, 3)
	s_val = get_rand_int(2, 4)

	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{rank}(\mathfrak{sl}_3(\mathbb{C})) \right)",
		r"\left( \operatorname{dim}(H^1(S_3, \mathbb{C}^*)) \right)",
		r"\left( \operatorname{dim}(\mathfrak{u}(1)) \cdot 2 \right)",
		r"\left( \operatorname{dim}(\mathfrak{so}(3)) - 1 \right)",
		r"\left( \operatorname{rank}(\mathfrak{so}(4)) \right)",
		r"\left( \operatorname{dim}(\mathfrak{sl}_2(\mathbb{C}))-1 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{rk}(\operatorname{Pic}(\mathbb{P}^1)) + 1 \right)",
		r"\left( \operatorname{dim}(H^0(\mathbb{P}^1, \mathcal{O}(1))) \right)",
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
		r"\left( |\operatorname{Aut}(S_3)| - 4 \right)",

		# --- Analysis & K-Theory ---
		r"\left( \operatorname{rank}(\operatorname{K}_0(\mathbb{P}^1)) \right)",
		r"\left( |\pi_0(O(2))| \right)",
		rf"\left( \left(\int_0^{{\infty}} \frac{{x^{{{s_val}-1}}}}{{e^x - 1}} \,dx \cdot \frac{{1}}{{\Gamma({s_val})\zeta({s_val})}}\right) \cdot 2 \right)",
	]
	return templates


def _get_3_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 3."""
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{dim}(\mathfrak{sl}_2(\mathbb{C})) \right)",
		r"\left( \operatorname{dim}(\mathfrak{su}(2)) \right)",
		r"\left( \operatorname{dim}(\operatorname{SO}(3)) \right)",
		r"\left( \operatorname{dim}(\operatorname{ad}(\mathfrak{su}(2))) \right)",
		r"\left( |W(A_2)| - 3 \right)",
		r"\left( \operatorname{rank}(\mathfrak{so}(7)) \right)",
		r"\left( |Irr(S_3)| \right)",
		r"\left( \operatorname{dim}(\mathfrak{g}_2) - 11 \right)",
		r"\left( \operatorname{dim}(\mathfrak{f}_4) - 49 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_7) - 4 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{dim}(H^0(\mathbb{P}^2, \mathcal{O}(1))) \right)",
		r"\left( \chi(\mathbb{CP}^2) \right)",
		r"\left( [\mathbb{Q}(\sqrt[3]{2}) : \mathbb{Q}] \right)",
		r"\left( b_1(\mathbb{T}^3) \right)",
		r"\left( c(3_1) \right)",
		r"\left( \operatorname{dim}(k[x,y,z]) \right)",
		r"\left( \deg(\nu_3(\mathbb{P}^1)) \right)",
		r"\left( c_1(T_{\mathbb{P}^2}) \cdot H \right)",
		r"\left( \sigma(E_8) - 5 \right)",

		# --- Advanced Number Theory ---
		r"\left( \zeta(-1) + \frac{37}{12} \right)",
		r"\left( h(-23) \right)",
		r"\left( \omega(30) \right)",
		r"\left( |\mathbb{A}_3| \right)",

		# --- Templated Expressions ---
		r"\left( \operatorname{rank}(\mathfrak{e}_8) - 5 \right)",
		r"\left( \frac{\Gamma(4)\Gamma(2)}{\Gamma(3)} \right)",
	]
	return templates


def _get_4_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 4."""
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{dim}(\mathfrak{so}(5)) - 6 \right)",
		r"\left( \operatorname{rank}(\mathfrak{so}(8)) \right)",
		r"\left( \operatorname{dim}(V_{\omega_1}(\mathfrak{sp}_4)) \right)",
		r"\left( \operatorname{dim}(\mathfrak{g}_2) - 10 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_7) - 3 \right)",
		r"\left( |W(A_2)| - 2 \right)",
		r"\left( \operatorname{dim}(\operatorname{ad}(\mathfrak{sl}_2(\mathbb{C}))) + 1 \right)",
		r"\left( \operatorname{dim}(\mathfrak{su}(3)) - 4 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{dim}(H^0(\mathbb{P}^3, \mathcal{O}(1))) \right)",
		r"\left( \chi(\mathbb{P}^2) + 1 \right)",
		r"\left( \operatorname{dim}(\operatorname{End}(\mathbb{C}^2)) \right)",
		r"\left( \deg(\nu_2(\mathbb{P}^2)) \right)",
		r"\left( \sum_i b_i(\mathbb{T}^2) \right)",
		r"\left( \operatorname{rank}(\pi_1(\Sigma_2)) \right)",
		r"\left( c_1(T_{\mathbb{P}^1 \times \mathbb{P}^1})^2 - 4 \right)",
		r"\left( \deg(K_{\mathbb{P}^2}) + 7 \right)",

		# --- Advanced Number Theory ---
		r"\left( \zeta(-3) + \frac{479}{120} \right)",
		r"\left( h(-39) \right)",
		r"\left( \operatorname{rank}(\mathfrak{f}_4) \right)",
		r"\left( \chi(\mathbb{CP}^3) \right)",
		r"\left( |\{\mathfrak{p} \subset \mathbb{Z}[i] \mid \mathfrak{p} | (13)\}| + 2 \right)",

		# --- Commutative Algebra & K-Theory ---
		r"\left( \operatorname{depth}(k[[w,x,y,z]]) \right)",
		r"\left( \operatorname{rank}(K_0(\mathbb{P}^1)) + 2 \right)",

		# --- Complex Analysis & Physics ---
		r"\left( \operatorname{Res}_{z=0} \frac{4\cos(z)}{z} \right)",
		r"\left( \sigma(E_8) - 4 \right)",
	]
	return templates


def _get_5_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 5."""
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{dim}(\mathfrak{sp}(4,\mathbb{C})) - 5 \right)",
		r"\left( \operatorname{dim}(\operatorname{U}(2)) + 1 \right)",
		r"\left( |Irr(D_4)| \right)",
		r"\left( \operatorname{rank}(\mathfrak{so}(11)) \right)",
		r"\left( \operatorname{dim}(\mathfrak{g}_2) - 9 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_8) - 3 \right)",
		r"\left( \sigma(E_8) - 3 \right)",
		r"\left( |W(A_2)| - 1 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{dim}(\operatorname{Symp}^5(\mathbb{C}^2)) - 1 \right)",
		r"\left( \operatorname{dim}(H^0(\mathbb{P}^4, \mathcal{O}(1))) \right)",
		r"\left( \chi(\mathbb{P}^2) + 2 \right)",
		r"\left( \chi(\mathbb{CP}^4) \right)",
		r"\left( c_1(T_{\mathbb{P}^2})^2 - 4 \right)",
		r"\left( b_1(\mathbb{T}^2) \cdot 2 + 1 \right)",
		r"\left( \deg(\nu_4(\mathbb{P}^1)) + 1 \right)",

		# --- Advanced Number Theory ---
		r"\left( h(-47) \right)",
		r"\left( v_2(32) \right)",
		r"\left( h(-23) + 2 \right)",
		r"\left( \zeta(-3) \cdot 120 + 4 \right)",

		# --- Templated & Combined ---
		r"\left( \operatorname{dim}(\mathfrak{sl}_2(\mathbb{C})) + 2 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_6) - 1 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_7) - 2 \right)",
		r"\left( \operatorname{dim}(\mathfrak{so}(4)) - 1 \right)",
		r"\left( \operatorname{dim}(\Lambda^2(\mathbb{C}^4)) - 1 \right)",
	]
	return templates


def _get_6_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 6."""
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{dim}(\mathfrak{so}(4,\mathbb{R})) \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_6) \right)",
		r"\left( |W(A_2)| \right)",
		r"\left( \operatorname{dim}(\mathfrak{so}(5)) - \operatorname{rank}(\mathfrak{so}(8)) \right)",
		r"\left( \operatorname{dim}(\Lambda^2(\mathbb{C}^4)) \right)",
		r"\left( \operatorname{dim}(\mathfrak{su}(3)) - 2 \right)",
		r"\left( \operatorname{dim}(\mathfrak{sp}(4,\mathbb{C})) - 4 \right)",
		r"\left( \operatorname{dim}(\mathfrak{g}_2) - 8 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{dim}(\operatorname{Symp}^6(\mathbb{C}^2)) - 1 \right)",
		r"\left( \phi(7) \right)",
		r"\left( -2 \deg(K_{\mathbb{P}^2}) \right)",
		r"\left( b_1(\mathbb{T}^2) \cdot 3 \right)",
		r"\left( h^{2,0}(\text{K3 surface}) + 5 \right)",
		r"\left( \chi(\mathbb{CP}^2) \cdot 2 \right)",
		r"\left( c_1^2(\mathbb{P}^2) - 3 \right)",

		# --- Advanced Number Theory ---
		r"\left( \zeta(-5) + \frac{1513}{252} \right)",
		r"\left( h(-87) \right)",
		r"\left( h(-23) \cdot 2 \right)",
		r"\left( v_2(2^6) \right)",
		r"\left( |\operatorname{Aut}(V_4)| \right)",

		# --- Complex Analysis ---
		r"\left( \operatorname{Res}_{z=0} \frac{e^{6z}-1}{z^2} \right)",

		# --- Templated & Combined ---
		r"\left( \operatorname{dim}(\mathfrak{sl}_2(\mathbb{C})) \cdot 2 \right)",
		r"\left( \zeta(0) \cdot (-12) \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_8) - 2 \right)",
	]
	return templates


def _get_7_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 7."""
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{rank}(\mathfrak{e}_7) \right)",
		r"\left( \operatorname{dim}(\operatorname{Sym}^6(\mathbb{C}^2)) \right)",
		r"\left( \operatorname{dim}(\operatorname{ad}(\mathfrak{su}(3))) - 1 \right)",
		r"\left( \operatorname{dim}(V_{\omega_1}(\mathfrak{g}_2)) \right)",
		r"\left( \chi(\mathbb{CP}^6) \right)",
		r"\left( |W(A_2)| + 1 \right)",
		r"\left( \operatorname{dim}(\mathfrak{sp}(4,\mathbb{C})) - 3 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{mult}_0(\mathbb{C}[x_1, \ldots, x_7]/(x_1 \cdots x_7)) \right)",
		r"\left( \operatorname{dim}(\operatorname{Symp}^7(\mathbb{C}^2)) - 1 \right)",
		r"\left( \tau(2^6) \right)",
		r"\left( b_1(\mathbb{T}^7) \right)",
		r"\left( \phi(9) + 1 \right)",
		r"\left( \deg(\nu_6(\mathbb{P}^1)) + 1 \right)",
		r"\left( c(7_1) \right)",

		# --- Advanced Number Theory ---
		r"\left( h(-71) \right)",
		r"\left( \operatorname{dim}(\Lambda^2(\mathbb{C}^5)) - 3 \right)",
		r"\left( \sum_{k=1}^5 p(5,k) \right)",
		r"\left( \phi(14) + 1 \right)",
		r"\left( \zeta(-3) \cdot 120 + 6 \right)",
		r"\left( h(-47) + 2 \right)",

		# --- Physics & Combined ---
		r"\left( \operatorname{dim}(\text{M-Theory}) - 4 \right)",
		r"\left( \sigma(E_8) - 1 \right)",
		r"\left( \operatorname{dim}(\mathfrak{g}_2) - 7 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_6) + 1 \right)",
		r"\left( \left(\int_{-\infty}^{\infty} \frac{dx}{(1+x^2)^4}\right) \cdot \frac{112}{5\pi} \right)",
	]
	return templates


def _get_8_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 8."""
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{dim}(\mathfrak{sl}(3,\mathbb{C})) \right)",
		r"\left( \operatorname{dim}(\mathfrak{so}(5)) - 2 \right)",
		r"\left( \operatorname{dim}(\operatorname{SU}(3)) \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_8) \right)",
		r"\left( \operatorname{dim}(\operatorname{ad}(\mathfrak{sl}_3(\mathbb{C}))) \right)",
		r"\left( |\Delta(\mathfrak{sp}_4)| \right)",
		r"\left( \operatorname{dim}(\mathfrak{f}_4) - 44 \right)",
		r"\left( \operatorname{dim}(\mathfrak{g}_2) - 6 \right)",
		r"\left( \operatorname{dim}(\mathfrak{e}_7) - 125 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{dim}(\operatorname{Symp}^8(\mathbb{C}^2)) - 1 \right)",
		r"\left( \sigma(E_8) \right)",
		r"\left( c_1(T_{\mathbb{P}^1 \times \mathbb{P}^1})^2 \right)",
		r"\left( \operatorname{dim}(\mathfrak{e}_8) - 240 \right)",
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
		r"\left( \operatorname{rank}(\mathfrak{e}_6) + 2 \right)",
		r"\left( \chi(\mathbb{CP}^2) \cdot 3 - 1 \right)",
	]
	return templates


def _get_9_templates() -> list:
	"""Return the full pool of LaTeX expressions that evaluate to 9."""
	templates = [
		# --- Lie Theory & Representation Theory ---
		r"\left( \operatorname{dim}(\mathfrak{so}(3) \otimes \mathfrak{so}(3)) \right)",
		r"\left( \operatorname{dim}(\mathfrak{sl}(3,\mathbb{C})) + 1 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_8) + 1 \right)",
		r"\left( \sigma(E_8) + 1 \right)",
		r"\left( |W(A_2)| + 3 \right)",
		r"\left( \operatorname{dim}(\mathfrak{g}_2) - 5 \right)",
		r"\left( \operatorname{dim}(\mathfrak{f}_4) - 43 \right)",
		r"\left( \operatorname{dim}(\mathfrak{e}_7) - 124 \right)",
		r"\left( \operatorname{dim}(\operatorname{ad}(\mathfrak{su}(3))) + 1 \right)",

		# --- Algebraic Geometry & Topology ---
		r"\left( \operatorname{dim}(\operatorname{Symp}^9(\mathbb{C}^2)) - 1 \right)",
		r"\left( c_1(T_{\mathbb{P}^2})^2 \right)",
		r"\left( h^{1,1}(\text{K3 surface}) - 11 \right)",
		r"\left( b_1(\mathbb{T}^3) \cdot 3 \right)",
		r"\left( c(5_1) + 4 \right)",

		# --- Advanced Number Theory ---
		r"\left( h(-199) \right)",
		r"\left( \tau(36) \right)",
		r"\left( v_3(3^9) \right)",
		r"\left( h(-87) + 3 \right)",
		r"\left( h(-47) + 4 \right)",
		r"\left( \deg(\nu_8(\mathbb{P}^1)) + 1 \right)",

		# --- Complex Analysis ---
		r"\left( \left(\int_{-\infty}^{\infty} \frac{dx}{(1+x^2)^5}\right) \cdot \frac{1152}{35\pi} \right)",
		r"\left( \operatorname{Res}_{z=0} \frac{9-z^2}{z(1-z)} \right)",

		# --- Templated & Combined ---
		r"\left( \operatorname{rank}(\mathfrak{e}_7) + 2 \right)",
		r"\left( \operatorname{rank}(\mathfrak{e}_6) + 3 \right)",
		r"\left( \operatorname{dim}(\mathfrak{so}(5)) - 1 \right)",
	]
	return templates


# ---------------------------------------------------------------------------
# Public digit functions  (each picks one template at random)
# ---------------------------------------------------------------------------

def eq_0() -> str:
	"""Return a random LaTeX expression that evaluates to 0."""
	logger.debug("eq_0: selecting template")
	chosen = random.choice(_get_0_templates())
	logger.debug("eq_0 choice: %s...", chosen[:60])
	return chosen


def eq_1() -> str:
	"""Return a random LaTeX expression that evaluates to 1."""
	logger.debug("eq_1: selecting template")
	chosen = random.choice(_get_1_templates())
	logger.debug("eq_1 choice: %s...", chosen[:60])
	return chosen


def eq_2() -> str:
	"""Return a random LaTeX expression that evaluates to 2."""
	logger.debug("eq_2: selecting template")
	chosen = random.choice(_get_2_templates())
	logger.debug("eq_2 choice: %s...", chosen[:60])
	return chosen


def eq_3() -> str:
	"""Return a random LaTeX expression that evaluates to 3."""
	logger.debug("eq_3: selecting template")
	chosen = random.choice(_get_3_templates())
	logger.debug("eq_3 choice: %s...", chosen[:60])
	return chosen


def eq_4() -> str:
	"""Return a random LaTeX expression that evaluates to 4."""
	logger.debug("eq_4: selecting template")
	chosen = random.choice(_get_4_templates())
	logger.debug("eq_4 choice: %s...", chosen[:60])
	return chosen


def eq_5() -> str:
	"""Return a random LaTeX expression that evaluates to 5."""
	logger.debug("eq_5: selecting template")
	chosen = random.choice(_get_5_templates())
	logger.debug("eq_5 choice: %s...", chosen[:60])
	return chosen


def eq_6() -> str:
	"""Return a random LaTeX expression that evaluates to 6."""
	logger.debug("eq_6: selecting template")
	chosen = random.choice(_get_6_templates())
	logger.debug("eq_6 choice: %s...", chosen[:60])
	return chosen


def eq_7() -> str:
	"""Return a random LaTeX expression that evaluates to 7."""
	logger.debug("eq_7: selecting template")
	chosen = random.choice(_get_7_templates())
	logger.debug("eq_7 choice: %s...", chosen[:60])
	return chosen


def eq_8() -> str:
	"""Return a random LaTeX expression that evaluates to 8."""
	logger.debug("eq_8: selecting template")
	chosen = random.choice(_get_8_templates())
	logger.debug("eq_8 choice: %s...", chosen[:60])
	return chosen


def eq_9() -> str:
	"""Return a random LaTeX expression that evaluates to 9."""
	logger.debug("eq_9: selecting template")
	chosen = random.choice(_get_9_templates())
	logger.debug("eq_9 choice: %s...", chosen[:60])
	return chosen


# ---------------------------------------------------------------------------
# CLI — run directly to audit the full template inventory
# ---------------------------------------------------------------------------

if __name__ == "__main__":
	_PROVIDERS = {
		0: _get_0_templates, 1: _get_1_templates, 2: _get_2_templates,
		3: _get_3_templates, 4: _get_4_templates, 5: _get_5_templates,
		6: _get_6_templates, 7: _get_7_templates, 8: _get_8_templates,
		9: _get_9_templates,
	}

	total = 0
	counts: dict = {}

	print("-" * 40)
	print("Equation Bank Inventory:")
	print("-" * 40)
	for digit, fn in _PROVIDERS.items():
		try:
			n = len(fn())
			counts[digit] = n
			total += n
			print(f"Digit {digit}: {n} equations")
		except Exception as exc:
			logger.error("Error counting templates for digit %d: %s", digit, exc)
			counts[digit] = "Error"

	print("-" * 40)
	print(f"Total Equations: {total}")
	print("-" * 40)

	output_path = os.path.join(os.path.dirname(__file__), "equation_bank_output_full.txt")
	logger.info("Exporting full equation bank to: %s", output_path)

	with open(output_path, "w", encoding="utf-8") as fh:
		fh.write("FULL PHD-LEVEL EQUATION BANK\n")
		fh.write("=" * 60 + "\n\n")
		for digit, fn in _PROVIDERS.items():
			fh.write(f"=== DIGIT {digit} ({counts.get(digit, 'N/A')} templates) ===\n")
			try:
				for i, eq in enumerate(fn()):
					fh.write(f"{i + 1:02d}: $$ {eq} $$\n")
			except Exception as exc:
				logger.error("Error exporting digit %d: %s", digit, exc, exc_info=True)
				fh.write(f"[ERROR — see log]\n")
			fh.write("\n")
		fh.write("=" * 60 + "\n")

	logger.info("Export complete: %s", output_path)
