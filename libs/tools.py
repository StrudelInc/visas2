from genericpath import isfile
import json
from ntpath import join
from os import listdir, remove
from geojson_rewind import rewind

visas_location = "./visas/"

countries_location = "./countries/countries.json"
data_location = "./countries/data/"

def load_visas():
    visa_countries = {
        "csvcid": {},
        "cca2": {},
        "cca3": {}
    }
    visa_files = [f for f in listdir(visas_location) if isfile(join(visas_location, f))]
    for filename in visa_files:
        if filename.endswith(".visas.json"):
            with open(visas_location + filename, "r") as r:
                visa_country_inst = json.loads(r.read())
                visa_countries["csvcid"][visa_country_inst["csvcid"]] = visa_country_inst

                if visa_country_inst["cca2"] != "":
                    visa_countries["cca2"][visa_country_inst["cca2"]] = visa_country_inst

                if visa_country_inst["cca3"] != "":
                    visa_countries["cca3"][visa_country_inst["cca3"]] = visa_country_inst

    return visa_countries

def save_visas(visa_countries):
    for csvcid in visa_countries["csvcid"]:
        with open(visas_location + csvcid + ".visas.json", "w") as w:
            w.write(json.dumps(visa_countries["csvcid"][csvcid], sort_keys=True, indent=4, separators=(',', ': ')))

def remove_csvc_csvcid(csvcid):
    remove(visas_location + csvcid + ".visas.json")

def load_geo():
    geo_countries = {
        "csvcid": {},
        "cca2": {},
        "cca3": {}
    }

    geo_files = [f for f in listdir(data_location) if isfile(join(data_location, f)) and f.endswith("geo.json")]
    for filename in geo_files:
        try:
            with open(data_location + filename, "r") as r:
                geo_inst = json.loads(r.read())

                feature = geo_inst["features"][0]

                cca3 = filename.replace(".geo.json", "").upper()
                
                geo_countries["cca2"][feature["properties"]["cca2"].upper()] = feature
                geo_countries["cca3"][cca3.upper()] = feature

                # if "cca3" in feature["properties"] and feature["properties"]["cca3"] != "":
                #     geo_countries["cca3"][feature["properties"]["cca3"]] = feature

                if "csvcid" in feature["properties"] and feature["properties"]["csvcid"] != "":
                    geo_countries["csvcid"][feature["properties"]["csvcid"]] = feature

        except Exception as e:
            print(filename)

    return geo_countries

def save_geo(geo_features_list: dict[str, dict[str, any]]):
    for key in geo_features_list["cca3"]:
        print(key)
        with open(data_location + key.lower() + ".geo.json", "w") as w:
            w.write(json.dumps({"type":"FeatureCollection","features":[geo_features_list["cca3"][key]]}))

def save_visas(visa_countries):
    for csvcid in visa_countries["csvcid"]:
        with open(visas_location + csvcid + ".visas.json", "w") as w:
            w.write(json.dumps(visa_countries["csvcid"][csvcid], sort_keys=True, indent=4, separators=(',', ': ')))

def remove_csvc_csvcid(csvcid):
    remove(visas_location + csvcid + ".visas.json")

def load_countries():
    countries_dict = {
        "csvcid": {},
        "cca2": {},
        "cca3": {}
    }

    with open(countries_location, "r") as r:
        countries_list = json.loads(r.read())

        for country in countries_list:
            if "csvcid" not in country:
                print("NOT IN " + country["cca3"])
            countries_dict["cca3"][country["cca3"]] = country
            countries_dict["cca2"][country["cca2"]] = country
            countries_dict["csvcid"][country["csvcid"]] = country

    return countries_dict

def save_countries(new_countries):
    countries_list = []

    for key in new_countries["cca3"]:
        countries_list.append(new_countries["cca3"][key])
    with open(countries_location, "w") as w:
        w.write(json.dumps(countries_list, sort_keys=True, indent=4, separators=(',', ': ')))

