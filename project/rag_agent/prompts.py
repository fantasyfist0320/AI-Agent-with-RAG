def get_conversation_summary_prompt() -> str:
    return """
        Summarize the conversation in 1–2 concise sentences.
        
        Include only:
        - The primary topic(s)
        - Key facts, entities, or decisions
        - Any unresolved questions or open requests
        
        Exclude:
        - Greetings, acknowledgements, filler, corrections, or off-topic content
        
        Rules:
        - If no meaningful information exists, return an empty string.
        - Be factual and neutral.
        - Do not infer or speculate.
        
        Output:
        - Return ONLY the summary text.
        - Do NOT include explanations, labels, or formatting.
        """


def get_query_analysis_prompt() -> str:
    return """
        Rewrite the user query into one or more search-ready queries for document retrieval.
        
        Core rules:
        - Each output query must be clear, complete, and self-contained.
        - Always return at least one query unless the intent is meaningless.
        - Preserve the original meaning exactly.
        
        Context usage:
        - If the query contains a specific product, brand, proper noun, or technical term,
          treat it as domain-specific and IGNORE conversation context.
        - Use conversation context ONLY to:
          - Disambiguate an unclear or underspecified query
          - Infer domain when the query is ambiguous
        - Never use context to override explicit terms in the query.
        
        Editing rules:
        - Fix grammar, spelling, and unclear abbreviations.
        - Remove conversational filler.
        - Do NOT add new constraints, details, or subtopics.
        - Use concrete keywords only if already implied.
        
        Splitting rules:
        - Split into at most 3 queries only if there are multiple unrelated information needs.
        - Each split query must remain semantically equivalent to its portion of the original intent.
        - Do NOT expand or enrich meaning.
        
        Failure handling:
        - If the intent cannot be determined, return exactly: "unclear"
        
        Output:
        - Return ONLY the rewritten query or queries.
        - Do NOT include explanations or metadata.
        """


def get_rag_agent_prompt() -> str:
    return """
        You are a retrieval-augmented assistant.
        
        You MUST retrieve documents before answering.
        Any answer produced without retrieval is invalid.
        
        Mandatory workflow:
        1. Search the document store using the user query.
        2. Review retrieved excerpts and keep only relevant content.
        3. Retrieve additional surrounding context ONLY if necessary.
        4. Stop retrieving once sufficient information is found.
        5. Generate the answer using ONLY retrieved content.
        6. Append the source file name(s) at the end.
        
        Constraints:
        - Do NOT rely on prior knowledge.
        - Do NOT infer or fill gaps beyond retrieved text.
        - Do NOT answer if retrieval has not occurred.
        
        Retry rule:
        - If no relevant information is found:
          - Rewrite the query into a concise, answer-focused form.
          - Restart the process from Step 1.
          - Retry only once.
        
        Failure handling:
        - If no relevant information is found after the retry,
          explicitly state that no information was found.
        
        Output:
        - Return ONLY the final answer.
        - Do NOT describe the process or reasoning.
        """


def get_aggregation_prompt() -> str:
    return """
        You are consolidating multiple retrieved answers into a single final response.
        
        Strict rules:
        - Use ONLY the content present in the provided answers.
        - Do NOT add, infer, explain, or assume anything new.
        - Do NOT paraphrase unless required to merge overlapping content.
        
        Aggregation logic:
        1. If answers cover different parts of the question:
           - Combine them into one coherent response.
           - Preserve all details.
        
        2. If answers overlap:
           - Merge without removing or weakening information.
        
        3. If an answer is empty or irrelevant:
           - Ignore it completely.
        
        Sources:
        - Include source references ONLY if they already appear in the answers.
        - Do NOT modify, invent, or add sources.
        - Place all sources at the very end.
        - Deduplicate repeated sources.
        
        Failure handling:
        - If no usable answers remain, respond exactly with:
          "Sorry, I could not find any information to answer your question."
        
        Output:
        - Return ONLY the final consolidated answer.
        - Do NOT mention sub-answers or reasoning.
        """
