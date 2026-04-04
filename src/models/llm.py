from openai import OpenAI

client = OpenAI()


def generate_answer(query, context_chunks):
    context = "\n\n".join([c["text"] for c in context_chunks])

    prompt = f"""
You are an automotive engineering assistant.

Answer ONLY from the context below.
If answer is not present, say "Not found in document".

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )

    return response.choices[0].message.content
