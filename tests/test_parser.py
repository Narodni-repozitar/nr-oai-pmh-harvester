def test_parser(app, db, xml):
    from nr_oai_pmh_harvester.parser import marcxml_parser
    from nr_oai_pmh_harvester.utils import transform_to_dict

    new_dict = transform_to_dict(marcxml_parser(xml))
    assert new_dict == {
        '001': '333449',
        '005': '20170627145737.0',
        '035__': {'a': 'oai:dspace.cuni.cz:20.500.11956/64309'},
        '04107': {'a': 'cze'},
        '046__': {'k': '2015-06-23'},
        '24500': {
            'a': 'Politika, média, manipulace. Politické zpravodajství, '
                 'publicistika a pragmatická lingvistika.',
            'b': 'Politics, media and manipulation: politics news and '
                 'pragmaticlinguistics'
        },
        '502__': {'b': 'Mgr.', 'c': 'Univerzita Karlova', 'd': '2015'},
        '520__': [{
            '9': 'eng',
            'a': "The master's thesis Politics, Media and Manipulation: "
                 'Political Journalism and Pragmatic Linguistics examines '
                 'contemporary Czech publicized political communication using '
                 'pragmatic analysis. It focuses on topics like power, '
                 'ideology and self-presentation of the political participants '
                 'in the media. It is also concerned with the framing of media '
                 'communication and with the communication strategies that the '
                 'political participants and journalists use. The research was '
                 'conducted with the use of quantitative pragmatic analysis. '
                 'Each sample was examined from many different angles. In this '
                 'thesis, pragmatic phenomenon are examined like the function '
                 'of the statements, speech acts, intertextuality, '
                 'conversational maxims, the use and violation of speech '
                 'etiquette, presupposition, conversational implicatures, '
                 'deixis, and reference. The semiotic analysis and the '
                 'examination of the context, from which the analyzed media '
                 'texts originated, is involved as well. Journalistic texts '
                 'from different types of media from the time of the first '
                 'Czech direct presidential election have been chosen as '
                 'samples for the analysis. The goal of the thesis is to '
                 'design a complex pragmatic analysis and describe the used '
                 'communication strategies of the participants.'
        },
            {
                '9': 'cze',
                'a': 'Diplomová práce Politika, média, manipulace. Politické '
                     'zpravodajství, publicistika a pragmatická lingvistika zkoumá '
                     'současnou českou medializovanou politickou komunikaci pomocí '
                     'pragmatické analýzy. Zaměřuje se na témata moci, ideologie a '
                     'sebeprezentace politických aktérů v médiích. Zabývá se '
                     'rámováním jejich komunikace médii a komunikačními '
                     'strategiemi, které oni i mediální pracovníci používají. '
                     'Výzkum je realizován pomocí kvalitativní pragmatické '
                     'analýzy, každý vzorek je zkoumán z mnoha různých úhlů. V '
                     'práci jsou zkoumány pragmatické fenomény, jako jsou '
                     'intertextualita, funkce výpovědí a používání řečových aktů, '
                     'konverzační maximy, používání a porušování řečové etikety, '
                     'presupozice, konverzační implikatury, deixe a reference. '
                     'Prostor je věnován také sémiotické analýze a analýze '
                     'kontextu, ve kterém daný text vznikl. Jako vzorek byly '
                     'vybrány zpravodajské a publicistické texty z různých typů '
                     'českých médií z období kampaně k první přímé prezidentské '
                     'volbě v ČR (tedy za období září 2012 až leden 2013). Cílem '
                     'práce je navrhnout komplexní pragmatickou analýzu a popsat '
                     'používané komunikační strategie aktérů.'
            }],
        '586__': {'a': 'obhájeno', 'b': 'successfully defended'},
        '6530_': [{'a': 'Political communication'},
                  {'a': 'pragmatic linguistic'},
                  {'a': 'political journalism'},
                  {'a': 'functions of the statements'},
                  {'a': 'speech acts'},
                  {'a': 'intertextuality'},
                  {'a': 'conversational maxims'},
                  {'a': 'semiotics'}],
        '653__': [{'a': 'Politická komunikace'},
                  {'a': 'pragmatická lingvistika'},
                  {'a': 'politická žurnalistika'},
                  {'a': 'funkce výpovědí'},
                  {'a': 'řečové akty'},
                  {'a': 'intertextualita'},
                  {'a': 'konverzační maximy'},
                  {'a': 'sémiotika'}],
        '7102_': [{
            '9': 'cze',
            'a': 'Univerzita Karlova',
            'b': 'Katedra mediálních studií',
            'g': 'Fakulta sociálních věd'
        },
            {
                '9': 'eng',
                'a': 'Charles University',
                'b': 'Department of Media Studies',
                'g': 'Faculty of Social Sciences'
            }],
        '720__': [{'a': 'Zicháčková, Adéla'},
                  {'e': 'advisor', 'i': 'Šoltys, Otakar'},
                  {'e': 'referee', 'i': 'Jirák, Jan'}],
        '85640': [{
            'u': 'http://hdl.handle.net/20.500.11956/64309',
            'z': 'Odkaz na původní záznam'
        },
            {'u': 'http://www.nusl.cz/ntk/nusl-333449', 'z': 'PID NUŠL'}],
        '909CO': {
            'o': 'oai:invenio.nusl.cz:333449',
            'p': ['etds', 'openaire', 'global']
        },
        '980__': {'a': 'diplomove_prace'},
        '996__': {
            '9': '1',
            'a': 'Dostupné v digitálním repozitáři UK.',
            'b': 'Available in the Charles University Digital Repository.'
        },
        '998__': {'a': 'univerzita_karlova_v_praze'},
        'leader': '00000coc  2200000uu 4500'
    }
