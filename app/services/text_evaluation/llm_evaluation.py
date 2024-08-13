# services/text_evaluation/llm_evaluation.py

import os
import logging
import asyncio
from openai import AsyncOpenAI
from .prompts import EVALUATION_PROMPT, QUESTION
from tenacity import retry, stop_after_attempt, wait_exponential

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def evaluate_with_llm(text):
    prompt = EVALUATION_PROMPT.format(QUESTION=QUESTION, answer=text)
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert language evaluator."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        logger.info(f"LLM Response Content: {content}")

        return parse_llm_response(content)
    except Exception as e:
        logger.error(f"Error in LLM evaluation: {str(e)}")
        raise

def parse_llm_response(content):
    lines = content.split('\n')
    results = {}
    categories = ['vocab', 'grammar', 'conjugation', 'cultural', 'expression']
    
    for category in categories:
        results[f"{category}_score"] = None
        results[f"{category}_eval"] = None

    for line in lines:
        for category in categories:
            if line.startswith(f"{category}_eval:"):
                logger.info(f"Processing line for category '{category}': {line}")
                parts = line.split(':', 2)
                if len(parts) == 3:
                    _, evaluation, score_part = parts
                    results[f"{category}_eval"] = evaluation.strip()
                    try:
                        results[f"{category}_score"] = float(score_part.strip().split()[0])
                    except (ValueError, IndexError):
                        logger.warning(f"Could not parse score for {category}")

    logger.info(f"Evaluation results: {results}")
    return results

async def batch_evaluate_with_llm(texts):
    tasks = [evaluate_with_llm(text) for text in texts]
    return await asyncio.gather(*tasks)