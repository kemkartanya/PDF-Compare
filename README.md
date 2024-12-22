
# Compare PDFs

compare pdfs versions

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`LLAMA_CLOUD_API_KEY`


## Installation


```bash
  git clone https://github.com/kemkartanya/PDF-Compare.git

  cd PDF-Compare
  
  python -m venv env
  env source/bin/activate

  pip install -r requirements.txt

  python api.py
```
    
## Method

Used llama-parse for parsing pdfs to markdown

compared markdown files using difflib

return json as diff b/w files 

