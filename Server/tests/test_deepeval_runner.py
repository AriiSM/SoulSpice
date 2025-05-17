import asyncio
import json
from deepeval.test_case import LLMTestCase
from deepeval.evaluate import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)
from app.services.llm_service import LLMService

# COMENZI TERMINAL:
# set OPENAI_API_KEY=
# (optional) set OPENAI_ORG_ID=
# am rulat cu deepeval test run tests\test_deepeval_runner.py din folderul Server


# 0. Initializeaza serviciul LLM local
llm_service = LLMService()

def your_llm_app(input, prompt_template=None):
    if prompt_template:
        full_prompt = prompt_template.format(input=input)
    else:
        full_prompt = input
    return asyncio.run(llm_service.generate_response(full_prompt))

# 1. Defineste promptul
prompt_template = (
    "You are SoulSpice, an expert chef and psychologist. "
    "Answer the following question in a helpful and professional way:\n{input}"
)

# 2. Context de test 
context_map = {
    "How do I make a healthy smoothie?": [
        "A healthy smoothie can be made using banana, spinach, berries, Greek yogurt, and almond milk."
    ],
    "What are the emotional benefits of cooking as a family?": [
        "Cooking together strengthens family bonds and promotes emotional wellbeing through shared experiences."
    ],
    "How can I introduce healthy eating habits to my children?": [
        "Introduce healthy foods gradually, involve children in meal prep, and model healthy eating habits yourself."
    ],
}


# 3. Defineste testele
test_cases = []
for question, context in context_map.items():
    test_cases.append(LLMTestCase(
        input=question,
        expected_output=context[0],
        actual_output=your_llm_app(question, prompt_template),
        retrieval_context=context
    ))

print(f"[INFO] Total test cases defined: {len(test_cases)}")


# 4. Defineste metricile
metrics = [
    AnswerRelevancyMetric(threshold=0.7, include_reason=True),
    FaithfulnessMetric(threshold=0.7, include_reason=True),
    ContextualRelevancyMetric(threshold=0.7, include_reason=True),
    ContextualPrecisionMetric(threshold=0.7, include_reason=True),
    ContextualRecallMetric(threshold=0.7, include_reason=True)
]

# 5. Ruleazs evaluarea
results = evaluate(
    identifier="SoulSpice Evaluation with Full Metrics",
    test_cases=test_cases,
    metrics=metrics,
    hyperparameters={"Prompt Template": prompt_template},
)


# 6. Salveaza raportul JSON
report_data = []

for case in results.test_cases:
    case_dict = {
        "input": case.input,
        "expected_output": case.expected_output,
        "actual_output": case.actual_output,
        "retrieval_context": case.retrieval_context,
        "metrics": []
    }

    for metric in case.metrics_output:
        case_dict["metrics"].append({
            "name": metric.name,
            "score": round(metric.score, 4),
            "threshold": metric.threshold,
            "status": "PASSED" if metric.score >= metric.threshold else "FAILED",
            "reason": metric.reason
        })

    report_data.append(case_dict)

try:
    with open("evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)
    print("[OK] Raportul a fost salvat in evaluation_report.json")
except Exception as e:
    print(f"[FAIL] Eroare la salvarea raportului: {e}")
