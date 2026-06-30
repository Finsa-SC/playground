
print("========================= Add and update value =======================")
device = {
  "ip": "192.168.1.1",
  "port_open": (80, 443),
  "status": "up",
  "ping": 6.54, #ms
}

device['waf'] = "cloudflare"
device.update({
  'os': 'Linux',
  'ttl': 64,
})
print(device)

print("\n\n========================= Delete value =======================")
user_data = dict(name="agus", age=12, married=False)
print(f"Before: {user_data}")
# del user_data['name']
user_data.pop('name')
print(f"After : {user_data}")


print("\n\n========================= access dict =======================")
data_dict = dict(font="Fira Code", size=12, color="black")
for key, value in data_dict.items():
  print(f"{key:<10}{value}") 


#print("\033[H\033[J", end="")
print("\n\n========================= Nested dict =======================")
agus   = dict(age=13, country='Indonesia',   married=False)
rahmat = dict(age=45, country='Netherlands', married=True)
joko   = dict(age=25, country='Indonesia',   married=False)

name = {}

name['Agus'] = agus
name['Rahmat'] = rahmat
name['Joko'] = joko

for key, value in name.items():
  print(f"{key}: {value.get('age')}")

print("\n\n========================= Merge Dict =======================")
food = {
  'burgers': 2,
  'potato': 1,
  'kfc': 3,
}
baverage = {
  'water': 1,
  'cola': 2,
}
merge = food | baverage # Using union

food.update(baverage) # Using update
print(food)
print(merge)
