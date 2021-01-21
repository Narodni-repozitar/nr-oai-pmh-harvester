def test_others_identifier_1(app, db):
    from nr_oai_pmh_harvester.rules.uk.others_identifier import original_record_oai
    res = original_record_oai(["oai:dspace.cuni.cz:20.500.11956/2079"])
    assert res == {
        'control_number': '264813',
        'recordIdentifiers': {
            'originalRecordOAI': 'oai:dspace.cuni.cz:20.500.11956/2079'
        }
    }
