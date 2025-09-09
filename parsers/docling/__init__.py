"""
Docling document processing module.

This module provides functionality to process documents using the Docling library.
It serves as the main entry point for document conversion operations, handling
the conversion of various document formats into a standardized document structure.

The module integrates with the Docling converter to process documents and return
structured document objects that can be used for further analysis or processing.
"""

import logging
from pathlib import Path

from .converter import doc_converter

_log = logging.getLogger(__name__)

def process_document_with_docling(source_path: Path):
    """
    Process a document using the Docling library.
    
    This function takes a document file path and converts it using the Docling
    converter. It handles the conversion process and returns the structured
    document object that can be used for further processing or analysis.
    
    Args:
        source_path (Path): The path to the source document file to be processed.
                           Should be a valid file path pointing to a supported
                           document format (e.g., PDF, DOCX, etc.).
    
    Returns:
        Document: A structured document object containing the parsed content
                 and metadata from the source file.
    
    Raises:
        FileNotFoundError: If the source_path does not exist.
        ValueError: If the document format is not supported or conversion fails.
        Exception: For other conversion-related errors that may occur during processing.
    
    Example:
        >>> from pathlib import Path
        >>> doc_path = Path("example.pdf")
        >>> document = process_document_with_docling(doc_path)
        >>> print(document.title)
    """
    _log.info("Converting document with Docling: %s", source_path)
    doc_res = doc_converter.convert(str(source_path))
    return doc_res.document
