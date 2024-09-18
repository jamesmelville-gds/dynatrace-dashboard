#!/usr/bin/env python3

import csv
from dynatrace_tiles import FirewallUtilisation,Dashboard,Header

def main():

    prodtiles = []
    nonprodtiles = []
    prodleft = 0
    nonprodleft = 0
    top = 0
    width = 38*6
    height = 38*3

    with open('firewalls-all.csv', 'r') as firewallsfile:
        firewallreader = csv.DictReader(firewallsfile)
        currentHeader = ""
        FirstHeader = True
        for firewall in firewallreader:
            if firewall['appName'] != currentHeader:
                if not FirstHeader:
                    top+=height
                prodtiles.append(Header(firewall['appName'],top,0,380,38))
                nonprodtiles.append(Header(firewall['appName'],top,0,380,38))
                FirstHeader = False
                prodleft =380
                nonprodleft = 380
            if firewall['envName'] in ['prod','production','integration', 'feature', 'production-preview', 'int', 'no-name', 'backup']:
                prodtiles.append(FirewallUtilisation(firewall['accountId'],firewall['envName'],firewall['firewallName'],top,prodleft,width,height))
                prodleft += width
            else:
                nonprodtiles.append(FirewallUtilisation(firewall['accountId'],firewall['envName'],firewall['firewallName'],top,nonprodleft,width,height))
                nonprodleft += width
            currentHeader = firewall['appName']


    proddash = Dashboard('Prod firewalls',
                     'james.melville@digital.cabinet-office.gov.uk',
                     prodtiles)
    
    with open('prod-dashboard.json', '+w') as dashfile:
        dashfile.write(proddash.toJson())
    
    nonproddash = Dashboard('Non-prod firewalls',
                     'james.melville@digital.cabinet-office.gov.uk',
                     nonprodtiles)
    
    with open('non-prod-dashboard.json', '+w') as dashfile:
        dashfile.write(nonproddash.toJson())

if __name__ == "__main__":
    main()