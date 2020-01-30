from bs4 import BeautifulSoup
import requests, string, urllib

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
            self.priority = True
    
    class _2x2x2:
        def __init__(self):
            self.name = "2x2x2 Cube"
            self.id_name = "222"
            self.query = ["2x2", "cube", "square", "2x2x2"]
            self.priority = False
    
    class _4x4x4:
        def __init__(self):
            self.name = "4x4x4 Cube"
            self.id_name = "444"
            self.query = ["4x4", "cube", "square", "4x4x4"]
            self.priority = False
    
    class _5x5x5:
        def __init__(self):
            self.name = "5x5x5 Cube"
            self.id_name = "555"
            self.query = ["5x5", "cube", "square", "5x5x5"]
            self.priority = False
    
    class _6x6x6:
        def __init__(self):
            self.name = "6x6x6 Cube"
            self.id_name = "666"
            self.query = ["6x6", "cube", "square", "6x6x6"]
            self.priority = False
    
    class _7x7x7:
        def __init__(self):
            self.name = "7x7x7 Cube"
            self.id_name = "777"
            self.query = ["7x7", "cube", "square", "7x7x7"]
            self.priority = False
    
    class _3x3x3bld:
        def __init__(self):
            self.name = "3x3x3 Blindfolded"
            self.id_name = "333bf"
            self.query = ["3x3", "cube", "square", "3x3x3", "blind", "bld"]
            self.priority = False
    
    class _3x3x3fmc:
        def __init__(self):
            self.name = "3x3x3 Fewest Moves"
            self.id_name = "333fm"
            self.query = ["3x3", "cube", "square", "3x3x3", "fmc", "fewest", "moves"]
            self.priority = False
    
    class _3x3x3oh:
        def __init__(self):
            self.name = "3x3x3 One-Handed"
            self.id_name = "333oh"
            self.query = ["3x3", "cube", "square", "3x3x3", "oh", "one", "handed"]
            self.priority = False
    
    class _3x3x3ft: # Rip feet lol
        def __init__(self):
            self.name = "3x3x3 With Feet"
            self.id_name = "333ft"
            self.query = ["3x3", "cube", "square", "3x3x3", "feet"]
            self.priority = False
    
    class clock:
        def __init__(self):
            self.name = "Clock"
            self.id_name = "clock"
            self.query = ["clock", "clk", "cloncc"]
            self.priority = False
    
    class megaminx:
        def __init__(self):
            self.name = "Megaminx"
            self.id_name = "minx"
            self.query = ["mega", "minx", "hexagon"]
            self.priority = False
    
    class square1:
        def __init__(self):
            self.name = "Square-1"
            self.id_name = "sq1"
            self.query = ["sq", "square", "squan", "1"]
            self.priority = False
    
    class _4x4x4bld:
        def __init__(self):
            self.name = "4x4x4 Blindfolded"
            self.id_name = "444bf"
            self.query = ["4x4", "cube", "square", "4x4x4", "blind", "bld"]
            self.priority = False
    
    class _5x5x5bld:
        def __init__(self):
            self.name = "5x5x5 Blindfolded"
            self.id_name = "555bf"
            self.query = ["5x5", "cube", "square", "5x5x5", "blind", "bld"]
            self.priority = False
    
    class _3x3x3mbld:
        def __init__(self):
            self.name = "3x3x3 Multi-Blind"
            self.id_name = "333mbf"
            self.query = ["3x3", "cube", "square", "3x3x3", "multi", "mbld", "bld", "blind"]
            self.priority = False
    
    class pyraminx:
        def __init__(self):
            self.name = "Pyraminx"
            self.id_name = "pyram"
            self.query = ["pyra", "minx", "triangle"]
            self.priority = False
    
    class skewb:
        def __init__(self):
            self.name = "Skewb"
            self.id_name = "skewb"
            self.query = ["skewb"]
            self.priority = False
    
    class EventNotFoundException(Exception):
        pass
    
    @staticmethod
    def get_event(event_id):
        """ Return the object for the event_id """

        event_classes = [getattr(Event, e) for e in dir(Event) if not e.startswith("__") and e not in ["get_event", "EventNotFoundException", "query_event"]]

        for i in event_classes:
            if i().id_name == event_id.lower():
                return i
        
        raise Event.EventNotFoundException(f"Could not locate the object for '{event_id}'")

    @staticmethod
    def query_event(query_string):
        """ Using the query strings of the objects to find an object """

        event_classes = [getattr(Event, e) for e in dir(Event) if not e.startswith("__") and e not in ["get_event", "EventNotFoundException", "query_event"]]
        event_rank = []

        for i in event_classes:
            ranking = 0

            for search_key in i().query:
                if search_key in query_string:
                    ranking += 1
            
            event_rank.append([(ranking / len(i().query)), i])
        
        find_first_item = lambda x: x[0]
        event_rank.sort(key = find_first_item, reverse = True)

        return event_rank[0][1]

