import sys
import os

def get_env(var, default = None):
        try:
                res = os.environ[var]
        except:
                if not default is None:
                        res = default
                else:
                        sys.stderr.write("Please set up " + var + " to access the virusbattle.com service\n")
                        sys.exit(-1)
        return res

server = get_env('VIRUSBATTLE_SERVER', "api.magic.cythereal.com")
port   = get_env("VIRUSBATTLE_PORT", 443)
protocol = get_env("VIRUSBATTLE_PROTOCOL", 'https')
all_services = "srlUnpacker,srlJuice,srlSimService,srlStatic".split(",")
serviceFilterList = get_env('VIRUSBATTLE_SERVICE_FILTER','').split(',')

def service_list ():
    return filter(lambda x: x not in serviceFilterList, all_services)

baseurl = protocol + "://" + server  + ":" + str(port)

def make_vburl (op, objID=None, usekey=True, **kwargs):
    if usekey:
        try:
            key = get_env('VIRUSBATTLE_KEY')
        except KeyError:
            raise VBMissingKeyError('Please set the environment variable VIRUSBATTLE_KEY to your APIKey.')
        url = baseurl +  "/" + op + "/" + key
    else:
        url = baseurl + "/" + op

    if objID is not None:
        url = url + "/" + objID
    if kwargs:
        arglist = map(lambda x: "%s=%s" % (x, kwargs[x]), kwargs.keys())
        wwwargs = "&".join(arglist)
        url = url + "/?" + wwwargs
    return url

class VBVersionError (Exception):
    pass
class VBMissingKeyError (Exception):
    pass

def check_version (result):
    version = result['vb_version']
    if not version == 'VB-0.4':
        raise VBVersionError("Virusbattle-SDK version not compatible with server. Please update the SDK using 'git pull'.")
    return result
