import json, sys, os
sys.path.insert(0, os.path.abspath('.'))
from src.retriever import build_dense_index, retrieve_dense

collection, model = build_dense_index('vectorstore')

questions = [
    'What is Newton first law of motion?',
    'What is Newton second law of motion?',
    'What is the definition of momentum?',
    'What is the SI unit of force?',
    'Why does a fielder pull his hands back while catching a ball?',
    'What is the formula for acceleration?'
]

log = []
for q in questions:
    results = retrieve_dense(q, collection, model, top_k=3)
    log.append({
        'question': q,
        'top_chunks': [{'chunk_id': c['chunk_id'], 'content_type': c.get('content_type',''), 'text': c['text'][:150]} for c in results]
    })
    print(f'Q: {q}')
    for r in results:
        print(f'  Chunk {r["chunk_id"]}: {r["text"][:100]}')
    print()

with open('retrieval_log.json', 'w') as f:
    json.dump(log, f, indent=2)
print('Saved retrieval_log.json')