# test_santaslist.py
import yaml
import santaslist

TEST_PEOPLE_STR = 'jeff hann (@obihann),bob bober (@bob),frank franklyn (@franky),george the dog (@george)'


def load_people():
    data = open('test/people.yml', 'r')
    return santaslist.load_people(yaml.load(data)['people'])


class TestSantasList(object):
    def test_load_people(self):
        assert isinstance(load_people(), list)

    def test_people(self):
        assert isinstance(santaslist.people(), list)

    def test_print_people(self):
        assert TEST_PEOPLE_STR == str(santaslist.print_people())

    def test_pairs(self):
        assert isinstance(santaslist.pairs(), list)

    def test_print_pairs(self):
        pairs = santaslist.print_pairs()
        assert isinstance(pairs, str)
        assert pairs != ''
