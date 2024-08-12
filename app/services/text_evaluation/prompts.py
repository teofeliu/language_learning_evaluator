# app/services/text_evaluation/prompts.py

EVALUATION_PROMPT = """
Evaluate the following text for:
1. Vocabulary (richness and appropriateness)
2. Grammar (correctness and complexity)
3. Conjugation (accuracy and variety of verb forms)
4. Cultural Understanding (references to customs, traditions, historical events, or societal norms)
5. Expression (clarity, style, and effectiveness of communication)

For each category, start by briefly evaluating and then providing a score from 1-10. Keep in mind this is a speech to text transcription, so some errors like punctuation may be because of the transcription service.

Question: {QUESTION}
Answer: {answer}

STRICTLY format your response as the following. The eval and score should be on the same line, and there should not be a blank line between categories.Your answer should have five lines total:
vocab_eval: [brief evaluation], vocab_score: [score]
grammar_eval:  [brief evaluation], grammar_score: [score]
conjugation_eval:  [brief evaluation], conjugation_score: [score]
cultural_eval:  [brief evaluation], cultural_score: [score]
expression_eval:  [brief evaluation], expression_score: [score]
"""

QUESTION = """
If you could transport yourself to one moment in history, which moment would it be and why? What would this moment feel like? Paint the scene. Be thorough with your answer.
"""