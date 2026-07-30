def build_request_body(
        system_prompt,
        user_prompt,
        model,
        temperature):

    return {

        "model": model,

        "messages": [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_prompt
            }

        ],

        "temperature": temperature

    }