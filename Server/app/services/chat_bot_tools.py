from sentence_transformers import SentenceTransformer # type: ignore
import faiss
import numpy as np
from openai import AsyncOpenAI

class TextChunkLoader:
    def __init__(self, delimiter='==CHUNK END=='):
        self.delimiter = delimiter

    def load_chunks(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().split(self.delimiter)


from transformers import pipeline
class ToxicityFilter:
    def __init__(self, threshold=0.5, log_file="toxic_log.txt"):
        self.model = pipeline("text-classification", model="unitary/toxic-bert")
        self.threshold = threshold
        self.log_file = log_file

    def is_toxic(self, text):
        score = self.model(text)[0]['score']
        return score > self.threshold, score

    def log(self, text, score, source="response"):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{source.upper()} - Toxicity: {score:.4f}]\n{text}\n\n")



class SemanticRetriever:
    def __init__(self, model_name, recipe_index_path, conv_index_path, recipe_chunks, conv_chunks):
        self.model = SentenceTransformer(model_name)
        self.recipe_index = faiss.read_index(recipe_index_path)
        self.conv_index = faiss.read_index(conv_index_path)
        self.recipe_chunks = recipe_chunks
        self.conv_chunks = conv_chunks

    def search(self, question, k=1):
        vector = self.model.encode([question])
        D1, I1 = self.recipe_index.search(np.array(vector), k)
        D2, I2 = self.conv_index.search(np.array(vector), k)

        recipes = [self.recipe_chunks[i] for i in I1[0]]
        convs = [self.conv_chunks[i] for i in I2[0]]
        return recipes + convs

class ResponseGenerator:
    def __init__(self, base_url, api_key, model):
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    async def generate(self, prompt, temperature=0.7):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content


class SemanticSearchAssistant:
    def __init__(self, retriever, responder, toxicity_filter, max_retries=3):
        self.retriever = retriever
        self.responder = responder
        self.toxicity_filter = toxicity_filter
        self.max_retries = max_retries

    def build_prompt(self, context, question, empathy=False):
        prefix = "Answer with empathy.\n\n" if empathy else ""
        
        build_prompt = f"{prefix}Context:{context}\nQuestion: {question} \nAnswer:"
       
        # print(f"[INFO] Prompt build: {build_prompt}")

        return build_prompt

    async def ask(self, question, k=1, temperature=0.7):

        is_toxic, score = self.toxicity_filter.is_toxic(question)
        print(f"[INFO] Question toxicity: {score:.4f}")
        if is_toxic:
            return "The question was flagged as potentially toxic and cannot be processed."

        context_chunks = self.retriever.search(question, k)
        context = "\n\n".join(context_chunks)

        for attempt in range(1, self.max_retries + 1):
            use_empathy = attempt > 1
            prompt = self.build_prompt(context, question, empathy=use_empathy)
            response = await self.responder.generate(prompt, temperature=temperature)
            is_resp_toxic, resp_score = self.toxicity_filter.is_toxic(response)
            
            print(f"[INFO] Attempt {attempt} - Response toxicity: {resp_score:.4f}")
            if not is_resp_toxic:
                return response

            self.toxicity_filter.log(response, resp_score, source="response")

        return "We're sorry, but we couldn't generate a safe response. Please try rephrasing your question."
