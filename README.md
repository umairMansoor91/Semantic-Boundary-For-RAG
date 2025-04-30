# Semantic Boundary Chunking Dataset Generation for RAG – Hadith Contradiction Dataset

This project focuses on extracting and semantically chunking Hadith texts for use in Retrieval-Augmented Generation (RAG) pipelines. It processes HTML-formatted Hadith content, segments narrations by chapters, and outputs a structured dataset in JSON. The aim is to support contradiction detection, Islamic NLP tasks, and fine-tuning of models on authentic Islamic knowledge.

---

## 🧠 Objective

To generate a clean and semantically structured dataset of Hadith narrations grouped by chapters, where the last narration in each chapter is treated as the **verdict**. This structure enables downstream applications like:

- Contradiction detection
- Semantic chunk retrieval

- Islamic reasoning using LLMs
- Dataset preparation for fine-tuning or RAG pipelines

---

## 📁 Dataset Format

The script outputs a JSON file structured like this:

```json
[
  {
    "chapter_title": "Title of Chapter",
    "hadiths": [
      {
        "hadith_number": "123",
        "text": "123 - Full Hadith text..."
      },
      ...
    ],
    "verdict": {
      "hadith_number": "456",
      "text": "456 - Concluding Hadith text..."
    }
    "title_number": 1
  },
  ...
]
