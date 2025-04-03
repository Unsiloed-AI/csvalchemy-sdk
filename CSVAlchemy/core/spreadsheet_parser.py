import re
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple, Optional, Set

logger = logging.getLogger(__name__)


def col_to_num(col: str) -> int:
    """
    Convert Excel column letter to column number

    Transforms alphabetic column references (A, B, ..., Z, AA, AB, etc.)
    into their corresponding 1-indexed numeric values.

    Args:
        col: Column letter (e.g., 'A', 'BC')

    Returns:
        Column number (1-indexed)

    Examples:
        >>> col_to_num('A')
        1
        >>> col_to_num('Z')
        26
        >>> col_to_num('AA')
        27
    """
    num = 0
    for c in col:
        num = num * 26 + (ord(c.upper()) - ord("A") + 1)
    return num


def num_to_col(num: int) -> str:
    """
    Convert column number to Excel column letter

    Transforms numeric column indices (1, 2, etc.) into their corresponding
    alphabetic Excel column references (A, B, ..., Z, AA, AB, etc.).

    Args:
        num: Column number (1-indexed)

    Returns:
        Column letter (e.g., 'A', 'BC')

    Examples:
        >>> num_to_col(1)
        'A'
        >>> num_to_col(26)
        'Z'
        >>> num_to_col(27)
        'AA'
    """
    letters = ""
    while num > 0:
        num, remainder = divmod(num - 1, 26)
        letters = chr(ord("A") + remainder) + letters
    return letters


def parse_address(addr: str) -> Tuple[int, int]:
    """
    Parse Excel address into row and column numbers

    Converts a standard Excel cell reference (e.g., 'A1', 'BC23') into
    a tuple of (row, column) numbers. Both are returned as 1-indexed values
    to match Excel's indexing system.

    Args:
        addr: Excel cell address (e.g., 'A1', 'BC23')

    Returns:
        Tuple of (row, column) as 1-indexed integers

    Raises:
        ValueError: If the address format is invalid

    Examples:
        >>> parse_address('A1')
        (1, 1)
        >>> parse_address('B5')
        (5, 2)
    """
    match = re.match(r"([A-Za-z]+)([0-9]+)", addr)
    if not match:
        raise ValueError(f"Invalid Excel address: {addr}")
    col, row = match.groups()
    return int(row), col_to_num(col)


def get_max_row_col(cells: Dict) -> Tuple[int, int]:
    """
    Get maximum row and column from a dictionary of cell addresses

    Args:
        cells: Dictionary with keys as Excel addresses

    Returns:
        Tuple of (max_row, max_col)
    """
    max_row, max_col = 0, 0
    for addr in cells:
        row, col = parse_address(addr)
        max_row = max(max_row, row)
        max_col = max(max_col, col)
    return max_row, max_col


def expand_range(range_str: str) -> List[str]:
    """
    Expand a range like 'A1:B3' to individual cell addresses

    Args:
        range_str: Excel range (e.g., 'A1:B3')

    Returns:
        List of individual cell addresses
    """
    if ":" not in range_str:
        return [range_str]

    start, end = range_str.split(":")
    start_row, start_col = parse_address(start)
    end_row, end_col = parse_address(end)

    addresses = []
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            addresses.append(f"{num_to_col(col)}{row}")

    return addresses


def update_formula(
    formula: str,
    row_mapping: Dict[int, int],
    col_mapping: Dict[int, int],
    sheet_name: Optional[str] = None,
) -> str:
    """
    Update cell references in a formula after cell remapping

    Args:
        formula: Excel formula
        row_mapping: Dictionary mapping original row numbers to new row numbers
        col_mapping: Dictionary mapping original column numbers to new column numbers
        sheet_name: Current sheet name

    Returns:
        Updated formula with mapped cell references
    """

    def replace_ref(match):
        ref = match.group(0)
        # Handle sheet references
        if "!" in ref:
            sheet_ref, cell_ref = ref.split("!")
            # If it's a reference to the current sheet, process it
            if sheet_name and sheet_ref == sheet_name:
                return f"{sheet_ref}!{replace_cell_ref(cell_ref)}"
            # External sheet reference, leave it unchanged
            return ref
        else:
            return replace_cell_ref(ref)

    def replace_cell_ref(ref):
        # Handle range references (e.g., A1:B2)
        if ":" in ref:
            start, end = ref.split(":")
            mapped_start = map_single_ref(start)
            mapped_end = map_single_ref(end)
            return (
                f"{mapped_start}:{mapped_end}" if mapped_start and mapped_end else ref
            )
        else:
            return map_single_ref(ref) or ref

    def map_single_ref(ref):
        try:
            row, col = parse_address(ref)
            if row in row_mapping and col in col_mapping:
                new_row = row_mapping[row]
                new_col = col_mapping[col]
                return f"{num_to_col(new_col)}{new_row}"
            return None
        except ValueError:
            # If parsing fails, it might be a named range or other reference
            return None

    # Use regex to match cell references in the formula
    cell_ref_pattern = (
        r"(?<![A-Za-z0-9_])([A-Za-z]+[0-9]+(?::[A-Za-z]+[0-9]+)?|\w+!\w+(?::\w+)?)"
    )
    updated_formula = re.sub(cell_ref_pattern, replace_ref, formula)

    return updated_formula


