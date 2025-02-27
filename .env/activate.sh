
if [ -e .venv/bin/activate ]; then
    source .venv/bin/activate
else
    python3 -m venv .venv
    source .venv/bin/activate
    uv pip install pip -U
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv pip install -e .
    uv lock
fi
