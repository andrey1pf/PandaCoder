from parserController.Parsers import parser_newsdataio


def test_context():
    print(parser_newsdataio.check_content('hi Show key events only'))
    assert parser_newsdataio.check_content('hi Show key events only') == 'hi '


test_context()
