from django.db import connections
from django.http import HttpResponseBadRequest,HttpResponseRedirect, HttpResponse
from collections import namedtuple,defaultdict,OrderedDict
from django.shortcuts import render_to_response,render
from views_default import csvparse, getdbname

import json
import cx_Oracle
import socket
import logging

logger = logging.getLogger('goldmine2')

# To enabling the comments on each component by user and storing the detail in table.
# cinscplp179:8002/gmjson/addcomments/?compname = router_ptest_scripts&comment = updated sonar and design&username=pramakr2&type=new
def addcomments(request):
   msg = {}
   if request.method == 'GET': 
      compname = request.GET.get('compname')
      comment = request.GET.get('comment')
      username = request.GET.get('username')
   cursor = getdbname()
   try:
      insertQuery = "INSERT INTO GM2_COMP_COMMENTS(COMPNAME, COMMENTS, USERNAME, TIMESTAMP) VALUES('"+str(compname)+"', '"+str(comment)+"', '"+str(username)+"', SYSDATE)"
      cursor.execute(insertQuery)
      msg['message'] = 'Successfully added comment' 
   except Exception as e:
      print str(e)
      logger.error(str(e))
   cursor.close()
   return HttpResponse(json.dumps(msg))
   
# Inserting type as true or false(new comp or not) in db
#cinscplp179:8002/gmjson/selnewcomp/?compname=att_yang_repo&username=pramakr2&type=true
def selnewcomp(request):
   msg = {}
   if request.method == 'GET': 
      type = request.GET.get('type')
      compname = request.GET.get('compname')
      username = request.GET.get('username')
   cursor = getdbname()

   """ INSERTING THE DATA WHERE COMPONENT NOT AVAILABLE"""
   try:
      insertQuery = "INSERT INTO GM2_COMP_TYPE(COMPNAME, TYPE, USERNAME) VALUES('"+str(compname)+"', '"+str(type)+"', '"+str(username)+"')"
      cursor.execute(insertQuery)
      msg['message'] = 'Successfully updated component status' 
   except Exception as e:
      print str(e)
      logger.error(str(e))

   cursor.close()
   return HttpResponse(json.dumps(msg))

# Listing all comments made by user for each comp and displaying in frontend
   
def showcomments(request):
   comments = {"threadlist":[]}
   if request.method == 'GET': 
      compname = request.GET.get('compname')
   cursor = getdbname()
   
   """comments portion"""
   try:
      selectQuery = "SELECT * FROM GM2_COMP_COMMENTS WHERE COMPNAME = '"+str(compname)+"'"
      cursor.execute(selectQuery)
      rows = cursor.fetchall()
      for row in rows:
         username = str(row[0])
         comment = str(row[1])
         compname = str(row[2])
         stamp = str(row[3])
         type = 'comment'
         comments['threadlist'].append({"componentname":compname, "msg":comment, "username":username, "type":type, "time":stamp})
   except Exception as e:
      print str(e)
      logger.error(str(e))
   
   """activity portion"""
   try:
      selectQuery = "SELECT * FROM GM2_COMP_ACTIVITY WHERE COMPNAME = '"+str(compname)+"'"
      cursor.execute(selectQuery)
      actrows = cursor.fetchall()
      if len(actrows)!=0:
         for actrow in actrows:
            type = 'activity'
            username = str(actrow[0])
            compname = str(actrow[1])
            activity = str(actrow[2])
            activitystamp = str(actrow[3])
            comments['threadlist'].append({"componentname":compname, "msg":activity, "username":username, "type":type, "time":activitystamp})
   except Exception as e:
      print str(e)
      logger.error(str(e))

   cursor.close()
   return HttpResponse(json.dumps(comments))
