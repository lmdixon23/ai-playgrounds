#!/usr/bin/env python3
"""Independent numeric regression tests for Lab 13's toy Transformer model."""

from __future__ import annotations

import json
import math
import sys
import unittest

from transformer_language_model_reference import (
    B_OUT,
    D_MODEL,
    MAX_CONTEXT,
    TOKEN_TO_ID,
    VOCAB,
    W_K,
    W_Q,
    apply_causal_mask,
    attention_scores,
    attention_weights,
    dot,
    entropy,
    forward_text,
    forward_tokens,
    input_vectors,
    row_times_matrix,
    stable_softmax,
    toy_tokenize,
    weighted_value_sum,
)


class TransformerLanguageModelTests(unittest.TestCase):
    def assertVectorClose(self, actual, expected, places=9):
        self.assertEqual(len(actual), len(expected))
        for a, e in zip(actual, expected, strict=True):
            self.assertAlmostEqual(a, e, places=places)

    def test_01_toy_tokenizer_separates_period_and_adds_bos(self):
        self.assertEqual(toy_tokenize("I like cats."), ["<BOS>", "i", "like", "cats", "."])

    def test_02_unknown_word_maps_to_unk(self):
        self.assertEqual(toy_tokenize("I admire cats"), ["<BOS>", "i", "<UNK>", "cats"])

    def test_03_context_truncation_preserves_bos(self):
        tokens = toy_tokenize("i like cats because they sleep play run")
        self.assertEqual(len(tokens), MAX_CONTEXT)
        self.assertEqual(tokens[0], "<BOS>")
        self.assertEqual(tokens[-1], "run")

    def test_04_position_vector_addition_has_known_fixture(self):
        vectors = input_vectors(("<BOS>", "i", "like", "cats"), use_positions=True)
        self.assertVectorClose(vectors[3], (0.4, 0.45, 0.9, 0.15), places=12)

    def test_05_q_projection_known_fixture(self):
        x = (0.4, 0.45, 0.9, 0.15)
        q = row_times_matrix(x, W_Q)
        self.assertVectorClose(q, (0.41, 0.37, 0.81, 0.225), places=12)

    def test_06_scaled_dot_product_known_fixture(self):
        q = (0.41, 0.37, 0.81, 0.225)
        k = (0.14, 0.01, 0.11, 0.02)
        expected = dot(q, k) / math.sqrt(D_MODEL)
        self.assertAlmostEqual(expected, 0.07735, places=12)

    def test_07_causal_mask_blocks_future_positions(self):
        scores = ((1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0))
        masked = apply_causal_mask(scores, causal_mask=True)
        self.assertEqual(masked[0], (1.0, None, None))
        self.assertEqual(masked[1], (4.0, 5.0, None))
        self.assertEqual(masked[2], (7.0, 8.0, 9.0))

    def test_08_stable_softmax_handles_large_tied_logits(self):
        probs = stable_softmax((1000.0, 1000.0, 999.0))
        self.assertAlmostEqual(sum(probs), 1.0, places=12)
        self.assertAlmostEqual(probs[0], probs[1], places=12)
        self.assertGreater(probs[0], probs[2])

    def test_09_attention_rows_sum_to_one_over_permitted_positions(self):
        result = forward_tokens(("<BOS>", "i", "like", "cats"))
        for i, row in enumerate(result.attention):
            self.assertAlmostEqual(sum(row), 1.0, places=12)
            self.assertTrue(all(abs(row[j]) < 1e-15 for j in range(i + 1, len(row))))

    def test_10_last_attention_row_matches_frozen_fixture(self):
        result = forward_tokens(("<BOS>", "i", "like", "cats"))
        expected = (
            0.20366059441088602,
            0.24469312034003501,
            0.2459995865850857,
            0.3056466986639933,
        )
        self.assertVectorClose(result.attention[-1], expected, places=12)

    def test_11_weighted_value_sum_is_literal_weighted_sum(self):
        weights = (0.25, 0.75)
        values = ((1.0, 2.0, 3.0, 4.0), (5.0, 6.0, 7.0, 8.0))
        self.assertVectorClose(weighted_value_sum(weights, values), (4.0, 5.0, 6.0, 7.0))

    def test_12_canonical_next_token_distribution_is_frozen(self):
        result = forward_text("I like cats")
        expected_logits = (
            -0.18820115792796333,
            -0.06357983759394537,
            0.18904917963808346,
            0.5753151089210979,
            1.0823176214402253,
            1.069705398168754,
            1.0698767278828187,
            1.0626103463153176,
            0.6220051149272534,
            0.6871139509931347,
            0.7099471359012399,
            0.8935451226757799,
        )
        expected_probs = (
            0.033464674725788665,
            0.03790608741521372,
            0.04880050856596046,
            0.07180877359614943,
            0.11922460797170813,
            0.11773036327754678,
            0.11775053571504349,
            0.11689801650878605,
            0.07524102816875437,
            0.08030288158835429,
            0.08215754549690947,
            0.09871497696978519,
        )
        self.assertVectorClose(result.logits, expected_logits, places=12)
        self.assertVectorClose(result.probabilities, expected_probs, places=12)
        self.assertEqual(VOCAB[max(range(len(VOCAB)), key=result.probabilities.__getitem__)], "cats")

    def test_13_token_substitution_changes_distribution(self):
        cats = forward_tokens(("<BOS>", "i", "like", "cats"))
        dogs = forward_tokens(("<BOS>", "i", "like", "dogs"))
        max_delta = max(abs(a - b) for a, b in zip(cats.probabilities, dogs.probabilities, strict=True))
        self.assertGreater(max_delta, 0.01)

    def test_14_without_positions_prior_token_permutation_is_invariant_at_last_position(self):
        a = forward_tokens(("<BOS>", "i", "like", "cats"), use_positions=False)
        b = forward_tokens(("<BOS>", "like", "i", "cats"), use_positions=False)
        self.assertVectorClose(a.probabilities, b.probabilities, places=12)

    def test_15_with_positions_same_permutation_changes_distribution(self):
        a = forward_tokens(("<BOS>", "i", "like", "cats"), use_positions=True)
        b = forward_tokens(("<BOS>", "like", "i", "cats"), use_positions=True)
        max_delta = max(abs(x - y) for x, y in zip(a.probabilities, b.probabilities, strict=True))
        self.assertGreater(max_delta, 1e-5)

    def test_16_removing_causal_mask_leaks_future_tokens_into_earlier_attention(self):
        masked = forward_tokens(("<BOS>", "i", "like", "cats"), causal_mask=True)
        unmasked = forward_tokens(("<BOS>", "i", "like", "cats"), causal_mask=False)
        self.assertEqual(masked.attention[1][2:], (0.0, 0.0))
        self.assertGreater(unmasked.attention[1][2], 0.0)
        self.assertGreater(unmasked.attention[1][3], 0.0)

    def test_17_temperature_changes_entropy_without_changing_logits(self):
        base = forward_text("I like cats", temperature=1.0)
        cold = forward_text("I like cats", temperature=0.5)
        hot = forward_text("I like cats", temperature=2.0)
        self.assertEqual(base.logits, cold.logits)
        self.assertEqual(base.logits, hot.logits)
        self.assertLess(entropy(cold.probabilities), entropy(base.probabilities))
        self.assertLess(entropy(base.probabilities), entropy(hot.probabilities))

    def test_18_invalid_temperature_fails_closed(self):
        with self.assertRaises(ValueError):
            stable_softmax((1.0, 2.0), temperature=0.0)
        with self.assertRaises(ValueError):
            stable_softmax((1.0, 2.0), temperature=float("nan"))

    def test_19_forward_rejects_context_longer_than_frozen_limit(self):
        with self.assertRaises(ValueError):
            forward_tokens(("<BOS>", "i", "like", "cats", "because", "they", "sleep"))

    def test_20_vocabulary_and_bias_lengths_remain_aligned(self):
        self.assertEqual(len(VOCAB), len(B_OUT))
        self.assertEqual(TOKEN_TO_ID["<UNK>"], 1)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TransformerLanguageModelTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    payload = {
        "harness": "tools/test_transformer_language_model.py",
        "testsRun": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "pass": result.wasSuccessful(),
    }
    print(json.dumps(payload, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
