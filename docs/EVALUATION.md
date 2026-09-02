# Retrieval and answer evaluation

A useful RAG system should be evaluated separately for retrieval and generation.

## Retrieval
- **Recall@K**: whether a known supporting chunk appears in the top K.
- **MRR**: how high the first relevant result ranks.
- **Modality coverage**: whether questions grounded in images/audio/video retrieve those sources.

## Generation
- **Groundedness**: every factual answer statement should be supported by retrieved context.
- **Citation correctness**: cited files/locators should contain the supporting fact.
- **Answer completeness**: all requested points supported by the source should be addressed.
- **Abstention quality**: insufficient context should result in a clear refusal to invent an answer.

A later production phase can add a golden QA dataset and automated model-as-judge scoring while retaining manual spot checks.
