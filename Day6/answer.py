class OrbitalMap(object):
    """docstring for OrbitalMap"""

    def __init__(self, link_list):
        super(OrbitalMap, self).__init__()
        
        self.orbital_map = {}
        self.orbital_map_parent = {}
        # Create dict of links
        # dict[A] = list of planets that orbit around A
        for link in link_list:
            tmp_orbit = link.split(")")
            center = tmp_orbit[0]
            orbital = tmp_orbit[1]

            self.orbital_map_parent[orbital] = center
            if not center in self.orbital_map:
                self.orbital_map[center] = [orbital]
            else:
                self.orbital_map[center].append(orbital)

            if not orbital in self.orbital_map:
                self.orbital_map[orbital] = []

        self.num_orbits = {}
        # Assume the existence of COM
        self.compute_num_orbits_rec('COM', -1)

    def compute_num_orbits_rec(self, center: str, num_orbit_parent: int=0):
        """
        Compute number of orbits for center based on the planet it orbits
        around and update children.
        """
        self.num_orbits[center] = num_orbit_parent + 1
        for tmp_orbit in self.orbital_map[center]:
            self.compute_num_orbits_rec(tmp_orbit, self.num_orbits[center])

    def sum_orbitals(self) -> int:
        """
        Return sum of orbitals
        """
        return sum(self.num_orbits.values())

    def dist(self, source: str, dest: str) -> int:
        """
        Return transfer distance for two objects to orbit around
        the same object.
        """
        adress_source = self.adress(source)
        adress_dest = self.adress(dest)
        # -3 to account for 'source', 'dest' and first planet of 'source'
        # +1 to account for first common ancestor lost 
        return len(set(adress_source).symmetric_difference(adress_dest)) - 2



    def adress(self, center: str) -> list:
        """
        Return list of orbits of the center, giving its 'adress' in the map.
        """
        if center == 'COM':
            return ['COM']
        else:
            return self.adress(self.orbital_map_parent[center]) + [center]


if __name__ == '__main__':
    with open("input.csv", mode='r') as input_file:

        test_link_list = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L"
        ]
        test_orbital_map = OrbitalMap(test_link_list)
        assert test_orbital_map.sum_orbitals() == 42

        links = input_file.read().split('\n')
        orbital_map = OrbitalMap(links)
        print("Answer 6.1: ", orbital_map.sum_orbitals())


        test_transfer_list = [
            "COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L",
            "K)YOU",
            "I)SAN"
        ]
        test_transfer_orbital_map = OrbitalMap(test_transfer_list)
        assert test_transfer_orbital_map.dist('YOU', 'SAN') == 4

        print("Answer 6.2: ", orbital_map.dist('YOU', 'SAN'))