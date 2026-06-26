
print("========================= Add and update value =======================")
device = {
  "ip": "192.168.1.1",
  "port_open": (80, 443),
  "status": "up",
  "ping": 6.54, #ms
}

device['waf'] = "cloudflare"
device['waf'] = ""
print(device)

print("\n\n========================= Delete value =======================")
user_data = dict(name="agus", age=12, married=False)
#user_data.del('name')
user_data.pop('name')
print(user_data)


print("\n\n========================= access dict =======================")
data_dict = dict(font="Fira Code", size=12, color="black")
for key, value in data_dict.items():
  print(f"{key:<10}{value}") 


print("\033[H\033[J", end="")
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
