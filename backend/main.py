from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend import codegen, intent, ir, lexer, parser, semantic

app = FastAPI()

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessRequest(BaseModel):
    sentence: str


@app.get("/")
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/styles.css")
async def styles():
    return FileResponse(FRONTEND_DIR / "styles.css")


@app.get("/app.js")
async def script():
    return FileResponse(FRONTEND_DIR / "app.js")


@app.post("/process")
async def process(request: ProcessRequest):
    preprocessed = lexer.preprocess(request.sentence)
    tokens = lexer.tokenize(request.sentence)
    syntax_result = parser.parse(tokens)
    semantic_result = semantic.analyze(tokens, syntax_result["rule"])
    intent_result = intent.extract(tokens, syntax_result["rule"])
    ir_result = ir.generate(syntax_result["rule"], intent_result["entities"])
    code_result = codegen.generate(ir_result)

    return {
        "preprocessed": preprocessed,
        "tokens": tokens,
        "syntax_status": syntax_result,
        "semantic_status": semantic_result,
        "intent": intent_result["intent"],
        "entities": intent_result["entities"],
        "ir": ir_result,
        "code": code_result,
    }
