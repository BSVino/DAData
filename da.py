def get_da_version_name(da_version):
  if da_version == 0:
    return "Omega"
  if da_version == 1:
    return "Delta and Epsilon"
  if da_version == 2:
    return "Zeta"
  if da_version == 3:
    return "Kappa"

def get_weapon_name(weapon_id, da_version):
  if da_version < 2:
    weapons = [
      'none',
      'fal',
      'mossberg',
      'mac10',
      'mp5k',
      'm1911',
      'beretta',
      'crowbar',
      'grenade',
      'brawl',
      'akimbo_m1911',
      'akimbo_beretta',
      'm16'
    ]
    return weapons[weapon_id]
  elif da_version >= 2 and da_version <= 3:
    weapons = [
      'none',
      'fal',
      'mossberg',
      'm16',
      'mac10',
      'mp5k',
      'akimbo_m1911',
      'akimbo_beretta',
      'm1911',
      'beretta',
      'grenade',
      'brawl',
    ]
    return weapons[weapon_id]
  else:
    return 'unknown'

def get_weapon_print_name(name):
  if name == 'akimbo_m1911':
    return 'Akimbo Stallions'
  if name == 'akimbo_beretta':
    return 'Akimbo Sentinels'
  if name == 'm1911':
    return 'Stallion 45'
  if name == 'beretta':
    return 'Sentinel 9'
  if name == 'mp5k':
    return 'Undertaker'
  if name == 'mac10':
    return 'Mac Daddy'
  if name == 'mossberg':
    return 'Persuader'
  if name == 'fal':
    return 'Vindicator'
  if name == 'm16':
    return 'Black Magic'
  if name == 'grenade':
    return 'H.E. Grenade'
  if name == 'brawl':
    return 'Brawl'

  return name

def get_character_print_name(name):
  if name == 'wish':
    return 'Vice'
  if name == 'frank':
    return 'Deisel'
  if name == 'eightball':
    return 'Eightball'
  if name == 'bomber':
    return 'Bomber'

  return name

