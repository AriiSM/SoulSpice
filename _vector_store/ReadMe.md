# 📁 `_vector_store` – Vector Database & FAISS Indexing

This folder contains the technical components for processing textual data (such as conversations and recipes), generating embeddings, and building a **FAISS index** for fast semantic search.

It serves as the core of the **vector store** system – handling text chunking, embedding creation, and indexing logic.

---

## 🗂 File Structure

| File                              | Description                                                                 |
|-----------------------------------|-----------------------------------------------------------------------------|
| `chunking_conversations.ipynb`    | Splits conversation data into manageable text chunks for embedding.         |
| `chunking_recipes_csv.ipynb`      | Preprocesses recipe data from a CSV file and chunks it into logical parts. |
| `indexing.ipynb`                  | Generates embeddings from chunked data and builds the FAISS index.         |
| `main.ipynb`                      | Runs the full pipeline: chunking → embedding → indexing. Main entry point for testing. |

---

## ⚙️ Implementation Details

- The FAISS index type used is: `IndexFlatL2`, which performs brute-force search using L2 (Euclidean) distance.
- The text data is split into chunks using a delimiter (`==CHUNK END==`) before embedding.
- Embeddings are generated using the **`all-MiniLM-L6-v2`** model from [SentenceTransformers](https://www.sbert.net/).
- The index creation process is handled by a function like:

---

## 📂 Folder Structure

```plaintext
_vector_store/
│
├── conversations_dataset/
│   ├── chunking_conversations.ipynb   
│   └── parsed_conversations.txt       
│
├── recipes_dataset/
│   ├── chunking_recipes_csv.ipynb      
│   └── parsed_recipes.txt     
│         
├── faiss_index/
│   └── indexing.ipynb              
│
├── main.ipynb             
└── ReadMe.md                        