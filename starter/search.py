from collections import namedtuple, defaultdict
from enum import Enum
from datetime import datetime
from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath
from functools import reduce


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?
        self.date = kwargs.get('date',None)
        self.start_date = kwargs.get('start_date',None)
        self.end_date = kwargs.get('end_date',None)
        self.number = kwargs.get('number',None)
        self.return_object = kwargs.get('return_object',None)
        self.filter = kwargs.get('filter',None)

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        if self.date:
            this_date_search = self.DateSearch(type=DateSearch.equals, values=self.date)
        elif self.start_date and self.end_date:
            this_date_search = self.DateSearch(type=DateSearch.between, values=[self.start_date, self.end_date])
        
        result = Query.Selectors(number=self.number, return_object=self.return_object, date_search=this_date_search, filters=self.filter)
        return result

class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        "diameter":["diameter_min_km", "diameter_max_km"],
        "is_hazardous": "is_potentially_hazardous_asteroid",
        "distance": "miss_distance_kilometers"
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
        "=":"get_equals",
        ">":"get_gt",
        "<":"get_sm"
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options, object):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """

        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        result = defaultdict(list)
        for filter_item in filter_options:
            filter_item_list = filter_item.split(":")
            result[object] = Filter(filter_item_list[0],object,filter_item_list[1],filter_item_list[2])
        return result

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
        if query.date_search.type == DateSearch.between:
            candidate_list = self.date_between(query.date_search.values, query.return_object, self.db.orbit_dict)
        elif query.date_search.type == DateSearch.equals:
            candidate_list = self.date_equals(query.date_search.values, query.return_object, self.db.orbit_dict)
        return candidate_list[:query.number]


    def date_equals(self, date: str, return_type: str, orbit_dict: dict):
        result = []
        base_date = datetime.strptime(date, "%Y-%m-%d")
        for key in orbit_dict.keys():
            try:
                this_date = datetime.strptime(key, "%Y-%b-%d %H:%M").replace(hour=0, minute=0)
            except:
                print(f"Failed to load {key}")
                continue
            if base_date == this_date:
                result.append(orbit_dict[key])
        if return_type == "Path":
            return result
        else:
            neo_set = set()
            neo_set = [x.neo_set for neo_list in result for x in neo_list.values()]
            neo_set = reduce(lambda x,y: x.union(y), neo_set)
            return [self.db.neo_dict[x] for x in neo_set]

    def date_between(self, date: list, return_type: str, orbit_dict: dict):
        result = []
        start_date = datetime.strptime(date[0], "%Y-%m-%d")
        end_date = datetime.strptime(date[1], "%Y-%m-%d")
        for key in orbit_dict.keys():
            try:
                this_date = datetime.strptime(key, "%Y-%b-%d %H:%M").replace(hour=0, minute=0)
            except:
                print(f"Failed to load {key}")
                continue
            if this_date >= start_date and this_date <= end_date:
                result.append(orbit_dict[key])
        if return_type == "Path":
            return result
        else:
            neo_set = set()
            neo_set = [x.neo_set for neo_list in result for x in neo_list.values()]
            neo_set = reduce(lambda x,y: x.union(y), neo_set)
            return [self.db.neo_dict[x] for x in neo_set]
             