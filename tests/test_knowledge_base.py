import json
import os
import pytest

KB_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge_base.json")

@pytest.fixture(scope="module")
def kb_data():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_kb_json_structure(kb_data):
    assert "metadata" in kb_data
    assert "nodes" in kb_data
    assert "emergency_entry_node" in kb_data
    assert kb_data["emergency_entry_node"] in kb_data["nodes"]

def test_kb_has_above_50_questions(kb_data):
    nodes = kb_data["nodes"]
    diagnostic_questions = [k for k in nodes.keys() if k != "q_emergency_triage"]
    assert len(diagnostic_questions) >= 50, f"Expected >= 50 questions, found {len(diagnostic_questions)}"

def test_node_schema_integrity(kb_data):
    nodes = kb_data["nodes"]
    required_node_keys = {"id", "category", "title", "question", "why", "options"}
    valid_categories = set(kb_data["metadata"]["categories"].keys()) | {"triage"}

    for node_id, node in nodes.items():
        assert required_node_keys.issubset(node.keys()), f"Node {node_id} is missing required keys"
        assert node["category"] in valid_categories, f"Node {node_id} has invalid category {node['category']}"
        assert isinstance(node["options"], list)
        assert len(node["options"]) >= 2, f"Node {node_id} must have at least 2 options"

        for opt in node["options"]:
            assert "key" in opt
            assert "label" in opt
            assert "is_healthy" in opt
            
            # Next question check
            next_q = opt.get("next_question")
            if next_q:
                assert next_q in nodes, f"Node {node_id} references non-existent next_question '{next_q}'"
                assert next_q != node_id, f"Node {node_id} has self-referential loop"

            # Leaf diagnosis check
            leaf = opt.get("leaf_diagnosis")
            if leaf:
                assert "title" in leaf
                assert "issue" in leaf
                assert "remediation" in leaf
                assert isinstance(leaf["remediation"], list)
                assert len(leaf["remediation"]) > 0

def test_dag_path_reachability(kb_data):
    """Verify that from emergency_entry_node, paths lead to either next questions or leaf diagnoses."""
    nodes = kb_data["nodes"]
    entry = kb_data["emergency_entry_node"]
    
    # Simple BFS traversal check to ensure valid graph connectivity
    visited = set()
    queue = [entry]

    while queue:
        curr = queue.pop(0)
        visited.add(curr)
        for opt in nodes[curr]["options"]:
            nxt = opt.get("next_question")
            if nxt and nxt not in visited and nxt not in queue:
                queue.append(nxt)

    assert len(visited) > 10, "Emergency traversal tree should reach multiple branches"

def test_subsystem_pipeline_metadata(kb_data):
    meta = kb_data["metadata"]
    assert "subsystem_pipeline" in meta
    assert "subsystem_gateways" in meta
    pipeline = meta["subsystem_pipeline"]
    gateways = meta["subsystem_gateways"]
    assert len(pipeline) == 7
    nodes = kb_data["nodes"]
    for cat in pipeline:
        assert cat in gateways, f"Missing gateway for category {cat}"
        gw_node_id = gateways[cat]
        assert gw_node_id in nodes, f"Gateway node {gw_node_id} not found in nodes"

