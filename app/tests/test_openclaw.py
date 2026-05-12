from app.openclaw_adapter import OpenClawAdapter


def test_openclaw_interpret_command_pause():
    adapter = OpenClawAdapter()
    result = adapter.interpret_command('/pause')
    assert result['action'] == 'pause'


def test_openclaw_summarize_listing():
    adapter = OpenClawAdapter()
    summary = adapter.summarize_listing({'title': 'Piso', 'price': 100000, 'location': 'Valencia', 'surface': 70})
    assert 'Valencia' in summary
