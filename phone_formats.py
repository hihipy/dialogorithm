"""
phone_formats.py

Complete phone number formatting module for international standards.
Contains all ~249 countries/territories with formatting rules, digit limits,
and validation logic, organized by UN geoscheme continents and subregions.

🎯 Key Features:
- UN Statistics Division geoscheme classification
- Local digit validation (excludes country codes)
- Country-specific formatting rules
- Complete world coverage (249+ entries)
- Antarctica handled as proper subregion

Usage:
    from phone_formats import COUNTRIES_BY_CONTINENT, get_digit_limit, format_display_number
"""

import re
from typing import Optional, Tuple, Dict, Any, List

# --- Complete UN Geoscheme Data Structure ---
COUNTRIES_BY_CONTINENT = {
	'Africa': {
		'Northern Africa': {
			"🇩🇿 Algeria": "+213 XXX XXX XXX",
			"🇪🇬 Egypt": "+20 X XXXX XXXX",
			"🇱🇾 Libya": "+218 XX XXX XXXX",
			"🇲🇦 Morocco": "+212 X XXX XXXX",
			"🇸🇩 Sudan": "+249 XXX XXX XXX",
			"🇹🇳 Tunisia": "+216 XX XXX XXX",
			"🇪🇭 Western Sahara": "+212 X XXX XXXX",
		},
		'Western Africa': {
			"🇧🇯 Benin": "+229 XX XX XXXX",
			"🇧🇫 Burkina Faso": "+226 XX XX XXXX",
			"🇨🇻 Cape Verde": "+238 XXX XXXX",
			"🇨🇮 Côte d'Ivoire": "+225 XX XX XXXX",
			"🇬🇲 Gambia": "+220 XXX XXXX",
			"🇬🇭 Ghana": "+233 XX XXX XXXX",
			"🇬🇳 Guinea": "+224 XXX XXX XXX",
			"🇬🇼 Guinea-Bissau": "+245 XX XXX XXX",
			"🇱🇷 Liberia": "+231 XX XXX XXX",
			"🇲🇱 Mali": "+223 XX XX XXXX",
			"🇲🇷 Mauritania": "+222 XXXX XXXX",
			"🇳🇪 Niger": "+227 XX XX XXXX",
			"🇳🇬 Nigeria": "+234 XXX XXX XXXX",
			"🇸🇳 Senegal": "+221 XXX XXX XXX",
			"🇸🇱 Sierra Leone": "+232 XX XXX XXX",
			"🇹🇬 Togo": "+228 XX XXX XXX",
		},
		'Eastern Africa': {
			"🇧🇮 Burundi": "+257 XX XX XXXX",
			"🇰🇲 Comoros": "+269 XXX XXXX",
			"🇩🇯 Djibouti": "+253 XX XX XX XX",
			"🇪🇷 Eritrea": "+291 X XXX XXX",
			"🇪🇹 Ethiopia": "+251 XXX XXX XXX",
			"🇰🇪 Kenya": "+254 XXX XXX XXX",
			"🇲🇬 Madagascar": "+261 XX XX XXX XX",
			"🇲🇼 Malawi": "+265 X XXX XXX",
			"🇲🇺 Mauritius": "+230 XXX XXXX",
			"🇾🇹 Mayotte": "+262 XXX XXX XXX",
			"🇲🇿 Mozambique": "+258 XX XXX XXXX",
			"🇷🇪 Réunion": "+262 XXX XXX XXX",
			"🇷🇼 Rwanda": "+250 XXX XXX XXX",
			"🇸🇨 Seychelles": "+248 XXX XXXX",
			"🇸🇴 Somalia": "+252 XXX XXX XXX",
			"🇸🇸 South Sudan": "+211 XXX XXX XXX",
			"🇹🇿 Tanzania": "+255 XXX XXX XXX",
			"🇺🇬 Uganda": "+256 XXX XXX XXX",
			"🇿🇲 Zambia": "+260 XXX XXX XXX",
			"🇿🇼 Zimbabwe": "+263 XX XXX XXXX",
		},
		'Central Africa': {
			"🇦🇴 Angola": "+244 XXX XXX XXX",
			"🇨🇲 Cameroon": "+237 XXXX XXXX",
			"🇨🇫 Central African Republic": "+236 XX XX XXXX",
			"🇹🇩 Chad": "+235 XX XX XX XX",
			"🇨🇬 Congo (Brazzaville)": "+242 XXX XXX XXX",
			"🇨🇩 Congo (Kinshasa)": "+243 XXX XXX XXX",
			"🇬🇶 Equatorial Guinea": "+240 XXX XXX XXX",
			"🇬🇦 Gabon": "+241 XX XX XXXX",
			"🇸🇹 São Tomé & Príncipe": "+239 XXX XXXX",
		},
		'Southern Africa': {
			"🇧🇼 Botswana": "+267 XX XXX XXX",
			"🇸🇿 Eswatini": "+268 XXXX XXXX",
			"🇱🇸 Lesotho": "+266 XXX XXXX",
			"🇳🇦 Namibia": "+264 XX XXX XXXX",
			"🇿🇦 South Africa": "+27 XX XXX XXXX",
			"🇸🇭 Saint Helena": "+290 XXXX",
		},
	},
	'Americas': {
		'Northern America': {
			"🇧🇲 Bermuda": "+1 441 XXX XXXX",
			"🇨🇦 Canada": "+1 (XXX) XXX-XXXX",
			"🇬🇱 Greenland": "+299 XXX XXX",
			"🇵🇲 Saint Pierre & Miquelon": "+508 XX XXXX",
			"🇺🇸 United States": "+1 (XXX) XXX-XXXX",
		},
		'Caribbean': {
			"🇦🇮 Anguilla": "+1 264 XXX XXXX",
			"🇦🇬 Antigua & Barbuda": "+1 268 XXX XXXX",
			"🇦🇼 Aruba": "+297 XXX XXXX",
			"🇧🇸 Bahamas": "+1 242 XXX XXXX",
			"🇧🇧 Barbados": "+1 246 XXX XXXX",
			"🇧🇶 Bonaire": "+599 XXX XXXX",
			"🇻🇬 British Virgin Islands": "+1 284 XXX XXXX",
			"🇰🇾 Cayman Islands": "+1 345 XXX XXXX",
			"🇨🇺 Cuba": "+53 X XXX XXXX",
			"🇨🇼 Curaçao": "+599 X XXX XXXX",
			"🇩🇲 Dominica": "+1 767 XXX XXXX",
			"🇩🇴 Dominican Republic": "+1 XXX XXX XXXX",
			"🇬🇩 Grenada": "+1 473 XXX XXXX",
			"🇬🇵 Guadeloupe": "+590 XXX XXX XXX",
			"🇭🇹 Haiti": "+509 XXXX XXXX",
			"🇯🇲 Jamaica": "+1 876 XXX XXXX",
			"🇲🇶 Martinique": "+596 XXX XXX XXX",
			"🇲🇸 Montserrat": "+1 664 XXX XXXX",
			"🇵🇷 Puerto Rico": "+1 XXX XXX XXXX",
			"🇰🇳 Saint Kitts & Nevis": "+1 869 XXX XXXX",
			"🇱🇨 Saint Lucia": "+1 758 XXX XXXX",
			"🇲🇫 Saint Martin": "+590 XXX XXX XXX",
			"🇻🇨 Saint Vincent & Grenadines": "+1 784 XXX XXXX",
			"🇸🇽 Sint Maarten": "+1 721 XXX XXXX",
			"🇹🇹 Trinidad & Tobago": "+1 868 XXX XXXX",
			"🇹🇨 Turks & Caicos Islands": "+1 649 XXX XXXX",
			"🇻🇮 U.S. Virgin Islands": "+1 340 XXX XXXX",
		},
		'Central America': {
			"🇧🇿 Belize": "+501 XXX XXXX",
			"🇨🇷 Costa Rica": "+506 XXXX XXXX",
			"🇸🇻 El Salvador": "+503 XXXX XXXX",
			"🇬🇹 Guatemala": "+502 XXXX XXXX",
			"🇭🇳 Honduras": "+504 XXXX XXXX",
			"🇲🇽 Mexico": "+52 XXX XXX XXXX",
			"🇳🇮 Nicaragua": "+505 XXXX XXXX",
			"🇵🇦 Panama": "+507 XXX XXXX",
		},
		'South America': {
			"🇦🇷 Argentina": "+54 9 XXX XXX XXXX",
			"🇧🇴 Bolivia": "+591 XXX XXX XX",
			"🇧🇻 Bouvet Island": "+47 XXXX XXXX",
			"🇧🇷 Brazil": "+55 XX XXXXX XXXX",
			"🇨🇱 Chile": "+56 X XXXX XXXX",
			"🇨🇴 Colombia": "+57 XXX XXX XXXX",
			"🇪🇨 Ecuador": "+593 XX XXX XXXX",
			"🇫🇰 Falkland Islands": "+500 XXXXX",
			"🇬🇫 French Guiana": "+594 XXX XXX XXX",
			"🇬🇸 South Georgia": "+500 XXXXX",
			"🇬🇾 Guyana": "+592 XXX XXXX",
			"🇵🇾 Paraguay": "+595 XXX XXX XXX",
			"🇵🇪 Peru": "+51 X XXX XXXX",
			"🇸🇷 Suriname": "+597 XXX XXXX",
			"🇺🇾 Uruguay": "+598 XXX XXX XXX",
			"🇻🇪 Venezuela": "+58 XXX XXX XXXX",
		},
	},
	'Asia': {
		'Central Asia': {
			"🇰🇿 Kazakhstan": "+7 XXX XXX XXXX",
			"🇰🇬 Kyrgyzstan": "+996 XXX XXX XXX",
			"🇹🇯 Tajikistan": "+992 XXX XXX XXX",
			"🇹🇲 Turkmenistan": "+993 XX XXX XXX",
			"🇺🇿 Uzbekistan": "+998 XX XXX XXXX",
		},
		'Eastern Asia': {
			"🇨🇳 China": "+86 XXX XXXX XXXX",
			"🇭🇰 Hong Kong": "+852 XXXX XXXX",
			"🇯🇵 Japan": "+81 XX XXXX XXXX",
			"🇲🇴 Macao": "+853 XXXX XXXX",
			"🇲🇳 Mongolia": "+976 XX XXXX XXXX",
			"🇰🇵 North Korea": "+850 XXX XXX XXXX",
			"🇰🇷 South Korea": "+82 XX XXX XXXX",
			"🇹🇼 Taiwan": "+886 X XXXX XXXX",
		},
		'South-Eastern Asia': {
			"🇧🇳 Brunei": "+673 XXX XXXX",
			"🇰🇭 Cambodia": "+855 XX XXX XXX",
			"🇮🇩 Indonesia": "+62 XXX XXXX XXXX",
			"🇱🇦 Laos": "+856 XX XXX XXX",
			"🇲🇾 Malaysia": "+60 X XXX XXXX",
			"🇲🇲 Myanmar": "+95 X XXX XXX",
			"🇵🇭 Philippines": "+63 XXX XXX XXXX",
			"🇸🇬 Singapore": "+65 XXXX XXXX",
			"🇹🇭 Thailand": "+66 X XXXX XXXX",
			"🇹🇱 Timor-Leste": "+670 XXX XXXX",
			"🇻🇳 Vietnam": "+84 XXX XXX XXXX",
		},
		'Southern Asia': {
			"🇦🇫 Afghanistan": "+93 XX XXX XXXX",
			"🇧🇩 Bangladesh": "+880 1XXX XXX XXX",
			"🇧🇹 Bhutan": "+975 XX XXX XXX",
			"🇮🇳 India": "+91 XXXXX XXXXX",
			"🇮🇷 Iran": "+98 XXX XXX XXXX",
			"🇲🇻 Maldives": "+960 XXX XXXX",
			"🇳🇵 Nepal": "+977 X XXX XXX",
			"🇵🇰 Pakistan": "+92 XXX XXX XXXX",
			"🇱🇰 Sri Lanka": "+94 XX XXX XXXX",
		},
		'Western Asia': {
			"🇦🇲 Armenia": "+374 XX XXX XXX",
			"🇦🇿 Azerbaijan": "+994 XX XXX XXXX",
			"🇧🇭 Bahrain": "+973 XXXX XXXX",
			"🇨🇾 Cyprus": "+357 XX XXX XXX",
			"🇬🇪 Georgia": "+995 XXX XXX XXX",
			"🇮🇶 Iraq": "+964 XXX XXX XXXX",
			"🇮🇱 Israel": "+972 XX XXX XXXX",
			"🇯🇴 Jordan": "+962 X XXX XXXX",
			"🇰🇼 Kuwait": "+965 XXXX XXXX",
			"🇱🇧 Lebanon": "+961 X XXX XXX",
			"🇴🇲 Oman": "+968 XXXX XXXX",
			"🇵🇸 Palestine": "+970 XXX XXX XXXX",
			"🇶🇦 Qatar": "+974 XXXX XXXX",
			"🇷🇺 Russia": "+7 XXX XXX XXXX",
			"🇸🇦 Saudi Arabia": "+966 X XXX XXXX",
			"🇸🇾 Syria": "+963 XXX XXX XXX",
			"🇹🇷 Turkey": "+90 XXX XXX XXXX",
			"🇦🇪 United Arab Emirates": "+971 XX XXX XXXX",
			"🇾🇪 Yemen": "+967 XXX XXX XXX",
		},
	},
	'Europe': {
		'Eastern Europe': {
			"🇧🇾 Belarus": "+375 XX XXX XXXX",
			"🇧🇬 Bulgaria": "+359 XXX XXX XXX",
			"🇨🇿 Czech Republic": "+420 XXX XXX XXX",
			"🇭🇺 Hungary": "+36 XX XXX XXXX",
			"🇲🇩 Moldova": "+373 XXX XXX XX",
			"🇵🇱 Poland": "+48 XXX XXX XXX",
			"🇷🇴 Romania": "+40 XXX XXX XXX",
			"🇷🇺 Russia": "+7 XXX XXX XXXX",
			"🇸🇰 Slovakia": "+421 XXX XXX XXX",
			"🇺🇦 Ukraine": "+380 XX XXX XXXX",
		},
		'Northern Europe': {
			"🇦🇽 Åland Islands": "+358 XX XXX XXXX",
			"🇩🇰 Denmark": "+45 XX XX XX XX",
			"🇪🇪 Estonia": "+372 XXX XXXX",
			"🇫🇴 Faroe Islands": "+298 XXX XXX",
			"🇫🇮 Finland": "+358 XX XXX XXXX",
			"🇬🇬 Guernsey": "+44 XXXX XXXXXX",
			"🇮🇸 Iceland": "+354 XXX XXXX",
			"🇮🇪 Ireland": "+353 XX XXX XXXX",
			"🇮🇲 Isle of Man": "+44 XXXX XXXXXX",
			"🇯🇪 Jersey": "+44 XXXX XXXXXX",
			"🇱🇻 Latvia": "+371 XX XXX XXX",
			"🇱🇹 Lithuania": "+370 XXX XX XXX",
			"🇳🇴 Norway": "+47 XXXX XXXX",
			"🇸🇯 Svalbard": "+47 XXXX XXXX",
			"🇸🇪 Sweden": "+46 XX XXX XXXX",
			"🇬🇧 United Kingdom": "+44 XXXX XXXXXX",
		},
		'Southern Europe': {
			"🇦🇱 Albania": "+355 XX XXX XXXX",
			"🇦🇩 Andorra": "+376 XXX XXX",
			"🇧🇦 Bosnia and Herzegovina": "+387 XX XXX XXX",
			"🇭🇷 Croatia": "+385 XX XXX XXX",
			"🇬🇮 Gibraltar": "+350 XXXX XXXX",
			"🇬🇷 Greece": "+30 XXX XXX XXXX",
			"🇮🇹 Italy": "+39 XXX XXX XXXX",
			"🇽🇰 Kosovo": "+383 XX XXX XXX",
			"🇲🇹 Malta": "+356 XXXX XXXX",
			"🇲🇪 Montenegro": "+382 XX XXX XXX",
			"🇲🇰 North Macedonia": "+389 XX XXX XXX",
			"🇵🇹 Portugal": "+351 XXX XXX XXX",
			"🇸🇲 San Marino": "+378 XXX XXX",
			"🇷🇸 Serbia": "+381 XX XXX XXX",
			"🇸🇮 Slovenia": "+386 XX XXX XXX",
			"🇪🇸 Spain": "+34 XXX XXX XXX",
			"🇻🇦 Vatican City": "+39 XXX XXX XXXX",
		},
		'Western Europe': {
			"🇦🇹 Austria": "+43 XXX XXX XXXX",
			"🇧🇪 Belgium": "+32 XXX XX XX XX",
			"🇫🇷 France": "+33 X XX XX XX XX",
			"🇩🇪 Germany": "+49 XXXX XXXXXXX",
			"🇱🇮 Liechtenstein": "+423 XXX XXXX",
			"🇱🇺 Luxembourg": "+352 XXX XXX XXX",
			"🇲🇨 Monaco": "+377 XX XX XX XX",
			"🇳🇱 Netherlands": "+31 XX XXX XXXX",
			"🇨🇭 Switzerland": "+41 XX XXX XXXX",
		},
	},
	'Oceania': {
		'Australia and New Zealand': {
			"🇦🇺 Australia": "+61 X XXXX XXXX",
			"🇨🇽 Christmas Island": "+61 X XXXX XXXX",
			"🇨🇨 Cocos (Keeling) Islands": "+61 X XXXX XXXX",
			"🇭🇲 Heard Island & McDonald Islands": "+672 XXX XXX",
			"🇳🇿 New Zealand": "+64 XX XXX XXXX",
			"🇳🇫 Norfolk Island": "+672 XXX XXX",
		},
		'Melanesia': {
			"🇫🇯 Fiji": "+679 XXX XXXX",
			"🇳🇨 New Caledonia": "+687 XX XXXX",
			"🇵🇬 Papua New Guinea": "+675 XXX XXX XXXX",
			"🇸🇧 Solomon Islands": "+677 XXXXX",
			"🇻🇺 Vanuatu": "+678 XXX XXX",
		},
		'Micronesia': {
			"🇬🇺 Guam": "+1 671 XXX XXXX",
			"🇰🇮 Kiribati": "+686 XXX XXX",
			"🇲🇭 Marshall Islands": "+692 XXX XXXX",
			"🇫🇲 Micronesia": "+691 XXX XXXX",
			"🇳🇷 Nauru": "+674 XXX XXX",
			"🇲🇵 Northern Mariana Islands": "+1 670 XXX XXXX",
			"🇵🇼 Palau": "+680 XXX XXXX",
		},
		'Polynesia': {
			"🇦🇸 American Samoa": "+1 684 XXX XXXX",
			"🇨🇰 Cook Islands": "+682 XX XXX",
			"🇵🇫 French Polynesia": "+689 XX XX XX XX",
			"🇳🇺 Niue": "+683 XXXX",
			"🇵🇳 Pitcairn Islands": "+872 XXX XXX",
			"🇼🇸 Samoa": "+685 XXX XXXX",
			"🇹🇰 Tokelau": "+690 XXXX",
			"🇹🇴 Tonga": "+676 XXX XXX",
			"🇹🇻 Tuvalu": "+688 XXX XXX",
			"🇼🇫 Wallis & Futuna": "+681 XX XXXX",
		},
	},
	'Antarctica': {
		'Antarctica': {
			"🇦🇶 Antarctica": "+672 XXX XXX",
		},
	},
}

