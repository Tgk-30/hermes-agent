from unittest.mock import patch


def test_kill_port_process_logs_failures(caplog):
    from gateway.platforms.whatsapp import _kill_port_process

    with patch("gateway.platforms.whatsapp.subprocess.run", side_effect=OSError("boom")):
        with caplog.at_level("WARNING"):
            _kill_port_process(3000)

    assert any("port 3000" in record.message for record in caplog.records)
