
#!/usr/bin/python3.9

import optparse
import os
import traceback
import platform
import re
import string
import sys
import collections
import shutil
import time
import base64
import html
import json
import asyncio
import aiohttp

from datetime import datetime

dictPy3GblEnv = collections.defaultdict()

# - - - - - Setup the Python3 'Global' Environment dictionary (standard) - - - - -

dictPy3GblEnv["bVerbose"]           = False
dictPy3GblEnv["bProcessingError"]   = False
dictPy3GblEnv["optParser"]          = optparse.OptionParser()
dictPy3GblEnv["sScriptId"]          = dictPy3GblEnv["optParser"].get_prog_name()
dictPy3GblEnv["sScriptVers"]        = "(v1.0203)"
dictPy3GblEnv["sScriptDisp"]        = ("%s %s:" % (dictPy3GblEnv["sScriptId"], dictPy3GblEnv["sScriptVers"]))
dictPy3GblEnv["cScriptArgc"]        = len(sys.argv)
dictPy3GblEnv["sOutputLogFile"]     = None

# - - - - - Setup the Python3 'Global' Environment dictionary (extended) - - - - -

dictPy3GblEnv["tmStartTime"]        = time.time()
dictPy3GblEnv["cHttpGetRequests"]   = 0
dictPy3GblEnv["cHttpPostRequests"]  = 0
dictPy3GblEnv["sCurrentWorkingDir"] = os.getcwd()
dictPy3GblEnv["sPythonVers"]        = ("v%s.%s.%s" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)) 
dictPy3GblEnv["sServerNode"]        = platform.node()
dictPy3GblEnv["sPlatform"]          = platform.system()
dictPy3GblEnv["sPlatformPathSep"]   = None
dictPy3GblEnv["bPlatformIsWindows"] = dictPy3GblEnv["sPlatform"].startswith('Windows')

if dictPy3GblEnv["bPlatformIsWindows"] == False:

    dictPy3GblEnv["bPlatformIsWindows"] = dictPy3GblEnv["sPlatform"].startswith('Microsoft')

if dictPy3GblEnv["bPlatformIsWindows"] == True:

    dictPy3GblEnv["sPlatformPathSep"] = "\\"

else:

    dictPy3GblEnv["sPlatformPathSep"] = "/"

# Parameter and Application 'global' item(s):

