from bs4 import BeautifulSoup
import requests, string

class Event:
    def __init__(self, name, id_name, query):
        self.name = name
        self.id_name = id_name
        self.query = query
    
    class _3x3x3:
        def __init__(self):
            self.name = "3x3x3 Cube"
            self.id_name = "333"
            self.query = ["3x3", "cube", "square", "3x3x3"]
    
    class _2x2x2:
        def __init__(self):
            self.name = "2x2x2 Cube"
            self.id_name = "222"
            self.query = ["2x2", "cube", "square", "2x2x2"]
    
    class _4x4x4:
        def __init__(self):
            self.name = "4x4x4 Cube"
            self.id_name = "444"
            self.query = ["4x4", "cube", "square", "4x4x4"]
    
    class _5x5x5:
        def __init__(self):
            self.name = "5x5x5 Cube"
            self.id_name = "555"
            self.query = ["5x5", "cube", "square", "5x5x5"]
    
    class _6x6x6:
        def __init__(self):
            self.name = "6x6x6 Cube"
            self.id_name = "666"
            self.query = ["6x6", "cube", "square", "6x6x6"]
    
    class _7x7x7:
        def __init__(self):
            self.name = "7x7x7 Cube"
            self.id_name = "777"
            self.query = ["7x7", "cube", "square", "7x7x7"]
    
    class _3x3x3bld:
        def __init__(self):
            self.name = "3x3x3 Blindfolded"
            self.id_name = "333bf"
            self.query = ["3x3", "cube", "square", "3x3x3", "blind", "bld"]
    
    class _3x3x3fmc:
        def __init__(self):
            self.name = "3x3x3 Fewest Moves"
            self.id_name = "333fm"
            self.query = ["3x3", "cube", "square", "3x3x3", "fmc", "fewest", "moves"]
    
    class _3x3x3oh:
        def __init__(self):
            self.name = "3x3x3 One-Handed"
            self.id_name = "333oh"
            self.query = ["3x3", "cube", "square", "3x3x3", "oh", "one", "handed"]
    
    class _3x3x3ft: # Rip feet lol
        def __init__(self):
            self.name = "3x3x3 With Feet"
            self.id_name = "333ft"
            self.query = ["3x3", "cube", "square", "3x3x3", "feet", "rip", "toe", "fetish"]
    
    class clock:
        def __init__(self):
            self.name = "Clock"
            self.id_name = "clock"
            self.query = ["clock", "clk", "cloncc"]
    
    class megaminx:
        def __init__(self):
            self.name = "Megaminx"
            self.id_name = "minx"
            self.query = ["mega", "minx", "hexagon"]
    
    class square1:
        def __init__(self):
            self.name = "Square-1"
            self.id_name = "sq1"
            self.query = ["sq", "square", "squan", "1"]
    
    class _4x4x4bld:
        def __init__(self):
            self.name = "4x4x4 Blindfolded"
            self.id_name = "444bf"
            self.query = ["4x4", "cube", "square", "4x4x4", "blind", "bld"]
    
    class _5x5x5bld:
        def __init__(self):
            self.name = "5x5x5 Blindfolded"
            self.id_name = "555bf"
            self.query = ["5x5", "cube", "square", "5x5x5", "blind", "bld"]
    
    class _3x3x3mbld:
        def __init__(self):
            self.name = "3x3x3 Multi-Blind"
            self.id_name = "333mbf"
            self.query = ["3x3", "cube", "square", "3x3x3", "multi", "mbld", "bld", "blind"]
    
    class pyraminx:
        def __init__(self):
            self.name = "Pyraminx"
            self.id_name = "pyram"
            self.query = ["pyra", "minx", "triangle"]
    
    class skewb:
        def __init__(self):
            self.name = "Skewb"
            self.id_name = "skewb"
            self.query = ["skewb"]
    
    class EventNotFoundException(Exception):
        pass
    
    @staticmethod
    def get_event(event_id):
        """ Return the object for the event_id """

        event_classes = [getattr(Event, e) for e in dir(Event) if not e.startswith("__") and e != "get_event" and e != "EventNotFoundException"]

        for i in event_classes:
            if i().id_name == event_id.lower():
                return i
        
        raise Event.EventNotFoundException(f"Could not locate the object for '{event_id}'")

