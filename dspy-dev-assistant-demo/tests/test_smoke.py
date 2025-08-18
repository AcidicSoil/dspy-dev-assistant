def test_smoke_import():
    import importlib
    cli = importlib.import_module("dspy_dev.cli")
    assert hasattr(cli, "app")
