from datetime import datetime
from typing import List, Iterable


class Publisher:

    def __init__(self, publisher_name: str):
        # This makes sure the setter is called here in the initializer/constructor as well.
        self.name = publisher_name
        self.__books: List[Book] = list()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def books(self) -> Iterable['Book']:
        return iter(self.__books)

    @name.setter
    def name(self, publisher_name: str):
        self.__name = "N/A"
        if isinstance(publisher_name, str):
            # Make sure leading and trailing whitespace is removed.
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name
    
    def add_book(self, book: 'Book'):
        if isinstance(book, Book) and book not in self.__books:
            self.__books.append(book)

    def __repr__(self):
        return f'<Publisher {self.name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.name == self.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class Author:

    def __init__(self, author_id: int, author_full_name: str):
        if not isinstance(author_id, int):
            raise ValueError

        if author_id < 0:
            raise ValueError

        self.__unique_id = author_id

        # Uses the attribute setter method.
        self.full_name = author_full_name

        # Initialize author colleagues data structure with empty set.
        # We use a set so each unique author is only represented once.
        self.__authors_this_one_has_worked_with = set()

    @property
    def unique_id(self) -> int:
        return self.__unique_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, author_full_name: str):
        if isinstance(author_full_name, str):
            # make sure leading and trailing whitespace is removed
            author_full_name = author_full_name.strip()
            if author_full_name != "":
                self.__full_name = author_full_name
            else:
                raise ValueError
        else:
            raise ValueError

    def add_coauthor(self, coauthor):
        if isinstance(coauthor, self.__class__) and coauthor.unique_id != self.unique_id:
            self.__authors_this_one_has_worked_with.add(coauthor)

    def check_if_this_author_coauthored_with(self, author):
        return author in self.__authors_this_one_has_worked_with

    def __repr__(self):
        return f'<Author {self.full_name}, author id = {self.unique_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __hash__(self):
        return hash(self.unique_id)


