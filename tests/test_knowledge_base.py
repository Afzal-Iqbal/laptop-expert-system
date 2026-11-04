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


def test_leaf_certainty_factors_and_determinism(kb_data):
    """Verify that all leaf diagnoses specify valid certainty factors and determinism flags."""
    nodes = kb_data["nodes"]
    leaf_count = 0
    for node_id, node in nodes.items():
        for opt in node["options"]:
            leaf = opt.get("leaf_diagnosis")
            if leaf:
                leaf_count += 1
                assert "certainty_factor" in leaf, f"Node {node_id}:{opt['key']} missing certainty_factor"
                cf = leaf["certainty_factor"]
                assert isinstance(cf, (int, float)), f"Certainty factor must be numeric in {node_id}:{opt['key']}"
                assert 0.0 <= cf <= 1.0, f"Certainty factor {cf} out of range in {node_id}:{opt['key']}"
                assert "is_deterministic" in leaf, f"Node {node_id}:{opt['key']} missing is_deterministic"
                assert isinstance(leaf["is_deterministic"], bool)

    assert leaf_count == 41, f"Expected 41 leaf diagnoses, found {leaf_count}"


def test_boundary_rules_metadata(kb_data):
    """Verify presence and validity of domain boundary rules in metadata."""
    meta = kb_data["metadata"]
    assert "boundary_rules" in meta
    bounds = meta["boundary_rules"]
    assert "domain" in bounds
    assert "certainty_threshold" in bounds
    assert 0.0 < bounds["certainty_threshold"] < 1.0
    assert "out_of_scope_conditions" in bounds
    assert isinstance(bounds["out_of_scope_conditions"], list)
    assert len(bounds["out_of_scope_conditions"]) > 0
    assert "limitation_statement" in bounds


def test_competing_hypotheses_structure(kb_data):
    """Verify that conditional leaves with competing hypotheses have well-formed alternatives."""
    nodes = kb_data["nodes"]
    hypotheses_count = 0
    for node_id, node in nodes.items():
        for opt in node["options"]:
            leaf = opt.get("leaf_diagnosis")
            if leaf and "competing_hypotheses" in leaf:
                hyp_list = leaf["competing_hypotheses"]
                assert isinstance(hyp_list, list)
                for hyp in hyp_list:
                    hypotheses_count += 1
                    assert "title" in hyp
                    assert "confidence" in hyp
                    assert 0.0 <= hyp["confidence"] <= 1.0
                    assert "differentiator" in hyp

    assert hypotheses_count > 10, "Should have competing hypotheses defined across ambiguous leaves"


def test_zero_cross_subsystem_linkage(kb_data):
    """Verify that no diagnostic question leaks into an unrelated foreign subsystem."""
    nodes = kb_data["nodes"]
    for nid, node in nodes.items():
        if nid == "q_emergency_triage":
            continue
        src_cat = node.get("category")
        for opt in node["options"]:
            nxt = opt.get("next_question")
            if nxt and nxt in nodes:
                tgt_cat = nodes[nxt].get("category")
                assert src_cat == tgt_cat, f"Cross-subsystem leak: {nid} ({src_cat}) -> {nxt} ({tgt_cat})"


def test_clinical_tests_schema(kb_data):
    """Verify that nodes with clinical desk tests have valid structured instructions."""
    nodes = kb_data["nodes"]
    nodes_with_tests = [n for n in nodes.values() if "clinical_test" in n]
    assert len(nodes_with_tests) >= 10, "Expected at least 10 physical clinical desk tests"

    for node in nodes_with_tests:
        test_info = node["clinical_test"]
        assert "test_name" in test_info and isinstance(test_info["test_name"], str)
        assert "instructions" in test_info and isinstance(test_info["instructions"], list)
        assert len(test_info["instructions"]) >= 1
        assert "expected_observation" in test_info and isinstance(test_info["expected_observation"], str)


def test_leaf_doctor_protocols(kb_data):
    """Verify that diagnostic leaves have is_common, prognosis, and prescription fields."""
    nodes = kb_data["nodes"]
    for node_id, node in nodes.items():
        for opt in node["options"]:
            leaf = opt.get("leaf_diagnosis")
            if leaf:
                assert "is_common" in leaf, f"Node {node_id}:{opt['key']} missing is_common"
                assert isinstance(leaf["is_common"], bool)
                assert "prognosis" in leaf, f"Node {node_id}:{opt['key']} missing prognosis"
                assert isinstance(leaf["prognosis"], str)
                assert len(leaf["prognosis"]) > 0
                assert "prescription" in leaf, f"Node {node_id}:{opt['key']} missing prescription"
                assert isinstance(leaf["prescription"], list)
                assert len(leaf["prescription"]) > 0



