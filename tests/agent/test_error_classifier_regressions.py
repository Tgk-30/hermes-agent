from agent.error_classifier import FailoverReason, _classify_400


def _result(reason, **kwargs):
    return {"reason": reason, **kwargs}


def test_classify_400_handles_missing_context_length_without_crashing():
    result = _classify_400(
        "bad request",
        "",
        {"message": "bad request"},
        provider="openai",
        model="gpt-test",
        approx_tokens=1024,
        context_length=None,
        num_messages=3,
        result_fn=_result,
    )

    assert result["reason"] == FailoverReason.format_error
    assert result["retryable"] is False


def test_classify_400_zero_context_length_does_not_force_overflow():
    result = _classify_400(
        "error",
        "",
        {"message": "error"},
        provider="openai",
        model="gpt-test",
        approx_tokens=32,
        context_length=0,
        num_messages=1,
        result_fn=_result,
    )

    assert result["reason"] == FailoverReason.format_error