class tools:
    def __init__(self):
        pass

    class countries:
        visa_countries = {}
        def __init__(self, args):
            self.visa_countries = load_visas()

            if args.countries_subcommand == "add":
                self.add(args.csvc, args.name, args.cca2, args.cca3, args.ccn3)

            if args.countries_subcommand == "remove":
                self.remove(args.csvc)

            if args.countries_subcommand == "contain":
                if not self.contains(args.csvc, args.cca2, args.cca3):
                    print("Visas country does not exists!")
                else:
                    print("Visas country exists!")


        def add(self, csvcid, name="", cca2="", cca3="", ccn3=""):
            if csvcid in self.visa_countries["csvcid"]:
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

            for key in self.visa_countries["csvcid"]:
                new_country["requirements"][key] = new_visa_req
                self.visa_countries["csvcid"][key]["requirements"][csvcid] = new_visa_req

            self.visa_countries["csvcid"][csvcid] = new_country

            save_visas(self.visa_countries)


        def remove(self, csvcid, force = False):
            if csvcid not in self.visa_countries["csvcid"] and not force:
                raise Exception(f"Can not delete {csvcid}. Does not exists!")       

            for key in self.visa_countries["csvcid"]:
                if csvcid in self.visa_countries["csvcid"][key]["requirements"]:
                    del self.visa_countries["csvcid"][key]["requirements"][csvcid]

            del self.visa_countries["csvcid"][csvcid]

            remove_csvc_csvcid(csvcid)
            save_visas(self.visa_countries)


        def contains(self, csvcid="", cca2="", cca3=""):
            if csvcid:
                return csvcid in self.visa_countries["csvcid"]

            if cca2:
                return cca2 in self.visa_countries["cca2"]

            if cca3:
                return cca3 in self.visa_countries["cca3"]

            return False


    class reform:
        visa_countries = {}
        countries_json = {}
        geo_json = {}

        def __init__(self, args):
            self.visa_countries = load_visas()
            self.countries_json = load_countries()
            self.geo_json = load_geo()

            if args.subcommand == "diff":
                self.diff()

            if args.subcommand == "refcountries":
                self.inject_ccas_visas()

            if args.subcommand == "csvcid":
                self.inject_csvc()


        def diff(self):
            for csvc in self.countries_json["csvcid"]:
                if csvc not in self.visa_countries["csvcid"]:
                    print("Visas missing " + csvc)

            for csvc in self.visa_countries["csvcid"]:
                if csvc not in self.countries_json["csvcid"]:
                    print("Countries missing " + csvc)

            for cca2 in self.countries_json["cca2"]:
                if cca2 not in self.geo_json["cca2"]:
                    print("Geo missing " + cca2)
            
            # for key in self.countries_json["cca2"]:
            #     if key not in self.visa_countries["cca2"]:
            #         print("Countries: Visas missing CCA2 " + key)

            # for key in self.countries_json["cca2"]:
            #     if key not in self.geo_json["cca2"]:
            #         print("Countries: Geo missing CCA2 " + key)
                    
        # def rewind_geo(self):
        #     for cca3 in self.geo_json["cca3"]:
        #         try:
        #             input = json.dumps({"type":"FeatureCollection","features":[self.geo_json["cca3"][cca3]]})

        #             rewind_out = rewind(input)
        #             rewind_decoded = json.loads(rewind_out)
        #             rewinded_feature = rewind_decoded["features"][0]

        #             self.geo_json["cca3"][cca3] = rewinded_feature
        #         except Exception as e:
        #             print(cca3, e)

        #     save_geo(self.geo_json)
                
        def inject_csvc(self):
            for cca3 in self.geo_json["cca3"]:
                del self.geo_json["cca3"][cca3]["cca2"]
                del self.geo_json["cca3"][cca3]["cca3"]
                del self.geo_json["cca3"][cca3]["ccn3"]
                del self.geo_json["cca3"][cca3]["csvcid"]
                del self.geo_json["cca3"][cca3]["name"]

                self.geo_json["cca3"][cca3]["properties"]["cca2"] = self.countries_json["cca3"][cca3]["cca2"]
                self.geo_json["cca3"][cca3]["properties"]["cca3"] = self.countries_json["cca3"][cca3]["cca3"]
                self.geo_json["cca3"][cca3]["properties"]["ccn3"] = self.countries_json["cca3"][cca3]["ccn3"]
                self.geo_json["cca3"][cca3]["properties"]["csvcid"] = self.countries_json["cca3"][cca3]["csvcid"]
                self.geo_json["cca3"][cca3]["properties"]["name"] = self.countries_json["cca3"][cca3]["name"]["common"]

            save_geo(self.geo_json)


        def inject_csvc_countries(self):
            for key in self.visa_countries["csvcid"]:
                if self.visa_countries["csvcid"][key]["cca2"] != "" and self.visa_countries["csvcid"][key]["cca2"] in self.countries_json["cca2"]:
                    self.countries_json["cca2"][self.visa_countries["csvcid"][key]["cca2"]]["csvcid"] = key


            save_countries(self.countries_json)


        def inject_ccas_visas(self):
            for key in self.countries_json["csvcid"]:
                self.visa_countries["csvcid"][key]["cca2"] = self.countries_json["csvcid"][key]["cca2"]
                self.visa_countries["csvcid"][key]["cca3"] = self.countries_json["csvcid"][key]["cca3"]
                self.visa_countries["csvcid"][key]["ccn3"] = self.countries_json["csvcid"][key]["ccn3"]
                self.visa_countries["csvcid"][key]["name"] = self.countries_json["csvcid"][key]["name"]["common"]

            save_visas(self.visa_countries)


    class visas:
        def __init__(self, args):
            pass