from genericpath import isfile
import json
from ntpath import join
from os import listdir, remove


visas_location = "./visas/"


def load_files():
    visa_countries = {}
    visa_files = [f for f in listdir(visas_location) if isfile(join(visas_location, f))]
    for filename in visa_files:
        if filename.endswith(".visas.json"):
            with open(visas_location + filename, "r") as r:
                visa_country_inst = json.loads(r.read())
                visa_countries[visa_country_inst["csvcid"]] = visa_country_inst
    
    return visa_countries

def save_files(visa_countries):
    for csvc in visa_countries:
        with open(visas_location + csvc + ".visas.json", "w") as w:
            w.write(json.dumps(visa_countries[csvc], sort_keys=True, indent=4, separators=(',', ': ')))

def remove_csvcid(csvcid):
    remove(visas_location + csvcid + ".visas.json")
        

class tools:
    def __init__(self):
        pass

    class countries:
        visa_countries = {}
        def __init__(self, args):
            self.visa_countries = load_files()

            print(args)

            if args.subcommand == "add":
                self.add(args.csvc, args.name, args.cca2, args.cca3, args.ccn3)

            if args.subcommand == "remove":
                self.remove(args.csvc)


            if args.subcommand == "contains":
                if not self.contains(args.csvc, args.cca2, args.cca3):
                    print("Visas country does not exists!")
                else:
                    print("Visas country exists!")

        def add(self, csvcid, name="", cca2="", cca3="", ccn3=""):
            if csvcid in self.visa_countries:
                raise Exception(f"Can not add {csvcid}. It already exists")
            
            new_country = {
                "cca2": cca2,
                "cca3": cca3,
                "ccn3": ccn3,
                "csvcid": csvcid,
                "jurisdiction": "state",
                "name": name,
                "requirements": {}
            }

            new_visa_req = {
                "additional_requirements": {
                    "passport_blank_pages": 2,
                    "passport_expiry_months": 3
                },
                "conflicts": [],
                "note": "",
                "requirement": "required",
                "stay_length": {}
            }

            for key in self.visa_countries:
                new_country["requirements"][key] = new_visa_req
                self.visa_countries[key]["requirements"][csvcid] = new_visa_req

            self.visa_countries[csvcid] = new_country

            save_files(self.visa_countries)

        def remove(self, csvcid, force = False):
            if csvcid not in self.visa_countries and not force:
                raise Exception(f"Can not delete {csvcid}. Does not exists!")       

            for key in self.visa_countries:
                if csvcid in self.visa_countries[key]["requirements"]:
                    del self.visa_countries[key]["requirements"][csvcid]

            del self.visa_countries[csvcid]

            remove_csvcid(csvcid)
            save_files(self.visa_countries)
            
        def contains(self, csvcid="", cca2="", cca3=""):
            if csvcid != "":
                return self.visa_countries[csvcid] != None

            if cca2 != "" or cca3 != "":
                for key in self.visa_countries:
                    if cca2 != "" and self.visa_countries[key]["cca2"] is cca2:
                        return True

                    if cca3 != "" and self.visa_countries[key]["cca3"] is cca3:
                        return True

            return False
    class visa:
        def __init__(self, args):
            pass