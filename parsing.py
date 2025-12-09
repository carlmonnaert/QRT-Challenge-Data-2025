from collections import defaultdict
import re

def parse_PROTEIN_CHANGE(protein):
    """Extracts the numeric position (hotspot) from protein change string."""
    protein = str(protein)
    if len(protein) == 0 or protein == 'nan':
        return 0
    # Regex to find the number in p.R882H -> 882
    match = re.search(r"(\d+)", protein)
    if match:
        return int(match.group(1))
    return 0

def parse_GENE(gene):
    """Returns the full gene name in uppercase."""
    gene = str(gene)
    if len(gene) == 0 or gene == 'nan':
        return "UNKNOWN"
    return gene.upper()

def parse_CYTO(iscn):
    """Parses ISCN strings for complex karyotypes and translocations."""
    iscn = str(iscn).upper().replace(" ", "")
    results = defaultdict(int)
    
    # 1. Detect Complex Karyotype
    clones = iscn.split("/")
    max_abnormalities = 0
    for clone in clones:
        abnormalities = re.findall(r"([+-]\d+|DEL|ADD|INV|T\(|DER)", clone)
        if len(abnormalities) > max_abnormalities:
            max_abnormalities = len(abnormalities)
    if max_abnormalities >= 3:
        results["Complex_Karyotype"] = 1

    # 2. Specific Translocations/Inversions
    structural = re.findall(r"(T|INV)\((\d+|X|Y)[;]?(\d+|X|Y)?\)", iscn)
    for type_, chrom1, chrom2 in structural:
        chrom2_str = f";{chrom2}" if chrom2 else ""
        key = f"{type_}({chrom1}{chrom2_str})"
        results[key] = 1

    # 3. Numeric changes
    numeric_changes = re.findall(r"(?<![0-9])([+-])(\d+|X|Y)(?=[,/]|$)", iscn)
    for sign, num in numeric_changes:
        key = f"{sign}{num}"
        results[key] = 1

    if not results:
        results["normal"] = 1
    return dict(results)