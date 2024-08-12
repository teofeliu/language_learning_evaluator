import os
import logging
from openai import AsyncOpenAI
from .prompts import EVALUATION_PROMPT, QUESTION

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def evaluate_with_llm(text):
    prompt = EVALUATION_PROMPT.format(QUESTION=QUESTION, answer=text)
    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert language evaluator."},
            {"role": "user", "content": prompt}
        ]
    )

    # Parse the response
    content = response.choices[0].message.content
    logger.info(f"LLM Response Content: {content}")  # Log content

    lines = content.split('\n')
    results = {}
    categories = ['vocab', 'grammar', 'conjugation', 'cultural', 'expression']
    
    for category in categories:
        results[f"{category}_score"] = None
        results[f"{category}_eval"] = None

    for line in lines:
        for category in categories:
            if line.startswith(f"{category}_eval:"):
                logger.info(f"Processing line for category '{category}': {line}")  # Log line and category
                eval_part, score_part = line.split(f"{category}_score:")
                evaluation = eval_part.split(':', 1)[1].strip()
                score = float(score_part.strip())
                results[f"{category}_score"] = score
                results[f"{category}_eval"] = evaluation

    logger.info(f"Evaluation results: {results}")  # Log final results
    return results