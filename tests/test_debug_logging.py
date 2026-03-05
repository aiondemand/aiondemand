import logging

import pytest
import responses

import aiod
from aiod.calls.urls import server_url
from aiod.configuration import config


@responses.activate
def test_no_logging_by_default(caplog):
    """Debug logging should be silent when debug_http is False (default)."""
    responses.get(
        f"{server_url()}datasets?offset=0&limit=10",
        json=[],
        status=200,
    )
    with caplog.at_level(logging.DEBUG, logger="aiod.calls.calls"):
        aiod.datasets.get_list()
    assert caplog.records == []


@responses.activate
def test_debug_logging_emits(caplog):
    """When debug_http is True, each request should produce a DEBUG log."""
    responses.get(
        f"{server_url()}datasets?offset=0&limit=10",
        json=[],
        status=200,
    )
    config.debug_http = True
    try:
        with caplog.at_level(logging.DEBUG, logger="aiod.calls.calls"):
            aiod.datasets.get_list()
        assert len(caplog.records) == 1
        msg = caplog.records[0].message
        assert "GET" in msg
        assert "200" in msg
        assert "ms" in msg
    finally:
        config.debug_http = False


@responses.activate
def test_debug_logging_includes_url(caplog):
    """The log message should contain the request URL."""
    url = f"{server_url()}datasets?offset=0&limit=10"
    responses.get(url, json=[], status=200)
    config.debug_http = True
    try:
        with caplog.at_level(logging.DEBUG, logger="aiod.calls.calls"):
            aiod.datasets.get_list()
        assert "datasets" in caplog.records[0].message
    finally:
        config.debug_http = False


@responses.activate
def test_no_sensitive_data_logged(caplog, valid_refresh_token):
    """Authorization headers and tokens must never appear in log output."""
    responses.post(
        f"http://not.set/not_set/datasets",
        json={"identifier": "data_abc"},
    )
    config.debug_http = True
    try:
        with caplog.at_level(logging.DEBUG, logger="aiod.calls.calls"):
            aiod.datasets.register(metadata=dict(name="Foo"))
        for record in caplog.records:
            assert "Bearer" not in record.message
            assert "valid_access" not in record.message
            assert "Authorization" not in record.message
    finally:
        config.debug_http = False


@responses.activate
def test_debug_logging_post_method(caplog, valid_refresh_token):
    """POST requests should log the correct HTTP method."""
    responses.post(
        f"http://not.set/not_set/datasets",
        json={"identifier": "data_abc"},
    )
    config.debug_http = True
    try:
        with caplog.at_level(logging.DEBUG, logger="aiod.calls.calls"):
            aiod.datasets.register(metadata=dict(name="Foo"))
        assert "POST" in caplog.records[0].message
    finally:
        config.debug_http = False


@responses.activate
def test_debug_logging_delete_method(caplog, valid_refresh_token):
    """DELETE requests should log the correct HTTP method."""
    responses.delete(
        f"http://not.set/not_set/datasets/1",
    )
    config.debug_http = True
    try:
        with caplog.at_level(logging.DEBUG, logger="aiod.calls.calls"):
            aiod.datasets.delete(identifier=1)
        assert "DELETE" in caplog.records[0].message
        assert "200" in caplog.records[0].message
    finally:
        config.debug_http = False
