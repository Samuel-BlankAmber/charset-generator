"""
This module provides functions for predicting flag characters using OpenAI's API.
This is highly experimental and should be used with caution.
"""

from typing import List

from openai import OpenAI


def assess_predictability(
    known_text: str, openai_api_key: str, model: str = "gpt-4o-mini",
    role: str = "You are a professional CTF hacker.",
    prompt: str = (
        "You will receive the first part of a flag. Analyze it and decide how confident you are in predicting "
        "the next character with 100% accuracy. Provide a brief explanation, then on a new line output exactly "
        "'~~' followed by one of these options: 'Very confident', 'Somewhat confident', or 'Not confident'.\n"
        "Example:\n"
        "The flag starts with 'CTF{' but many characters could follow.\n"
        "~~Not confident\n"
    )
) -> str:
    """
    Assess the predictability of the next flag character using OpenAI's API.

    Args:
        known_text (str): The known part of the flag.
        openai_api_key (str): API key for OpenAI.
        model (str): Model to use for prediction.
        role (str): Role description for the AI.
        prompt (str): Prompt template for the AI.

    Returns:
        str: Index of the confidence level (0: Not confident, 1: Somewhat confident, 2: Very confident).

    Raises:
        ValueError: If no known text is provided or if the response format is unexpected.
    """
    if not known_text:
        raise ValueError("No known text provided")

    CONFIDENCE_LEVELS = [
        "Not confident",
        "Somewhat confident",
        "Very confident",
    ]
    client = OpenAI(api_key=openai_api_key)
    full_prompt = prompt + f"Here is the first part: {known_text}"
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": full_prompt},
        ],
    )
    content = completion.choices[0].message.content
    try:
        confidence = content.split("~~")[1].strip(".")
    except IndexError:
        raise ValueError(
            f"Response format error. Expected token '~~'. Got: {content}")
    if confidence not in CONFIDENCE_LEVELS:
        raise ValueError(
            f"Unexpected confidence level: {confidence}. Expected one of: {CONFIDENCE_LEVELS}")
    return CONFIDENCE_LEVELS.index(confidence)


def predict_next_char(
    known_text: str, openai_api_key: str, banned_chars: List[str] = [], model: str = "gpt-4o-mini",
    role: str = "You are a professional CTF hacker.",
    prompt: str = (
        "You will receive the first part of a flag. Predict the next character with no extra text. "
        "Your answer must be exactly one character. Note that flags may include leet speak or underscores.\n"
    )
) -> str:
    """
    Predict the next flag character using OpenAI's API.

    Args:
        known_text (str): The known part of the flag.
        openai_api_key (str): API key for OpenAI.
        banned_chars (List[str]): Characters that should not be used in the prediction.
        model (str): Model to use for prediction.
        role (str): Role description for the AI.
        prompt (str): Prompt template for the AI.

    Returns:
        str: The predicted character.

    Raises:
        ValueError: If no known text is provided or if the AI's response is not a single character.
    """
    if not known_text:
        raise ValueError("No known text provided")

    client = OpenAI(api_key=openai_api_key)
    banned_instruction = f"Do not use these characters: {', '.join(banned_chars)}.\n" if banned_chars else ""
    known_instruction = f"Here is the first part: {known_text}"
    full_prompt = prompt + banned_instruction + known_instruction
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": full_prompt},
        ],
    )
    char = completion.choices[0].message.content
    if len(char) != 1:
        raise ValueError(
            "Expected a single character but the AI responded with more: " + char)
    return char