class Book:

    def __init__(self, book_id: int, book_title: str):
        if not isinstance(book_id, int):
            raise ValueError

        if book_id < 0:
            raise ValueError

        self.__book_id = book_id

        # use the attribute setter
        self.title = book_title
        self.__reading_list_users: List[User] = list()
        self.__reviews = []
        self.__description = None
        self.__publisher = None
        self.__authors = []
        self.__release_year = None
        self.__ebook = None
        self.__num_pages = None
        self.__image_hyperlink = None
        self.__language = None
        self.__language_iso_codes = ['aar', 'abk', 'ace', 'ach', 'ada', 'ady', 'afa', 'afh', 'afr', 'ain', 'aka', 'akk', 'alb', 'ale', 'alg', 'alt', 'amh', 'ang', 'anp', 'apa', 'ara', 'arc', 'arg', 'arm', 'arn', 'arp', 'art', 'arw', 'asm', 'ast', 'ath', 'aus', 'ava', 'ave', 'awa', 'aym', 'aze', 'bad', 'bai', 'bak', 'bal', 'bam', 'ban', 'baq', 'bas', 'bat', 'bej', 'bel', 'bem', 'ben', 'ber', 'bho', 'bih', 'bik', 'bin', 'bis', 'bla', 'bnt', 'tib', 'bos', 'bra', 'bre', 'btk', 'bua', 'bug', 'bul', 'bur', 'byn', 'cad', 'cai', 'car', 'cat', 'cau', 'ceb', 'cel', 'cze', 'cha', 'chb', 'che', 'chg', 'chi', 'chk', 'chm', 'chn', 'cho', 'chp', 'chr', 'chu', 'chv', 'chy', 'cmc', 'cnr', 'cop', 'cor', 'cos', 'cpe', 'cpf', 'cpp', 'cre', 'crh', 'crp', 'csb', 'cus', 'wel', 'dak', 'dan', 'dar', 'day', 'del', 'den', 'ger', 'dgr', 'din', 'div', 'doi', 'dra', 'dsb', 'dua', 'dum', 'dut', 'dyu', 'dzo', 'efi', 'egy', 'en-US', 'eka', 'gre', 'elx', 'eng', 'enm', 'epo', 'est', 'ewe', 'ewo', 'fan', 'fao', 'per', 'fat', 'fij', 'fil', 'fin', 'fiu', 'fon', 'fre', 'frm', 'fro', 'frr', 'frs', 'fry', 'ful', 'fur', 'gaa', 'gay', 'gba', 'gem', 'geo', 'gez', 'gil', 'gla', 'gle', 'glg', 'glv', 'gmh', 'goh', 'gon', 'gor', 'got', 'grb', 'grc', 'grn', 'gsw', 'guj', 'gwi', 'hai', 'hat', 'hau', 'haw', 'heb', 'her', 'hil', 'him', 'hin', 'hit', 'hmn', 'hmo', 'hrv', 'hsb', 'hun', 'hup', 'iba', 'ibo', 'ice', 'ido', 'iii', 'ijo', 'iku', 'ile', 'ilo', 'ina', 'inc', 'ind', 'ine', 'inh', 'ipk', 'ira', 'iro', 'ita', 'jav', 'jbo', 'jpn', 'jpr', 'jrb', 'kaa', 'kab', 'kac', 'kal', 'kam', 'kan', 'kar', 'kas', 'kau', 'kaw', 'kaz', 'kbd', 'kha', 'khi', 'khm', 'kho', 'kik', 'kin', 'kir', 'kmb', 'kok', 'kom', 'kon', 'kor', 'kos', 'kpe', 'krc', 'krl', 'kro', 'kru', 'kua', 'kum', 'kur', 'kut', 'lad', 'lah', 'lam', 'lao', 'lat', 'lav', 'lez', 'lim', 'lin', 'lit', 'lol', 'loz', 'ltz', 'lua', 'lub', 'lug', 'lui', 'lun', 'luo', 'lus', 'mac', 'mad', 'mag', 'mah', 'mai', 'mak', 'mal', 'man', 'mao', 'map', 'mar', 'mas', 'may', 'mdf', 'mdr', 'men', 'mga', 'mic', 'min', 'mis', 'mkh', 'mlg', 'mlt', 'mnc', 'mni', 'mno', 'moh', 'mon', 'mos', 'mul', 'mun', 'mus', 'mwl', 'mwr', 'myn', 'myv', 'nah', 'nai', 'nap', 'nau', 'nav', 'nbl', 'nde', 'ndo', 'nds', 'nep', 'new', 'nia', 'nic', 'niu', 'nno', 'nob', 'nog', 'non', 'nor', 'nqo', 'nso', 'nub', 'nwc', 'nya', 'nym', 'nyn', 'nyo', 'nzi', 'oci', 'oji', 'ori', 'orm', 'osa', 'oss', 'ota', 'oto', 'paa', 'pag', 'pal', 'pam', 'pan', 'pap', 'pau', 'peo', 'phi', 'phn', 'pli', 'pol', 'pon', 'por', 'pra', 'pro', 'pus', 'qaa-qtz', 'que', 'raj', 'rap', 'rar', 'roa', 'roh', 'rom', 'rum', 'run', 'rup', 'rus', 'sad', 'sag', 'sah', 'sai', 'sal', 'sam', 'san', 'sas', 'sat', 'scn', 'sco', 'sel', 'sem', 'sga', 'sgn', 'shn', 'sid', 'sin', 'sio', 'sit', 'sla', 'slo', 'slv', 'sma', 'sme', 'smi', 'smj', 'smn', 'smo', 'sms', 'sna', 'snd', 'snk', 'sog', 'som', 'son', 'sot', 'spa', 'srd', 'srn', 'srp', 'srr', 'ssa', 'ssw', 'suk', 'sun', 'sus', 'sux', 'swa', 'swe', 'syc', 'syr', 'tah', 'tai', 'tam', 'tat', 'tel', 'tem', 'ter', 'tet', 'tgk', 'tgl', 'tha', 'tig', 'tir', 'tiv', 'tkl', 'tlh', 'tli', 'tmh', 'tog', 'ton', 'tpi', 'tsi', 'tsn', 'tso', 'tuk', 'tum', 'tup', 'tur', 'tut', 'tvl', 'twi', 'tyv', 'udm', 'uga', 'uig', 'ukr', 'umb', 'und', 'urd', 'uzb', 'vai', 'ven', 'vie', 'vol', 'vot', 'wak', 'wal', 'war', 'was', 'wen', 'wln', 'wol', 'xal', 'xho', 'yao', 'yap', 'yid', 'yor', 'ypk', 'zap', 'zbl', 'zen', 'zgh', 'zha', 'znd', 'zul', 'zun', 'zxx', 'zza', 'zho']
        self.__languages_in_english = ['Afar', 'Abkhazian', 'Achinese', 'Acoli', 'Adangme', 'Adyghe; Adygei', 'Afro-Asiatic languages', 'Afrihili', 'Afrikaans', 'Ainu', 'Akan', 'Akkadian', 'Albanian', 'Aleut', 'Algonquian languages', 'Southern Altai', 'Amharic', 'English, Old (ca.450-1100)', 'Angika', 'Apache languages', 'Arabic', 'Official Aramaic (700-300 BCE); Imperial Aramaic (700-300 BCE)', 'Aragonese', 'Armenian', 'Mapudungun; Mapuche', 'Arapaho', 'Artificial languages', 'Arawak', 'Assamese', 'Asturian; Bable; Leonese; Asturleonese', 'Athapascan languages', 'Australian languages', 'Avaric', 'Avestan', 'Awadhi', 'Aymara', 'Azerbaijani', 'Banda languages', 'Bamileke languages', 'Bashkir', 'Baluchi', 'Bambara', 'Balinese', 'Basque', 'Basa', 'Baltic languages', 'Beja; Bedawiyet', 'Belarusian', 'Bemba', 'Bengali', 'Berber languages', 'Bhojpuri', 'Bihari languages', 'Bikol', 'Bini; Edo', 'Bislama', 'Siksika', 'Bantu languages', 'Tibetan', 'Bosnian', 'Braj', 'Breton', 'Batak languages', 'Buriat', 'Buginese', 'Bulgarian', 'Burmese', 'Blin; Bilin', 'Caddo', 'Central American Indian languages', 'Galibi Carib', 'Catalan; Valencian', 'Caucasian languages', 'Cebuano', 'Celtic languages', 'Czech', 'Chamorro', 'Chibcha', 'Chechen', 'Chagatai', 'Chinese', 'Chuukese', 'Mari', 'Chinook jargon', 'Choctaw', 'Chipewyan; Dene Suline', 'Cherokee', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', 'Chuvash', 'Cheyenne', 'Chamic languages', 'Montenegrin', 'Coptic', 'Cornish', 'Corsican', 'Creoles and pidgins, English based', 'Creoles and pidgins, French-based', 'Creoles and pidgins, Portuguese-based', 'Cree', 'Crimean Tatar; Crimean Turkish', 'Creoles and pidgins', 'Kashubian', 'Cushitic languages', 'Welsh', 'Dakota', 'Danish', 'Dargwa', 'Land Dayak languages', 'Delaware', 'Slave (Athapascan)', 'German', 'Dogrib', 'Dinka', 'Divehi; Dhivehi; Maldivian', 'Dogri', 'Dravidian languages', 'Lower Sorbian', 'Duala', 'Dutch, Middle (ca.1050-1350)', 'Dutch; Flemish', 'Dyula', 'Dzongkha', 'Efik', 'Egyptian (Ancient)', 'English', 'Ekajuk', 'Greek, Modern (1453-)', 'Elamite', 'English', 'English, Middle (1100-1500)', 'Esperanto', 'Estonian', 'Ewe', 'Ewondo', 'Fang', 'Faroese', 'Persian', 'Fanti', 'Fijian', 'Filipino; Pilipino', 'Finnish', 'Finno-Ugrian languages', 'Fon', 'French', 'French, Middle (ca.1400-1600)', 'French, Old (842-ca.1400)', 'Northern Frisian', 'Eastern Frisian', 'Western Frisian', 'Fulah', 'Friulian', 'Ga', 'Gayo', 'Gbaya', 'Germanic languages', 'Georgian', 'Geez', 'Gilbertese', 'Gaelic; Scottish Gaelic', 'Irish', 'Galician', 'Manx', 'German, Middle High (ca.1050-1500)', 'German, Old High (ca.750-1050)', 'Gondi', 'Gorontalo', 'Gothic', 'Grebo', 'Greek, Ancient (to 1453)', 'Guarani', 'Swiss German; Alemannic; Alsatian', 'Gujarati', "Gwich'in", 'Haida', 'Haitian; Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Herero', 'Hiligaynon', 'Himachali languages; Western Pahari languages', 'Hindi', 'Hittite', 'Hmong; Mong', 'Hiri Motu', 'Croatian', 'Upper Sorbian', 'Hungarian', 'Hupa', 'Iban', 'Igbo', 'Icelandic', 'Ido', 'Sichuan Yi; Nuosu', 'Ijo languages', 'Inuktitut', 'Interlingue; Occidental', 'Iloko', 'Interlingua (International Auxiliary Language Association)', 'Indic languages', 'Indonesian', 'Indo-European languages', 'Ingush', 'Inupiaq', 'Iranian languages', 'Iroquoian languages', 'Italian', 'Javanese', 'Lojban', 'Japanese', 'Judeo-Persian', 'Judeo-Arabic', 'Kara-Kalpak', 'Kabyle', 'Kachin; Jingpho', 'Kalaallisut; Greenlandic', 'Kamba', 'Kannada', 'Karen languages', 'Kashmiri', 'Kanuri', 'Kawi', 'Kazakh', 'Kabardian', 'Khasi', 'Khoisan languages', 'Central Khmer', 'Khotanese; Sakan', 'Kikuyu; Gikuyu', 'Kinyarwanda', 'Kirghiz; Kyrgyz', 'Kimbundu', 'Konkani', 'Komi', 'Kongo', 'Korean', 'Kosraean', 'Kpelle', 'Karachay-Balkar', 'Karelian', 'Kru languages', 'Kurukh', 'Kuanyama; Kwanyama', 'Kumyk', 'Kurdish', 'Kutenai', 'Ladino', 'Lahnda', 'Lamba', 'Lao', 'Latin', 'Latvian', 'Lezghian', 'Limburgan; Limburger; Limburgish', 'Lingala', 'Lithuanian', 'Mongo', 'Lozi', 'Luxembourgish; Letzeburgesch', 'Luba-Lulua', 'Luba-Katanga', 'Ganda', 'Luiseno', 'Lunda', 'Luo (Kenya and Tanzania)', 'Lushai', 'Macedonian', 'Madurese', 'Magahi', 'Marshallese', 'Maithili', 'Makasar', 'Malayalam', 'Mandingo', 'Maori', 'Austronesian languages', 'Marathi', 'Masai', 'Malay', 'Moksha', 'Mandar', 'Mende', 'Irish, Middle (900-1200)', "Mi'kmaq; Micmac", 'Minangkabau', 'Uncoded languages', 'Mon-Khmer languages', 'Malagasy', 'Maltese', 'Manchu', 'Manipuri', 'Manobo languages', 'Mohawk', 'Mongolian', 'Mossi', 'Multiple languages', 'Munda languages', 'Creek', 'Mirandese', 'Marwari', 'Mayan languages', 'Erzya', 'Nahuatl languages', 'North American Indian languages', 'Neapolitan', 'Nauru', 'Navajo; Navaho', 'Ndebele, South; South Ndebele', 'Ndebele, North; North Ndebele', 'Ndonga', 'Low German; Low Saxon; German, Low; Saxon, Low', 'Nepali', 'Nepal Bhasa; Newari', 'Nias', 'Niger-Kordofanian languages', 'Niuean', 'Norwegian Nynorsk; Nynorsk, Norwegian', 'Bokm\x8cl, Norwegian; Norwegian Bokm\x8cl', 'Nogai', 'Norse, Old', 'Norwegian', "N'Ko", 'Pedi; Sepedi; Northern Sotho', 'Nubian languages', 'Classical Newari; Old Newari; Classical Nepal Bhasa', 'Chichewa; Chewa; Nyanja', 'Nyamwezi', 'Nyankole', 'Nyoro', 'Nzima', 'Occitan (post 1500)', 'Ojibwa', 'Oriya', 'Oromo', 'Osage', 'Ossetian; Ossetic', 'Turkish, Ottoman (1500-1928)', 'Otomian languages', 'Papuan languages', 'Pangasinan', 'Pahlavi', 'Pampanga; Kapampangan', 'Panjabi; Punjabi', 'Papiamento', 'Palauan', 'Persian, Old (ca.600-400 B.C.)', 'Philippine languages', 'Phoenician', 'Pali', 'Polish', 'Pohnpeian', 'Portuguese', 'Prakrit languages', 'Proven\x8dal, Old (to 1500);Occitan, Old (to 1500)', 'Pushto; Pashto', 'Reserved for local use', 'Quechua', 'Rajasthani', 'Rapanui', 'Rarotongan; Cook Islands Maori', 'Romance languages', 'Romansh', 'Romany', 'Romanian; Moldavian; Moldovan', 'Rundi', 'Aromanian; Arumanian; Macedo-Romanian', 'Russian', 'Sandawe', 'Sango', 'Yakut', 'South American Indian languages', 'Salishan languages', 'Samaritan Aramaic', 'Sanskrit', 'Sasak', 'Santali', 'Sicilian', 'Scots', 'Selkup', 'Semitic languages', 'Irish, Old (to 900)', 'Sign Languages', 'Shan', 'Sidamo', 'Sinhala; Sinhalese', 'Siouan languages', 'Sino-Tibetan languages', 'Slavic languages', 'Slovak', 'Slovenian', 'Southern Sami', 'Northern Sami', 'Sami languages', 'Lule Sami', 'Inari Sami', 'Samoan', 'Skolt Sami', 'Shona', 'Sindhi', 'Soninke', 'Sogdian', 'Somali', 'Songhai languages', 'Sotho, Southern', 'Spanish', 'Sardinian', 'Sranan Tongo', 'Serbian', 'Serer', 'Nilo-Saharan languages', 'Swati', 'Sukuma', 'Sundanese', 'Susu', 'Sumerian', 'Swahili', 'Swedish', 'Classical Syriac', 'Syriac', 'Tahitian', 'Tai languages', 'Tamil', 'Tatar', 'Telugu', 'Timne', 'Tereno', 'Tetum', 'Tajik', 'Tagalog', 'Thai', 'Tigre', 'Tigrinya', 'Tiv', 'Tokelau', 'Klingon; tlhIngan-Hol', 'Tlingit', 'Tamashek', 'Tonga (Nyasa)', 'Tonga (Tonga Islands)', 'Tok Pisin', 'Tsimshian', 'Tswana', 'Tsonga', 'Turkmen', 'Tumbuka', 'Tupi languages', 'Turkish', 'Altaic languages', 'Tuvalu', 'Twi', 'Tuvinian', 'Udmurt', 'Ugaritic', 'Uighur; Uyghur', 'Ukrainian', 'Umbundu', 'Undetermined', 'Urdu', 'Uzbek', 'Vai', 'Venda', 'Vietnamese', 'Volap\x9fk', 'Votic', 'Wakashan languages', 'Wolaitta; Wolaytta', 'Waray', 'Washo', 'Sorbian languages', 'Walloon', 'Wolof', 'Kalmyk; Oirat', 'Xhosa', 'Yao', 'Yapese', 'Yiddish', 'Yoruba', 'Yupik languages', 'Zapotec', 'Blissymbols; Blissymbolics; Bliss', 'Zenaga', 'Standard Moroccan Tamazight', 'Zhuang; Chuang', 'Zande languages', 'Zulu', 'Zuni', 'No linguistic content; Not applicable', 'Zaza; Dimili; Dimli; Kirdki; Kirmanjki; Zazaki', "Chinese"]


    @property
    def book_id(self) -> int:
        return self.__book_id
    
    @property
    def reading_list_users(self) -> Iterable['User']:
        return iter(self.__reading_list_users)
    
    def add_reading_list_user(self, user: 'User'):
        self.__reading_list_users.append(user)

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        if isinstance(book_title, str):
            book_title = book_title.strip()
            if book_title != "":
                self.__title = book_title
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def image_hyperlink(self) -> str:
        return self.__image_hyperlink

    @image_hyperlink.setter
    def image_hyperlink(self, image_hyperlink: str):
        self.__image_hyperlink = image_hyperlink

    @property
    def reviews(self):
        return self.__reviews

    @property
    def language(self) -> str:
        return self.__language

    @language.setter
    def language(self, book_language: str):
        if isinstance(book_language, str):
            book_language = book_language.strip()
            if book_language != "":
                self.__language = self.__languages_in_english[self.__language_iso_codes.index(book_language)]
            else:
                self.__language = "English"

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        if isinstance(release_year, int) and release_year >= 0:
            self.__release_year = release_year
        else:
            raise ValueError

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description.strip()

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
            publisher.add_book(self)
        else:
            self.__publisher = None

    @property
    def authors(self) -> List[Author]:
        return self.__authors

    def add_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            return

        self.__authors.append(author)

    def remove_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            self.__authors.remove(author)

    @property
    def ebook(self) -> bool:
        return self.__ebook

    @ebook.setter
    def ebook(self, is_ebook: bool):
        if isinstance(is_ebook, bool):
            self.__ebook = is_ebook

    @property
    def num_pages(self) -> int:
        return self.__num_pages

    @num_pages.setter
    def num_pages(self, num_pages: int):
        if isinstance(num_pages, int) and num_pages >= 0:
            self.__num_pages = num_pages

    def add_review(self, review):
        self.__reviews.append(review)

    def __repr__(self):
        return f'<Book {self.title}, book id = {self.book_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.book_id == other.book_id

    def __lt__(self, other):
        return self.book_id < other.book_id

    def __hash__(self):
        return hash(self.book_id)


class Review:

    def __init__(self, book: Book, review_text: str, rating: int, user):
        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        if isinstance(user, User):
            self.__user = user
        else:
            self.__user = None

        if isinstance(review_text, str):
            self.__review_text = review_text.strip()
        else:
            self.__review_text = "N/A"

        if isinstance(rating, int) and rating >= 1 and rating <= 5:
            self.__rating = rating
        else:
            raise ValueError

        self.__timestamp = datetime.now()

    @property
    def user(self):
        return self.__user

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return other.book == self.book and other.review_text == self.review_text \
               and other.rating == self.rating and other.timestamp == self.timestamp

    def __repr__(self):
        return f'<Review of book {self.book}, rating = {self.rating}, timestamp = {self.timestamp}>'


class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or not isinstance(user_name, str):
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

        if password == "" or not isinstance(password, str) or len(password) < 7:
            self.__password = None
        else:
            self.__password = password

        self.__read_books = list()
        self.__reviews = list()
        self.__pages_read = 0
        self.__reading_list: List[Book] = list()

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def read_books(self) -> List[Book]:
        return self.__read_books

    @property
    def reviews(self) -> List[Review]:
        return self.__reviews

    @property
    def reading_list(self) -> List[Book]:
        return self.__reading_list

    def add_to_reading_list(self, book: Book):
        if isinstance(book, Book):
            self.__reading_list.append(book)

    def remove_from_reading_list(self, book: Book):
        if isinstance(book, Book):
            self.__reading_list.remove(book)

    @property
    def pages_read(self) -> int:
        return self.__pages_read

    def read_a_book(self, book: Book):
        if isinstance(book, Book):
            self.__read_books.append(book)
            if book.num_pages is not None:
                self.__pages_read += book.num_pages

    def add_review(self, review: Review):
        if isinstance(review, Review):
            # Review objects are in practice always considered different due to their timestamp.
            self.__reviews.append(review)

    def __repr__(self):
        return f'<User {self.user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.user_name

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)
class BooksInventory:

    def __init__(self):
        self.__books = {}
        self.__prices = {}
        self.__stock_count = {}

    def add_book(self, book: Book, price: int, nr_books_in_stock: int):
        self.__books[book.book_id] = book
        self.__prices[book.book_id] = price
        self.__stock_count[book.book_id] = nr_books_in_stock

    def remove_book(self, book_id: int):
        self.__books.pop(book_id)
        self.__prices.pop(book_id)
        self.__stock_count.pop(book_id)

    def find_book(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__books[book_id]
        return None

    def find_price(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__prices[book_id]
        return None

    def find_stock_count(self, book_id: int):
        if book_id in self.__books.keys():
            return self.__stock_count[book_id]
        return None

    def search_book_by_title(self, book_title: str):
        for book_id in self.__books.keys():
            if self.__books[book_id].title == book_title:
                return self.__books[book_id]
        return None


def make_review(book: Book, review_text: str, rating: int, user: User):
    review = Review(book, review_text, rating, user)
    user.add_review(review)
    book.add_review(review)
    return review