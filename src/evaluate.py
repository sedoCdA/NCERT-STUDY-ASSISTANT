import json
import csv
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
from src.generator import answer

questions = [
    # Direct (6)
    {"id": 1,  "question": "State Newton's first law of motion.", "type": "direct", "expected": "in_scope"},
    {"id": 2,  "question": "What is the definition of momentum?", "type": "direct", "expected": "in_scope"},
    {"id": 3,  "question": "What is the SI unit of force?", "type": "direct", "expected": "in_scope"},
    {"id": 4,  "question": "State Newton's third law of motion.", "type": "direct", "expected": "in_scope"},
    {"id": 5,  "question": "What is the relationship between force mass and acceleration?", "type": "direct", "expected": "in_scope"},
    {"id": 6,  "question": "Why does a fielder pull his hands back while catching a cricket ball?", "type": "direct", "expected": "in_scope"},

    # Paraphrased (3)
    {"id": 7,  "question": "Why does a passenger jerk forward when a bus brakes suddenly?", "type": "paraphrased", "expected": "in_scope"},
    {"id": 8,  "question": "Why can a small bullet cause more damage than a slow heavy object?", "type": "paraphrased", "expected": "in_scope"},
    {"id": 9,  "question": "Why does a boat move backward when a sailor jumps forward?", "type": "paraphrased", "expected": "in_scope"},

    # Out of scope (3)
    {"id": 10, "question": "What are the differences between aerobic and anaerobic respiration?", "type": "out_of_scope", "expected": "refuse"},
    {"id": 11, "question": "Who was the first Prime Minister of India?", "type": "out_of_scope", "expected": "refuse"},
    {"id": 12, "question": "Explain how Newton's laws apply to planets orbiting the Sun.", "type": "out_of_scope", "expected": "refuse"},
]

def evaluate_all(questions, output_path):
    results = []

    for q in questions:
        print(f"Testing Q{q['id']}: {q['question'][:60]}...")
        result = answer(q["question"], use_dense=True, strict=True)

        refused = "don't have that in my study materials" in result["answer"].lower()

        row = {
            "id": q["id"],
            "type": q["type"],
            "question": q["question"],
            "answer": result["answer"],
            "chunk_ids": str(result["chunk_ids"]),
            "refused": refused,
            "correctness": "",
            "grounding": "",
            "refusal_appropriate": ""
        }
        results.append(row)
        print(f"  Refused: {refused}")
        print(f"  Answer: {result['answer'][:120]}")
        print()

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved to {output_path}")

if __name__ == "__main__":
    evaluate_all(questions, "eval_scored.csv")