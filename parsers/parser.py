from pathlib import Path

from parsers.docling.docling_processor import process_document_with_docling
from parsers.llmwhisperer.client import process_document_with_llmwhisperer

class Parser:
    """A class to parse documents using different underlying parsing engines.

    Currently supports 'docling' and 'llmwhisperer'. The parser type is specified
    during initialization, and the parse method handles dispatching to the
    appropriate parsing logic.
    """
    def __init__(self, parser_type: str = "docling"):
        """
        Initializes the Parser with a specified type.

        Args:
            parser_type (str, optional): The type of parser to use. Defaults to "docling".
        """
        self.parser_type = parser_type
        self.docling_document = None

    def parse(self, source_path: Path) -> str | None:
        """
        Parses a document from the given source path.

        If the parser type is 'docling', it returns the markdown content of the document
        and stores the Docling document object in `self.docling_document`.
        If the parser type is 'llmwhisperer', it returns the extracted text.

        Args:
            source_path (Path): The path to the document to parse.

        Returns:
            str | None: The parsed content (markdown or extracted text), or None if parsing fails.
        """
        if self.parser_type == "docling":
            doc = process_document_with_docling(source_path)
            if doc:
                self.docling_document = doc
                return doc.export_to_markdown()
            return None
        if self.parser_type == "llmwhisperer":
            return process_document_with_llmwhisperer(source_path)
        return None

