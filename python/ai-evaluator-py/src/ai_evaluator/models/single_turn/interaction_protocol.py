from ai_evaluator.models.single_turn.ground_truth_entry_protocol import GroundTruthEntryProtocol


class InteractionProtocol(GroundTruthEntryProtocol):
    response: str
