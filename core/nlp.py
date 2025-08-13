from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ParsedQuery:
	loan_type: str | None
	location: str | None
	property_type: str | None
	is_first_time_buyer: bool
	is_veteran: bool


def parse_free_text_query(text: str) -> ParsedQuery:
	"""Very lightweight parser using regex/keywords to keep the PoC simple.

	Examples handled:
	- "Underwrite home loan for a first-time buyer in New Mexico with rural property"
	- "Home loan New Mexico urban veteran"
	"""
	lower = text.lower()

	loan_type = None
	if "home loan" in lower or "mortgage" in lower:
		loan_type = "home_loan"

	location = None
	if "new mexico" in lower or re.search(r"\bnm\b", lower):
		location = "New Mexico"
	elif "texas" in lower or re.search(r"\btx\b", lower):
		location = "Texas"

	property_type = None
	if "rural" in lower:
		property_type = "rural"
	elif "urban" in lower:
		property_type = "urban"

	is_first_time_buyer = "first-time" in lower or "first time" in lower
	is_veteran = "veteran" in lower or "va" in lower

	return ParsedQuery(
		loan_type=loan_type,
		location=location,
		property_type=property_type,
		is_first_time_buyer=is_first_time_buyer,
		is_veteran=is_veteran,
	)


