from parsing.parserController import parser_newsdataio

def test_context():
    assert parser_newsdataio.check_content('hi Show key events only') == 'hi '