# --- LOCAL DIGIT LIMITS: CRITICAL FOR VALIDATION ---
# These are LOCAL digits only (excluding country code)
# Example: US is +1 (555) 123-4567 → LOCAL_DIGITS = "5551234567" (10 digits)
LOCAL_DIGIT_LIMITS_BY_CODE = {
	1: 10,  # US/Canada/Caribbean
	7: 10,  # Russia/Kazakhstan
	20: 9,  # Egypt
	27: 9,  # South Africa
	30: 10,  # Greece
	31: 9,  # Netherlands
	32: 9,  # Belgium
	33: 10,  # France
	34: 9,  # Spain
	36: 9,  # Hungary
	39: 10,  # Italy/Vatican
	40: 9,  # Romania
	41: 9,  # Switzerland
	43: 11,  # Austria
	44: 11,  # UK/Crown Dependencies
	45: 8,  # Denmark
	46: 9,  # Sweden
	47: 8,  # Norway/Svalbard/Bouvet
	48: 9,  # Poland
	49: 11,  # Germany
	51: 9,  # Peru
	52: 10,  # Mexico
	53: 8,  # Cuba
	54: 10,  # Argentina
	55: 11,  # Brazil
	56: 9,  # Chile
	57: 10,  # Colombia
	58: 10,  # Venezuela
	60: 9,  # Malaysia
	61: 9,  # Australia/Christmas/Cocos
	62: 11,  # Indonesia
	63: 10,  # Philippines
	64: 9,  # New Zealand
	65: 8,  # Singapore
	66: 9,  # Thailand
	81: 10,  # Japan
	82: 10,  # South Korea
	84: 9,  # Vietnam
	86: 11,  # China
	90: 10,  # Turkey
	91: 10,  # India
	92: 10,  # Pakistan
	93: 9,  # Afghanistan
	94: 9,  # Sri Lanka
	95: 9,  # Myanmar
	98: 10,  # Iran
	211: 9,  # South Sudan
	212: 9,  # Morocco/Western Sahara
	213: 9,  # Algeria
	216: 8,  # Tunisia
	218: 9,  # Libya
	220: 7,  # Gambia
	221: 9,  # Senegal
	222: 8,  # Mauritania
	223: 8,  # Mali
	224: 9,  # Guinea
	225: 8,  # Côte d'Ivoire
	226: 8,  # Burkina Faso
	227: 8,  # Niger
	228: 8,  # Togo
	229: 8,  # Benin
	230: 7,  # Mauritius
	231: 8,  # Liberia
	232: 8,  # Sierra Leone
	233: 9,  # Ghana
	234: 10,  # Nigeria
	235: 8,  # Chad
	236: 8,  # Central African Republic
	237: 9,  # Cameroon
	238: 7,  # Cape Verde
	239: 7,  # São Tomé & Príncipe
	240: 9,  # Equatorial Guinea
	241: 8,  # Gabon
	242: 9,  # Congo (Brazzaville)
	243: 9,  # Congo (Kinshasa)
	244: 9,  # Angola
	245: 7,  # Guinea-Bissau
	248: 7,  # Seychelles
	249: 9,  # Sudan
	250: 9,  # Rwanda
	251: 9,  # Ethiopia
	252: 8,  # Somalia
	253: 8,  # Djibouti
	254: 9,  # Kenya
	255: 9,  # Tanzania
	256: 9,  # Uganda
	257: 8,  # Burundi
	258: 9,  # Mozambique
	260: 9,  # Zambia
	261: 10,  # Madagascar
	262: 9,  # Mayotte/Réunion
	263: 9,  # Zimbabwe
	264: 9,  # Namibia
	265: 9,  # Malawi
	266: 8,  # Lesotho
	267: 8,  # Botswana
	268: 8,  # Eswatini
	269: 7,  # Comoros
	290: 4,  # Saint Helena
	291: 7,  # Eritrea
	297: 7,  # Aruba
	298: 6,  # Faroe Islands
	299: 6,  # Greenland
	350: 8,  # Gibraltar
	351: 9,  # Portugal
	352: 9,  # Luxembourg
	353: 9,  # Ireland
	354: 7,  # Iceland
	355: 9,  # Albania
	356: 8,  # Malta
	357: 8,  # Cyprus
	358: 10,  # Finland/Åland
	359: 9,  # Bulgaria
	370: 8,  # Lithuania
	371: 8,  # Latvia
	372: 8,  # Estonia
	373: 8,  # Moldova
	374: 8,  # Armenia
	375: 9,  # Belarus
	376: 6,  # Andorra
	377: 8,  # Monaco
	378: 10,  # San Marino
	380: 9,  # Ukraine
	381: 9,  # Serbia
	382: 8,  # Montenegro
	383: 8,  # Kosovo
	385: 9,  # Croatia
	386: 8,  # Slovenia
	387: 8,  # Bosnia and Herzegovina
	389: 8,  # North Macedonia
	420: 9,  # Czech Republic
	421: 9,  # Slovakia
	423: 7,  # Liechtenstein
	500: 5,  # Falkland Islands/South Georgia
	501: 7,  # Belize
	502: 8,  # Guatemala
	503: 8,  # El Salvador
	504: 8,  # Honduras
	505: 8,  # Nicaragua
	506: 8,  # Costa Rica
	507: 8,  # Panama
	508: 6,  # Saint Pierre & Miquelon
	509: 8,  # Haiti
	590: 9,  # Guadeloupe/Saint Martin
	591: 8,  # Bolivia
	592: 7,  # Guyana
	593: 9,  # Ecuador
	594: 9,  # French Guiana
	595: 9,  # Paraguay
	596: 9,  # Martinique
	597: 7,  # Suriname
	598: 8,  # Uruguay
	599: 7,  # Netherlands Antilles/Curaçao/Bonaire
	670: 8,  # Timor-Leste
	671: 7,  # Guam
	672: 6,  # Norfolk Island/Antarctica
	673: 7,  # Brunei
	674: 7,  # Nauru
	675: 8,  # Papua New Guinea
	676: 7,  # Tonga
	677: 7,  # Solomon Islands
	678: 7,  # Vanuatu
	679: 7,  # Fiji
	680: 7,  # Palau
	681: 6,  # Wallis & Futuna
	682: 5,  # Cook Islands
	683: 4,  # Niue
	684: 7,  # American Samoa
	685: 7,  # Samoa
	686: 8,  # Kiribati
	687: 6,  # New Caledonia
	688: 5,  # Tuvalu
	689: 8,  # French Polynesia
	690: 4,  # Tokelau
	691: 7,  # Micronesia
	692: 7,  # Marshall Islands
	850: 10,  # North Korea
	852: 8,  # Hong Kong
	853: 8,  # Macao
	855: 9,  # Cambodia
	856: 10,  # Laos
	872: 6,  # Pitcairn Islands
	880: 10,  # Bangladesh
	886: 9,  # Taiwan
	960: 7,  # Maldives
	961: 8,  # Lebanon
	962: 9,  # Jordan
	963: 9,  # Syria
	964: 10,  # Iraq
	965: 8,  # Kuwait
	966: 9,  # Saudi Arabia
	967: 9,  # Yemen
	968: 8,  # Oman
	970: 9,  # Palestine
	971: 9,  # UAE
	972: 9,  # Israel
	973: 8,  # Bahrain
	974: 8,  # Qatar
	975: 8,  # Bhutan
	976: 8,  # Mongolia
	977: 10,  # Nepal
	992: 9,  # Tajikistan
	993: 8,  # Turkmenistan
	994: 9,  # Azerbaijan
	995: 9,  # Georgia
	996: 9,  # Kyrgyzstan
	998: 9,  # Uzbekistan
}