class RankingHook:
    def __init__(self, hook_object, track):
        self.hook_object = hook_object
        self.track = track # This will later be used for tracking particular elements, rather than only tracking the name and result of the first place of the hook_object.

        self.current_result_schema = self.hook_object.results
    
    def get_changes(self):
        new_results = self.hook_object.update()

        if self.current_result_schema[0].name != new_results[0].name or self.current_result_schema[0].result != new_results[0].result:
            return new_results[0]
        
        return False
        

class Ranking:
    def __init__(self, event, area = "world", ranking_type = "single"):
        self.event = event()
        self.area = area
        self.ranking_type = ranking_type

        self.url = f"https://www.worldcubeassociation.org/results/rankings/{self.event.id_name}/{self.ranking_type}?region={self.area}"
        self.request = requests.get(self.url, headers = {"User-Agent": "WCA Discord Bot"})
        self.page = BeautifulSoup(self.request.content, "html.parser")

        table = self.page.findAll("tbody")[0].findAll("tr")
        self.results = []
        for i in table:
            pos = i.findAll("td", {"class": "pos"})[0].text.strip()
            name = i.findAll("td", {"class": "name"})[0].text.strip()
            wca_id = i.findAll("td", {"class": "name"})[0].findAll("a")[0]['href'].replace("/persons/", "").strip()
            result = i.findAll("td", {"class": "result"})[0].text.strip()
            country = [i.findAll("td", {"class": "country"})[0].findAll("span")[0]['class'][1].replace('flag-icon-', ''), i.findAll("td", {"class": "country"})[0].text.strip()]
            competition = i.findAll("td", {"class": "competition"})[0].findAll("a")[0]['href'].replace('/competitions/', '')

            self.results.append(Ranking.Result(pos, name, result, country, competition, wca_id))
        
    def update(self):
        self.request = requests.get(self.url, headers = {"User-Agent": "WCA Discord Bot"})
        self.page = BeautifulSoup(self.request.content, "html.parser")

        table = self.page.findAll("tbody")[0].findAll("tr")
        self.results = []
        for i in table:
            pos = i.findAll("td", {"class": "pos"})[0].text.strip()
            name = i.findAll("td", {"class": "name"})[0].text.strip()
            wca_id = i.findAll("td", {"class": "name"})[0].findAll("a")[0]['href'].replace("/persons/", "").strip()
            result = i.findAll("td", {"class": "result"})[0].text.strip()
            country = [i.findAll("td", {"class": "country"})[0].findAll("span")[0]['class'][1].replace('flag-icon-', ''), i.findAll("td", {"class": "country"})[0].text.strip()]
            competition = i.findAll("td", {"class": "competition"})[0].findAll("a")[0]['href'].replace('/competitions/', '')

            self.results.append(Ranking.Result(pos, name, result, country, competition, wca_id))
        
        return self.results
    
    class Result:
        def __init__(self, pos, name, result, country, competiton, wca_id):
            self.position = pos
            self.name = name
            self.result = result
            self.country = country
            self.competiton = competiton
            self.wca_id = wca_id

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

class Search:
    def __init__(self, query):
        self.query = query
        self.url = f"https://www.worldcubeassociation.org/search?q={urllib.parse.quote(query)}"
        self.request = requests.get(self.url, headers={"User-Agent": "WCA Discord Bot"})
        self.page = BeautifulSoup(self.request.content, "html.parser")
        
        # Get person results
        self.user_result = []
        for i in self.page.findAll("tbody")[0].findAll("tr"):
            try:
                avatar = i.findAll("div")[0]['data-content'].replace('<img src=\'', '').replace('\'></img>', '')
            except KeyError:
                avatar = "https://www.worldcubeassociation.org/assets/missing_avatar_thumb-f0ea801c804765a22892b57636af829edbef25260a65d90aaffbd7873bde74fc.png"
            wca_id = i.findAll("td")[1].text.strip()
            name = i.findAll("td")[2].text.strip()
            country = i.findAll("td")[3].text.strip()

            self.user_result.append(Search.User(wca_id, name, country, avatar))
    
    class User:
        def __init__(self, wca_id, name, country, avatar):
            self.wca_id = wca_id
            self.name = name
            self.country = country
            self.avatar = avatar
            
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
    def best_event(event_pb, ranking):
        low_i = 999999999999999999
        low_e = None

        for i in event_pb:
            try:
                if int(getattr(i, ranking)) < low_i:
                    low_i = int(getattr(i, ranking))
                    low_e = i
            except ValueError:
                pass
        return low_e

    @staticmethod
    def worst_event(event_pb, ranking):
        low_i = 0
        low_e = None

        for i in event_pb:
            try:
                if getattr(i, ranking) < low_i:
                    low_i = getattr(i, ranking)
                    low_e = i
            except:
                pass
        return low_e


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