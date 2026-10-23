import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))

from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement
from utils import (
    generate_id_from_pointer,
    extract_name_parts,
    get_individual_relative_path,
)
from data_extraction import get_name
from html_generation import (
    ANCESTOR_SLOTS,
    compute_ancestor_layout,
    generate_ancestors_section,
)


def get_all_valid_ancestor_combinations():
    """Return all 675 valid connected ancestor path combinations across 3 generations."""
    all_slots = [s['path'] for s in ANCESTOR_SLOTS]
    valid_trees = []
    for mask in range(1, 1 << len(all_slots)):
        chosen = {all_slots[i] for i in range(len(all_slots)) if mask & (1 << i)}
        # Every present node at depth > 1 must have its parent present
        if all(len(p) == 1 or p[:-1] in chosen for p in chosen):
            valid_trees.append(chosen)
    return valid_trees


def test_only_parents_1_generation_compact():
    """When only father and mother are present, height and spacing should be compact."""
    tops, width, height = compute_ancestor_layout([('father',), ('mother',)])
    assert width == 620
    assert height < 280  # Previously 1200px!
    assert tops[('father',)] < tops[()] < tops[('mother',)]
    # Root individual is centered midway between father and mother
    assert tops[()] == (tops[('father',)] + tops[('mother',)]) // 2


def test_single_parent_only_father_or_mother():
    """When only one parent is known, layout is compact and properly ordered."""
    tops_f, width_f, height_f = compute_ancestor_layout([('father',)])
    assert width_f == 620
    assert height_f < 220
    assert tops_f[('father',)] < tops_f[()]

    tops_m, width_m, height_m = compute_ancestor_layout([('mother',)])
    assert width_m == 620
    assert height_m < 220
    assert tops_m[()] < tops_m[('mother',)]


def test_asymmetric_branches_paternal_vs_maternal():
    """When one side has grandparents/great-grandparents and the other side only has a parent."""
    # Paternal grandparents present, maternal grandparents missing
    paternal_2gen = [('father',), ('father', 'father'), ('father', 'mother'), ('mother',)]
    tops, width, height = compute_ancestor_layout(paternal_2gen)
    assert width == 930
    assert height < 400
    # Father centered between paternal grandfather and paternal grandmother
    assert tops[('father',)] == (tops[('father', 'father')] + tops[('father', 'mother')]) // 2
    # Self centered between father and mother
    assert tops[()] == (tops[('father',)] + tops[('mother',)]) // 2

    # Full paternal 3-gen, only mother on maternal side
    paternal_3gen = [
        ('father',), ('father', 'father'), ('father', 'father', 'father'), ('father', 'father', 'mother'),
        ('father', 'mother'), ('father', 'mother', 'father'), ('father', 'mother', 'mother'),
        ('mother',),
    ]
    tops3, width3, height3 = compute_ancestor_layout(paternal_3gen)
    assert width3 == 1234
    assert height3 < 650  # Roughly half of the full 3-gen height


def test_maternal_only_lineage_connectors():
    """Verify that when a node only has a mother (no father), outgoing connector lines are still rendered."""
    ged_content = """0 HEAD
1 SOUR Test
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
0 @I1@ INDI
1 NAME Child /One/
2 GIVN Child
2 SURN One
1 SEX M
1 FAMC @F1@
0 @I2@ INDI
1 NAME Mother /One/
2 GIVN Mother
2 SURN One
1 SEX F
1 FAMC @F2@
1 FAMS @F1@
0 @I3@ INDI
1 NAME Grandma /One/
2 GIVN Grandma
2 SURN One
1 SEX F
1 FAMS @F2@
0 @F1@ FAM
1 WIFE @I2@
1 CHIL @I1@
0 @F2@ FAM
1 WIFE @I3@
1 CHIL @I2@
0 TRLR
"""
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".ged", delete=False, encoding="utf-8") as f:
        f.write(ged_content)
        tmp_ged = f.name

    try:
        parser = Parser()
        parser.parse_file(tmp_ged)
        individuals_data = {}
        child_elem = None
        for elem in parser.get_root_child_elements():
            if isinstance(elem, IndividualElement):
                ind_id = generate_id_from_pointer(elem.get_pointer())
                name = get_name(elem)
                s, g = extract_name_parts(name)
                individuals_data[ind_id] = {'name': name, 'path': get_individual_relative_path(s, g, ind_id)}
                if elem.get_pointer() == "@I1@":
                    child_elem = elem
                    child_id = ind_id

        html = generate_ancestors_section(parser, child_elem, child_id, individuals_data)
        # Outgoing inline connectors at left: 285px (from Self to Mother) and left: 595px (from Mother to Grandma)
        assert 'left: 285px; width: 15px' in html
        assert 'left: 595px; width: 15px' in html
    finally:
        os.remove(tmp_ged)


def test_all_675_valid_combinations_invariants():
    """
    Exhaustively test all 675 valid connected ancestor tree combinations across 3 generations:
    1. No vertical overlap within any column (minimum 120px center-to-center / 40px gap between 80px boxes).
    2. Strict vertical ordering: for every parent-child pair, father_top < child_top < mother_top.
    3. Exact centering: whenever both father and mother are present for any node, node_top == midpoint(father_top, mother_top).
    4. Positive coordinates: all box tops >= 5px and within container_height.
    """
    valid_trees = get_all_valid_ancestor_combinations()
    assert len(valid_trees) == 675

    for tree in valid_trees:
        tops, width, height = compute_ancestor_layout(tree)

        # 1. Check bounds
        for path, top in tops.items():
            assert top >= 5, f"Box {path} top {top} < 5"
            assert top + 80 <= height, f"Box {path} bottom {top + 80} exceeds container height {height}"

        # 2. Check no column overlaps (boxes in same column must be >= 120px apart)
        for col in range(4):
            col_paths = sorted([p for p in tops if len(p) == col])
            for i in range(len(col_paths) - 1):
                p1, p2 = col_paths[i], col_paths[i + 1]
                assert tops[p2] - tops[p1] >= 120, (
                    f"Overlap/tight spacing in col {col} between {p1} ({tops[p1]}) and {p2} ({tops[p2]})"
                )

        # 3. Check father/mother ordering and midpoint centering
        all_nodes = set(tree) | {()}
        for node in all_nodes:
            f_path = node + ('father',)
            m_path = node + ('mother',)
            has_f = f_path in tree
            has_m = m_path in tree

            if has_f:
                assert tops[f_path] < tops[node], f"Father {f_path} not above {node}"
            if has_m:
                assert tops[m_path] > tops[node], f"Mother {m_path} not below {node}"
            if has_f and has_m:
                expected_mid = (tops[f_path] + tops[m_path]) / 2.0
                assert abs(tops[node] - expected_mid) <= 1.0, (
                    f"Node {node} ({tops[node]}) not centered between {f_path} ({tops[f_path]}) and {m_path} ({tops[m_path]})"
                )