# --- Utility Dictionary: A flat version for quick lookups ---
# Generated programmatically to avoid redundancy.
ALL_COUNTRIES = {}
for continent_data in COUNTRIES_BY_CONTINENT.values():
	if isinstance(continent_data, dict) and any(isinstance(v, dict) for v in continent_data.values()):
		# Has subregions
		for subregion_data in continent_data.values():
			if isinstance(subregion_data, dict):
				ALL_COUNTRIES.update(subregion_data)
	else:
		# No subregions (like Antarctica)
		ALL_COUNTRIES.update(continent_data)


def extract_country_code_from_label(country_label: str) -> Optional[Tuple[int, str]]:
	"""
	Extract country code and an associated region code from a country label.

	Args:
		country_label: String like "🇺🇸 United States"

	Returns:
		A tuple of (country_code, region_code) or (None, None) if not found.
	"""
	fmt = ALL_COUNTRIES.get(country_label)
	if not fmt:
		return None, None

	# Find the code after the plus sign
	match = re.match(r"\+(\d+)", fmt)
	if not match:
		return None, None

	country_code = int(match.group(1))

	# Optional: Extract region code using the phonenumbers library
	try:
		from phonenumbers.phonenumberutil import region_code_for_country_code
		region = region_code_for_country_code(country_code)
		return country_code, region
	except (ImportError, KeyError):
		# Fallback if the library is not installed or the code is unassigned
		return country_code, None


