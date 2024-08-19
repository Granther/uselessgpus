# Use Less GPUs!!
- Do you think we could use less GPU's for inference if we just has a smalled LLM with a good RAG system

### My Proposal
- Sumbit query to small LLM with large ctx window
- Use Tavily to find websites pertaining to the query
- Scrape said websites and put them in a vector DB
- Use vector DB for standard RAG and future queries

### Today
- Tavily Search and Unstructured Scraping