class Utils:
    @staticmethod
    def is_wca_id(s : str):
        """ Determines if a string is a valid WCA id or is a name """

        wca_id = "####AAAA##"
        for i, _i in zip(s, wca_id):
            if _i == "#":
                if i in string.digits:
                    continue
                else:
                    return False
            if _i == "A":
                if i in string.ascii_letters:
                    continue
                else:
                    return False
        return True

class User:
    def __init__(self, wca_id, name, country, gender, comp_count, completed_solves, avatar, personal_records, medal_collection):
        self.wca_id = wca_id
        self.name = name
        self.country = country
        self.gender = gender
        self.comp_count = comp_count
        self.completed_solves = completed_solves
        self.personal_records = personal_records
        self.medal_collection = medal_collection
        self.avatar = avatar
    
    class PersonalRecord:
        def __init__(self, event, nr_single, cr_single, wr_single, single, average, wr_average, cr_average, nr_average):
            self.event = event
            self.nr_single = nr_single
            self.cr_single = cr_single
            self.wr_single = wr_single
            self.single = single
            self.average = average
            self.wr_average = wr_average
            self.cr_average = cr_average
            self.nr_average = nr_average
    
    class Medals:
        def __init__(self, gold, silver, bronze, wr, cr, nr):
            self.gold = gold
            self.silver = silver
            self.bronze = bronze
            self.wr = wr
            self.cr = cr
            self.nr = nr

    @staticmethod
    def from_page(url):
        """ Download the contents at the URL and create a User object """

        web_data = requests.get(url, headers={"User-Agent": "WCA Discord Bot"})
        web_data = BeautifulSoup(web_data.content, 'html.parser')

        name = web_data.findAll("div", {"id": "person"})[0].findAll("h2")[0].text.strip()
        try:
            avatar = web_data.findAll("img", {"class": "avatar"})[0]['src']
        except IndexError:
            avatar = "https://www.worldcubeassociation.org/assets/missing_avatar_thumb-f0ea801c804765a22892b57636af829edbef25260a65d90aaffbd7873bde74fc.png"
        country = [web_data.findAll("td", {"class": "country"})[0].contents[0]['class'][1].replace("flag-icon-", ""), web_data.findAll("td", {"class": "country"})[0].text.strip()]
        wca_id = web_data.findAll("tbody")[0].findAll("td")[1].text.strip()
        gender = web_data.findAll("tbody")[0].findAll("td")[2].text.strip()
        comp_count = web_data.findAll("tbody")[0].findAll("td")[3].text.strip()
        completed_solves = web_data.findAll("tbody")[0].findAll("td")[4].text.strip()

        # Create personal records
        personal_records = []
        pr_table = web_data.findAll("tbody")[1].findAll("tr")

        for i in pr_table:
            event = Event.get_event(i.findAll("td", {"class": "event"})[0]['data-event'])
            nr_single = i.findAll("td", {"class": "country-rank"})[0].text.strip()
            cr_single = i.findAll("td", {"class": "continent-rank"})[0].text.strip()
            wr_single = i.findAll("td", {"class": "world-rank"})[0].text.strip()
            single = i.findAll("td", {"class": "single"})[0].text.strip()
            average = i.findAll("td", {"class": "average"})[0].text.strip()
            nr_average = i.findAll("td", {"class": "country-rank"})[1].text.strip()
            cr_average = i.findAll("td", {"class": "continent-rank"})[1].text.strip()
            wr_average = i.findAll("td", {"class": "world-rank"})[1].text.strip()

            pr_object = User.PersonalRecord(event, nr_single, cr_single, wr_single, single, average, nr_average, cr_average, wr_average)
            personal_records.append(pr_object)
        
        # Create medal collection
        try:
            medal_div = web_data.findAll("div", {"class": "col-md-6 medal-collection"})[0].findAll("tbody")[0].findAll("td")
            gold = medal_div[0].text.strip()
            silver = medal_div[1].text.strip()
            bronze = medal_div[2].text.strip()
        except IndexError:
            gold = 0
            silver = 0
            bronze = 0

        try:
            record_div = web_data.findAll("div", {"class": "col-md-6 record-collection"})[0].findAll("tbody")[0].findAll("td")
            wr = record_div[0].text.strip()
            cr = record_div[1].text.strip()
            nr = record_div[2].text.strip()
        except IndexError:
            wr = 0
            cr = 0
            nr = 0

        medal_collection = User.Medals(gold, silver, bronze, wr, cr, nr)

        user_object = User(wca_id, name, country, gender, comp_count, completed_solves, avatar, personal_records, medal_collection)
        return user_object