def get_digit_limit(country_code: int) -> int:
	"""
	Get the maximum allowed number of LOCAL digits for a country code.
	This does NOT include the country code digits.

	Args:
		country_code: The international country calling code.

	Returns:
		The maximum number of LOCAL digits allowed, defaulting to 15.
	"""
	return LOCAL_DIGIT_LIMITS_BY_CODE.get(country_code, 15)


def format_display_number(digits: str, country_code: int) -> str:
	"""
	Format a string of LOCAL digits for display based on country-specific rules.

	Args:
		digits: A string containing only the LOCAL phone number digits.
		country_code: The international country calling code.

	Returns:
		A formatted phone number string.
	"""
	if not digits:
		return ""

	# Country-specific formatting rules
	if country_code == 1 and len(digits) == 10:  # US/Canada
		return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
	elif country_code == 44:  # UK
		if len(digits) == 10:  # Standard format
			return f"{digits[:4]} {digits[4:]}"
		elif len(digits) == 11:  # Mobile/other formats
			return f"{digits[:5]} {digits[5:]}"
	elif country_code == 33 and len(digits) >= 9:  # France
		# Format as X XX XX XX XX
		if len(digits) == 10:
			return f"{digits[0]} {digits[1:3]} {digits[3:5]} {digits[5:7]} {digits[7:9]}"
		else:
			return ' '.join(re.findall(r'.{1,2}', digits))
	elif country_code == 49 and len(digits) >= 10:  # Germany
		return f"{digits[:4]} {digits[4:]}"
	elif country_code == 81 and len(digits) == 10:  # Japan
		return f"{digits[:2]}-{digits[2:6]}-{digits[6:]}"
	elif country_code == 82 and len(digits) >= 9:  # South Korea
		return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
	elif country_code == 86 and len(digits) == 11:  # China
		return f"{digits[:3]} {digits[3:7]} {digits[7:]}"
	elif country_code == 91 and len(digits) == 10:  # India
		return f"{digits[:5]} {digits[5:]}"
	elif country_code == 61 and len(digits) == 9:  # Australia
		return f"{digits[0]} {digits[1:5]} {digits[5:]}"
	elif country_code == 55 and len(digits) in [10, 11]:  # Brazil
		if len(digits) == 11:
			return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
		return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"

	# Generic formatting fallback for other countries
	if len(digits) <= 6:
		return digits
	elif len(digits) <= 10:
		return f"{digits[:3]} {digits[3:6]} {digits[6:]}"
	else:
		return f"{digits[:3]} {digits[3:6]} {digits[6:10]} {digits[10:]}"


