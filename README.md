# Charset Generator

## Overview

This package is designed to make CTF char-by-char bruteforce simpler.

## Installation

    pip install charset-generator

## Documentation

Charsets can be generated from `string.printable` using `gen_charset`.

If `frequency_sorted` is `True`, then it will be ordered based on frequency,
with the most frequent characters appearing first.

```py
gen_charset(regex: str, frequency_sorted: bool = False) -> str:
```

Characters can be produced from a generator using `yielding.yield_charset`.

If `allow_interruptions` is `True`, then the user can press the `interrupt_key`,
to temporarily take over, allowing them to choose the next character. This is
useful for cases where the user can predict the next character faster than it
would take to bruteforce through the charset.

```py
yielding.yield_charset(regex: str, frequency_sorted: bool = False, allow_interruptions: bool = False, interrupt_key: str = "esc") -> Generator[str, None, None]:
```

`ai.assess_predictability` and `ai.predict_next_char` are both highly experimental.

Together, they allow you to use OpenAI to predict the next character of a flag,
given some prefix `known_text`.

Use these with caution.

```py
ai.assess_predictability(
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
) -> str
```

```py
ai.predict_next_char(
    known_text: str, openai_api_key: str, banned_chars: List[str] = [], model: str = "gpt-4o-mini",
    role: str = "You are a professional CTF hacker.",
    prompt: str = (
        "You will receive the first part of a flag. Predict the next character with no extra text. "
        "Your answer must be exactly one character. Note that flags may include leet speak or underscores.\n"
    )
) -> str
```
