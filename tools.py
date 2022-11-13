#!/usr/bin/python3

import os
import argparse

# SIZES = {
#     "s": "Small",
#     "m": "Medium",
#     "l": "Large",
#     "xl": "Extra large",
#     "xxl": "Extra extra large"
# }

# CRUSTS = {"normal": "", "thin": " thin crust", "deep": " deep dish"}


# def build_pizza(order):
#     pizza = f"{SIZES[order.size]}{CRUSTS[order.crust]}"
#     if order.toppings:
#         pizza +=  " with " + ", ".join(order.toppings)
#     if order.cheese:
#         pizza += " plus extra cheese"
#     if order.sauce:
#         pizza += " and extra sauce"
#     return pizza


"""tool
Usage:
  tool.py build [ --geo | --info | --visa | --validate ]
  tool.py visa add <cca2> <name> [--default-policy=<visa_type>] [--default-requirement=<visa_type>] [--force]
  tool.py visa set <visa_type> <from-cca2> (--cross | --requirement | --policy) <to-cca2>... [--note=<note>] [--time=<time>]
  tool.py visa rm <cca2> [--force]
  
Options:
  -h --help     Show this screen.
  --version     Show version.
  build
  --geo         Validate and build geo  data
  --info        Validate and build info data
  --visa        Validate and build visa data
  --validate    Validate all data
  visa
  -defp --default-policy=<type>      Sets default visa policy         [default: r] r - required
  -defr --default-requirement=<type> Sets default visa requirement    [default: r] r - required
  -f --force                      Force
  -x --cross                      Cross visa set between this countries
  -r --requirement                Sets requirement for the countrie to the countrie(s)
  -p --policy                     Sets policy of the countrie to the countrie(s)
  --note=<note>                   Sets note        [default: None]
  --time=<time>                   Sets visa length [default: None]
"""
from libs.tools import tools

def main():
    parser = argparse.ArgumentParser(prog="Visas Editing Tools", add_help=True)

    subparsers = parser.add_subparsers(dest = "command")

    # ----- Countries CLI ----- #
    countries_cmd = subparsers.add_parser("countries", help="Manage countries")
    countries_subparsers = countries_cmd.add_subparsers(dest = "subcommand")

    countries_list_subparsers = countries_subparsers.add_parser("list", help="List available countries")

    countries_add_subparsers = countries_subparsers.add_parser("add", help="Add new country")
    countries_add_subparsers.add_argument("--csvc", type=str, help="Visas2 country code", required=True)
    countries_add_subparsers.add_argument("--name", type=str, help="Country name")
    countries_add_subparsers.add_argument("--cca3", type=str, help="Alpha3 country code")
    countries_add_subparsers.add_argument("--cca2", type=str, help="Alpha2 country code")
    countries_add_subparsers.add_argument("--ccn3", type=str, help="Numeric3 country code")


    countries_contains_subparsers = countries_subparsers.add_parser("contains", help="Find existing country")
    countries_contains_subparsers.add_argument("--csvc", type=str, help="Visas2 country code")
    countries_contains_subparsers.add_argument("--cca3", type=str, help="Alpha3 country code")
    countries_contains_subparsers.add_argument("--cca2", type=str, help="Alpha2 country code")
    countries_contains_subparsers.add_argument("--ccn3", type=str, help="Numeric3 country code")
    
    countries_remove_subparsers = countries_subparsers.add_parser("remove", help="Remove country")
    countries_remove_subparsers.add_argument("--csvc", type=str, help="Visas2 country code", required=True)

    # ----- Visa relationship CLI ----- #
    visas_cmd = subparsers.add_parser("visas", help="Manage visa requirements")
    visas_subparsers = visas_cmd.add_subparsers(dest = "subcommand")

    visas_set_subparsers = visas_subparsers.add_parser("set", help="Add new country")
    visas_set_subparsers.add_argument("--requirement", type=str, help="Policy definition", required=True)
    visas_set_subparsers.add_argument("--from-csvc", type=str, help="Country implementing", required=True)
    visas_set_subparsers.add_argument("--to-csvc", type=str, nargs="+", help="Countries affected", required=True)
    visas_set_subparsers.add_argument("--passport-pages", type=int, help="Min passport pages")

    args = parser.parse_args()
    # ---------- #

    # print(args)
    try:
        if args.command == "countries":
            tools.countries(args)
            
        if args.command == "visas":
            tools.visas(args)
    except Exception as e:
        print("Error")
        print(e)

if __name__ == "__main__":
    main()