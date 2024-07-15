
from django.shortcuts import render
import requests
from django.http import JsonResponse
from supabase import create_client, Client
from datetime import date,datetime
#from rest_framework.views import APIView 
#from rest_framework.response import Response 
import plotly.express as px
import plotly.graph_objects as go

#from .utils import get_plot


TODAY = date.today().strftime("%Y-%m-%d")
TODAY = datetime(2024,4,2).strftime("%Y-%m-%d")


SUPABASE_URL = 'https://yiqlyfgpuclqunecsasi.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlpcWx5ZmdwdWNscXVuZWNzYXNpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTIzMjM5MzgsImV4cCI6MjAyNzg5OTkzOH0.xbT6_ncD_jNAWwnxwV98ZPxN34vACWDZ2aXiVbbFZc0'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_data_from_supabase(request,queryParams=None):
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
    }
    response = requests.get(f'{SUPABASE_URL}/rest/v1/Records', headers=headers,params=queryParams)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
def mainView(request):
        data = fetch_data_from_supabase(request)
        top_up=[]
        top_down=[]
        for item in data:
              if item["decision"].lower()=="up" and item['date']==TODAY:
                   top_up.append(item)
              elif item["decision"].lower()=="down" and item['date']==TODAY:    
                    top_down.append(item)
        top_up.sort(key = comp, reverse=True)         
        top_down.sort(key = comp,reverse=True)
        top_down_3=[]
        top_up_3=[]

        if(len(top_down)>3):
             top_down_3=[top_down[0],top_down[1],top_down[2]]
        else: 
             top_down_3=  top_down   
        if(len(top_up)>3):
             top_down_3=[top_up[0],top_up[1],top_up[2]]    
        else:
             top_up_3 = top_up  

        q= request.GET.get('q') if request.GET.get('q') !=None else ""
        Searchdata=None
        if(q):
          queryParams = {
            "select": "*",
            "symbol": f"ilike.%{q}%",
            "date": f'eq.{TODAY}'
          }
          Searchdata = fetch_data_from_supabase(request,queryParams)

               
 
        context ={"top_up":top_up_3,"top_down":top_down_3,"date_today":TODAY,"Searchdata":Searchdata,"q":q}    
        #context = {"data":type(data[0]["close"])}      
        return  render(request, 'main.html',context)          

def comp(a):
     return a["m3n_prob"]
                       
def recordPage(request,pk):
     queryParams={
          "select":"*",
          "index":f'eq.{pk}',
          "date":f'eq.{TODAY}'
     }
     
     data = fetch_data_from_supabase(request,queryParams)
     chart = get_graph(request,data)
     decision=data[0]["decision"].lower()
     context = {"data":data[0],"chart":chart,"decision":decision}

     return render(request,"recordPage.html",context)
     

def get_graph(request,data):

     ItemName = data[0]["symbol"]
     queryParamsGraph ={
          "select":"*",
          "symbol":f'eq.{ItemName}',
     }
     graphItem = fetch_data_from_supabase(request,queryParamsGraph)
     xlist=[]
     ylist =[]
     for i in range(len(graphItem)):
          xlist.append(graphItem[i]["date"])
          ylist.append(graphItem[i]["m3n_prob"])
     chart = get_plot(xlist,ylist)   
     return chart  

def get_plot(xchart,ychart):
     fig = px.line(
        x= xchart,
        y=ychart,
        title = "Record Graph",
        markers=True,
        labels = {'x':"date", 'y':'m3n_prob'}
          )
     # fig = go.Figure()
     # fig.add_trace(go.Scatter(x=xchart, y=ychart,
     #                mode='lines+markers',
     #                width=0.2))
      
     chart = fig.to_html()
     return chart

   
