#!/usr/bin/python3

import argparse
from libs.tools import tools

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

def upperCaseCodes(args):
    if "csvc" in vars(args) and args.csvc is not None:
        args.csvc = args.csvc.upper()

    if "cca3" in vars(args) and args.cca3 is not None:
        args.cca3 = args.cca3.upper()
    
    if "cca2" in vars(args) and args.cca2 is not None:
        args.cca2 = args.cca2.upper()

    if "ccn3" in vars(args) and args.ccn3 is not None:
        args.ccn3 = args.ccn3.upper()


    return args

def main():
    parser = argparse.ArgumentParser(prog="Visas Editing Tools", add_help=True)
    subparsers = parser.add_subparsers(dest = "command")

    # ----- Visa relationship CLI ----- #
    visas_cmd = subparsers.add_parser("visas", help="Manage visa requirements")
    visas_subparsers = visas_cmd.add_subparsers(dest = "subcommand")

    visas_set_subparsers = visas_subparsers.add_parser("set", help="Add new country")
    visas_set_subparsers.add_argument("--requirement", type=str, help="Policy definition", required=True)
    visas_set_subparsers.add_argument("--from-csvc", type=str, help="Country implementing", required=True)
    visas_set_subparsers.add_argument("--to-csvc", type=str, nargs="+", help="Countries affected", required=True)
    visas_set_subparsers.add_argument("--passport-pages", type=int, help="Min passport pages")


    # ----- Visa Countries CLI ----- #
    visa_countries_cmd = visas_subparsers.add_parser("countries", help="Manage countries")
    visa_countries_subparsers = visa_countries_cmd.add_subparsers(dest = "countries_subcommand")

    countries_list_subparsers = visa_countries_subparsers.add_parser("list", help="List available countries")

    visa_countries_add_subparsers = visa_countries_subparsers.add_parser("add", help="Add new country")
    visa_countries_add_subparsers.add_argument("--csvc", type=str, help="Visas2 country code", required=True)
    visa_countries_add_subparsers.add_argument("--name", type=str, help="Country name")
    visa_countries_add_subparsers.add_argument("--cca3", type=str, help="Alpha3 country code")
    visa_countries_add_subparsers.add_argument("--cca2", type=str, help="Alpha2 country code")
    visa_countries_add_subparsers.add_argument("--ccn3", type=str, help="Numeric3 country code")


    visa_countries_contains_subparsers = visa_countries_subparsers.add_parser("contain", help="Find existing country")
    visa_countries_contains_subparsers.add_argument("--csvc", type=str, help="Visas2 country code")
    visa_countries_contains_subparsers.add_argument("--cca3", type=str, help="Alpha3 country code")
    visa_countries_contains_subparsers.add_argument("--cca2", type=str, help="Alpha2 country code")
    visa_countries_contains_subparsers.add_argument("--ccn3", type=str, help="Numeric3 country code")
    
    visa_countries_remove_subparsers = visa_countries_subparsers.add_parser("remove", help="Remove country")
    visa_countries_remove_subparsers.add_argument("--csvc", type=str, help="Visas2 country code", required=True)


    # ----- Visa relationship CLI ----- #
    reforms_cmd = subparsers.add_parser("reform", help="Reform visas")
    reforms_subparsers = reforms_cmd.add_subparsers(dest = "subcommand")

    reforms_subparsers.add_parser("diff", help="Diff")
    reforms_subparsers.add_parser("refcountries", help="Reform countries")
    reforms_subparsers.add_parser("csvcid", help="Rewind geojson")
    # ---------- #

    args = parser.parse_args()
    print(args)

    args = upperCaseCodes(args)

    # try:
    if args.command == "visas":
        if args.subcommand == "countries":
            tools.countries(args)
        else:
            tools.visas(args)
    elif args.command == "reform":
        tools.reform(args)
        
    # except Exception as e:
    #     print("Error", e)

if __name__ == "__main__":
    main()