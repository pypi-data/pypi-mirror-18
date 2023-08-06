###############################################################################
#
#   Copyright: (c) 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from ..structure import Structure, StructureError

import unittest
import pickle


# --- Unit tests
class RegTest(unittest.TestCase):
    def setUp(self):
        # --- perform set-up actions, if any
        pass

    def tearDown(self):
        # --- perform clean-up actions, if any
        pass

    def test_constructors(self):
        struct0 = Structure({"a": 1.0, "b": 2.0, "c": 3.0})
        struct1 = Structure({"a": 1, "b": 2, "c": 3})
        struct2 = Structure(a=1, b=2, c=3)
        struct3 = Structure([("a", 1), ("b", 2), ("c", 3)])
        struct4 = Structure()
        struct4["a"] = 1
        struct4["b"] = 2
        struct4["c"] = 3

        self.assertEqual(struct0, struct1)
        self.assertEqual(struct1, struct2)
        self.assertEqual(struct2, struct3)
        self.assertEqual(struct3, struct4)

    def test_error(self):
        self.assertRaises(StructureError, Structure, {"a": None})
        self.assertRaises(StructureError, Structure, {"a": "*"})

    def test_algerba(self):
        struct1 = Structure(a=1, b=2, c=3)
        struct2 = Structure(b=10, c=10, d=10)

        self.assertEqual(1 + struct1, Structure(a=2, b=3, c=4))
        self.assertEqual(struct1 + 1.0, Structure(a=2, b=3, c=4))

        self.assertEqual(2 * struct1, Structure(a=2, b=4, c=6))
        self.assertEqual(struct1 * 2, Structure(a=2, b=4, c=6))

        add_struct = Structure({"a": 1, "b": 12, "c": 13, "d": 10})
        sub_struct = Structure({"a": -1, "b": 8, "c": 7, "d": 10})

        self.assertEqual(struct2 + struct1, add_struct)
        self.assertEqual(struct2 - struct1, sub_struct)

        struct2 += struct1

        self.assertEqual(struct2, Structure(a=1, b=12, c=13, d=10))
        self.assertEqual(-2*struct1, Structure(a=-2, b=-4, c=-6))

    def test_pickling(self):
        struct = Structure({"a": 1, "b": 2, "c": 3})
        self.assertEqual(struct, pickle.loads(pickle.dumps(struct, 2)))


if __name__ == "__main__":
    unittest.main()
