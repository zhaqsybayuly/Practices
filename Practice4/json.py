import json

# load the sample JSON file
with open("exercices/json/sample-data.json", "r") as f:
    data = json.load(f)

# print header
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':>7} {'MTU':>6}")
print(f"{'-' * 50} {'-' * 20}  {'-' * 6}  {'-' * 6}")

# go through every interface in imdata and print its dn, description, speed and mtu
for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    dn = attrs["dn"]
    descr = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]
    print(f"{dn:<50} {descr:<20} {speed:>7} {mtu:>6}")