def detect_headers(sheet: Dict) -> Tuple[Set[int], Set[int]]:
    """
    Detect likely header rows and columns in a spreadsheet

    Args:
        sheet: Dictionary of cell addresses to cell values

    Returns:
        Tuple of (header_rows, header_cols) containing sets of row and column indices
    """
    # Implementation logic for header detection
    header_rows = set()
    header_cols = set()

    # Simple heuristic: headers tend to be text cells with numeric data below/to the right
    # More sophisticated detection would be implemented here

    return header_rows, header_cols


def structural_anchor_extraction(
    cells: Dict, sheet_name: str, row_anchors: int, col_anchors: int, k: int
) -> Tuple[Dict, Dict, Dict]:
    """
    Extract structural anchors from a spreadsheet to create a compact representation

    Args:
        cells: Dictionary of cell addresses to cell values
        sheet_name: Name of the current sheet
        row_anchors: Number of row anchors to extract
        col_anchors: Number of column anchors to extract
        k: Context window size

    Returns:
        Tuple of (extracted_cells, row_mapping, col_mapping)
    """
    logger.info(
        f"Extracting structural anchors for sheet {sheet_name} with {row_anchors} row anchors and {col_anchors} column anchors"
    )

    # Get max dimensions
    max_row, max_col = get_max_row_col(cells)

    # Score rows and columns for informativeness
    row_scores = {i: 0 for i in range(1, max_row + 1)}
    col_scores = {i: 0 for i in range(1, max_col + 1)}

    # Calculate scores based on cell content
    for addr, cell in cells.items():
        row, col = parse_address(addr)

        # Add to scores based on cell characteristics (non-empty, formula, etc.)
        cell_type = cell.get("type", "")
        if cell_type == "formula":
            row_scores[row] += 3
            col_scores[col] += 3
        elif cell_type in ["text", "string"]:
            row_scores[row] += 2
            col_scores[col] += 2
        else:
            row_scores[row] += 1
            col_scores[col] += 1

    # Select top-scoring rows and columns as anchors
    top_rows = sorted(row_scores.keys(), key=lambda r: row_scores[r], reverse=True)[
        :row_anchors
    ]
    top_cols = sorted(col_scores.keys(), key=lambda c: col_scores[c], reverse=True)[
        :col_anchors
    ]

    # Create mappings for rows and columns
    row_mapping = {r: i + 1 for i, r in enumerate(sorted(top_rows))}
    col_mapping = {c: i + 1 for i, c in enumerate(sorted(top_cols))}

    # Extract cells based on anchors and context window
    extracted_cells = {}

    for addr, cell in cells.items():
        row, col = parse_address(addr)

        # Include cell if it's within k distance of an anchor
        in_row_context = any(abs(row - anchor_row) <= k for anchor_row in top_rows)
        in_col_context = any(abs(col - anchor_col) <= k for anchor_col in top_cols)

        if in_row_context and in_col_context:
            extracted_cells[addr] = cell

    logger.info(
        f"Extracted {len(extracted_cells)} cells from {len(cells)} original cells"
    )

    return extracted_cells, row_mapping, col_mapping


