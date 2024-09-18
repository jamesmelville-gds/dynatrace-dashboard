import json
import jsonpickle

class Tile:
  def __init__(self,name,tileType,top=0,left=0,width=0,height=0):
    self.name = name
    self.tileType = tileType
    self.configured = True
    self.bounds = {"top" : top,
                    "left" : left,
                    "width" : width,
                    "height" : height
                    }
  def toJson(self):
    return json.dumps(json.loads(jsonpickle.encode(self)), indent=2)
  def setLeft(self,left):
     self.bounds['left'] = left
  def setTop(self,top):
    self.bounds['top'] = top


class Dashboard:
    def __init__(self,name,owner,tiles):
        self.dashboardMetadata= {
        "name": name,
        "shared": False,
        "owner": owner,
        "hasConsistentColors": False
        }
        self.tiles = tiles
    def toJson(self):
      return json.dumps(json.loads(jsonpickle.encode(self)), indent=2)

class Header(Tile):
    def __init__(self, name, top=0, left=0, width=0, height=0):
       super().__init__(name, 'HEADER', top, left, width, height)


class FirewallUtilisation(Tile):
    def __init__(self, accountId, tilename, fwname, top, left, width,height):
        super().__init__(tilename, "DATA_EXPLORER",top, left, width, height)
        self.tileFilter= {}
        self.isAutoRefreshDisabled = False
        self.customName = f'{tilename}'
        self.queries = [
          {
            "id": "A",
            "metric": "cloud.aws.networkfirewall.passedPacketsByAccountIdAvailabilityZoneEngineFirewallNameRegion",
            "spaceAggregation": "AUTO",
            "timeAggregation": "DEFAULT",
            "splitBy": [],
            "sortBy": "DESC",
            "sortByDimension": "",
"filterBy": {
            "filterOperator": "AND",
            "nestedFilters": [
              {
                "filter": "aws.account.id",
                "filterType": "DIMENSION",
                "filterOperator": "OR",
                "nestedFilters": [],
                "criteria": [
                  {
                    "value": f"{accountId}",
                    "evaluator": "EQ"
                  }
                ]
              },
              {
                "filter": "firewallname",
                "filterType": "DIMENSION",
                "filterOperator": "OR",
                "nestedFilters": [],
                "criteria": [
                  {
                    "value": f"{fwname}",
                    "evaluator": "EQ"
                  }
                ]
              }
            ],
            "criteria": []
          },
            "limit": 20,
            "rate": "NONE",
            "enabled": True
          }
        ]
        self.visualConfig= {
          "type": "GRAPH_CHART",
          "global": {},
          "rules": [
            {
              "matcher" : "A:",
              "properties" : {
                "color": "DEFAULT"
              },
              "seriesOverrides": []
            }
          ],
          "axes": {
            "xAxis": {
              "displayName": "",
              "visible": True
            },
            "yAxes": [
              {
                "displayName" : "",
                "visible" : True,
                "min" : "AUTO",
                "max" : "AUTO",
                "position" : "LEFT",
                "queryIds" : [
                  "A"
                ],
                "defaultAxis" : True
              }
            ]
          },
          "heatmapSettings" : {
            "yAxis" : "VALUE",
            "showLabels" : False
          },
          "singleValueSettings" : {
            "showTrend" : True,
            "showSparkLine" : True,
            "linkTileColorToThreshold" : True
          },
          "thresholds" : [
            {
              "axisTarget" : "LEFT",
              "rules" : [
                {
                  "color" : "#7dc540"
                },
                {
                  "color" : "#f5d30f"
                },
                {
                  "color" : "#dc172a"
                }
              ],
              "visible" : True
            }
          ],
          "tableSettings" : {
            "hiddenColumns" : []
          },
          "graphChartSettings": {
            "connectNulls" : False
          },
          "honeycombSettings": {
            "showHive" : True,
            "showLegend" : True,
            "showLabels" : False,
          },
        }
        
        self.queriesSettings = {
            "resolution" : "",
        }

        self.metricExpressions= [
          f"resolution=null&(cloud.aws.networkfirewall.passedPacketsByAccountIdAvailabilityZoneEngineFirewallNameRegion:filter(and(or(eq(\"aws.account.id\",\"{accountId}\")),or(eq(firewallname,{fwname})))):splitBy():sort(value(auto,descending)):limit(20)):limit(100):names"
        ]