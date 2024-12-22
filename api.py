from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from diff_json import generate_diff_json
from diff_md import create_markdown_file
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


app = FastAPI()


# Ensure the sample_pdfs directory exists
OUTPUT_DIR = "sample_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read environment variables
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

if not LLAMA_CLOUD_API_KEY:
    raise RuntimeError(
        "LLAMA_CLOUD_API_KEY is missing. Please add it to your .env file."
    )


@app.get("/")
async def hello_world():
    return "hello world!"


@app.post("/compare-pdfs/")
async def compare_pdfs(
    old_version: UploadFile = File(...), new_version: UploadFile = File(...)
):
    if not (
        old_version.filename.endswith(".pdf") and new_version.filename.endswith(".pdf")
    ):
        return JSONResponse(
            content={"message": "Both files must be PDFs."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Temporary file paths
    old_pdf_path = os.path.join(OUTPUT_DIR, "temp_old_version.pdf")
    new_pdf_path = os.path.join(OUTPUT_DIR, "temp_new_version.pdf")

    try:
        # Save uploaded files to disk
        with open(old_pdf_path, "wb") as f:
            f.write(await old_version.read())
        with open(new_pdf_path, "wb") as f:
            f.write(await new_version.read())

        # Parse PDF files to markdown
        llama_parser = LlamaParse(result_type="markdown")
        old_markdown = await llama_parser.aload_data(old_pdf_path)
        new_markdown = await llama_parser.aload_data(new_pdf_path)

        # Create markdown files
        old_md_path = os.path.join(OUTPUT_DIR, "old_version.md")
        new_md_path = os.path.join(OUTPUT_DIR, "new_version.md")
        create_markdown_file(old_md_path, old_markdown)
        create_markdown_file(new_md_path, new_markdown)

        # Generate JSON diff
        diff_json = generate_diff_json(old_md_path, new_md_path)

        # Clean up temporary markdown and PDF files
        os.remove(old_md_path)
        os.remove(new_md_path)
        os.remove(old_pdf_path)
        os.remove(new_pdf_path)

        # Return success response with diff
        return JSONResponse(
            content={
                "message": "PDF comparison complete.",
                "output": diff_json,
                "status": "success",
            },
            status_code=status.HTTP_200_OK,
        )

    except HTTPException as e:

        # Cleanup in case of failure
        if os.path.exists(old_md_path):
            os.remove(old_md_path)
        if os.path.exists(new_md_path):
            os.remove(new_md_path)
        if os.path.exists(old_pdf_path):
            os.remove(old_pdf_path)
        if os.path.exists(new_pdf_path):
            os.remove(new_pdf_path)

        # Return internal server error response
        return JSONResponse(
            content={"message": f"An error occurred: {str(e)}", "status": "error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
