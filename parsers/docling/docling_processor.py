import logging
from pathlib import Path

from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractOcrOptions,
)
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
    PowerpointFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

_log = logging.getLogger(__name__)

pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True
pipeline_options.ocr_options = TesseractOcrOptions(lang=["auto"])
pipeline_options.accelerator_options = AcceleratorOptions(
    num_threads=4,
    device=AcceleratorDevice.AUTO,
)
pipeline_options.images_scale = 2.0
pipeline_options.generate_picture_images = True
pipeline_options.generate_table_images = True

doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=StandardPdfPipeline, pipeline_options=pipeline_options
        ),
        InputFormat.DOCX: WordFormatOption(pipeline_cls=SimplePipeline),
        InputFormat.PPTX: PowerpointFormatOption(pipeline_cls=SimplePipeline),
    }
)

def process_document_with_docling(source_path: Path):
    _log.info("Converting document with Docling: %s", source_path)
    doc_res = doc_converter.convert(str(source_path))
    return doc_res.document
