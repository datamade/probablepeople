#!/usr/bin/env python3
"""
Enhanced Medical Professional Name Parser

This module provides enhanced parsing capabilities for medical professional names
with proper handling of multiple comma-separated credentials.

Key Enhancement:
- Parses "Dr. John Smith MD, PhD, FACP"
- Returns: SuffixOther as ['MD', 'PhD', 'FACP'] instead of 'MD, PhD, FACP'

Usage:
    from enhanced_parser import parse_medical_name

    result = parse_medical_name("Taylor Anne Jordan ATC, LAT")
    print(result)
    # Output: ({'GivenName': 'Taylor', 'MiddleName': 'Anne', 'Surname': 'Jordan',
    #          'SuffixOther': ['ATC', 'LAT']}, 'Person')
"""

from typing import Dict, List, Tuple, Union

import probablepeople as pp


def parse_medical_name(
    name: str, model_type: str = "person"
) -> Tuple[Dict[str, Union[str, List[str]]], str]:
    """
    Parse a medical professional name with enhanced multi-credential support.

    Args:
        name: The full name string to parse
        model_type: The model to use ('person', 'generic', etc.)

    Returns:
        Tuple of (parsed_components_dict, name_type)

    Example:
        >>> parse_medical_name("Dr. Sarah Johnson MD, PhD")
        ({'PrefixOther': 'Dr.', 'GivenName': 'Sarah', 'Surname': 'Johnson',
          'SuffixOther': ['MD', 'PhD']}, 'Person')
    """
    tagged = {}
    prev_label = None
    and_label = False
    proxy_label = False
    aka_label = False

    interrupting_tags = (
        "CorporationNameOrganization",
        "CorporationNameBranchType",
        "CorporationNameBranchIdentifier",
        "ProxiedCorporationNameOrganization",
        "OtherCorporationNameOrganization",
        "OtherCorporationNameBranchType",
        "OtherCorporationNameBranchIdentifier",
    )

    # Parse the name into tokens and labels
    for token, label in pp.parse(name, model_type):
        if label == "And":
            and_label = True
        elif label == "AKA":
            aka_label = True
        elif label == "ProxyFor":
            proxy_label = True
        elif and_label and label in tagged:
            label = "Second" + label
        elif aka_label and label in tagged:
            label = "Other" + label
        elif proxy_label and label in tagged:
            label = "Proxied" + label

        # Special handling for SuffixOther to allow multiple credentials
        if label == "SuffixOther":
            if label not in tagged:
                tagged[label] = []
            # Clean the token (remove commas and extra spaces)
            clean_token = token.rstrip(",").strip()
            if clean_token:
                tagged[label].append(clean_token)
        else:
            # Normal handling for other labels
            if label not in tagged:
                tagged[label] = [token]
            elif label == prev_label or prev_label in interrupting_tags:
                tagged[label].append(token)
            elif label in interrupting_tags:
                tagged[label].append(token)
            else:
                # Handle unexpected repeats by appending
                if isinstance(tagged[label], list):
                    tagged[label].append(token)
                else:
                    tagged[label] = [tagged[label], token]

        prev_label = label

    # Post-process results
    final_result = {}
    for label, tokens in tagged.items():
        if label == "SuffixOther":
            # Keep credentials as a list for multi-credential support
            if len(tokens) == 1:
                # For single credentials, some applications might expect a string
                # But we'll keep as list for consistency
                final_result[label] = tokens
            else:
                final_result[label] = tokens
        else:
            # Join tokens for single-value labels
            if isinstance(tokens, list):
                final_result[label] = " ".join(tokens)
            else:
                final_result[label] = tokens

    # Determine name type (simplified logic)
    name_type = "Person"

    return final_result, name_type


def demonstrate_enhanced_parsing():
    """Demonstrate the enhanced parsing capabilities."""

    test_cases = [
        "Taylor Anne Jordan ATC, LAT",
        "Dr. Sarah Johnson MD, PhD, FACP",
        "Michael Smith RN, BSN, CEN",
        "Jennifer Farroll ATC, LAT, EdD",
        "Eric M Bugaieski MD",
        "Tina A. Hudson CADC-INTERN",
        "Anna Lee NP, MSN, FNP-BC",
        "Prof. David Wilson PhD, MD",
        "Rebecca Thompson LCSW, PhD, ACSW",
        "Amanda C Chambers, PNP, CNP, NP",
        "Paige Davis Licensed Clinical Social Worker",
        "Timothy Eugene Vandyke, PHYSICAL THERAPIST A",
        "Young, Shan J. MD",
        "Md hamid ansari, Phd",
        "Terry Walker, OD, MS, FACE",
        "Dr. John Smith MD, FACP",
        "Sarah Johnson, RN, BSN, MSN",
        "Mohammed Ali Hassan, DDS, MS",
        "Prof. Robert Brown, PhD, FACS",
        "Lisa Chen, PharmD, BCPS",
        "David Wilson Jr., DO, FACEP",
        "Dr. Maria Garcia-Rodriguez, MD, PhD, FAAP",
        "James Thompson, PA-C, MS",
        "John Michael Doe, MBA",
        "Doe John Michael, MBA",
        "Doe, Jane Elizabeth, PhD, MBA",
        "Martin Luther King Jr., MD",
    ]

    print("🏥 Enhanced Medical Professional Name Parser")
    print("=" * 60)
    print("Demonstrating multi-credential parsing capabilities\n")

    for name in test_cases:
        print(f"📝 Input: {name}")

        try:
            # Enhanced parsing
            result, name_type = parse_medical_name(name)

            print(f"   Type: {name_type}")
            print(f"   Components: {result}")

            # Show credentials specifically
            credentials = result.get("SuffixOther", [])
            if credentials:
                count = len(credentials)
                print(f"   📋 Credentials ({count}): {credentials}")
            else:
                print("   📋 No credentials detected")

        except Exception as e:
            print(f"   ❌ Error: {e}")

        print()


if __name__ == "__main__":
    demonstrate_enhanced_parsing()
