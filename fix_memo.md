# Fix Memo - Stage 5

## The Failure
Q12: "Explain how Newton's laws apply to planets orbiting the Sun."
Type: out_of_scope (hard - uses chapter vocabulary)
v1 result: Answered confidently using Newton's law chunks
v1 failure mode: Ambiguous query - question used chapter vocabulary
("Newton's laws") so retriever returned relevant-looking chunks,
and permissive prompt allowed LLM to extend beyond context.

## The Fix
Tightened prompt v2 with two changes:
1. Explicitly scoped to "Chapter 8 - Force and Laws of Motion ONLY"
2. Added instruction: "Do NOT infer or extend beyond the context"

## Score Delta
Before fix: 2/3 out-of-scope refused (67%)
After fix:  3/3 out-of-scope refused (100%)
In-scope correctness: unchanged at 9/9

## Honest Assessment
The fix worked for Q12 specifically. However it may be fragile - a question like "Explain Newton's laws in the context of rocket science"
would likely still fail because the retriever returns relevant chunks
and the LLM may still extend. 
A more robust fix would be explicit topic classification before retrieval.