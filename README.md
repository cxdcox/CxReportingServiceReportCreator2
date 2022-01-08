# Checkmarx Python tools

## Code Repository

This code repository contains several Checkmarx tools written in Python.

All tools will display their command 'help':

    > python3.9 <Tool-Name>.py --help

All tools will run under version 3 of Python (Python 3.7+). 
Python (for your OS) can be downloaded from: https://www.python.org/downloads/

Some of the tools have extra Python package requirements. Make sure you have
the latest version of 'pip'. From a 'elevated' (Admin) command prompt, run

    > python3.9 -m pip install pip

If this complains that you already have 'pip' installed but should upgrade, run

    > python3.9 -m pip install --upgrade pip

If the terminal complains that 'python3.8' is not found, try just 'python'.

To apply the required packages, run

    > pip install <package-name>

On Windows, the following 'extra' pip install commands may need to be issued:

    > pip install python-interface
    > pip install tqdm
    > pip install opencv-python

## Tool Functions

--- Tools Listing ---

1) CxReportingServiceReportCreator2.py - Creates Checkmarx Reporting Service Scan Vulnerability report.

## Tool #1 Notes (CxReportingServiceCreator2)

1) CxReportingServiceReportCreator2 - Creates Checkmarx Reporting Service Scan Vulnerability report.

--- Extra Package requirement(s) - Note: Some package(s) may already be installed ---

Run 'pip install <package-name>' for:

1) base64
2) html
3) json
4) asyncio
5) aiohttp

--- Source File(s) for the Tool(s) ---

    --- Commands ---
 1) CxReportingServiceReportCreator2.py

    --- Classes ---
 1) HttpRequestHandlerClient - Embedded within 'CxReportingServiceReportCreator2.py'

--- Documentation File(s) for the Tool(s) ---

 1) README.md - (this file) Documentation for CxReportingServiceReportCreator2.

## Setup instructions

--- How to setup to run the Tool ---

1) Make sure that a version of Python 3 (v3.7+) is installed. You can download Python (for your OS) from: https://www.python.org/downloads/

2) Make sure you have the latest version of 'pip'. From a 'elevated' (Admin) command prompt, 
   run: python -m pip install pip

3) Make sure you have the latest version of 'html'. From a 'elevated' (Admin) command prompt, 
   run: pip install html

4) Make sure you have the latest version of 'json'. From a 'elevated' (Admin) command prompt, 
   run: pip install json

5) Make sure you have the latest version of 'asyncio'. From a 'elevated' (Admin) command prompt, 
   run: pip install asyncio

6) Make sure you have the latest version of 'aiohttp'. From a 'elevated' (Admin) command prompt, 
   run: pip install aiohttp

7) On Windows:

       a) The following 'extra' pip install commands may need to be issued:
           pip install python-interface
           pip install tqdm
           pip install opencv-python

       b) In the Python installation directory the 'interface' package

           <Python-installation-directory>\Lib\site-packages\interface

          This directory may be named with an upper-case 'I' as 'Interface',
          if it is, rename it to 'interface' (lower-case 'i').

8) Download the 'CxReportingServiceReportCreator2_1.zip' (zip) file 
   and extract it to a subdirectory (on any machine with Python 3.7+ installed).

9) In a 'normal' command prompt, CD into the tool directory (containing the 'CxReportingServiceReportCreator2.py' file). 
   Run: python3.9 CxReportingServiceReportCreator2.py --help 

   This should display 'help' like the following:

        CxReportingServiceReportCreator2.py (v1.0203): The platform 'system' is [Darwin]...
        Usage: CxReportingServiceReportCreator2.py [options]

        Options:
          -h, --help            show this help message and exit
          -v, --verbose         Run VERBOSE
          -l LOG_FILE, --log-file=LOG_FILE
                                (Output) 'log' file [generated]
          --cxrs-host=CxRS-Server-Host
                                'cxrs' Server 'host'
          --cxrs-port=CxRS-Server-Port
                                'cxrs' Server 'port'
          --token-type=ACCESS_TOKEN_TYPE
                                (OAuth2) 'implicit' Access 'token' TYPE
          --token=ACCESS_TOKEN  (OAuth2) 'implicit' Access 'token'
          --scan-id=CXRS_SCAN_ID
                                'cxrs' Report Scan ID
          --report-name=CXRS_REPORT_NAME
                                'cxrs' Report Name
          --report-format=CXRS_REPORT_FORMAT
                                'cxrs' Report Format
## Operation

--- How to run the Tool ---

1) In a 'normal' command prompt, CD into the tool directory (containing the 'CxReportingServiceReportCreator2.py' file).

   Note: The 'token' is stolen from the HTTP/HTTPS Session that logged in to CxSAST/CxReportingService (Swagger).
         See 'Checkmarx_Implicit-Flow-Auth-Vulnerability_CxSAST-CxReportingService_12202021.pdf' for instructions.

   Run: 
       python CxReportingServiceReportCreator2.py
       -v 
       --cxrs-host=darylcoxe36c
       --cxrs-port=9000
       --token-type=Bearer
       --token=xxx (ACCESS_TOKEN (OAuth2) 'implicit' Access 'token')
       --scan-id=1000165
       --report-name=CxRS_Report_Name
       --report-format=PDF
       > CxReportingServiceReportCreator2.ot1_01082022.log 2>&1 

   Where: 
       a) The command can all be on one line. It's broken out to separate lines here to make it easier to read.
       c) The --cxrs-host needs to be updated to point to your CxReportingService host (by DNS name or IP).
          Like 'darylcoxe36c' or an IP like '192.168.1.155'.
       d) The --cxrs-port is the port that your CxReportingService is running on.
       e) The --token-type is the 'type' of the Token (default is 'Bearer').
       e) The --token is the 'stolen' Token from a CxSAST/CxReportingService login and 'implicit' authentication.
       f) The --scan-id is the ID of the Scan to pull the report for.
       g) The --report-name is name you want to give the report.
       h) The --report-format is the format of the report file (PDF or XML).

   Then:
       a) A Report of 'report-format' type with the 'report-name' (plus a date stamp) will be created in the current working directory.


