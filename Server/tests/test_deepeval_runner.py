from deepeval.prompt import Prompt
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval import evaluate
from openai import OpenAI

import os
os.environ["OPENAI_API_KEY"] = ""  # cheia ta reală


# Cont pe deepEval cu stud -> se genereaza un API key : KEY
# pt reconectare : deepeval login --confident-api-key KEY
# PASI:
# 1. in terminal: deepeval login, apoi acolo se pune api key
# 2. in terminal: deepeval test run tests\


client = OpenAI()

def your_llm_app(input, prompt=None):
    if prompt:
        full_prompt = prompt.interpolate(inputs={"input": input})
    else:
        full_prompt = input
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": full_prompt}],
    )
    return response.choices[0].message.content.strip()


# 1. Load dataset and prompt
dataset = EvaluationDataset()
dataset.pull(alias="soulspice-dataset")  # ← înlocuiește cu aliasul tău real

prompt = Prompt(alias="soulspice-prompt")  # ← înlocuiește cu aliasul tău real
prompt.pull()


# 2. Generează test cases
for golden in dataset.goldens:
    test_case = LLMTestCase(
        input=golden.input,
        actual_output=your_llm_app(golden.input, prompt),
        expected_output=golden.expected_output
    )
    dataset.test_cases.append(test_case)


# 3. Rulează evaluarea
evaluate(
    identifier="SoulSpice Prompt Eval - May",
    test_cases=dataset.test_cases,
    metrics=[AnswerRelevancyMetric()],
    hyperparameters={"Prompt Version": prompt}
)
