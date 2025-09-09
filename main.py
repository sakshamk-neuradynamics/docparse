"""
Docling Document Converter
"""

import logging
from pathlib import Path
import os

from dotenv import load_dotenv
import streamlit as st

from parsers import Parser

load_dotenv()

logging.basicConfig(level=logging.INFO)

# --- Streamlit App ---
st.set_page_config(layout="wide")
st.title("Document Parser App")

# Create two columns for the layout
left_column, right_column = st.columns([1, 2])

with left_column:
    st.header("Upload Document & Select Parser")
    uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "pptx"])
    parser_choice = st.selectbox(
        "Select Parser",
        ("docling", "llmwhisperer"),
        help="Docling: Better for structured documents with tables/images. LLMWhisperer: Better for text extraction."
    )
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.info(f"File size: {uploaded_file.size} bytes")

with right_column:
    st.header("Parsed Content")
    if uploaded_file is not None:
        # Ensure output directory exists for temporary files
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded file to a temporary location
        temp_file_path = Path(os.path.join(output_dir, uploaded_file.name))
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner(f"Processing with {parser_choice}..."):
            parser_instance = Parser(parser_type=parser_choice)
            parsed_content = parser_instance.parse(temp_file_path)

        if parsed_content:
            st.success("Document parsed successfully!")
            
            # Add download button
            file_extension = "md" if parser_choice == "docling" else "txt"
            st.download_button(
                label=f"Download {parser_choice.upper()} output",
                data=parsed_content,
                file_name=f"{uploaded_file.name.split('.')[0]}_{parser_choice}.{file_extension}",
                mime="text/plain"
            )
            
            if parser_choice == "docling":
                # For Docling, display as markdown
                right_column.markdown(parsed_content)
            else:
                # For LLMWhisperer, split on page breaks and display as plain text
                pages = parsed_content.split("<<<")
                st.write(f"**Found {len(pages)} pages:**")
                
                for i, page_content in enumerate(pages, 1):
                    with st.expander(f"Page {i}", expanded=(i == 1)):
                        st.text(page_content.strip())
        else:
            right_column.error("Failed to parse document.")

        # Clean up temporary file
        os.remove(temp_file_path)
    else:
        st.info("Upload a document to get started.")

    

# --- Old File Processing Logic (Commented out) ---
# SOURCE = Path("./input/2408.09869v5.pdf")

# # LLMWhisperer Implementation
# _log.info("Processing document with LLMWhisperer")
# llm_whisperer_parser_instance = Parser(parser_type="llmwhisperer")
# llm_whisperer_time_start = time.time()
# result_text = llm_whisperer_parser_instance.parse(SOURCE)
# llm_whisperer_time_end = time.time()
# _log.info("LLMWhisperer Time taken: %s seconds", llm_whisperer_time_end - llm_whisperer_time_start)

# if result_text:
#     # Split the text into pagewise texts array
#     FORM_FEED_CHAR = chr(12)
#     pagewise_texts = result_text.split(f"<<<{FORM_FEED_CHAR}")

#     for i, page_text in enumerate(pagewise_texts):
#         output_filename = output_dir / f"llm_whisperer_page_{i+1}.txt"
#         with open(output_filename, "w", encoding="utf-8") as f:
#             f.write(page_text.strip())
#         _log.info("LLMWhisperer page %d text saved to %s", i+1, output_filename)

#     print(*pagewise_texts, sep="\n")

# # Docling Implementation
# _log.info("Converting document with Docling")
# docling_parser_instance = Parser(parser_type="docling")
# time_start = time.time()
# markdown_content = docling_parser_instance.parse(SOURCE)
# time_end = time.time()
# _log.info("Docling Time taken: %s seconds", time_end - time_start)

# if docling_parser_instance.docling_document:
#     doc = docling_parser_instance.docling_document
#     DOC_FILENAME = SOURCE.stem

#     # Save page images
#     for page_no, page in doc.pages.items():
#         if not page.image:
#             continue
#         page_no = page.page_no
#         page_image_filename = output_dir / f"{DOC_FILENAME}-{page_no}.png"
#         with page_image_filename.open("wb") as fp:
#             page.image.pil_image.save(fp, format="PNG")

#     # Save images of figures and tables
#     TABLE_COUNTER = 0
#     PICTURE_COUNTER = 0
#     for element, _level in doc.iterate_items():
#         if isinstance(element, TableItem):
#             TABLE_COUNTER += 1
#             element_image_filename = (
#                 output_dir / f"{DOC_FILENAME}-table-{TABLE_COUNTER}.png"
#             )
#             with element_image_filename.open("wb") as fp:
#                 element.get_image(doc).save(fp, "PNG")

#         if isinstance(element, PictureItem):
#             PICTURE_COUNTER += 1
#             element_image_filename = (
#                 output_dir / f"{DOC_FILENAME}-picture-{PICTURE_COUNTER}.png"
#             )
#             with element_image_filename.open("wb") as fp:
#                 element.get_image(doc).save(fp, "PNG")

#     _log.info("Saving document to output.md")
#     # The markdown content is already returned by the parse method, so we can save it directly
#     if markdown_content:
#         with open(output_dir / f"{DOC_FILENAME}.md", "w", encoding="utf-8") as f:
#             f.write(markdown_content)
#         _log.info("Docling markdown saved to %s/%s.md", output_dir, DOC_FILENAME)
