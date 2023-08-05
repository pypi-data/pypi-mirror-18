# -*- coding: UTF-8 -*-
import unittest

from pandasticsearch.operators import *


class TestOperators(unittest.TestCase):
    def test_metric_agg(self):
        self.assertEqual(MetricAggregator('x', 'avg').build(), {'avg(x)': {'avg': {'field': 'x'}}})
        self.assertEqual(MetricAggregator('x', 'max').build(), {'max(x)': {'max': {'field': 'x'}}})

    def test_grouper(self):
        nested_grouper = Grouper('a', inner=Grouper('b', inner=Grouper('c')))
        print(nested_grouper.build())
        self.assertEqual(nested_grouper.build(),
                         {
                             'a': {
                                 'terms': {'field': 'a', 'size': 20},
                                 'aggregations': {
                                     'b': {
                                         'terms': {'field': 'b', 'size': 20},
                                         'aggregations': {
                                             'c': {'terms': {'field': 'c', 'size': 20}}}}}}})

    def test_range_grouper(self):
        range_grouper = RangeGrouper('a', [1, 3, 6])
        print(range_grouper.build())
        self.assertEqual(range_grouper.build(), {
            'range(1,3,6)': {'range': {'ranges': [{'to': 3, 'from': 1}, {'to': 6, 'from': 3}], 'field': 'a'}}})

    def test_sorter(self):
        self.assertEqual(Sorter('x').build(), {'x': {'order': 'desc'}})
        self.assertEqual(Sorter('x', mode='avg').build(), {'x': {'order': 'desc', 'mode': 'avg'}})

    def test_leaf_boolean_filter(self):
        self.assertEqual(GreaterEqual('a', 2).build(), {"range": {"a": {"gte": 2}}})
        self.assertEqual(LessEqual('a', 2).build(), {"range": {"a": {"lte": 2}}})
        self.assertEqual(Less('a', 2).build(), {"range": {"a": {"lt": 2}}})
        self.assertEqual(Equal('a', 2).build(), {"term": {"a": 2}})
        exp = Equal('a', 2)
        self.assertEqual((~exp).build()['bool'], {"must_not": {"term": {"a": 2}}})
        self.assertEqual(Greater('a', 2).build(), {"range": {"a": {"gt": 2}}})
        self.assertEqual(IsIn('a', [1, 2, 3]).build(), {'terms': {'a': [1, 2, 3]}})
        self.assertEqual(Null('a').build(), {'missing': {'field': 'a'}})

    def test_and_filter(self):
        self.assertEqual(
            (GreaterEqual('a', 2) & Less('b', 3)).build()['bool'],
            {
                'must': [
                    {'range': {'a': {'gte': 2}}},
                    {'range': {'b': {'lt': 3}}}]
            })

        self.assertEqual(
            (GreaterEqual('a', 2) & Less('b', 3) & Equal('c', 4)).build()['bool'],
            {
                'must': [
                    {'range': {'a': {'gte': 2}}},
                    {'range': {'b': {'lt': 3}}},
                    {'term': {'c': 4}}]
            })

        self.assertEqual(
            (GreaterEqual('a', 2) & (Less('b', 3) & Equal('c', 4))).build()['bool'],
            {
                'must': [
                    {'range': {'b': {'lt': 3}}},
                    {'term': {'c': 4}},
                    {'range': {'a': {'gte': 2}}}]
            })

    def test_or_filter(self):
        self.assertEqual(
            (GreaterEqual('a', 2) | Less('b', 3)).build()['bool'],
            {
                'should': [
                    {'range': {'a': {'gte': 2}}},
                    {'range': {'b': {'lt': 3}}}]
            })

        self.assertEqual(
            (GreaterEqual('a', 2) | Less('b', 3) | Equal('c', 4)).build()['bool'],
            {
                'should': [
                    {'range': {'a': {'gte': 2}}},
                    {'range': {'b': {'lt': 3}}},
                    {'term': {'c': 4}}]
            })

        self.assertEqual(
            (GreaterEqual('a', 2) | (Less('b', 3) | Equal('c', 4))).build()['bool'],
            {
                'should': [
                    {'range': {'b': {'lt': 3}}},
                    {'term': {'c': 4}},
                    {'range': {'a': {'gte': 2}}}]
            })

    def test_not_filter(self):
        self.assertEqual(
            (~GreaterEqual('a', 2)).build()['bool'],
            {
                'must_not':
                    {'range': {'a': {'gte': 2}}}})

    def test_not_not_filter(self):
        exp = GreaterEqual('a', 2)
        print((~exp).build())
        print((~~exp).build())
        self.assertEqual(
            (~~exp).build()['bool'],
            {
                'must_not': {
                    'bool': {
                        'must_not':
                            {'range': {'a': {'gte': 2}}}}}})

    def test_not_and_filter(self):
        exp = GreaterEqual('a', 2) & Less('b', 3)
        self.assertEqual(
            (~exp).build()['bool'],
            {
                'must_not': {
                    'bool': {
                        'must': [
                            {'range': {'a': {'gte': 2}}},
                            {'range': {'b': {'lt': 3}}}]
                    }
                }
            })

    def test_and_or_filter(self):
        exp = Less('b', 3) | Equal('c', 4)
        actual = GreaterEqual('a', 2) & exp

        self.assertEqual(
            actual.build()['bool'],
            {
                'must': [
                    {'range': {'a': {'gte': 2}}},
                    {
                        'bool': {
                            'should': [
                                {'range': {'b': {'lt': 3}}},
                                {'term': {'c': 4}}
                            ]
                        }
                    }]
            })


if __name__ == '__main__':
    unittest.main()
