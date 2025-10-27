# test_main.py

import json
import pytest
from unittest.mock import MagicMock, AsyncMock

import main

@pytest.fixture
def mock_aiomqtt_client(mocker):
    patch_target = 'main.Client'
    try:
        mock_client_class = mocker.patch(patch_target, autospec=True)
    except (AttributeError, ImportError):
        pytest.fail(f"Failed to patch '{patch_target}'. Check the import path in main.py.")

    mock_client_instance = AsyncMock(name="MockClientInstance")
    mock_client_instance.subscribe = AsyncMock(name="MockSubscribe")
    mock_client_instance.publish = AsyncMock(name="MockPublish")
    mock_client_instance.messages = AsyncMock(name="MockMessages")

    mock_client_class.return_value = mock_client_instance
    mock_client_instance.__aenter__.return_value = mock_client_instance
    mock_client_instance.__aexit__ = AsyncMock(return_value=None, name="MockAexit")

    return mock_client_instance

# --- Tests ---

@pytest.mark.asyncio
async def test_on_message_invalid_json(mocker, mock_aiomqtt_client, capsys):
    """Test on_message with invalid JSON payload."""
    mock_run_coro = mocker.patch('asyncio.run_coroutine_threadsafe')

    invalid_payload = b"this is not json"
    mock_message = MagicMock()
    mock_message.payload = invalid_payload
    mock_message.topic = main.FOOD_TOPIC

    main.on_message(mock_aiomqtt_client, mock_message)

    captured = capsys.readouterr()
    assert "Error processing message:" in captured.out
    mock_run_coro.assert_not_called()


@pytest.mark.asyncio
async def test_serve_food(mocker, mock_aiomqtt_client, capsys):
    """Test the serve_food coroutine directly."""
    mock_sleep = mocker.patch('asyncio.sleep', new_callable=AsyncMock)

    input_json = {"table": 3, "food": "Burger"}
    wait_time = 5

    await main.serve_food(mock_aiomqtt_client, input_json, wait_time)

    mock_sleep.assert_awaited_once_with(wait_time)
    captured = capsys.readouterr()
    assert "Serving table 3 with Burger" in captured.out

    mock_aiomqtt_client.publish.assert_awaited_once_with(
        main.SERVE_TOPIC, json.dumps(input_json)
    )