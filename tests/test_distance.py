import pytest
from decimal import Decimal
from deepdiff import DeepDiff
from deepdiff.helper import get_diff_length


class TestDeepDistance:

    @pytest.mark.parametrize('diff, expected_length', [
        (
            {'set_item_added': {'root[1]': {6}}},
            1
        ),
        (
            {
                'iterable_items_added_at_indexes': {
                    'root': {
                        0: 7,
                        6: 8,
                        1: 4,
                        2: 4,
                        5: 4
                    }
                },
                'iterable_items_removed_at_indexes': {
                    'root': {
                        6: 6,
                        0: 5
                    }
                }
            },
            7
        ),
        (
            {
                'type_changes': {
                    'root': {
                        'old_type': float,
                        'new_type': Decimal,
                        'new_value': Decimal('3.2')
                    }
                }
            },
            3
        ),
    ])
    def test_diff_length(self, diff, expected_length):
        length = get_diff_length(diff)
        assert expected_length == length

    def test_distance_of_the_same_objects(self):
        t1 = [{1, 2, 3}, {4, 5, 6}]
        t2 = [{4, 5, 6}, {1, 2, 3}]
        ddiff = DeepDiff(t1, t2, ignore_order=True)
        assert {} == ddiff
        assert 0 == get_diff_length(ddiff)
        assert '0' == str(ddiff.get_deep_distance())[:10]
        assert 9 == ddiff._DeepDiff__get_item_rough_length(ddiff.t1)
        assert 9 == ddiff._DeepDiff__get_item_rough_length(ddiff.t2)

    def test_distance_of_list_sets(self):
        t1 = [{1, 2, 3}, {4, 5}]
        t2 = [{4, 5, 6}, {1, 2, 3}]
        ddiff = DeepDiff(t1, t2, ignore_order=True)
        delta = ddiff.to_delta_dict(report_repetition_required=False)
        assert {'set_item_added': {'root[1]': {6}}} == delta
        assert 1 == get_diff_length(ddiff)
        assert '0.05882352' == str(ddiff.get_deep_distance())[:10]
        assert 8 == ddiff._DeepDiff__get_item_rough_length(ddiff.t1)
        assert 9 == ddiff._DeepDiff__get_item_rough_length(ddiff.t2)

    def test_distance_of_list_sets2(self):
        t1 = [{1, 2, 3}, {4, 5}, {1}]
        t2 = [{4, 5, 6}, {1, 2, 3}, {1, 4}]
        ddiff = DeepDiff(t1, t2, ignore_order=True)
        delta = ddiff.to_delta_dict(report_repetition_required=False)
        assert {'set_item_added': {'root[2]': {4}, 'root[1]': {6}}} == delta
        assert 2 == get_diff_length(ddiff)
        assert '0.09090909' == str(ddiff.get_deep_distance())[:10]
        assert 10 == ddiff._DeepDiff__get_item_rough_length(ddiff.t1)
        assert 12 == ddiff._DeepDiff__get_item_rough_length(ddiff.t2)

    def test_distance_of_list_sets_and_strings(self):
        t1 = [{1, 2, 3}, {4, 5, 'hello', 'right!'}, {4, 5, (2, 4, 7)}]
        t2 = [{4, 5, 6, (2, )}, {1, 2, 3}, {5, 'hello', 'right!'}]
        ddiff = DeepDiff(t1, t2, ignore_order=True)
        delta = ddiff.to_delta_dict(report_repetition_required=False)
        expected = {
            'set_item_removed': {
                'root[2]': {(2, 4, 7)},
                'root[1]': {4}
            },
            'set_item_added': {
                'root[2]': {(2, ), 6}
            }
        }
        assert expected == delta
        assert 6 == get_diff_length(ddiff)
