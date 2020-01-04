import re

class GameShark:

    def __init__(self):
        self.cheats = {}
        try:
            with open('gameshark.txt','r') as cheat_list:
                for line in cheat_list.readlines():
                    if re.match('^[0-9a-f]{8}\s*$',line.lower()):
                        address = ( int('0x'+line[4:6].lower(),16) ) | ( int('0x'+line[6:8].lower(),16) << 8 )
                        value = int('0x'+line[2:4].lower(),16)
                        self.cheats[address] = value
        except:
            pass
        self.cheats_enabled = len(self.cheats) != 0

