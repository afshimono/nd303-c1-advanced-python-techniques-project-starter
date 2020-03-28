class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.orbit_set = set()
        self.id = kwargs.get('id', None)
        if not self.id:
            raise Exception('No id for NEO!')
        self.name = kwargs.get('name', None)
        self.nasa_jpl_url = kwargs.get('nasa_jpl_url', None)
        self.is_potentially_hazardous_asteroid = kwargs.get('is_potentially_hazardous_asteroid', None)
        self.diameter_min_km = kwargs.get('estimated_diameter_min_kilometers', None)
        self.diameter_max_km = kwargs.get('estimated_diameter_max_kilometers', None)


    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?
        self.orbit_set.add(orbit)
        orbit.update_neos(self)

    def get_orbits(self):
        '''
        Returns the set of orbit objects
        '''
        return self.orbit_set


class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.neo_set = set()
        self.close_approach_date = kwargs.get('close_approach_date')
        self.close_approach_date_full = kwargs.get('close_approach_date_full')
        self.miss_distance_kilometers = kwargs.get('miss_distance_kilometers')
        self.orbiting_body = kwargs.get('orbiting_body')
        self.kilometers_per_second = kwargs.get('kilometers_per_second')

    def update_neos(self, neo_obj: NearEarthObject):
        """
        Adds the id to the set of NEO Ids
        """
        self.neo_set.add(neo_obj)

