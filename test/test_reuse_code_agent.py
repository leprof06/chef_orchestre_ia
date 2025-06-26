import base64
from unittest import mock

import pytest

from agents.reuse_code_agent import ReuseCodeAgent
from orchestrator import orchestrate_workflow
from agents.code_agent import CodeAgent


@mock.patch('agents.reuse_code_agent.requests.get')
def test_handle_task_returns_code(mock_get):
    search_resp = mock.Mock()
    search_resp.status_code = 200
    search_resp.json.return_value = {
        "total_count": 1,
        "items": [{"url": "https://api.github.com/repos/x/y/contents/file.py"}]
    }
    file_resp = mock.Mock()
    file_resp.status_code = 200
    encoded = base64.b64encode(b"print('hello')").decode('utf-8')
    file_resp.json.return_value = {"content": encoded}
    mock_get.side_effect = [search_resp, file_resp]

    agent = ReuseCodeAgent()
    assert agent.handle_task('query') == "print('hello')"


@mock.patch('agents.reuse_code_agent.requests.get')
def test_handle_task_returns_none_when_no_results(mock_get):
    search_resp = mock.Mock()
    search_resp.status_code = 200
    search_resp.json.return_value = {"total_count": 0, "items": []}
    mock_get.return_value = search_resp

    agent = ReuseCodeAgent()
    assert agent.handle_task('query') is None


def test_orchestrator_calls_reuse_before_code():
    calls = []

    reuse = mock.Mock(spec=ReuseCodeAgent)
    code_agent = mock.Mock(spec=CodeAgent)

    def reuse_side_effect(query):
        calls.append('reuse')
        return 'code'

    def code_side_effect(code):
        calls.append('code')

    reuse.handle_task.side_effect = reuse_side_effect
    code_agent.handle_task.side_effect = code_side_effect

    orchestrate_workflow('q', reuse_agent=reuse, code_agent=code_agent)

    assert calls == ['reuse', 'code']
