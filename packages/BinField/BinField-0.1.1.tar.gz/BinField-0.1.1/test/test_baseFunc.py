import copy
import pickle
import unittest

from binfield import BinField


class BaseFunctionality(unittest.TestCase):
    def test_not_mapped_no_len(self):
        test_value = 42

        bf = BinField(test_value)

        self.assertEqual(
            repr(bf),
            '{cls}(x=0x{x:0{len}X}, base=16)'.format(
                cls=bf.__class__.__name__,
                x=int(bf),
                len=len(bf) * 2,
            )
        )

        self.assertEqual(
            dir(bf), ['_bit_size_', '_mapping_', '_mask_', '_value_']
        )

        self.assertEqual(bf._bit_size_, test_value.bit_length())
        self.assertEqual(bf._value_, test_value)
        self.assertIsNone(bf._mapping_)
        self.assertIsNone(bf._mask_)

        self.assertEqual(int(bf), test_value)
        self.assertEqual(bin(bf), bin(test_value))

        self.assertEqual(abs(bf), test_value)
        self.assertGreater(bf, test_value - 1)
        self.assertGreaterEqual(bf, test_value - 1)
        self.assertGreaterEqual(bf, test_value)
        self.assertLess(bf, test_value + 1)
        self.assertLessEqual(bf, test_value + 1)
        self.assertLessEqual(bf, test_value)
        self.assertEqual(bf, test_value)
        self.assertNotEqual(bf, 0)

        self.assertEqual(bool(bf), True)

        bf &= 1
        test_value &= 1

        self.assertEqual(bf, test_value)

        bf |= 1
        test_value |= 1

        self.assertEqual(bf, test_value)

        bf ^= 2
        test_value ^= 2

        self.assertEqual(bf, test_value)

        test_value = 42
        bf = BinField(test_value)

        self.assertEqual(bf & 1, test_value & 1)
        self.assertEqual(bf | 1, test_value | 1)
        self.assertEqual(bf ^ 1, test_value ^ 1)

        bf += 1
        test_value += 1

        self.assertEqual(bf, test_value)

        bf -= 1
        test_value -= 1

        self.assertEqual(bf + 1, test_value + 1)
        self.assertEqual(bf - 1, test_value - 1)

        self.assertEqual(bf * 2, test_value * 2)
        self.assertEqual(bf << 1, test_value << 1)
        self.assertEqual(bf >> 1, test_value >> 1)

        self.assertEqual(bf[0], 0)

        self.assertIsInstance(bf[0: 2], BinField)
        self.assertEqual(bf[0: 2]._bit_size_, 2)

        self.assertIsInstance(bf[: 2], BinField)
        self.assertEqual(bf[: 2]._bit_size_, 2)

        self.assertIsInstance(bf[(0, 2)], BinField)
        self.assertEqual(bf[(0, 2)]._bit_size_, 2)

        self.assertIsInstance(bf[[0, 2]], BinField)
        self.assertEqual(bf[[0, 2]]._bit_size_, 2)

        bf[0] = 1
        self.assertEqual(bf[0], 1)

        bf[1: 3] = 3
        self.assertEqual(bf[1: 3], 3)

        bf[:3] = 0
        self.assertEqual(bf[0: 3], 0)

        bf[(0, 2)] = 3
        self.assertEqual(bf[0: 2], 3)

        with self.assertRaises(ValueError):
            bf -= 100  # negative result

        with self.assertRaises(ValueError):
            bf - 100  # negative result

        with self.assertRaises(IndexError):
            bf[2:1]  # invalid slice

        with self.assertRaises(IndexError):
            bf[None]  # invalid index type

        with self.assertRaises(IndexError):
            bf['test']  # no mapping

        with self.assertRaises(TypeError):
            bf[0] = None

        with self.assertRaises(IndexError):
            bf[None] = 10  # invalid index type

        with self.assertRaises(IndexError):
            bf['test'] = 10  # no mapping

        with self.assertRaises(ValueError):
            bf[0:2] = 10  # bigger, than slice

        with self.assertRaises(ValueError):
            bf[:2] = 10  # bigger, than slice

        with self.assertRaises(ValueError):
            bf[1] = 10  # bigger, than 1 bit

        new_bf = pickle.loads(pickle.dumps(bf, -1))
        self.assertEqual(new_bf, bf)

        bf |= 0xff
        self.assertEqual(
            str(bf),
            '255<0xFF (0b11111111)>'
        )

    def test_positive_mapped_no_len(self):
        class MappedBinField(BinField):
            test_index = 0
            test_slc = slice(1, 3)
            test_list_slc = [3, 5]

        mbf = MappedBinField(7)

        self.assertEqual(
            repr(mbf),
            '{cls}(x=0x{x:0{len}X}, base=16)'.format(
                cls=mbf.__class__.__name__,
                x=int(mbf),
                len=len(mbf) * 2,
            )
        )

        self.assertEqual(mbf._mask_, None)  # Mask is not generated

        self.assertEqual(mbf['test_index'], mbf[0])
        self.assertEqual(mbf['test_slc'], mbf[1: 3])
        self.assertEqual(mbf['test_list_slc'], mbf[3: 5])

        self.assertEqual(mbf.test_index, mbf[0])
        self.assertEqual(mbf.test_slc, mbf[1: 3])
        self.assertEqual(mbf.test_list_slc, mbf[3: 5])

        mbf['test_index'] = 0
        self.assertEqual(mbf['test_index'], 0)

        mbf['test_slc'] = 0
        self.assertEqual(mbf['test_slc'], 0)

        mbf['test_slc'][1] = 1
        self.assertEqual(mbf['test_slc'], 2)

    def test_positive_mapped_nested(self):
        class NestedMappedBinField(BinField):
            test_index = 0
            nested_block = {
                '_index_': (1, 6),
                'single_bit': 0,
                'multiple': (1, 3)
            }
            _size_ = 8

        nbf = NestedMappedBinField(0xFF)

        self.assertEqual(
            dir(nbf),
            [
                '_bit_size_', '_mapping_', '_mask_', '_value_',
                'nested_block', 'test_index'
            ]
        )

        self.assertEqual(nbf, 0b11111111)  # Mask not recalculated
        self.assertEqual(nbf.nested_block, 0b00011111)  # Index was used
        self.assertEqual(nbf.nested_block.single_bit, 0b1)
        self.assertEqual(nbf.nested_block.multiple, 0b11)

        self.assertIsInstance(nbf + 1, int)  # owerflow _size_
        self.assertEqual(nbf + 1, 256)

        nbf.nested_block = 0

        self.assertEqual(nbf, 0b11000001)  # Nested block is masked

        with self.assertRaises(OverflowError):
            nbf += 100  # overflow

        with self.assertRaises(IndexError):
            nbf[256]

        with self.assertRaises(OverflowError):
            nbf[256] = 1

        with self.assertRaises(OverflowError):
            nbf[:256] = 0xBA

        with self.assertRaises(ValueError):
            nbf[0:1] = 2

        with self.assertRaises(ValueError):
            pickle.dumps(nbf.nested_block, -1)  # Linked object

        nested_copy = copy.copy(nbf.nested_block)
        self.assertFalse(nested_copy is nbf.nested_block)
        # Hash will be the same due to class memorize.
        self.assertEqual(hash(nested_copy), hash(nbf.nested_block))
        nested_copy.single_bit = 1
        self.assertNotEqual(nbf.nested_block, nested_copy)
        # Data changed -> hash changed
        self.assertNotEqual(hash(nested_copy), hash(nbf.nested_block))
        self.assertEqual(nbf, 0b11000001)  # Original
        self.assertEqual(
            str(nbf),
            '193<\n'
            '  test_index=1<0x01 (0b1)>,\n'
            '  nested_block=(\n'
            '    single_bit=0<0x00 (0b0)>,\n'
            '    multiple=0<0x00 (0b00)>\n'
            '  )\n'
            '(0xC1) (0b11000001)>'
        )
        self.assertEqual(nbf[:], nbf)  # Full slice calls self-copy
