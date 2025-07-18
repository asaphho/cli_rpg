from engine.contexts.context import Context


class DialogueContext(Context):
    def __init__(self, parent_context: Context, context_data: dict):
        super().__init__(parent_context=parent_context,
                         context_type='dialogue',
                         context_data=context_data)

