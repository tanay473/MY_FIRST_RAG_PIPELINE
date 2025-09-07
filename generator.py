# -*- coding: utf-8 -*-
"""
Handles generating responses using the local LLM.
"""
from openai import OpenAI
import config

class Generator:
    """A class to generate text using an LLM served by LM Studio."""
    def __init__(self):
        self.client = OpenAI(
            base_url=config.LM_STUDIO_BASE_URL,
            api_key=config.LM_STUDIO_API_KEY
        )

    def generate_response(self, query, context):
        """
        Generates a response using the LLM with the retrieved context.
        """
        print("\nGenerating response from LLM...")
        
        system_prompt = (
            "You are a helpful assistant. Answer the user's query based on the "
            "following context. If the context does not contain the answer, "
            "state that you don't have enough information."
        )
        
        context_str = "\n\n".join(context)
        
        user_prompt = f"""
        Context:
        ---
        {context_str}
        ---
        Query: {query}
        """
        
        completion = self.client.chat.completions.create(
            model=config.LM_STUDIO_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
        )

        return completion.choices[0].message.content