dictPy3GblEnv["cxAccessTokenType"]         = "Bearer"
dictPy3GblEnv["cxAccessToken"]             = ""
# Example:                                 = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkFFRUYyQUE2RTgxNTVGMjY2MDMzNjM1MzcyQjgxODNEMzUxODUyQUEiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJydThxcHVnVlh5WmdNMk5UY3JnWVBUVVlVcW8ifQ.eyJuYmYiOjE2NDAwMTY4NTksImV4cCI6MTY0MDAyMDQ1OSwiaXNzIjoiaHR0cDovL0RBUllMQ09YRTM2Qy9DeFJlc3RBUEkvYXV0aC9pZGVudGl0eSIsImF1ZCI6WyJodHRwOi8vREFSWUxDT1hFMzZDL0N4UmVzdEFQSS9hdXRoL2lkZW50aXR5L3Jlc291cmNlcyIsInJlcG9ydGluZ19hcGkiXSwiY2xpZW50X2lkIjoicmVwb3J0aW5nX3NlcnZpY2Vfc3dhZ2dlciIsInN1YiI6IjEiLCJhdXRoX3RpbWUiOjE2NDAwMTY2ODcsImlkcCI6ImxvY2FsIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZGNveCIsInRlYW0iOlsiL0N4U2VydmVyIiwiL0N4U2VydmVyL1NQIiwiL0N4U2VydmVyL1NQL0NvbXBhbnkiLCIvQ3hTZXJ2ZXIvU1AvQ29tcGFueS9Vc2VycyIsIi9DeFNlcnZlci9TUC9Db21wYW55L1VzZXJzL0RhcnlsX0NveCJdLCJzYXN0LXBlcm1pc3Npb25zIjpbInNhdmUtb3NhLXNjYW4iLCJzYXZlLXNhc3Qtc2NhbiIsInNhdmUtcHJvamVjdCIsInZpZXctZmFpbGVkLXNhc3Qtc2NhbiIsIm9wZW4taXNzdWUtdHJhY2tpbmctdGlja2V0cyIsImNyZWF0ZS1wcmVzZXQiLCJkb3dubG9hZC1zY2FuLWxvZyIsInNlZS1zdXBwb3J0LWxpbmsiLCJ2aWV3LXJlc3VsdHMiLCJtYW5hZ2UtZGF0YS1hbmFseXNpcy10ZW1wbGF0ZXMiLCJnZW5lcmF0ZS1zY2FuLXJlcG9ydCIsIm1hbmFnZS1yZXN1bHQtY29tbWVudCIsImV4cG9ydC1zY2FuLXJlc3VsdHMiLCJ1c2UtY3hhdWRpdCIsIm1hbmFnZS1jdXN0b20tZGVzY3JpcHRpb24iLCJ1cGRhdGUtYW5kLWRlbGV0ZS1wcmVzZXQiLCJtYW5hZ2UtcmVzdWx0LXNldmVyaXR5IiwibWFuYWdlLXJlc3VsdC1hc3NpZ25lZSIsInNldC1yZXN1bHQtc3RhdGUtdG92ZXJpZnkiLCJzZXQtcmVzdWx0LXN0YXRlLWNvbmZpcm1lZCIsInNldC1yZXN1bHQtc3RhdGUtdXJnZW50Iiwic2V0LXJlc3VsdC1zdGF0ZS1wcm9wb3NlZG5vdGV4cGxvaXRhYmxlIiwic2V0LXJlc3VsdC1zdGF0ZS1iYWNrbG9nIiwic2V0LXJlc3VsdC1zdGF0ZS1pZ25vcmUiLCJzZXQtcmVzdWx0LXN0YXRlLWZhbHNlcG9zaXRpdmUiLCJzZXQtcmVzdWx0LXN0YXRlLW5vdGV4cGxvaXRhYmxlIiwiZGVsZXRlLXNhc3Qtc2NhbiIsImRlbGV0ZS1wcm9qZWN0IiwidXNlLW9kYXRhIiwibWFuYWdlLWRhdGEtcmV0ZW50aW9uIiwibWFuYWdlLWVuZ2luZS1zZXJ2ZXJzIiwibWFuYWdlLXN5c3RlbS1zZXR0aW5ncyIsIm1hbmFnZS1leHRlcm5hbC1zZXJ2aWNlcy1zZXR0aW5ncyIsIm1hbmFnZS1jdXN0b20tZmllbGRzIiwibWFuYWdlLWlzc3VlLXRyYWNraW5nLXN5c3RlbXMiLCJtYW5hZ2UtcHJlLXBvc3Qtc2Nhbi1hY3Rpb25zIiwiZG93bmxvYWQtc3lzdGVtLWxvZ3MiXSwic2NvcGUiOlsicmVwb3J0aW5nX2FwaSJdLCJhbXIiOlsicHdkIl19.Gq6XX37rF1BVjOXLYBfEcuYmR56vM08Chmd0aag0XpKq-YZ-MgG2O_3KyDs9BQBPmohDX6qyMH2_N7LyfGY5MsGK9bWFDL6JiXuQ5YtUa7_fBZrxx7jbSbmYjomJiKG7SHXlyeGsPLJ1DyDjqJJ3zCNq_i-ekGEhUKwN2DJuB5gNmVlVKnZakUKwn4OkgS2ivsH3qNZnbCY37QGKaL2MuJ2S16-EVpORlyUWFn-XvIaUWFR5gTNfiFVBugaF9PFuq6yPKMXYxhkyrZcfJ8RTeiE5xbcy_1BW0Vyc8U3MxiTom4WIndXav6O1_yPogHBKWXybwR0L4F6ilqe6Ycps4A" 
# NOTE: The token above is 'stolen' from the Web browser 'auth' and implicit response...
dictPy3GblEnv["sCxRSServerHost"]           = "darylcoxe36c"
dictPy3GblEnv["sCxRSServerPort"]           = "9000"
dictPy3GblEnv["cxReqReportScanId"]         = "1000165"
dictPy3GblEnv["cxReqReportName"]           = "Python3ScanVulnerabilityReport"
dictPy3GblEnv["cxReqReportFormat"]         = "PDF"

# Class to handle all 'http'/'https' 'client' traffic and requests:

