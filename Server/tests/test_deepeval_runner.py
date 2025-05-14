import asyncio
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval import evaluate
from app.services.llm_service import LLMService
import os
os.environ["OPENAI_API_KEY"] = ""  # cheia ta reală

# =========================
# 0. Inițializează serviciul LLM local
# =========================
llm_service = LLMService()

def your_llm_app(input, prompt_template=None):
    """
    Generează răspunsul folosind modelul local din LM Studio.
    """
    if prompt_template:
        full_prompt = prompt_template.format(input=input)
    else:
        full_prompt = input

    return asyncio.run(llm_service.generate_response(full_prompt))


# =========================
# 1. Definește promptul local (ca string simplu)
# =========================
prompt_template = (
    "You are SoulSpice, an expert chef and psychologist. "
    "Answer the following question in a helpful and professional way:\n{input}"
)

# =========================
# 2. Definește testele manual, local
# =========================
test_cases = [
    LLMTestCase(
        input="How do I make a healthy smoothie?",
        expected_output="Use spinach, banana, frozen berries, Greek yogurt, and almond milk. Blend until smooth and enjoy.",
        actual_output=your_llm_app("How do I make a healthy smoothie?", prompt_template)
    ),
    LLMTestCase(
        input="What are the emotional benefits of cooking as a family?",
        expected_output="Cooking as a family strengthens emotional bonds, encourages communication, and creates a sense of shared accomplishment.",
        actual_output=your_llm_app("What are the emotional benefits of cooking as a family?", prompt_template)
    ),
    LLMTestCase(
        input="How can I introduce healthy eating habits to my children?",
        expected_output="Introduce healthy foods gradually, involve children in meal preparation, and be a role model with your own eating habits.",
        actual_output=your_llm_app("How can I introduce healthy eating habits to my children?", prompt_template)
    )
]

print(f"[INFO] Total test cases defined: {len(test_cases)}")


# =========================
# 3. Rulează evaluarea
# =========================
evaluate(
    identifier="SoulSpice Local Prompt Evaluation",
    test_cases=test_cases,
    metrics=[AnswerRelevancyMetric()],
    hyperparameters={"Prompt Template": prompt_template}
)
