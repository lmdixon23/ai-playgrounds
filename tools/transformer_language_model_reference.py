#!/usr/bin/env python3
"""Deterministic reference model for Lab 13: Transformer Language Modeling.

This is intentionally a hand-sized decoder-like block, not a pretrained or frontier
language model.  It uses only the Python standard library so its arithmetic can be
replayed independently of the browser applet.

Pipeline:
    toy tokenization
      -> token embedding + optional position vector
      -> one scaled-dot-product causal self-attention head
      -> residual connection
      -> small ReLU feed-forward network + residual connection
      -> output projection
      -> next-token softmax / temperature

The fixed weights are pedagogical fixtures.  They are not learned parameters copied
from GPT, Claude, Gemini, or any other deployed model.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable, Sequence

D_MODEL = 4
MAX_CONTEXT = 6

VOCAB = (
    "<BOS>",
    "<UNK>",
    "i",
    "like",
    "cats",
    "dogs",
    "sleep",
    "play",
    ".",
    "because",
    "they",
    "run",
)
TOKEN_TO_ID = {token: index for index, token in enumerate(VOCAB)}

# Small fixed vectors chosen for readable arithmetic and non-degenerate scenarios.
TOKEN_EMBEDDINGS = {
    "<BOS>": (0.20, 0.00, 0.10, 0.00),
    "<UNK>": (0.00, 0.10, 0.00, 0.10),
    "i": (0.80, 0.10, 0.00, 0.20),
    "like": (0.20, 0.90, 0.10, 0.00),
    "cats": (0.10, 0.40, 0.90, 0.20),
    "dogs": (0.10, 0.50, 0.70, 0.50),
    "sleep": (0.00, 0.20, 0.80, 0.90),
    "play": (0.20, 0.30, 0.70, 0.80),
    ".": (0.00, 0.10, 0.20, 0.90),
    "because": (0.30, 0.70, 0.20, 0.10),
    "they": (0.70, 0.20, 0.10, 0.40),
    "run": (0.10, 0.20, 0.60, 0.80),
}

POSITION_VECTORS = (
    (0.00, 0.00, 0.00, 0.00),
    (0.10, -0.05, 0.05, 0.00),
    (0.20, 0.00, -0.05, 0.05),
    (0.30, 0.05, 0.00, -0.05),
    (0.40, 0.00, 0.05, 0.00),
    (0.50, -0.05, 0.00, 0.05),
)

W_Q = (
    (0.80, 0.10, 0.00, 0.00),
    (0.00, 0.70, 0.20, 0.00),
    (0.10, 0.00, 0.80, 0.10),
    (0.00, 0.10, 0.00, 0.90),
)
W_K = (
    (0.70, 0.00, 0.20, 0.00),
    (0.10, 0.80, 0.00, 0.00),
    (0.00, 0.10, 0.70, 0.20),
    (0.00, 0.00, 0.20, 0.80),
)
W_V = (
    (0.90, 0.00, 0.00, 0.10),
    (0.00, 0.80, 0.10, 0.00),
    (0.10, 0.00, 0.90, 0.00),
    (0.00, 0.10, 0.00, 0.90),
)

# One four-unit hidden layer.  ReLU makes the block nonlinear without making the
# fixture too large to inspect.
W_FF1 = (
    (0.60, -0.20, 0.10, 0.00),
    (0.10, 0.70, -0.10, 0.20),
    (-0.20, 0.10, 0.60, 0.30),
    (0.00, 0.20, 0.10, 0.70),
)
B_FF1 = (0.00, 0.05, 0.00, -0.05)
W_FF2 = (
    (0.50, 0.10, 0.00, 0.00),
    (0.00, 0.50, 0.10, 0.00),
    (0.10, 0.00, 0.50, 0.10),
    (0.00, 0.10, 0.00, 0.50),
)
B_FF2 = (0.00, 0.00, 0.00, 0.00)

# Output columns correspond to VOCAB.  The weights are deliberately small; the
# purpose is to expose how contextual representation changes logits, not to produce
# realistic prose.
W_OUT = (
    (0.10, 0.00, 0.20, 0.10, 0.10, 0.10, 0.00, 0.10, 0.00, 0.20, 0.30, 0.10),
    (0.00, 0.10, 0.10, 0.30, 0.20, 0.20, 0.10, 0.10, 0.00, 0.30, 0.10, 0.10),
    (0.00, 0.00, 0.00, 0.10, 0.40, 0.35, 0.35, 0.30, 0.10, 0.10, 0.10, 0.25),
    (0.00, 0.10, 0.00, 0.00, 0.10, 0.20, 0.45, 0.40, 0.50, 0.00, 0.20, 0.35),
)
B_OUT = (-0.30, -0.25, -0.15, -0.05, 0.00, 0.00, 0.05, 0.05, 0.10, -0.05, -0.05, 0.00)

TOKEN_PATTERN = re.compile(r"[A-Za-z]+|[.]", re.UNICODE)


@dataclass(frozen=True)
class ForwardResult:
    tokens: tuple[str, ...]
    token_ids: tuple[int, ...]
    inputs: tuple[tuple[float, ...], ...]
    queries: tuple[tuple[float, ...], ...]
    keys: tuple[tuple[float, ...], ...]
    values: tuple[tuple[float, ...], ...]
    raw_scores: tuple[tuple[float, ...], ...]
    masked_scores: tuple[tuple[float | None, ...], ...]
    attention: tuple[tuple[float, ...], ...]
    attention_outputs: tuple[tuple[float, ...], ...]
    residual1: tuple[tuple[float, ...], ...]
    feed_forward: tuple[tuple[float, ...], ...]
    final_states: tuple[tuple[float, ...], ...]
    logits: tuple[float, ...]
    probabilities: tuple[float, ...]
    temperature: float
    causal_mask: bool
    use_positions: bool


def toy_tokenize(text: str, add_bos: bool = True) -> list[str]:
    tokens = [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]
    normalized = [token if token in TOKEN_TO_ID else "<UNK>" for token in tokens]
    if add_bos:
        normalized.insert(0, "<BOS>")
    if not normalized:
        normalized = ["<BOS>"] if add_bos else []
    if len(normalized) > MAX_CONTEXT:
        normalized = normalized[-MAX_CONTEXT:]
        if add_bos and normalized[0] != "<BOS>":
            # The toy model keeps the beginning marker when truncation is needed.
            normalized = ["<BOS>"] + normalized[-(MAX_CONTEXT - 1):]
    return normalized


def ids_for(tokens: Sequence[str]) -> list[int]:
    return [TOKEN_TO_ID.get(token, TOKEN_TO_ID["<UNK>"]) for token in tokens]


def vec_add(a: Sequence[float], b: Sequence[float]) -> tuple[float, ...]:
    return tuple(x + y for x, y in zip(a, b, strict=True))


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def row_times_matrix(row: Sequence[float], matrix: Sequence[Sequence[float]]) -> tuple[float, ...]:
    if not matrix:
        return ()
    width = len(matrix[0])
    if len(row) != len(matrix):
        raise ValueError("row/matrix dimension mismatch")
    if any(len(r) != width for r in matrix):
        raise ValueError("ragged matrix")
    return tuple(sum(row[i] * matrix[i][j] for i in range(len(row))) for j in range(width))


def stable_softmax(values: Sequence[float], temperature: float = 1.0) -> tuple[float, ...]:
    if temperature <= 0 or not math.isfinite(temperature):
        raise ValueError("temperature must be finite and > 0")
    if not values:
        return ()
    scaled = [value / temperature for value in values]
    peak = max(scaled)
    exps = [math.exp(value - peak) for value in scaled]
    denom = sum(exps)
    return tuple(value / denom for value in exps)


def entropy(probabilities: Sequence[float]) -> float:
    return -sum(p * math.log(p) for p in probabilities if p > 0)


def input_vectors(tokens: Sequence[str], use_positions: bool = True) -> tuple[tuple[float, ...], ...]:
    if len(tokens) > MAX_CONTEXT:
        raise ValueError("context exceeds MAX_CONTEXT")
    out: list[tuple[float, ...]] = []
    for index, token in enumerate(tokens):
        embedding = TOKEN_EMBEDDINGS.get(token, TOKEN_EMBEDDINGS["<UNK>"])
        position = POSITION_VECTORS[index] if use_positions else (0.0,) * D_MODEL
        out.append(vec_add(embedding, position))
    return tuple(out)


def project_rows(rows: Sequence[Sequence[float]], matrix: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    return tuple(row_times_matrix(row, matrix) for row in rows)


def attention_scores(
    queries: Sequence[Sequence[float]],
    keys: Sequence[Sequence[float]],
) -> tuple[tuple[float, ...], ...]:
    scale = math.sqrt(len(queries[0])) if queries else 1.0
    return tuple(tuple(dot(q, k) / scale for k in keys) for q in queries)


def apply_causal_mask(
    scores: Sequence[Sequence[float]],
    causal_mask: bool = True,
) -> tuple[tuple[float | None, ...], ...]:
    masked: list[tuple[float | None, ...]] = []
    for i, row in enumerate(scores):
        masked.append(tuple(None if causal_mask and j > i else value for j, value in enumerate(row)))
    return tuple(masked)


def attention_weights(masked_scores: Sequence[Sequence[float | None]]) -> tuple[tuple[float, ...], ...]:
    rows: list[tuple[float, ...]] = []
    for row in masked_scores:
        permitted = [value for value in row if value is not None]
        probs = iter(stable_softmax(permitted))
        rows.append(tuple(0.0 if value is None else next(probs) for value in row))
    return tuple(rows)


def weighted_value_sum(weights: Sequence[float], values: Sequence[Sequence[float]]) -> tuple[float, ...]:
    if len(weights) != len(values):
        raise ValueError("weights/value count mismatch")
    if not values:
        return ()
    width = len(values[0])
    return tuple(sum(weights[i] * values[i][j] for i in range(len(values))) for j in range(width))


def feed_forward(state: Sequence[float]) -> tuple[float, ...]:
    hidden_pre = vec_add(row_times_matrix(state, W_FF1), B_FF1)
    hidden = tuple(max(0.0, value) for value in hidden_pre)
    return vec_add(row_times_matrix(hidden, W_FF2), B_FF2)


def logits_from_state(state: Sequence[float]) -> tuple[float, ...]:
    return vec_add(row_times_matrix(state, W_OUT), B_OUT)


def forward_tokens(
    tokens: Sequence[str],
    *,
    use_positions: bool = True,
    causal_mask: bool = True,
    temperature: float = 1.0,
) -> ForwardResult:
    normalized = tuple(token if token in TOKEN_TO_ID else "<UNK>" for token in tokens)
    if not normalized:
        raise ValueError("at least one token is required")
    if len(normalized) > MAX_CONTEXT:
        raise ValueError("context exceeds MAX_CONTEXT")

    inputs = input_vectors(normalized, use_positions=use_positions)
    queries = project_rows(inputs, W_Q)
    keys = project_rows(inputs, W_K)
    values = project_rows(inputs, W_V)
    scores = attention_scores(queries, keys)
    masked = apply_causal_mask(scores, causal_mask=causal_mask)
    weights = attention_weights(masked)
    attn_out = tuple(weighted_value_sum(row, values) for row in weights)
    residual1 = tuple(vec_add(x, a) for x, a in zip(inputs, attn_out, strict=True))
    ff = tuple(feed_forward(state) for state in residual1)
    final_states = tuple(vec_add(state, delta) for state, delta in zip(residual1, ff, strict=True))
    logits = logits_from_state(final_states[-1])
    probabilities = stable_softmax(logits, temperature=temperature)

    return ForwardResult(
        tokens=normalized,
        token_ids=tuple(ids_for(normalized)),
        inputs=inputs,
        queries=queries,
        keys=keys,
        values=values,
        raw_scores=scores,
        masked_scores=masked,
        attention=weights,
        attention_outputs=attn_out,
        residual1=residual1,
        feed_forward=ff,
        final_states=final_states,
        logits=logits,
        probabilities=probabilities,
        temperature=temperature,
        causal_mask=causal_mask,
        use_positions=use_positions,
    )


def forward_text(
    text: str,
    *,
    use_positions: bool = True,
    causal_mask: bool = True,
    temperature: float = 1.0,
) -> ForwardResult:
    return forward_tokens(
        toy_tokenize(text),
        use_positions=use_positions,
        causal_mask=causal_mask,
        temperature=temperature,
    )


def top_tokens(result: ForwardResult, n: int = 5) -> list[tuple[str, float]]:
    pairs = list(zip(VOCAB, result.probabilities, strict=True))
    pairs.sort(key=lambda pair: (-pair[1], pair[0]))
    return pairs[:n]


def format_vector(values: Iterable[float], digits: int = 4) -> str:
    return "[" + ", ".join(f"{value:.{digits}f}" for value in values) + "]"


if __name__ == "__main__":
    result = forward_text("I like cats")
    print("tokens:", result.tokens)
    print("last attention:", format_vector(result.attention[-1]))
    print("top next tokens:")
    for token, probability in top_tokens(result):
        print(f"  {token:>8}: {probability:.6f}")
