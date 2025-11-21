"""LangGraph workflow definition."""

from langgraph.graph import StateGraph, END
from agents import State, InputHandler, Predictor, ResultEvaluator, OutputHandler


def create_workflow(ground_truth_df):
    """Create the LangGraph workflow."""
    
    # Initialize agents
    input_handler = InputHandler()
    predictor = Predictor()
    evaluator = ResultEvaluator(ground_truth_df)
    output_handler = OutputHandler()
    
    # Create graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("input_handler", input_handler.process)
    workflow.add_node("processor", predictor.process)
    workflow.add_node("evaluator", evaluator.process)
    workflow.add_node("output_handler", output_handler.process)
    
    # Define edges
    workflow.set_entry_point("input_handler")
    workflow.add_edge("input_handler", "processor")
    workflow.add_edge("processor", "evaluator")
    workflow.add_edge("evaluator", "output_handler")
    workflow.add_edge("output_handler", END)
    
    return workflow.compile()
