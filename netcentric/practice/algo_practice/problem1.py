## 
# Problem: Compress a string such that 'AAABCCDDDD' becomes 'A3BC2D4'. 
# Only compress the string if it saves space.
#

from nose.tools import assert_equal

class CompressString(object):

    def compress(self, string):
        if string is None or not string: 
            return string
        
        compressed = ""
        prev_letter = string[0]
        count = 0
        for letter in string:
            if prev_letter == letter:
                count += 1
            else:
                compressed += prev_letter + (str(count) if count > 1 else '')
                prev_letter = letter
                count = 1
        compressed += prev_letter + (str(count) if count > 1 else '')
        return compressed if len(compressed) < len(string) else string



class TestCompress(object):

    def test_compress(self, func):
        assert_equal(func(None), None)
        assert_equal(func(''), '')
        assert_equal(func('AABBCC'), 'AABBCC')
        assert_equal(func('AAABCCDDDDE'), 'A3BC2D4E')
        assert_equal(func('BAAACCDDDD'), 'BA3C2D4')
        assert_equal(func('AAABAACCDDDD'), 'A3BA2C2D4')
        print('Success: test_compress')


def main():
    test = TestCompress()
    compress_string = CompressString()
    test.test_compress(compress_string.compress)


if __name__ == '__main__':
    main()