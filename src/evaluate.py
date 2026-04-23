import json
import csv
import os
import sys

# Ensure the project root is on sys.path when running src/evaluate.py directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generator import answer

# Your full question set
questions = [
    # --- DIRECT (Pick 10 things clearly stated in the chapter) ---
    
    # 3 questions about definitions
    {"id": 1, "question": "How does the chapter define Inertia?", "type": "direct", "expected": "in_scope"},
    {"id": 2, "question": "State Newton's First Law of Motion.", "type": "direct", "expected": "in_scope"},
    {"id": 3, "question": "What is the definition of Momentum?", "type": "direct", "expected": "in_scope"},
    
    # 3 questions about formulas
    {"id": 4, "question": "What is the mathematical formula for Momentum (p)?", "type": "direct", "expected": "in_scope"},
    {"id": 5, "question": "Provide the mathematical formulation of the Second Law of Motion (Force in terms of mass and acceleration).", "type": "direct", "expected": "in_scope"},
    {"id": 6, "question": "What is the formula for the Conservation of Momentum for two objects (m1, m2) before and after a collision?", "type": "direct", "expected": "in_scope"},
    
    # 2 questions about examples in the chapter
    {"id": 7, "question": "According to the chapter, why does a fielder pull his hands backwards while catching a fast-moving cricket ball?", "type": "direct", "expected": "in_scope"},
    {"id": 8, "question": "Explain the example of the glass pane breaking when hit by a fast-moving stone vs a slow-moving one.", "type": "direct", "expected": "in_scope"},
    
    # 2 questions about units or quantities
    {"id": 9, "question": "What is the SI unit of Force and its symbol?", "type": "direct", "expected": "in_scope"},
    {"id": 10, "question": "What are the SI units of Momentum?", "type": "direct", "expected": "in_scope"},

    # --- PARAPHRASED (Take 3 direct questions and reword them) ---
    
    {"id": 11, "question": "Why is it difficult to suddenly stop or start moving when you are standing in a bus that abruptly changes its motion?", "type": "paraphrased", "expected": "in_scope"},
    {"id": 12, "question": "Why can a small bullet cause significantly more damage than a larger object thrown by hand at low speed?", "type": "paraphrased", "expected": "in_scope"},
    {"id": 13, "question": "Why does a rowing boat move backward when a sailor jumps out of it in the forward direction?", "type": "paraphrased", "expected": "in_scope"},

    # --- OUT-OF-SCOPE (3 easy + 1 hard) ---
    
    # Easy: completely unrelated topic
    {"id": 14, "question": "What are the primary differences between aerobic and anaerobic respiration?", "type": "out_of_scope", "expected": "refuse"},
    # Easy: another subject entirely
    {"id": 15, "question": "Who was the first Prime Minister of independent India?", "type": "out_of_scope", "expected": "refuse"},
    # Easy: general knowledge
    {"id": 16, "question": "Which planet in our solar system is famously known as the Red Planet?", "type": "out_of_scope", "expected": "refuse"},
    # Hard: sounds like physics but not in chapter
    {"id": 17, "question": "Explain how a massive object like a star can warp the fabric of spacetime to create a black hole.", "type": "out_of_scope", "expected": "refuse"}
]

def evaluate_all(questions, output_path):
    results = []
    
    for q in questions:
        print(f"Testing Q{q['id']}: {q['question'][:50]}...")
        
        # Get answer from your pipeline
        result = answer(q["question"])
        
        # Check if system refused
        refused = "don't have enough information" in result["answer"].lower()
        
        # Build result row
        row = {
            "id": q["id"],
            "type": q["type"],
            "question": q["question"],
            "answer": result["answer"],
            "chunks_retrieved": [c["chunk_id"] for c in result["chunks"]],
            "refused": refused,
            # You fill these manually after running
            "correctness": "",      # yes / partial / no
            "grounding": "",        # yes / no
            "refusal_appropriate": "" # yes / no / na
        }
        results.append(row)
        print(f"  Refused: {refused}")
        print(f"  Answer: {result['answer'][:100]}")
        print()
    
    # Save to CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    evaluate_all(questions, "evaluation_results.csv")