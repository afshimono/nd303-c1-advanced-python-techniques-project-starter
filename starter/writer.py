from enum import Enum
from models import NearEarthObject, OrbitPath


class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        pass

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting output e.g. filename
        :return: bool representing if write successful or not
        """
        # TODO: Using the OutputFormat, how can we organize our 'write' logic for output to stdout vs to csvfile
        # TODO: into instance methods for NEOWriter? Write instance methods that write() can call to do the necessary
        # TODO: output format.
        try:
            if format == OutputFormat.display.value:
                for item in data:
                    if isinstance(item, NearEarthObject):
                        self.__print_neo(item)
                    elif isinstance(item, OrbitPath):
                        self.__print_orb(item) 
            elif format == OutputFormat.csv_file.value:
                pass          
            return True
        except:
            return False
        


    def __print_neo(self, neo_obj: NearEarthObject):
        print(f"Id: {neo_obj.id}  Hazardous: {neo_obj.is_potentially_hazardous_asteroid} \
Min Diam: {neo_obj.diameter_min_km} Max Diam: {neo_obj.diameter_max_km}")

    def __print_orb(self, orb_obj: OrbitPath):
        print(f"Approach date: {orb_obj.close_approach_date}  Miss Dist: {orb_obj.miss_distance_kilometers} \
Orbit Body: {orb_obj.orbiting_body}  Km/s: {orb_obj.kilometers_per_second}")

