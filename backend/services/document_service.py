import io
from pathlib import Path

UPLOADED_DIR = Path(__file__).parent.parent / "uploaded"


def extract_text(filename: str, content: bytes) -> str:
    """
    Extract plain text from uploaded files.
    Supports: .pdf, .txt, .json
    Returns empty string if extraction fails or type is unsupported.
    """
    ext = Path(filename).suffix.lower()

    if ext == ".txt":
        return content.decode("utf-8", errors="ignore")

    if ext == ".json":
        return content.decode("utf-8", errors="ignore")

    if ext == ".pdf":
        return _extract_pdf(content)

    return ""


def _extract_pdf(content: bytes) -> str:
    """
    Try pdfplumber first (fast, free, works for text-based PDFs).
    Fall back to AWS Textract for scanned/image-based PDFs.
    """
    text = _try_pdfplumber(content)
    if text.strip():
        return text

    text = _try_pypdf2(content)
    if text.strip():
        return text

    # Both failed — PDF is likely image-based, use AWS Textract OCR
    return _try_textract(content)


def _try_pdfplumber(content: bytes) -> str:
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    pages.append(t.strip())
        return "\n\n".join(pages)
    except Exception:
        return ""


def _try_pypdf2(content: bytes) -> str:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(content))
        pages = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                pages.append(t.strip())
        return "\n\n".join(pages)
    except Exception:
        return ""


def _try_textract(content: bytes) -> str:
    """
    Use AWS Textract to OCR image-based or scanned PDFs.
    Multi-page PDFs are uploaded to a temp S3 bucket, processed async,
    then the result is fetched and the temp file deleted.
    Requires AWS credentials and an S3 bucket name in TEXTRACT_S3_BUCKET env var.
    """
    try:
        import boto3
        import os
        import time
        import uuid

        region = os.getenv("BEDROCK_REGION", "us-east-1")
        bucket = os.getenv("TEXTRACT_S3_BUCKET", "")
        if not bucket:
            return ""

        s3 = boto3.client("s3", region_name=region)
        textract = boto3.client("textract", region_name=region)

        # Upload PDF to S3 temp location
        key = f"textract-temp/{uuid.uuid4()}.pdf"
        s3.put_object(Bucket=bucket, Key=key, Body=content)

        try:
            # Start async job
            job = textract.start_document_text_detection(
                DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
            )
            job_id = job["JobId"]

            # Poll until complete (max 60 seconds)
            for _ in range(12):
                time.sleep(5)
                result = textract.get_document_text_detection(JobId=job_id)
                status = result["JobStatus"]
                if status == "SUCCEEDED":
                    lines = [
                        b["Text"]
                        for b in result.get("Blocks", [])
                        if b["BlockType"] == "LINE"
                    ]
                    # Handle pagination
                    while "NextToken" in result:
                        result = textract.get_document_text_detection(
                            JobId=job_id, NextToken=result["NextToken"]
                        )
                        lines += [
                            b["Text"]
                            for b in result.get("Blocks", [])
                            if b["BlockType"] == "LINE"
                        ]
                    return "\n".join(lines)
                elif status == "FAILED":
                    return ""
        finally:
            # Always clean up the temp S3 file
            try:
                s3.delete_object(Bucket=bucket, Key=key)
            except Exception:
                pass

        return ""
    except Exception:
        return ""


def save_uploaded_text(assistant_id: str, filename: str, text: str) -> Path:
    """
    Save extracted text to uploaded/<assistant_id>/<filename>.txt
    so the retrieval service can search it.
    """
    assistant_dir = UPLOADED_DIR / assistant_id
    assistant_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(filename).stem + ".txt"
    filepath = assistant_dir / safe_name
    filepath.write_text(text, encoding="utf-8")
    return filepath
