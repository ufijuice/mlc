"""
Modal Logic Converter: Converts unstructured text and statements
into structured, modal-qualified beliefs using rule-based heuristics.
"""

import re
from typing import List, Dict, Tuple, Optional
from mlc.types import Modality, RelationCategory
from mlc.modal_map import MODAL_LEXICON, RELATION_LEXICON


class ModalConverter:
    """
    Parses natural language observations, extracts modal attitudes,
    and maps them to formal discrete relational structures.
    """

    def __init__(self):
        self.modal_lexicon = MODAL_LEXICON
        self.relation_lexicon = RELATION_LEXICON

    def detect_modality(self, text: str) -> Tuple[Modality, float]:
        """
        Analyze text for modal auxiliary verbs, adverbs, and axiomatic keywords.
        Returns the detected Modality and default observer confidence.
        """
        text_lower = text.lower()

        # Check for multi-word modals first, then single words
        sorted_keys = sorted(self.modal_lexicon.keys(), key=lambda k: -len(k))
        for keyword in sorted_keys:
            # Match keyword as whole word or bounded phrase
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                mod = self.modal_lexicon[keyword]
                # Modulate initial confidence based on modality
                if mod == Modality.AXIOMATIC:
                    return mod, 1.00
                elif mod == Modality.NECESSITY:
                    return mod, 0.98
                elif mod == Modality.PROBABILITY:
                    return mod, 0.85
                elif mod == Modality.POSSIBILITY:
                    return mod, 0.60
                elif mod == Modality.HYPOTHETICAL:
                    return mod, 0.50
                elif mod == Modality.PROHIBITION:
                    return mod, 0.95
                return mod, 0.95

        return Modality.FACTUAL, 0.95

    def parse_statement(self, sentence: str) -> Optional[Dict]:
        """
        Heuristic converter from simple declarative sentences to (S, P, O, Modality, Confidence).
        Matches patterns like:
          - "A must be inside B"
          - "Socrates is a human"
          - "Alice works for Google"
        """
        clean = sentence.strip().rstrip(".").strip()
        modality, confidence = self.detect_modality(clean)

        # Remove common modal words from predicate extraction
        cleaned_for_pred = clean
        for modal_word in sorted(self.modal_lexicon.keys(), key=lambda k: -len(k)):
            cleaned_for_pred = re.sub(r'\b' + re.escape(modal_word) + r'\b', '', cleaned_for_pred, flags=re.IGNORECASE)

        # Look for relational markers from relation lexicon
        sorted_rel_keys = sorted(self.relation_lexicon.keys(), key=lambda k: -len(k))
        for rel in sorted_rel_keys:
            pattern = r'^(.*?)\s+' + re.escape(rel) + r'\s+(.*)$'
            match = re.match(pattern, clean, re.IGNORECASE)
            if match:
                subj = match.group(1).strip()
                obj = match.group(2).strip()
                # Clean any lingering modal words in subject/object
                pred = rel.replace(" ", "_")
                return {
                    "subject": subj,
                    "predicate": pred,
                    "object": obj,
                    "modality": modality,
                    "confidence": confidence,
                    "context": sentence,
                }

        # Fallback regex for standard verbs "Subject verb Object"
        parts = clean.split()
        if len(parts) >= 3:
            subj = parts[0]
            obj = " ".join(parts[2:])
            pred = parts[1]
            return {
                "subject": subj,
                "predicate": pred,
                "object": obj,
                "modality": modality,
                "confidence": confidence,
                "context": sentence,
            }

        return None