def validate_digit_input(current_digits: str, country_code: int) -> bool:
	"""
	Validate if the current LOCAL digit string is within the country's length limit.

	Args:
		current_digits: The current string of LOCAL digits entered.
		country_code: The international country calling code.

	Returns:
		True if the length is valid, False otherwise.
	"""
	if not current_digits.isdigit():
		return False
	max_digits = get_digit_limit(country_code)
	return len(current_digits) <= max_digits


def get_country_list() -> list:
	"""
	Get a single, sorted list of all available country labels.

	Returns:
		A list of country labels with flag emojis, sorted alphabetically.
	"""
	return sorted(ALL_COUNTRIES.keys())


def get_format_example(country_label: str) -> str:
	"""
	Get the phone number format example for a specific country.

	Args:
		country_label: The country name with its flag emoji.

	Returns:
		A format string (e.g., "+1 (XXX) XXX-XXXX") or an empty string if not found.
	"""
	return ALL_COUNTRIES.get(country_label, "")


def get_countries_by_continent_and_subregion(continent: str = None, subregion: str = None) -> list:
	"""
	Get countries filtered by continent and/or subregion according to UN geoscheme.

	Args:
		continent: The continent name (e.g., 'Asia', 'Europe')
		subregion: The subregion name (e.g., 'Western Europe', 'South-Eastern Asia')

	Returns:
		A sorted list of country labels matching the criteria.
	"""
	if continent and continent not in COUNTRIES_BY_CONTINENT:
		return []

	if continent == 'Antarctica':
		# Antarctica has a single subregion with the same name
		return sorted(COUNTRIES_BY_CONTINENT['Antarctica']['Antarctica'].keys())

	if not continent:
		# Return all countries if "All Continents" is selected
		return sorted(ALL_COUNTRIES.keys())

	continent_data = COUNTRIES_BY_CONTINENT[continent]

	if not subregion:
		# Return all countries in the continent
		countries = []
		for subregion_data in continent_data.values():
			if isinstance(subregion_data, dict):
				countries.extend(subregion_data.keys())
		return sorted(countries)

	# Return countries in specific subregion
	if subregion not in continent_data:
		return []

	return sorted(continent_data[subregion].keys())


