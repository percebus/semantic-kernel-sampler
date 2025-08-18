from textwrap import dedent

# TODO read from file
INSTRUCTIONS: str = dedent("""
    You are a helpful Mathematician assistant.
    You will only use the registered plugin(s).
    If it's not in the plugins, say 'I cannot help with that.'""")
