import logging
import time
from pathlib import Path

from unstract.llmwhisperer import LLMWhispererClientV2
from unstract.llmwhisperer.client_v2 import LLMWhispererClientException

_log = logging.getLogger(__name__)

def process_document_with_llmwhisperer(file_path: Path) -> str | None:
    """
    Processes a document using the LLMWhisperer API and returns the extracted text.
    """
    _log.info("Processing document with LLMWhisperer: %s", file_path)
    llm_whisperer_client = LLMWhispererClientV2()
    llm_whisperer_time_start = time.time()
    try:
        llm_whisperer_result = llm_whisperer_client.whisper(
            file_path=str(file_path),
            wait_for_completion=True,
            wait_timeout=200
        )
        llm_whisperer_time_end = time.time()
        _log.info("LLMWhisperer processing complete: %s", llm_whisperer_result["status"])
        _log.info(
            "LLMWhisperer Time taken: %s seconds",
            llm_whisperer_time_end - llm_whisperer_time_start
        )

        if "extraction" in llm_whisperer_result and "result_text" in llm_whisperer_result["extraction"]:
            return llm_whisperer_result["extraction"]["result_text"]
        return None

    except LLMWhispererClientException as e:
        _log.error("LLMWhisperer Error: %s, Status Code: %s", e.error_message(), e.status_code)
        return None