def get_continent_structure() -> Dict[str, list]:
	"""
	Get the complete UN geoscheme structure showing continents and their subregions.

	Returns:
		Dictionary mapping continent names to lists of their subregions.
	"""
	structure = {}
	for continent, data in COUNTRIES_BY_CONTINENT.items():
		if continent == 'Antarctica':
			structure[continent] = ['Antarctica']  # Antarctica has one subregion
		else:
			structure[continent] = list(data.keys())
	return structure


# --- Helper functions for easy integration ---

def get_all_country_codes() -> list:
	"""Get a sorted list of all unique country codes."""
	return sorted(LOCAL_DIGIT_LIMITS_BY_CODE.keys())


def get_countries_by_continent() -> Dict[str, Dict[str, str]]:
	"""
	Get the dictionary of all countries, grouped by continent.
	DEPRECATED: Use get_countries_by_continent_and_subregion() for UN geoscheme structure.

	Returns:
		A flattened dictionary for backward compatibility.
	"""
	# Flatten the structure for backward compatibility
	flat_structure = {}
	for continent, data in COUNTRIES_BY_CONTINENT.items():
		if continent == 'Antarctica':
			flat_structure[continent] = data['Antarctica']
		else:
			# Flatten subregions into single continent entry
			continent_countries = {}
			for subregion_data in data.values():
				continent_countries.update(subregion_data)
			flat_structure[continent] = continent_countries
	return flat_structure