def data_format_aggregation(sheet: Dict, numerical_categories: List[str]) -> Dict:
    """
    Aggregate cells with similar formats into regions for more compact representation

    Args:
        sheet: Dictionary of cell addresses to cell values
        numerical_categories: List of numerical format categories to match

    Returns:
        Dictionary with regions and their representative formats
    """
    # Implementation of region-based aggregation
    aggregated_data = {"regions": [], "metadata": {}}

    def is_adjacent(addr1: str, addr2: str) -> bool:
        """Check if two cells are adjacent"""
        row1, col1 = parse_address(addr1)
        row2, col2 = parse_address(addr2)
        return (abs(row1 - row2) <= 1 and col1 == col2) or (
            abs(col1 - col2) <= 1 and row1 == row2
        )

    # Group cells by format
    format_groups = {}
    for addr, cell in sheet.items():
        cell_format = cell.get("format", "General")
        if cell_format not in format_groups:
            format_groups[cell_format] = []
        format_groups[cell_format].append(addr)

    # Find regions for numerical formats
    for fmt, addresses in format_groups.items():
        if fmt in numerical_categories and len(addresses) > 1:
            # Use clustering/grouping to identify regions
            # For now, use a simplified approach
            regions = []
            visited = set()

            for addr in addresses:
                if addr in visited:
                    continue

                region = {addr}
                to_check = [addr]

                while to_check:
                    current = to_check.pop()
                    for other in addresses:
                        if (
                            other not in visited
                            and other not in region
                            and is_adjacent(current, other)
                        ):
                            region.add(other)
                            to_check.append(other)
                            visited.add(other)

                if len(region) > 1:
                    regions.append(sorted(list(region)))

            for i, region in enumerate(regions):
                min_row, min_col = float("inf"), float("inf")
                max_row, max_col = 0, 0

                for addr in region:
                    row, col = parse_address(addr)
                    min_row = min(min_row, row)
                    min_col = min(min_col, col)
                    max_row = max(max_row, row)
                    max_col = max(max_col, col)

                top_left = f"{num_to_col(min_col)}{min_row}"
                bottom_right = f"{num_to_col(max_col)}{max_row}"

                aggregated_data["regions"].append(
                    {
                        "id": f"{fmt}_{i}",
                        "format": fmt,
                        "range": f"{top_left}:{bottom_right}",
                        "size": len(region),
                    }
                )

    return aggregated_data


def inverted_index_translation(sheet: Dict) -> Dict:
    """
    Create an inverted index representation of the spreadsheet

    Args:
        sheet: Dictionary of cell addresses to cell values

    Returns:
        Inverted index mapping values to addresses
    """
    inverted_index = {}

    for addr, cell in sheet.items():
        value = cell.get("value", "")

        if value not in inverted_index:
            inverted_index[value] = []

        inverted_index[value].append(addr)

    return inverted_index


def detect_merged_cells(cells: Dict, max_distance: int = 5) -> List[Dict]:
    """
    Detect likely merged cells based on empty cell patterns

    Args:
        cells: Dictionary of cell addresses to cell values
        max_distance: Maximum distance to consider for merged cells

    Returns:
        List of detected merged cell ranges
    """
    # Implementation of merged cell detection
    merged_cells = []
    # Algorithm would analyze patterns of empty cells
    # For a production version, this would be much more sophisticated

    return merged_cells


def extract_references(formula: str, current_sheet: Optional[str] = None) -> Set[str]:
    """
    Extract cell references from a formula

    Args:
        formula: Excel formula
        current_sheet: Current sheet name

    Returns:
        Set of cell references in the formula
    """
    references = set()

    # Match A1-style references including sheet references
    pattern = (
        r"(?<![A-Za-z0-9_])((?:[A-Za-z0-9_]+!)?[A-Za-z]+[0-9]+(?::[A-Za-z]+[0-9]+)?)"
    )

    for match in re.finditer(pattern, formula):
        ref = match.group(1)
        references.add(ref)

    return references


