import pytest

from code_two.postcodeuk import PostCodeUk


class TestPostCodeUk:
    @pytest.mark.parametrize('postcode', [
        None, 1, [],
    ])
    def test__init_invalid_postcode(self, postcode):
        with pytest.raises(TypeError):
            PostCodeUk(postcode)

    @pytest.mark.parametrize('postcode', [
        (PostCodeUk('EC1A 1BB')), #AANA NAA
        (PostCodeUk('W1A 0AX')), #ANA NAA
        (PostCodeUk('M1 1AE')), #AN NAA
        (PostCodeUk('B33 8TH')), #ANN NAA
        (PostCodeUk('CR2 6XH')), #AAN NAA
        (PostCodeUk('DN55 1PT')) #AANN NAA
    ])
    def test_valid_postcode(self, postcode):
        assert postcode.is_valid()

    @pytest.mark.parametrize('postcode', [
        (PostCodeUk('invalid')),
        (PostCodeUk('')),
        (PostCodeUk('B3 8C')),
        (PostCodeUk('CR2@ 6XH')),
        (PostCodeUk('DN55-1PT'))
    ])
    def test_in_valid_postcode(self, postcode):
        assert not postcode.is_valid()

    @pytest.mark.parametrize('postcode, expected', [
        (PostCodeUk('EC1A 1BB'), 'EC1A'),
        (PostCodeUk('W1A 0AX'), 'W1A'),
        (PostCodeUk('M1 1AE'), 'M1'),
        (PostCodeUk('B33 8TH'), 'B33'),
        (PostCodeUk('CR2 6XH'), 'CR2'),
        (PostCodeUk('DN55 1PT'), 'DN55'),
        (PostCodeUk(''), None),
        (PostCodeUk('invalid'), None)
    ])
    def test_get_outward(self, postcode, expected):
        assert postcode.get_outward() == expected

    @pytest.mark.parametrize('postcode, expected', [
        (PostCodeUk('EC1A 1BB'), '1BB'),
        (PostCodeUk('W1A 0AX'), '0AX'),
        (PostCodeUk('M1 1AE'), '1AE'),
        (PostCodeUk('B33 8TH'), '8TH'),
        (PostCodeUk('CR2 6XH'), '6XH'),
        (PostCodeUk('DN55 1PT'), '1PT'),
        (PostCodeUk(''), None),
        (PostCodeUk('invalid'), None)
    ])
    def test_get_inward(self, postcode, expected):
        assert postcode.get_inward() == expected

    def test_random_postcode(self):
        for i in range(50):
            postcode = PostCodeUk(PostCodeUk.random_postcode())
            assert postcode.is_valid()

    @pytest.mark.parametrize('text, postcodes, expected', [
        ('Example of text with postcode W1A 0AX and other postcode'
         'EC1A 1BB', ['EC1A 1BB', 'W1A 0AX'], ['EC1A 1BB', 'W1A 0AX']),
        ('Other text with on postcode M1 1AE none postcodes informed', [], ['M1 1AE']),
        ('Other text withiout postcode', ['M1 1AE'], []),
    ])
    def test_find_all_in_text_valid(self, text, postcodes, expected):
        assert sorted(PostCodeUk.find_all_in_text(text, postcodes)) == sorted(expected)

    @pytest.mark.parametrize('text, postcodes, expected', [
        ('Example of text with postcode W1A 0AX and other postcode'
         'EC1A 1BB invalid post code informed', 1, TypeError),
        ('Other text with on postcode M1 1AE invalid postcodes informed', [10],
         'all postcodes should be valid'),
    ])
    def test_find_all_in_text_invalid(self, text, postcodes, expected):
        if expected == TypeError:
            with pytest.raises(TypeError):
                PostCodeUk.find_all_in_text(text, postcodes) == expected
        else:
            assert PostCodeUk.find_all_in_text(text, postcodes) == expected