class HttpRequestHandlerClient(object):

    sClassMod         = __name__
    sClassId          = "HttpRequestHandlerClient"
    sClassVers        = "(v1.0101)"
    sClassDisp        = sClassMod+"."+sClassId+" "+sClassVers+": "

    dictPy3GblEnv     = None
    dictReqHandlerEnv = None

    def __init__(self, dictPy3GblEnv=None):

        try:

            self.setPy3GblEnv(dictPy3GblEnv=dictPy3GblEnv)

            self.dictReqHandlerEnv = collections.defaultdict()

            # - - - - - Setup the AioHttp 'Request' Handler Environment dictionary (standard) - - - - -

            self.dictReqHandlerEnv["sReqHandlerId"]             = self.sClassId
            self.dictReqHandlerEnv["sReqHandlerVers"]           = self.sClassVers
            self.dictReqHandlerEnv["sReqHandlerDisp"]           = self.sClassDisp

            self.dictReqHandlerEnv["cxAioHttpSession"]          = None
            self.dictReqHandlerEnv["cxReqReportOutputFile"]     = None
            self.dictReqHandlerEnv["bCxReportSvcReportDone"]    = False
            self.dictReqHandlerEnv["cxReportSvcReportId"]       = -1
            self.dictReqHandlerEnv["cxReportSvcReportIdStatus"] = None

        except Exception as inst:

            print("%s '__init__()' - exception occured..." % (self.sClassDisp))
            print(type(inst))
            print(inst)

            excType, excValue, excTraceback = sys.exc_info()
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

            print("- - - ")
            print('\n'.join(asTracebackLines))
            print("- - - ")

    def getPy3GblEnv(self):

        return self.dictPy3GblEnv

    def setPy3GblEnv(self, dictPy3GblEnv=False):

        self.dictPy3GblEnv = dictPy3GblEnv

    def dump_fields(self):

        if self.dictPy3GblEnv["bVerbose"] == True:

            print("%s Dump of the variable(s) content of this class:" % (self.sClassDisp))
            print("%s The contents of 'dictPy3GblEnv' is [%s]..." % (self.sClassDisp, self.dictPy3GblEnv))
            print("%s The contents of 'dictReqHandlerEnv' is [%s]..." % (self.sClassDisp, self.dictReqHandlerEnv))

    def toString(self):

        asObjDetail = list();

        asObjDetail.append("'sClassDisp' is [%s], " % (self.sClassDisp))
        asObjDetail.append("'dictPy3GblEnv' is [%s], " % (self.dictPy3GblEnv))
        asObjDetail.append("'dictReqHandlerEnv' is [%s]. " % (self.dictReqHandlerEnv))

        return ''.join(asObjDetail)

    def __str__(self):

        return self.toString()

    def __repr__(self):

        return self.toString()

    async def retrieveCxReportingServiceReport(self) -> None:

        assert len(self.dictPy3GblEnv) > 0, "Default Python3 'Global' Environmental dictionary 'self.dictPy3GblEnv' has NO Element(s) - Fatal!"
        assert len(self.dictReqHandlerEnv) > 0, "AioHttp 'Request' Handler Environmental dictionary 'dictReqHandlerEnv' has NO Element(s) - Fatal!"

        async with aiohttp.ClientSession() as self.dictReqHandlerEnv["cxAioHttpSession"]:

            await self.__connectHttpClientSession()

            if self.dictPy3GblEnv["bProcessingError"] == True:
            
                print("%s 'HttpRequestHandlerClient.__connectHttpClientSession()' - returned a 'processing' error flag - Error!" % (self.dictPy3GblEnv["sScriptDisp"]))

                return

            await self.__createScanVulnerabilityReport()

            if self.dictReqHandlerEnv["cxReportSvcReportId"] < 0:

                self.dictPy3GblEnv["bProcessingError"] = True

                print("%s 'HttpRequestHandlerClient.__createScanVulnerabilityReport()' - 'client' Session failed to create a Report ID - Error!" % (self.dictPy3GblEnv["sScriptDisp"]))

                return

            self.dictReqHandlerEnv["bCxReportSvcReportDone"] == False

            while self.dictReqHandlerEnv["bCxReportSvcReportDone"] == False:

                await self.__updateReportAvailability()

                if self.dictReqHandlerEnv["bCxReportSvcReportDone"] == False:

                    print("%s 'client' Session indicates that the Report ID has Not 'Finished' ('status' is [%s]) - waiting 10 seconds..." % (self.dictPy3GblEnv["sScriptDisp"], self.dictReqHandlerEnv["cxReportSvcReportIdStatus"]))

                    await asyncio.sleep(10)

            print("%s 'client' Session indicates that the Report ID has 'Finished' ('status' is [%s])..." % (self.dictPy3GblEnv["sScriptDisp"], self.dictReqHandlerEnv["cxReportSvcReportIdStatus"]))

            self.dictReqHandlerEnv["cxReqReportOutputFile"] = None

            await self.__fetchScanVulnerabilityReport()

            if self.dictReqHandlerEnv["cxReqReportOutputFile"] != None:

                self.dictReqHandlerEnv["cxReqReportOutputFile"] = self.dictReqHandlerEnv["cxReqReportOutputFile"].strip()

            if self.dictReqHandlerEnv["cxReqReportOutputFile"] == None or \
               len(self.dictReqHandlerEnv["cxReqReportOutputFile"]) < 1:

                self.dictPy3GblEnv["bProcessingError"] = True

                print("%s 'HttpRequestHandlerClient.__fetchScanVulnerabilityReport()' - 'client' Session failed to retrieve a CxReportingService 'report' - Error!" % (self.dictPy3GblEnv["sScriptDisp"]))

                return

            return

    async def __connectHttpClientSession(self) -> None:

        assert len(self.dictPy3GblEnv) > 0, "Default Python3 'Global' Environmental dictionary 'self.dictPy3GblEnv' has NO Element(s) - Fatal!"
        assert len(self.dictReqHandlerEnv) > 0, "AioHttp 'Request' Handler Environmental dictionary 'dictReqHandlerEnv' has NO Element(s) - Fatal!"

        try:

        # =====================================================================================================
        #   # This version does NOT make a call to get the 'identity' token (it's 'stolen' from the browser)...
        #
        #   await self.retrieveOAuth2IdentityConnectToken()
        #
        #   if self.dictPy3GblEnv["bProcessingError"] == True:
        #
        #       return
        # =====================================================================================================

            if self.dictPy3GblEnv["cxAccessToken"] != None:

                self.dictPy3GblEnv["cxAccessToken"] = self.dictPy3GblEnv["cxAccessToken"].strip()

            if self.dictPy3GblEnv["cxAccessToken"] == None or \
               len(self.dictPy3GblEnv["cxAccessToken"]) < 1:

                self.dictPy3GblEnv["bProcessingError"] = True

                print("%s 'HttpRequestHandlerClient.__connectHttpClientSession()' - 'client' Session failed to obtain an OAuth2 'access' Token and 'authorize' grant - Error!" % (self.dictPy3GblEnv["sScriptDisp"]))

                return

            return

        except Exception as inst:

            print("%s 'HttpRequestHandlerClient.__connectHttpClientSession()' - exception occured..." % (self.dictPy3GblEnv["sScriptDisp"]))
            print(type(inst))
            print(inst)

            excType, excValue, excTraceback = sys.exc_info()
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

            print("- - - ")
            print('\n'.join(asTracebackLines))
            print("- - - ", flush=True)

            self.dictPy3GblEnv["bProcessingError"] = True

    async def __createScanVulnerabilityReport(self) -> None:

        assert len(self.dictPy3GblEnv) > 0, "Default Python3 'Global' Environmental dictionary 'self.dictPy3GblEnv' has NO Element(s) - Fatal!"
        assert len(self.dictReqHandlerEnv) > 0, "AioHttp 'Request' Handler Environmental dictionary 'dictReqHandlerEnv' has NO Element(s) - Fatal!"

        self.dictPy3GblEnv["bProcessingError"]            = False
        self.dictReqHandlerEnv["bCxReportSvcReportDone"]  = False
        self.dictPy3GblEnv["cHttpPostRequests"]          += 1

        cxReqRespOk   = [201]
        cxReqType     = "POST"
        cxReqURL      = ("http://%s:%s/api/reports" % (self.dictPy3GblEnv["sCxRSServerHost"], self.dictPy3GblEnv["sCxRSServerPort"]))
        cxReqJsonLoad = {"templateId"    : 1,
                         "entityId"      : [self.dictPy3GblEnv["cxReqReportScanId"]],
                         "reportName"    : self.dictPy3GblEnv["cxReqReportName"],
                         "filters"       : [],
                         "outputFormat"  : self.dictPy3GblEnv["cxReqReportFormat"]
                        }
        cxReqHeaders  = {
                         "Accept"        : "application/json",
                         "Content-Type"  : "application/json",
                         "Authorization" : ("%s %s" % (self.dictPy3GblEnv["cxAccessTokenType"], self.dictPy3GblEnv["cxAccessToken"])),
                         "cache-control" : "no-cache"
                        }

        try:

            print("%s Issuing a '%s' to URL [%s] with 'json' data of [%s] and header(s) of [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqType, cxReqURL, cxReqJsonLoad, cxReqHeaders), flush=True)

            async with self.dictReqHandlerEnv["cxAioHttpSession"].request(cxReqType, cxReqURL, json=cxReqJsonLoad, headers=cxReqHeaders) as cxReqResponse:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status)))
                print("")

                if cxReqResponse.status in cxReqRespOk:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status)))

                else:

                    self.dictPy3GblEnv["bProcessingError"] = True

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status), cxReqRespOk))

                if self.dictPy3GblEnv["bVerbose"] == True:

                    print("%s The URL Request returned Response text of [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], await cxReqResponse.text()))
                    print("")

                else:

                    print("")

                if self.dictPy3GblEnv["bProcessingError"] == True:

                    return

                cxReqResponseJson = await cxReqResponse.json()

                print("%s Response 'json' is [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponseJson))
                print("")

                if "reportId" in cxReqResponseJson:
             
                    self.dictReqHandlerEnv["cxReportSvcReportId"] = cxReqResponseJson["reportId"]
             
                print("%s The URL Request returned Response 'json' value(s) of:" % (self.dictPy3GblEnv["sScriptDisp"]))
                print("    'reportId' (%d)..." % (self.dictReqHandlerEnv["cxReportSvcReportId"]))
                print("", flush=True)

        except Exception as inst:

            print("%s 'HttpRequestHandlerClient.__createScanVulnerabilityReport()' - exception occured..." % (self.dictPy3GblEnv["sScriptDisp"]))
            print(type(inst))
            print(inst)

            excType, excValue, excTraceback = sys.exc_info()
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

            print("- - - ")
            print('\n'.join(asTracebackLines))
            print("- - - ", flush=True)

            self.dictPy3GblEnv["bProcessingError"] = True

    async def __updateReportAvailability(self) -> None:

        assert len(self.dictPy3GblEnv) > 0, "Default Python3 'Global' Environmental dictionary 'self.dictPy3GblEnv' has NO Element(s) - Fatal!"
        assert len(self.dictReqHandlerEnv) > 0, "AioHttp 'Request' Handler Environmental dictionary 'dictReqHandlerEnv' has NO Element(s) - Fatal!"

        self.dictPy3GblEnv["bProcessingError"]            = False
        self.dictReqHandlerEnv["bCxReportSvcReportDone"]  = False
        self.dictPy3GblEnv["cHttpGetRequests"]           += 1

        cxReqRespOk   = [200]
        cxReqType     = "GET"
        cxReqURL      = ("http://%s:%s/api/reports/%d/status" % (self.dictPy3GblEnv["sCxRSServerHost"], self.dictPy3GblEnv["sCxRSServerPort"], self.dictReqHandlerEnv["cxReportSvcReportId"]))
        cxReqJsonLoad = {"id"            : self.dictReqHandlerEnv["cxReportSvcReportId"]
                        }
        cxReqHeaders  = {
                         "Accept"        : "application/json",
                         "Content-Type"  : "application/json",
                         "Authorization" : ("%s %s" % (self.dictPy3GblEnv["cxAccessTokenType"], self.dictPy3GblEnv["cxAccessToken"])),
                         "cache-control" : "no-cache"
                        }

        try:

            print("%s Issuing a '%s' to URL [%s] with 'json' data of [%s] and header(s) of [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqType, cxReqURL, cxReqJsonLoad, cxReqHeaders), flush=True)

            async with self.dictReqHandlerEnv["cxAioHttpSession"].request(cxReqType, cxReqURL, json=cxReqJsonLoad, headers=cxReqHeaders) as cxReqResponse:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status)))
                print("")

                if cxReqResponse.status in cxReqRespOk:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status)))

                else:

                    self.dictPy3GblEnv["bProcessingError"] = True

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status), cxReqRespOk))

                if self.dictPy3GblEnv["bVerbose"] == True:

                    print("%s The URL Request returned Response text of [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], await cxReqResponse.text()))
                    print("")

                else:

                    print("")

                if self.dictPy3GblEnv["bProcessingError"] == True:

                    return

                cxReqResponseJson = await cxReqResponse.json()

                print("%s Response 'json' is [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponseJson))
                print("")

                cxReportingSvcStatusReportId     = None
                cxReportingSvcStatusReport       = None
                cxReportingSvcStatusCreationDate = None
                cxReportingSvcStatusMessage      = None

                if "reportId" in cxReqResponseJson:

                    cxReportingSvcStatusReportId     = cxReqResponseJson["reportId"]

                if "reportStatus" in cxReqResponseJson:

                    cxReportingSvcStatusReport       = cxReqResponseJson["reportStatus"]
                    self.dictReqHandlerEnv["cxReportSvcReportIdStatus"]        = cxReqResponseJson["reportStatus"] 

                if "creationDate" in cxReqResponseJson:

                    cxReportingSvcStatusCreationDate = cxReqResponseJson["creationDate"]

                if "message" in cxReqResponseJson:

                    cxReportingSvcStatusMessage      = cxReqResponseJson["message"]

                print("%s The URL Request returned Response 'json' value(s) of:" % (self.dictPy3GblEnv["sScriptDisp"]))
                print("    'reportId'     (%d)..." % (cxReportingSvcStatusReportId))
                print("    'reportStatus' [%s]..." % (cxReportingSvcStatusReport))
                print("    'creationDate' [%s]..." % (cxReportingSvcStatusCreationDate))
                print("    'message'      [%s]..." % (cxReportingSvcStatusMessage))
                print("", flush=True)

                if cxReportingSvcStatusReport == "Finished":

                    self.dictReqHandlerEnv["bCxReportSvcReportDone"] = True

                else:

                    self.dictReqHandlerEnv["bCxReportSvcReportDone"] = False

        except Exception as inst:

            print("%s 'HttpRequestHandlerClient.__updateReportAvailability()' - exception occured..." % (self.dictPy3GblEnv["sScriptDisp"]))
            print(type(inst))
            print(inst)

            excType, excValue, excTraceback = sys.exc_info()
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

            print("- - - ")
            print('\n'.join(asTracebackLines))
            print("- - - ", flush=True)

            self.dictPy3GblEnv["bProcessingError"] = True

    async def __fetchScanVulnerabilityReport(self) -> None:

        assert len(self.dictPy3GblEnv) > 0, "Default Python3 'Global' Environmental dictionary 'self.dictPy3GblEnv' has NO Element(s) - Fatal!"
        assert len(self.dictReqHandlerEnv) > 0, "AioHttp 'Request' Handler Environmental dictionary 'dictReqHandlerEnv' has NO Element(s) - Fatal!"

        self.dictPy3GblEnv["bProcessingError"]           = False
        self.dictReqHandlerEnv["cxReqReportOutputFile"]  = None
        self.dictPy3GblEnv["cHttpGetRequests"]          += 1

        cxReqRespOk   = [200]
        cxReqType     = "GET"
        cxReqURL      = ("http://%s:%s/api/reports/%d" % (self.dictPy3GblEnv["sCxRSServerHost"], self.dictPy3GblEnv["sCxRSServerPort"], self.dictReqHandlerEnv["cxReportSvcReportId"]))
        cxReqJsonLoad = {"id"            : self.dictReqHandlerEnv["cxReportSvcReportId"]
                        }
        cxReqHeaders  = {
                         "Accept"        : "application/json",
                         "Content-Type"  : "application/json",
                         "Authorization" : ("%s %s" % (self.dictPy3GblEnv["cxAccessTokenType"], self.dictPy3GblEnv["cxAccessToken"])),
                         "cache-control" : "no-cache"
                        }

        try:

            print("%s Issuing a '%s' to URL [%s] with 'json' data of [%s] and header(s) of [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqType, cxReqURL, cxReqJsonLoad, cxReqHeaders), flush=True)

            async with self.dictReqHandlerEnv["cxAioHttpSession"].request(cxReqType, cxReqURL, json=cxReqJsonLoad, headers=cxReqHeaders) as cxReqResponse:

                print("%s The URL Request returned a 'status' code of [%s] Type [%s]..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status)))
                print("")

                if cxReqResponse.status in cxReqRespOk:

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is a 'good' response..." % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status)))

                else:

                    self.dictPy3GblEnv["bProcessingError"] = True

                    print("%s The URL Request returned a 'status' code of [%s] Type [%s] is NOT a 'good' response of [%s] - Error!" % (self.dictPy3GblEnv["sScriptDisp"], cxReqResponse.status, type(cxReqResponse.status), cxReqRespOk))

                if self.dictPy3GblEnv["bProcessingError"] == True:

                    return

                # Deal with the 'response' as 'binary'...

                print("%s Read the URL Request 'response' BODY as 'binary'..." % (self.dictPy3GblEnv["sScriptDisp"]))

                cxReqResponseBody = await cxReqResponse.read()

                if cxReqResponseBody == None:

                    self.dictPy3GblEnv["bProcessingError"] = True

                    print("%s Read the URL Request 'response' BODY as a 'binary' of (0) byte(s) - Error!" % (self.dictPy3GblEnv["sScriptDisp"]))

                    return

                print("%s Read the URL Request 'response' BODY as a 'binary' of (%d) byte(s)..." % (self.dictPy3GblEnv["sScriptDisp"], len(cxReqResponseBody)))

                dtNow                                           = datetime.now()
                sDTNowFilenameStamp                             = dtNow.strftime("%Y%m%d-%H.%M.%S")
                self.dictPy3GblEnv["sCurrentWorkingDir"]        = os.getcwd()
                self.dictPy3GblEnv["sReqReportFormatLow"]       = self.dictPy3GblEnv["cxReqReportFormat"].lower()
                self.dictPy3GblEnv["sReqReportFilenameExt"]     = ("%s_%s_%s.%s" % (self.dictPy3GblEnv["cxReqReportName"], self.dictPy3GblEnv["cxReqReportScanId"], sDTNowFilenameStamp, self.dictPy3GblEnv["sReqReportFormatLow"]))
                self.dictReqHandlerEnv["cxReqReportOutputFile"] = os.path.join(self.dictPy3GblEnv["sCurrentWorkingDir"], self.dictPy3GblEnv["sReqReportFilenameExt"])

                if self.dictPy3GblEnv["bVerbose"] == True:

                    print("%s CxReportingService 'variable(s)':" % (self.dictPy3GblEnv["sScriptDisp"]))
                    print("    'sDTNowFilenameStamp'                          [%s]..." % (sDTNowFilenameStamp))
                    print("    'dictPy3GblEnv[\"sCurrentWorkingDir\"]'        [%s]..." % (self.dictPy3GblEnv["sCurrentWorkingDir"]))
                    print("    'dictPy3GblEnv[\"sReqReportFormatLow\"]'       [%s]..." % (self.dictPy3GblEnv["sReqReportFormatLow"]))
                    print("    'dictPy3GblEnv[\"sReqReportFilenameExt\"]'     [%s]..." % (self.dictPy3GblEnv["sReqReportFilenameExt"]))
                    print("    'dictReqHandlerEnv[\"cxReqReportOutputFile\"]' [%s]..." % (self.dictReqHandlerEnv["cxReqReportOutputFile"]))
                    print("", flush=True);

                print("%s Opening the 'dictReqHandlerEnv[\"cxReqReportOutputFile\"]' file of [%s] in 'binary' mode to write (%d) byte(s)..." % (self.dictPy3GblEnv["sScriptDisp"], self.dictReqHandlerEnv["cxReqReportOutputFile"], len(cxReqResponseBody)))

                fCxReqReportOutput = open(self.dictReqHandlerEnv["cxReqReportOutputFile"], 'w+b')

                fCxReqReportOutput.write(cxReqResponseBody)
                fCxReqReportOutput.close()

                print("%s Closed the 'dictReqHandlerEnv[\"cxReqReportOutputFile\"]' file of [%s] after writing (%d) byte(s)..." % (self.dictPy3GblEnv["sScriptDisp"], self.dictReqHandlerEnv["cxReqReportOutputFile"], len(cxReqResponseBody)))
                print("", flush=True);

                return

        except Exception as inst:

            print("%s 'HttpRequestHandlerClient.__fetchScanVulnerabilityReport()' - exception occured..." % (self.dictPy3GblEnv["sScriptDisp"]))
            print(type(inst))
            print(inst)

            excType, excValue, excTraceback = sys.exc_info()
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

            print("- - - ")
            print('\n'.join(asTracebackLines))
            print("- - - ", flush=True)

            self.dictPy3GblEnv["bProcessingError"] = True

# - - - - - - -
# 'main' method:
# - - - - - - -

def main():

    global dictPy3GblEnv

    # - - - - - TEST - - - - -
    #   dictPy3GblEnv = {}

    assert len(dictPy3GblEnv) > 0, "Default Python3 'Global' Environmental dictionary 'dictPy3GblEnv' has NO Element(s) - Fatal!"

    try:

        dtNow       = datetime.now()
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S")

        print("%s The CxReportingService Report 'creator' #2 by Python is starting execution from Server [%s] on [%s] under Python [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sServerNode"], sDTNowStamp, dictPy3GblEnv["sPythonVers"]))
        print("")

        if dictPy3GblEnv["bPlatformIsWindows"] == True:

            import win32con
            import win32api

            print("%s The platform 'system' of [%s] indicates this is a Microsoft/Windows system - 'win32con'/'win32api' have been imported..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sPlatform"]))

        else:

            print("%s The platform 'system' is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sPlatform"]))

        # NOTE: 'cxrs' is CxReportingService...

        dictPy3GblEnv["optParser"].add_option("-v", "--verbose", dest="run_verbose", default=False, help="Run VERBOSE", action="store_true")
        dictPy3GblEnv["optParser"].add_option("-l", "--log-file", dest="log_file", default="", help="(Output) 'log' file [generated]")

        dictPy3GblEnv["optParser"].add_option("--cxrs-host", dest="cxrs_server_host", default="darylcoxe36c", help="'cxrs' Server 'host'", metavar="CxRS-Server-Host")
        dictPy3GblEnv["optParser"].add_option("--cxrs-port", dest="cxrs_server_port", default="9000", help="'cxrs' Server 'port'", metavar="CxRS-Server-Port")
        dictPy3GblEnv["optParser"].add_option("--token-type", dest="access_token_type", default="Bearer", help="(OAuth2) 'implicit' Access 'token' TYPE")
        dictPy3GblEnv["optParser"].add_option("--token", dest="access_token", default="", help="(OAuth2) 'implicit' Access 'token'")
        dictPy3GblEnv["optParser"].add_option("--scan-id", dest="cxrs_scan_id", default="1000165", help="'cxrs' Report Scan ID")
        dictPy3GblEnv["optParser"].add_option("--report-name", dest="cxrs_report_name", default="Python3ScanVulnerabilityReport", help="'cxrs' Report Name")
        dictPy3GblEnv["optParser"].add_option("--report-format", dest="cxrs_report_format", default="PDF", help="'cxrs' Report Format")

        (options, args) = dictPy3GblEnv["optParser"].parse_args()

        dictPy3GblEnv["bVerbose"]          = options.run_verbose
        dictPy3GblEnv["sCxRSServerHost"]   = options.cxrs_server_host.strip()
        dictPy3GblEnv["sCxRSServerPort"]   = options.cxrs_server_port.strip()
        dictPy3GblEnv["sOutputLogFile"]    = options.log_file.strip()

        dictPy3GblEnv["cxAccessTokenType"] = options.access_token_type.strip()
        dictPy3GblEnv["cxAccessToken"]     = options.access_token.strip()
        dictPy3GblEnv["cxReqReportScanId"] = options.cxrs_scan_id.strip()
        dictPy3GblEnv["cxReqReportName"]   = options.cxrs_report_name.strip()
        dictPy3GblEnv["cxReqReportFormat"] = options.cxrs_report_format.strip()

        if dictPy3GblEnv["sCxRSServerHost"] != None:

            dictPy3GblEnv["sCxRSServerHost"] = dictPy3GblEnv["sCxRSServerHost"].strip()

        if dictPy3GblEnv["sCxRSServerHost"] == None or \
           len(dictPy3GblEnv["sCxRSServerHost"]) < 1:

            dictPy3GblEnv["sCxRSServerHost"] = "darylcoxe36c"

        if dictPy3GblEnv["sCxRSServerPort"] != None:

            dictPy3GblEnv["sCxRSServerPort"] = dictPy3GblEnv["sCxRSServerPort"].strip()

        if dictPy3GblEnv["sCxRSServerPort"] == None or \
           len(dictPy3GblEnv["sCxRSServerPort"]) < 1:

            dictPy3GblEnv["sCxRSServerPort"] = "9000"

        dictPy3GblEnv["iCxRSServerPort"] = int(dictPy3GblEnv["sCxRSServerPort"])

        if dictPy3GblEnv["cxAccessTokenType"] != None:

            dictPy3GblEnv["cxAccessTokenType"] = dictPy3GblEnv["cxAccessTokenType"].strip()

        if dictPy3GblEnv["cxAccessTokenType"] == None or \
           len(dictPy3GblEnv["cxAccessTokenType"]) < 1:

            dictPy3GblEnv["cxAccessTokenType"] = "Bearer"

        if dictPy3GblEnv["cxAccessToken"] != None:

            dictPy3GblEnv["cxAccessToken"] = dictPy3GblEnv["cxAccessToken"].strip()

        if dictPy3GblEnv["cxAccessToken"] == None or \
           len(dictPy3GblEnv["cxAccessToken"]) < 1:

            dictPy3GblEnv["cxAccessToken"] = ""

        if dictPy3GblEnv["cxReqReportScanId"] != None:

            dictPy3GblEnv["cxReqReportScanId"] = dictPy3GblEnv["cxReqReportScanId"].strip()

        if dictPy3GblEnv["cxReqReportScanId"] == None or \
           len(dictPy3GblEnv["cxReqReportScanId"]) < 1:

            dictPy3GblEnv["cxReqReportScanId"] = "1000165"

        if dictPy3GblEnv["cxReqReportName"] != None:

            dictPy3GblEnv["cxReqReportName"] = dictPy3GblEnv["cxReqReportName"].strip()

        if dictPy3GblEnv["cxReqReportName"] == None or \
           len(dictPy3GblEnv["cxReqReportName"]) < 1:

            dictPy3GblEnv["cxReqReportName"] = "Python3ScanVulnerabilityReport"

        if dictPy3GblEnv["cxReqReportFormat"] != None:

            dictPy3GblEnv["cxReqReportFormat"] = dictPy3GblEnv["cxReqReportFormat"].strip()

        if dictPy3GblEnv["cxReqReportFormat"] == None or \
           len(dictPy3GblEnv["cxReqReportFormat"]) < 1:

            dictPy3GblEnv["cxReqReportFormat"] = "PDF"

    #   if dictPy3GblEnv["bVerbose"] == True:

        print("%s Command VERBOSE flag is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["bVerbose"]))
        print("%s Command 'dictPy3GblEnv' is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv))
        print("")
        print("%s Command 'cxrs' Server host (string) is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sCxRSServerHost"]))
        print("%s Command 'cxrs' Server port (string) is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sCxRSServerPort"]))
        print("%s Command 'cxrs' Server port (int)    is (%d)..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["iCxRSServerPort"]))
        print("%s Command 'cxrs' Access 'token' TYPE  is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["cxAccessTokenType"]))
        print("%s Command 'cxrs' Access 'token'       is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["cxAccessToken"]))
        print("%s Command 'cxrs' Report 'scan id'     is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["cxReqReportScanId"]))
        print("%s Command 'cxrs' Report 'name'        is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["cxReqReportName"]))
        print("%s Command 'cxrs' Report 'format'      is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["cxReqReportFormat"]))
        print("")
        print("%s Command (Output) 'log' file is [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sOutputLogFile"]))
        print("", flush=True)

        if dictPy3GblEnv["sOutputLogFile"] != None:

            dictPy3GblEnv["sOutputLogFile"] = dictPy3GblEnv["sOutputLogFile"].strip()

        if dictPy3GblEnv["sOutputLogFile"] == None or \
           len(dictPy3GblEnv["sOutputLogFile"]) < 1:

            print("%s The (Output) 'log' filename is None or Empty - this output will be bypassed - Warning!" % (dictPy3GblEnv["sScriptDisp"]))

            dictPy3GblEnv["sOutputLogFile"] == None

        else:

            if dictPy3GblEnv["bVerbose"] == True:

                print("")
                print("%s Generating the (Output) 'log' into the file [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sOutputLogFile"]))
                print("")

    #   Main 'processing'...

        try:

            httpReqHandler = HttpRequestHandlerClient(dictPy3GblEnv)
            asyncioLoop    = asyncio.get_event_loop()

            asyncioLoop.run_until_complete(httpReqHandler.retrieveCxReportingServiceReport())

            asyncioLoop.close()

        except Exception as inst:

            print("%s 'main()' - 'main()' - exception occured..." % (dictPy3GblEnv["sScriptDisp"]))
            print(type(inst))
            print(inst)

            excType, excValue, excTraceback = sys.exc_info()
            asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

            print("- - - ")
            print('\n'.join(asTracebackLines))
            print("- - - ", flush=True)

            dictPy3GblEnv["bProcessingError"] = True

        except KeyboardInterrupt:

            print("%s 'main()' - KeyboardInterrupt - Web Server is Shutting down..." % (dictPy3GblEnv["sScriptDisp"]))
            print("", flush=True)

    #   Cleanup...

        dtNow       = datetime.now()
        sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S")

        print("")        
        print("%s The CxReportingService Report 'creator' #2 by Python is ending execution from Server [%s] on [%s] under Python [%s]..." % (dictPy3GblEnv["sScriptDisp"], dictPy3GblEnv["sServerNode"], sDTNowStamp, dictPy3GblEnv["sPythonVers"]))
        print("", flush=True)

    except Exception as inst:

        print("%s 'main()' - exception occured..." % (dictPy3GblEnv["sScriptDisp"]))
        print(type(inst))
        print(inst)

        excType, excValue, excTraceback = sys.exc_info()
        asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

        print("- - - ")
        print('\n'.join(asTracebackLines))
        print("- - - ", flush=True)

        dictPy3GblEnv["bProcessingError"] = True

        return False

    return True

# - - - - - - -
# 'main' logic:
# - - - - - - -

if __name__ == '__main__':

    try:

        pass

    except Exception as inst:

        print("%s '<before>-main()' - exception occured..." % (dictPy3GblEnv["sScriptDisp"]))
        print(type(inst))
        print(inst)

        excType, excValue, excTraceback = sys.exc_info()
        asTracebackLines                = traceback.format_exception(excType, excValue, excTraceback)

        print("- - - ")
        print('\n'.join(asTracebackLines))
        print("- - - ")

        sys.exit(99)

    bCmdExecOk  = main()

    dtNow       = datetime.now()
    sDTNowStamp = dtNow.strftime("%Y/%m/%d at %H:%M:%S")
    tmEndTime   = time.time()
    tmElapsed   = (tmEndTime - dictPy3GblEnv["tmStartTime"])
    sTMElapsed  = time.strftime("%H:%M:%S", time.gmtime(tmElapsed))

    print("%s The CxReportingService Report 'creator' #2 by Python is ending execution with an 'elapsed' time of [%s - (%d)]..." % (dictPy3GblEnv["sScriptDisp"], sTMElapsed, tmElapsed))
    print("", flush=True)

    if bCmdExecOk                        == False or \
       dictPy3GblEnv["bProcessingError"] == True:

        print("%s Exiting with a Return Code of (31)..." % (dictPy3GblEnv["sScriptDisp"]))
        print("", flush=True)

        sys.exit(31)

    print("%s Exiting with a Return Code of (0)..." % (dictPy3GblEnv["sScriptDisp"]))
    print("", flush=True)

    sys.exit(0)