def encode_sheet(
    workbook: Dict, sheet_name: str, k: int, numerical_categories: List[str]
) -> Dict:
    """
    Args:
        workbook: Dictionary representation of the Excel workbook
        sheet_name: Name of the sheet to encode
        k: Context window size for structural extraction
        numerical_categories: List of numerical format categories to match

    Returns:
        Encoded representation of the sheet
    """
    sheet = workbook.get(sheet_name, {})

    logger.info(f"Encoding sheet '{sheet_name}' with {len(sheet)} cells")

    # 1. Structural Anchor Extraction
    extracted_cells, row_mapping, col_mapping = structural_anchor_extraction(
        sheet, sheet_name, row_anchors=5, col_anchors=5, k=k
    )

    # 2. Data Format Aggregation
    aggregated_data = data_format_aggregation(extracted_cells, numerical_categories)

    # 3. Inverted Index Translation
    inverted_index = inverted_index_translation(extracted_cells)

    # 4. Detect Merged Cells
    merged_cells = detect_merged_cells(sheet)

    # 5. Process Formulas and Build Dependency Graph
    formula_cells = {}
    dependency_graph = {}

    for addr, cell in extracted_cells.items():
        if cell.get("type") == "formula":
            formula = cell.get("formula", "")
            formula_cells[addr] = {
                "formula": formula,
                "updated_formula": update_formula(
                    formula, row_mapping, col_mapping, sheet_name
                ),
            }

            # Extract dependencies
            refs = extract_references(formula, sheet_name)
            if refs:
                dependency_graph[addr] = list(refs)

    # 6. Combine into final encoded representation
    encoded = {
        "sheet_name": sheet_name,
        "extracted_cells": extracted_cells,
        "row_mapping": row_mapping,
        "col_mapping": col_mapping,
        "aggregated_data": aggregated_data,
        "inverted_index": inverted_index,
        "merged_cells": merged_cells,
        "formula_cells": formula_cells,
        "dependency_graph": dependency_graph,
        "metadata": {
            "original_cell_count": len(sheet),
            "extracted_cell_count": len(extracted_cells),
            "compression_ratio": len(extracted_cells) / max(1, len(sheet)),
        },
    }

    return encoded


def encode_workbook(workbook: Dict, params: Dict) -> Dict:
    """

    Args:
        workbook: Dictionary representation of the Excel workbook
        params: Parameters for encoding

    Returns:
        Encoded representation of the workbook
    """
    k = params.get("k", 3)
    numerical_categories = params.get(
        "numerical_categories",
        ["General", "Number", "Currency", "Accounting", "Percentage"],
    )
    parallel = params.get("parallel", True)
    max_workers = params.get("max_workers", 4)

    sheet_names = list(workbook.keys())
    encoded_workbook = {
        "sheets": {},
        "metadata": {
            "sheet_count": len(sheet_names),
            "total_cells": sum(len(workbook[sheet]) for sheet in sheet_names),
        },
    }

    logger.info(f"Encoding workbook with {len(sheet_names)} sheets")

    # Process sheets in parallel if enabled
    if parallel and len(sheet_names) > 1:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for sheet_name in sheet_names:
                future = executor.submit(
                    encode_sheet, workbook, sheet_name, k, numerical_categories
                )
                futures[future] = sheet_name

            for future in futures:
                sheet_name = futures[future]
                try:
                    encoded_workbook["sheets"][sheet_name] = future.result()
                except Exception as e:
                    logger.error(f"Error encoding sheet {sheet_name}: {str(e)}")
                    encoded_workbook["sheets"][sheet_name] = {
                        "error": str(e),
                        "sheet_name": sheet_name,
                    }
    else:
        # Process sheets sequentially
        for sheet_name in sheet_names:
            try:
                encoded_workbook["sheets"][sheet_name] = encode_sheet(
                    workbook, sheet_name, k, numerical_categories
                )
            except Exception as e:
                logger.error(f"Error encoding sheet {sheet_name}: {str(e)}")
                encoded_workbook["sheets"][sheet_name] = {
                    "error": str(e),
                    "sheet_name": sheet_name,
                }

    # Add cross-sheet dependencies
    encoded_workbook["cross_sheet_dependencies"] = {}

    for sheet_name, encoded_sheet in encoded_workbook["sheets"].items():
        if "dependency_graph" in encoded_sheet:
            for addr, refs in encoded_sheet["dependency_graph"].items():
                for ref in refs:
                    if "!" in ref:
                        ref_sheet, _ = ref.split("!")
                        if ref_sheet != sheet_name:
                            if (
                                sheet_name
                                not in encoded_workbook["cross_sheet_dependencies"]
                            ):
                                encoded_workbook["cross_sheet_dependencies"][
                                    sheet_name
                                ] = {}

                            if (
                                ref_sheet
                                not in encoded_workbook["cross_sheet_dependencies"][
                                    sheet_name
                                ]
                            ):
                                encoded_workbook["cross_sheet_dependencies"][
                                    sheet_name
                                ][ref_sheet] = []

                            encoded_workbook["cross_sheet_dependencies"][sheet_name][
                                ref_sheet
                            ].append({"from": f"{sheet_name}!{addr}", "to": ref})

    return encoded_workbook
