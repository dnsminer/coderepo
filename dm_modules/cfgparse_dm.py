#__author__ = 'dleece'
# pass config file and data to be viewed

import ConfigParser

def ConfigSectionMap(section,parsehandle):
    cfgdict = {}
    cfgoptions = parsehandle.options(section)
    for cfgoption in cfgoptions:
        try:
            cfgdict[cfgoption] = parsehandle.get(section, cfgoption)
            if cfgdict[cfgoption] == -1:
                print "invalid parameter" + cfgoption
        except:
            print ('exception thrown, on %s' % cfgoption)
            cfgdict[cfgoption] = None
    return  cfgdict


def opencfg(filepath,sectionname):
    cfgparser=ConfigParser.ConfigParser()
    cfgparser.read(filepath)
    cfgsectiondict = ConfigSectionMap(sectionname,cfgparser)

    return cfgsectiondict