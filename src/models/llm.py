from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI()


def generate_answer(query: str, context_chunks: List[Dict[str, Any]]) -> str:
    """
    Generate a grounded answer using retrieved context chunks.

    Args:
        query: The user's question
        context_chunks: List of retrieved chunks with content and metadata

    Returns:
        Generated answer based on the context
    """

    # Format context with metadata
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        chunk_type = chunk.get("metadata", {}).get("type", "unknown")
        page = chunk.get("metadata", {}).get("page", "unknown")

        # Format chunk based on type
        if chunk_type == "table":
            content = f"[TABLE from page {page}]:\n{chunk['content']}"
        elif chunk_type == "image":
            content = f"[IMAGE DESCRIPTION from page {page}]:\n{chunk['content']}"
        else:
            content = f"[TEXT from page {page}]:\n{chunk['content']}"

        context_parts.append(f"--- Context Chunk {i} ---\n{content}")

    context = "\n\n".join(context_parts)

    # Enhanced RAG prompt template
    prompt = f"""You are an expert automotive engineering assistant specializing in fuel efficiency, emission standards, and transportation policy.

Your task is to provide accurate, well-grounded answers based ONLY on the provided context. Follow these guidelines:

1. **Grounded Answers**: Base your response exclusively on information from the provided context chunks. Do not use external knowledge.

2. **Content Types**: The context may include:
   - TEXT: Regular document text
   - TABLE: Structured data in tabular format
   - IMAGE: Visual content descriptions

3. **Answer Structure**:
   - Be concise but comprehensive
   - Cite specific pages when relevant
   - If information spans multiple chunks, synthesize it coherently
   - Use bullet points or numbered lists for clarity when appropriate

4. **Handling Missing Information**:
   - If the context doesn't contain relevant information, say: "Based on the available documents, I cannot find information about [topic]."
   - Do not make assumptions or provide information not present in the context.

5. **Technical Accuracy**: Maintain technical precision, especially for engineering specifications, standards, and data.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides accurate, grounded answers based only on the provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1,  # Low temperature for more deterministic, factual responses
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating answer: {str(e)}. Please check your OpenAI API configuration."


def generate_answer_with_sources(query: str, context_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate an answer with detailed source information.

    Returns:
        Dictionary containing answer, sources, and metadata
    """
    answer = generate_answer(query, context_chunks)

    # Extract source information
    sources = []
    for chunk in context_chunks:
        source_info = {
            "content": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],
            "type": chunk.get("metadata", {}).get("type", "unknown"),
            "page": chunk.get("metadata", {}).get("page", "unknown"),
            "score": chunk.get("score", 0)
        }
        sources.append(source_info)

    return {
        "answer": answer,
        "sources": sources,
        "total_sources": len(sources),
        "query": query
    }
