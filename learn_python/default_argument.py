# Nilai dari default parameter tidak hilang selama fungsi masih ada


def defaults(item = "noname", lst= []):
  lst.append(item)
  return lst

print(defaults("agus"))
print(defaults("rahmat"))
print(defaults.__defaults__)



def logger(name, cache= set()):
  cache.add(name)
  return cache

print(logger("joko"))
print(logger("joko"))
print(logger('budianto'))
