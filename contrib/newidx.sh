#!/bin/bash -x
curl -XPUT http://localhost:9200/dmlogstash2-2015.09.16 -d '
{
    "mappings" : {
      "_default_" : {
        "dynamic_templates" : [ {
          "message_field" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string"
            },
            "match" : "message",
            "match_mapping_type" : "string"
          }
        }, {
          "string_fields" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string",
              "fields" : {
                "raw" : {
                  "index" : "not_analyzed",
                  "ignore_above" : 256,
                  "doc_values" : true,
                  "type" : "string"
                }
              }
            },
            "match" : "*",
            "match_mapping_type" : "string"
          }
        }, {
          "float_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "float"
            },
            "match" : "*",
            "match_mapping_type" : "float"
          }
        }, {
          "integer_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "integer"
            },
            "match" : "*",
            "match_mapping_type" : "integer"
          }
        }, {
          "long_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "long"
            },
            "match" : "*",
            "match_mapping_type" : "long"
          }
        }, {
          "date_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "date"
            },
            "match" : "*",
            "match_mapping_type" : "date"
          }
        } ],
        "_all" : {
          "enabled" : true,
          "omit_norms" : true
        },
        "properties" : {
          "@version" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "geoip" : {
            "dynamic" : "true",
            "properties" : {
              "location" : {
                "type" : "geo_point"
              }
            }
          }
        }
      },
      "DNSQRY" : {
        "dynamic_templates" : [ {
          "message_field" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string"
            },
            "match" : "message",
            "match_mapping_type" : "string"
          }
        }, {
          "string_fields" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string",
              "fields" : {
                "raw" : {
                  "index" : "not_analyzed",
                  "ignore_above" : 256,
                  "doc_values" : true,
                  "type" : "string"
                }
              }
            },
            "match" : "*",
            "match_mapping_type" : "string"
          }
        }, {
          "float_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "float"
            },
            "match" : "*",
            "match_mapping_type" : "float"
          }
        }, {
          "integer_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "integer"
            },
            "match" : "*",
            "match_mapping_type" : "integer"
          }
        }, {
          "long_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "long"
            },
            "match" : "*",
            "match_mapping_type" : "long"
          }
        }, {
          "date_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "date"
            },
            "match" : "*",
            "match_mapping_type" : "date"
          }
        } ],
        "_all" : {
          "enabled" : true,
          "omit_norms" : true
        },
        "properties" : {
          "@timestamp" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "@version" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "MessageRemainder" : {
            "type" : "string",
            "index" : "not_analyzed",
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "QuerySettings" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "doc_values" : true,
                "ignore_above" : 256
              }
            }
          },
          "RNodeIP" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "doc_values" : true,
                "ignore_above" : 256
              }
            }
          },
          "RQEventDate" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "RQEventFacility" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "RQEventTime" : {
            "type" : "date",
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            },
            "format" : "HH:mm:ss.SSS"
          },
          "RQType" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "RQuery" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "RequestNum" : {
            "type" : "integer",
            "index" : "analyzed",
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "View" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "geoip" : {
            "dynamic" : "true",
            "properties" : {
              "location" : {
                "type" : "geo_point"
              }
            }
          },
          "host" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "message" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            }
          },
          "tags" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "type" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          }
        }
      },
      "PDNS" : {
        "dynamic_templates" : [ {
          "message_field" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string"
            },
            "match" : "message",
            "match_mapping_type" : "string"
          }
        }, {
          "string_fields" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string",
              "fields" : {
                "raw" : {
                  "index" : "not_analyzed",
                  "ignore_above" : 256,
                  "type" : "string",
                  "doc_values" : true
                }
              }
            },
            "match" : "*",
            "match_mapping_type" : "string"
          }
        }, {
          "float_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "float"
            },
            "match" : "*",
            "match_mapping_type" : "float"
          }
        }, {
          "integer_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "integer"
            },
            "match" : "*",
            "match_mapping_type" : "integer"
          }
        }, {
          "long_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "long"
            },
            "match" : "*",
            "match_mapping_type" : "long"
          }
        }, {
          "date_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "date"
            },
            "match" : "*",
            "match_mapping_type" : "date"
          }
        } ],
        "_all" : {
          "enabled" : true,
          "omit_norms" : true
        },
        "properties" : {
          "@timestamp" : {
            "type" : "date",
            "format" : "dateOptionalTime"
          },
          "@version" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "AA" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "TTL0" : {
            "type" : "float",
            "store" : true,
            "fields" : {
              "raw" : {
                "type" : "float"
              }
            }
          },
          "TTLrem" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "Z" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "answers" : {
            "type" : "string",
            "index" : "not_analyzed",
            "doc_values" : true
          },
          "eventtime" : {
            "type" : "float",
            "store" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "geoip" : {
            "dynamic" : "true",
            "properties" : {
              "location" : {
                "type" : "geo_point"
              }
            }
          },
          "host" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "message" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            }
          },
          "pitboss" : {
            "type" : "ip",
            "store" : true,
            "doc_values" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "qclass" : {
            "type" : "integer",
            "store" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "qclassname" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "qtype" : {
            "type" : "integer",
            "store" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "qtypename" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "query" : {
            "type" : "string",
            "index" : "not_analyzed",
            "doc_values" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "rc" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "doc_values" : true,
                "ignore_above" : 256
              }
            }
          },
          "rcode" : {
            "type" : "integer",
            "store" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "rcodename" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "remcodes" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "soans" : {
            "type" : "ip",
            "store" : true,
            "doc_values" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "tags" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "type" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          }
        }
      },
      "RPZ" : {
        "dynamic_templates" : [ {
          "message_field" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string"
            },
            "match" : "message",
            "match_mapping_type" : "string"
          }
        }, {
          "string_fields" : {
            "mapping" : {
              "index" : "analyzed",
              "omit_norms" : true,
              "type" : "string",
              "fields" : {
                "raw" : {
                  "index" : "not_analyzed",
                  "ignore_above" : 256,
                  "doc_values" : true,
                  "type" : "string"
                }
              }
            },
            "match" : "*",
            "match_mapping_type" : "string"
          }
        }, {
          "float_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "float"
            },
            "match" : "*",
            "match_mapping_type" : "float"
          }
        }, {
          "integer_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "integer"
            },
            "match" : "*",
            "match_mapping_type" : "integer"
          }
        }, {
          "long_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "long"
            },
            "match" : "*",
            "match_mapping_type" : "long"
          }
        }, {
          "date_fields" : {
            "mapping" : {
              "doc_values" : true,
              "type" : "date"
            },
            "match" : "*",
            "match_mapping_type" : "date"
          }
        } ],
        "_all" : {
          "enabled" : true,
          "omit_norms" : true
        },
        "properties" : {
          "@timestamp" : {
            "type" : "date",
            "doc_values" : true,
            "format" : "dateOptionalTime"
          },
          "@version" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "file" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "doc_values" : true,
                "ignore_above" : 256
              }
            }
          },
          "geoip" : {
            "dynamic" : "true",
            "properties" : {
              "location" : {
                "type" : "geo_point"
              }
            }
          },
          "host" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "doc_values" : true,
                "ignore_above" : 256
              }
            }
          },
	  "RPZdate" : {
            "type" : "date",
            "format" : "dd-MMM-yyyy",
            "index" : "not_analyzed",
            "norms" : {
              "enabled" : false
            }
          },
	  "RPZtime" : {
            "type" : "date",
            "format" : "HH:mm:ss.SSS",
            "index" : "not_analyzed",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "PRGType" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "RPZfacility" : {
            "type" : "string",
            "index" : "not_analyzed"
          },
          "RPZClient" : {
            "type" : "ip",
            "store" : true,
            "doc_values" : true,
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "ignore_above" : 256
              }
            }
          },
          "RPZView" : {
            "type" : "string",
            "index" : "not_analyzed",
            "doc_values" : true
	  },
          "RPZTrigger" : {
            "type" : "string",
            "index" : "not_analyzed",
            "doc_values" : true
	  },
          "RPZAction" : {
            "type" : "string",
            "index" : "not_analyzed",
            "doc_values" : true
	  },
          "RPZQry" : {
            "type" : "string",
            "index" : "not_analyzed",
            "doc_values" : true
	  },
          "RPZRewrite" : {
            "type" : "string",
            "index" : "not_analyzed",
            "doc_values" : true
	  },
          "message" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            }
          },
          "offset" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "doc_values" : true,
                "ignore_above" : 256
              }
            }
          },
          "type" : {
            "type" : "string",
            "norms" : {
              "enabled" : false
            },
            "fields" : {
              "raw" : {
                "type" : "string",
                "index" : "not_analyzed",
                "doc_values" : true,
                "ignore_above" : 256
              }
            }
          }
        }
      }
    }
  }
}'