def search_countries(query: str) -> list:
	"""
	Search for countries by name.

	Args:
		query: The search term to match against country labels.

	Returns:
		A sorted list of matching country labels.
	"""
	query = query.lower().strip()
	if not query:
		return []

	matches = [
		country_label for country_label in ALL_COUNTRIES
		if query in country_label.lower()
	]
	return sorted(matches)


def get_country_stats() -> Dict[str, Any]:
	"""Get statistics about the phone format database."""
	total_countries = len(ALL_COUNTRIES)
	total_codes = len(set(LOCAL_DIGIT_LIMITS_BY_CODE.keys()))

	digit_distribution = {}
	for limit in LOCAL_DIGIT_LIMITS_BY_CODE.values():
		digit_distribution[limit] = digit_distribution.get(limit, 0) + 1

	continent_stats = {}
	for continent, data in COUNTRIES_BY_CONTINENT.items():
		if continent == 'Antarctica':
			continent_stats[continent] = {'total': len(data['Antarctica']), 'subregions': 1}
		else:
			total_in_continent = sum(len(subregion) for subregion in data.values())
			continent_stats[continent] = {
				'total': total_in_continent,
				'subregions': len(data)
			}

	return {
		'total_countries': total_countries,
		'total_country_codes': total_codes,
		'digit_limit_distribution': sorted(digit_distribution.items()),
		'continent_breakdown': continent_stats,
		'coverage_percentage': round((total_countries / 249) * 100, 1)  # Based on ISO 3166-1 count
	}


