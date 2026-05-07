import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.ai_providers import call_huggingface_router
from services.prompt_service import build_prompt, refine_prompt_text, suggest_improvements
from services.schemas import (
    AIResponse,
    PromptRequest,
    PromptResponse,
    RefinePromptRequest,
    TestPromptRequest,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger('prompto_dina')


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.post('/generate_prompt', response_model=PromptResponse)
def generate_prompt(data: PromptRequest):
    logger.info('generate_prompt request: %s', data.dict())
    prompt = build_prompt(data)
    suggestions = suggest_improvements(data)
    return PromptResponse(prompt=prompt, suggestions=suggestions)


@app.post('/test_prompt', response_model=AIResponse)
def test_prompt(data: TestPromptRequest):
    logger.info('test_prompt request: %s', data.dict())
    try:
        response = call_huggingface_router(data.prompt)
    except Exception as exc:
        logger.exception('HuggingFace inference failed')
        raise
    logger.info('test_prompt response length: %d', len(response) if response else 0)
    return AIResponse(response=response)


@app.post('/refine_prompt', response_model=PromptResponse)
def refine_prompt(data: RefinePromptRequest):
    logger.info('refine_prompt request: %s', data.dict())
    refined = refine_prompt_text(data.prompt, data.action)
    return PromptResponse(prompt=refined)


@app.get('/ping')
def ping():
    return {'status': 'ok', 'message': 'Backend disponible'}


@app.get('/')
def read_root():
    return {'message': 'Prompt Builder API opérationnelle'}
