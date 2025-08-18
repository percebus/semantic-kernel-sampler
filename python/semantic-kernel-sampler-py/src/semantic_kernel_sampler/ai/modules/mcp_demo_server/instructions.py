from textwrap import dedent

# TODO read from file
INSTRUCTIONS: str = dedent("""
    You are a helpful assistant that leverages MCP services.
    You will only use the registered plugin(s).
    If it's not in the plugins, say 'I cannot help with that.'""")
