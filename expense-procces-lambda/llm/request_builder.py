def build_request_body(
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float
) -> dict:
    """
    Builds the request payload for a chat completion API.

    Args:
        system_prompt: System instructions that define the assistant's behavior.
        user_prompt: User input to be processed by the language model.
        model: Identifier of the language model to use.
        temperature: Sampling temperature controlling response randomness.

    Returns:
        A dictionary containing the request payload expected by the API.
    """

    # Build and return the request payload.
    return {

        # Language model to be used for the request.
        "model": model,

        # Conversation history sent to the model.
        "messages": [

            # System message defining the assistant's behavior.
            {
                "role": "system",
                "content": system_prompt
            },

            # User message containing the input to process.
            {
                "role": "user",
                "content": user_prompt
            }

        ],

        # Controls the randomness of the generated response.
        "temperature": temperature

    }