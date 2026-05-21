uv venv
.venv\Scripts\activate

uv pip instal "fastapi[standard]"
uv pip show fastapi

fastapi dev .\practicingFastAPI\main.py