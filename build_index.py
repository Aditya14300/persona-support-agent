from src.rag_pipeline import RAGPipeline

rag = RAGPipeline()

rag.build_index()

print("Knowledge Base Indexed Successfully")
