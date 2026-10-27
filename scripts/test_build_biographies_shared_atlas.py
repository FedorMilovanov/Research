import copy
import unittest
import xml.etree.ElementTree as ET
from build_biographies_shared_atlas import load, validate, render


class SharedAtlasTests(unittest.TestCase):
    def setUp(self):
        self.graph, self.registry = load()

    def test_current_and_svg_parse(self):
        output = render(self.graph, self.registry)
        root = ET.fromstring(output['biographies-shared.svg'])
        self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
        self.assertEqual(len(root.findall('{http://www.w3.org/2000/svg}a')), len(self.graph['nodes']))

    def test_deterministic_and_read_only(self):
        before = copy.deepcopy((self.graph, self.registry))
        self.assertEqual(render(self.graph, self.registry), render(self.graph, self.registry))
        self.assertEqual(before, (self.graph, self.registry))

    def test_missing_evidence_fails(self):
        self.graph['edges'][0]['refs'] = []
        with self.assertRaisesRegex(ValueError, 'without evidence'):
            validate(self.graph, self.registry)

    def test_unknown_anchor_fails(self):
        self.graph['edges'][0]['refs'] = ['invented']
        with self.assertRaisesRegex(ValueError, 'Unknown anchor'):
            validate(self.graph, self.registry)

    def test_missing_owner_fails(self):
        self.graph['nodes'][0]['owner'] = 'absent-biographical-owner.md'
        with self.assertRaisesRegex(ValueError, 'Missing or unsafe'):
            validate(self.graph, self.registry)

    def test_unsafe_owner_fails(self):
        self.graph['nodes'][0]['owner'] = '../../etc/passwd'
        with self.assertRaisesRegex(ValueError, 'Missing or unsafe'):
            validate(self.graph, self.registry)

    def test_no_navigation_laundering(self):
        edge = next(e for e in self.graph['edges'] if e['type'] == 'NAVIGATION')
        edge['refs'] = ['BIO-02']
        with self.assertRaisesRegex(ValueError, 'masquerade'):
            validate(self.graph, self.registry)

    def test_state_axis_required(self):
        del self.registry['anchors'][1]['accessState']
        with self.assertRaisesRegex(ValueError, 'Missing state axis'):
            validate(self.graph, self.registry)

    def test_hold_not_dropped(self):
        self.registry['anchors'][1]['holds'] = []
        with self.assertRaisesRegex(ValueError, 'publication boundary'):
            validate(self.graph, self.registry)

    def test_excluded_edges_not_drawn(self):
        rendered = render(self.graph, self.registry)
        svg = rendered['biographies-shared.svg']
        for edge in self.graph['excludedLinks']:
            self.assertNotIn(edge['id'], svg)
            self.assertIn(edge['id'], rendered['index.html'])

    def test_html_escaping(self):
        self.graph['nodes'][0]['label'] = '<script>bad</script>'
        doc = render(self.graph, self.registry)['index.html']
        self.assertNotIn('<script>bad</script>', doc)
        self.assertIn('&lt;script&gt;bad&lt;/script&gt;', doc)

    def test_directory_owner_fails(self):
        self.graph['nodes'][0]['owner'] = 'БИОГРАФИИ'
        with self.assertRaisesRegex(ValueError, 'Missing or unsafe owner'):
            validate(self.graph, self.registry)

    def test_unknown_node_fails(self):
        self.graph['edges'][0]['to'] = 'invented'
        with self.assertRaisesRegex(ValueError, 'Unknown node'):
            validate(self.graph, self.registry)


if __name__ == '__main__':
    unittest.main()
