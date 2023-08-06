from __future__ import unicode_literals
import sys

from pogoiv.data import get_csv

from pogoiv.poke_data_error import PokeDataError

class BaseStats:
    BASE_ATTACK = 'base_attack'
    BASE_DEFENSE = 'base_defense'
    BASE_STAMINA = 'base_stamina'

    def __init__(self):
        self._stats = self._load_stats()

    def _load_stats(self):
        reader = get_csv('base_stats.tsv')

        stats = {}
        for index, row in enumerate(reader):
            if index == 0:
                continue
            name, attack, defense, stamina = row
            stats[self._utf8ify(name.lower())] = {
                self.BASE_ATTACK: int(attack),
                self.BASE_DEFENSE: int(defense),
                self.BASE_STAMINA: int(stamina)
            }
        return stats

    def get_base_stats(self, pokemon_name):
        self.validate_pokemon(pokemon_name)
        return self._stats[self._utf8ify(pokemon_name.lower())]

    def _utf8ify(self, input_string):
        if sys.version_info < (3, 0):
            if not isinstance(input_string, unicode):
                input_string = input_string.decode('utf-8')
        return input_string

    def validate_pokemon(self, pokemon_name):
        if self._utf8ify(pokemon_name.lower()) not in self._stats:
            raise PokeDataError("Could not find Pokemon matching: {}".format(pokemon_name))