# --- Main execution block for demonstrating and testing the module ---
if __name__ == "__main__":
	print("📞 Phone Formats Module Demo (UN Geoscheme)")
	print("=" * 50)

	# 1. Test a specific country
	test_country = "🇺🇸 United States"
	print(f"Country: {test_country}")

	code, region = extract_country_code_from_label(test_country)
	if code:
		print(f"Code: +{code}, Region: {region}")
		print(f"LOCAL Digit Limit: {get_digit_limit(code)}")

		# 2. Test formatting
		test_digits = "5551234567"
		formatted = format_display_number(test_digits, code)
		print(f"Formatted: +{code} {formatted}")
	else:
		print("Could not retrieve country details.")

	print("-" * 50)

	# 3. Show database statistics
	stats = get_country_stats()
	print("📊 Database Stats (UN Geoscheme):")
	print(f"  - Total Countries/Territories: {stats['total_countries']}")
	print(f"  - Unique Country Codes: {stats['total_country_codes']}")
	print(f"  - World Coverage: {stats['coverage_percentage']}%")

	# 4. Show continent breakdown
	print("\n🌍 Continent Breakdown:")
	for continent, info in stats['continent_breakdown'].items():
		subregion_text = f" ({info['subregions']} subregions)" if info['subregions'] > 0 else ""
		print(f"  - {continent}: {info['total']} countries{subregion_text}")

	# 5. Test subregion filtering
	print("-" * 50)
	print("🔍 Testing UN Subregion Filtering:")

	# Test Western Europe
	western_europe = get_countries_by_continent_and_subregion('Europe', 'Western Europe')
	print(f"Western Europe ({len(western_europe)} countries):")
	for country in western_europe[:3]:  # Show first 3
		print(f"  - {country}")

	# Test South-Eastern Asia (includes Christmas Island per UN)
	se_asia = get_countries_by_continent_and_subregion('Asia', 'South-Eastern Asia')
	print(f"\nSouth-Eastern Asia ({len(se_asia)} countries):")
	christmas_island = [c for c in se_asia if 'Christmas' in c]
	if christmas_island:
		print(f"  - {christmas_island[0]} (UN classification)")

	# 6. Test Antarctica
	antarctica = get_countries_by_continent_and_subregion('Antarctica')
	print(f"\nAntarctica ({len(antarctica)} entries):")
	for entry in antarctica:
		print(f"  - {entry}")

	# 7. Show continent structure
	print("-" * 50)
	structure = get_continent_structure()
	print("🗺️  UN Geoscheme Structure:")
	for continent, subregions in structure.items():
		if subregions and subregions != ['Antarctica']:
			print(f"{continent}: {', '.join(subregions)}")
		else:
			print(f"{continent}: (single subregion)")

	# 8. Test digit validation logic
	print("-" * 50)
	print("🧪 Testing Digit Validation Logic:")

	# Test US number validation (should be 10 LOCAL digits)
	us_code = 1
	print(f"US (+{us_code}) - Max LOCAL digits: {get_digit_limit(us_code)}")

	# Test various input lengths
	test_inputs = ["555", "5551234", "5551234567", "55512345678"]
	for test_input in test_inputs:
		is_valid = validate_digit_input(test_input, us_code)
		formatted = format_display_number(test_input, us_code) if is_valid else "INVALID"
		print(f"  Input '{test_input}' ({len(test_input)} digits): {is_valid} → {formatted}")

# --- Export public components of the module ---
__all__ = [
	'COUNTRIES_BY_CONTINENT',
	'ALL_COUNTRIES',
	'LOCAL_DIGIT_LIMITS_BY_CODE',
	'extract_country_code_from_label',
	'get_digit_limit',
	'format_display_number',
	'validate_digit_input',
	'get_country_list',
	'get_format_example',
	'get_all_country_codes',
	'get_countries_by_continent',  # Deprecated but maintained for compatibility
	'get_countries_by_continent_and_subregion',  # New UN geoscheme function
	'get_continent_structure',
	'search_countries',
	'get_country_stats'
]
