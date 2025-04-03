# Core Processing Configuration
DEFAULT_CONFIG = {
    # Structural Extraction Parameters
    "structural": {
        "row_anchors": 5,  # Number of row anchors to extract
        "col_anchors": 5,  # Number of column anchors to extract
        "k": 3,  # Context window size for structural extraction
        "detect_headers": True,  # Automatically detect and mark headers
        "max_merged_distance": 5,  # Maximum distance to consider for merged cell detection
    },
    # Data Format Parameters
    "data_format": {
        "numerical_categories": [
            "General",
            "Number",
            "Currency",
            "Accounting",
            "Percentage",
            "Scientific",
        ],
        "date_formats": ["Short Date", "Long Date", "Time"],
        "aggregate_regions": True,  # Whether to aggregate similar data regions
        "preserve_formulas": True,  # Whether to preserve formula structure
    },
    # Spreadsheet Processing
    "processing": {
        "parallel": True,  # Use parallel processing for multi-sheet workbooks
        "max_workers": 4,  # Maximum number of parallel workers
        "chunk_size": 1000,  # Chunk size for large spreadsheets
        "memory_limit": "4GB",  # Memory limit for processing
    },
    # Output Configuration
    "output": {
        "format": "json",  # Output format (json, yaml, msgpack)
        "compression": None,  # Compression method (None, 'gzip', 'zlib')
        "include_metadata": True,  # Include metadata in output
        "include_statistics": True,  # Include statistics in output
    },
    # Advanced Features
    "features": {
        "pivot_tables": True,  # Extract and encode pivot tables
        "charts": True,  # Extract and encode charts
        "data_validation": True,  # Extract data validation rules
        "conditional_formatting": True,  # Extract conditional formatting
        "external_connections": False,  # Process external data connections
        "macros": False,  # Process VBA macros (requires additional permissions)
    },
    # Error Handling
    "error_handling": {
        "on_formula_error": "skip",  # Options: "skip", "warn", "raise", "fallback"
        "on_reference_error": "warn",  # Options: "skip", "warn", "raise"
        "log_level": "INFO",  # Options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    },
}


def get_config():
    """Returns a copy of the default configuration."""
    import copy

    return copy.deepcopy(DEFAULT_CONFIG)


def merge_config(user_config):
    """Merges user configuration with default configuration."""
    import copy

    config = copy.deepcopy(DEFAULT_CONFIG)

    def recursive_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                recursive_update(d[k], v)
            else:
                d[k] = v

    recursive_update(config, user_config)
    return config
