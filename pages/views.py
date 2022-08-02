from django.shortcuts import render
from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required
import ee, eemont, geemap
import pandas as pd
import folium
from folium import plugins
import json
class phenology(TemplateView):
    template_name = 'pages/phenology.html'
# Create your views here.
@login_required 
def phenology(request):
    if request.method == 'GET':
        message = "selectionner la date et le polygone"
        context={
            'messages':[message]
        }
        return render(request ,'pages/home.html', context )
    elif 'phenology' in request.POST:
        start_date=request.POST.get("Start_date")
        end_date=request.POST.get("end_date")
        la1= float(request.POST.get("la1"))
        lg1= float(request.POST.get("lg1"))
        la2= float(request.POST.get("la2"))
        lg2= float(request.POST.get("lg2")) 
        la3= float(request.POST.get("la3"))
        lg3= float(request.POST.get("lg3")) 
        la4= float(request.POST.get("la4"))
        lg4= float(request.POST.get("lg4"))
        
        figure = folium.Figure()
        #create Folium Object
        m = folium.Map(
            location=[lg1, la1],
            zoom_start=13
        )
        basemaps = {
        'Google Satellite': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Satellite',
            overlay = True,
            control = True
        ),}
        basemaps['Google Satellite'].add_to(m)
        folium.Polygon([(lg1, la1), (lg2, la2), (lg3,la3),(lg4,la4)],
               weight=2,
               color="red",
               fill_color="yellow",
               fill_opacity=0.3).add_to(m)
        #add map to figure
        m.add_to(figure)
        m.add_child(folium.LayerControl())
        figure.render()
        Map = geemap.Map()
        polygon = ee.Geometry.Polygon(
        [[[la1,lg1],
        [la2,lg2],
        [la3,lg3],
        [la4,lg4]]]).buffer(50)
        s2 = ((ee.ImageCollection('COPERNICUS/S2_SR'))
            .filterDate('2019-07-01','2022-07-20')
            .filterBounds(polygon)
            .maskClouds(method = 'qa')
            .maskClouds(prob = 30)
            .maskClouds(buffer = 50)
            .maskClouds(cloudDist = 30)
            .scale().maskClouds(scaledImage = True)
            .maskClouds(dark = 0.1)
            .maskClouds(cdi = -0.5)
            .scaleAndOffset()
            .spectralIndices(['NDVI']))
        ts = s2.getTimeSeriesByRegion(geometry = polygon,
                              bands = ['NDVI'],
                              reducer = [ee.Reducer.mean()],
                              scale = 30)
        tsPandas = geemap.ee_to_pandas(ts)
        tsPandas['date'] = pd.to_datetime(tsPandas['date'],infer_datetime_format = True)
        tsPandas = pd.melt(tsPandas,
                        id_vars = ['reducer','date'],
                        value_vars = ['NDVI'],
                        var_name = 'Index',
                        value_name = 'Value')
        tsPandas.drop( tsPandas[ tsPandas['Value'] ==-9999 ].index, inplace=True)
        context = {
            'date' : tsPandas ['date'].to_list(),
            'value' : tsPandas ['Value'].to_list(),
            'map' : figure  ,                               
        }
        return render(request , 'pages/phenology.html' , context )
    
    elif 'NDWI' in request.POST:
            start_date=request.POST.get("Start_date")
            end_date=request.POST.get("end_date")
            la1= float(request.POST.get("la1"))
            lg1= float(request.POST.get("lg1"))
            la2= float(request.POST.get("la2"))
            lg2= float(request.POST.get("lg2")) 
            la3= float(request.POST.get("la3"))
            lg3= float(request.POST.get("lg3")) 
            la4= float(request.POST.get("la4"))
            lg4= float(request.POST.get("lg4"))
            figure = folium.Figure()
            #create Folium Object
            m = folium.Map(
                location=[lg1, la1],
                zoom_start=13
            )
            basemaps = {
            'Google Satellite': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Satellite',
                overlay = True,
                control = True
            ),}
            basemaps['Google Satellite'].add_to(m)
            folium.Polygon([(lg1, la1), (lg2, la2), (lg3,la3),(lg4,la4)],
                weight=2,
                color="red",
                fill_color="yellow",
                fill_opacity=0.3).add_to(m)
            #add map to figure
            m.add_to(figure)
            m.add_child(folium.LayerControl())
            figure.render()
            Map = geemap.Map()
            polygon = ee.Geometry.Polygon(
            [[[la1,lg1],
            [la2,lg2],
            [la3,lg3],
            [la4,lg4]]]).buffer(50)
            s2 = ((ee.ImageCollection('COPERNICUS/S2_SR'))
                .filterDate(start_date,end_date)
                .filterBounds(polygon)
                .maskClouds(method = 'qa')
                .maskClouds(prob = 30)
                .maskClouds(buffer = 50)
                .maskClouds(cloudDist = 30)
                .scale().maskClouds(scaledImage = True)
                .maskClouds(dark = 0.1)
                .maskClouds(cdi = -0.5)
                .scaleAndOffset()
                .spectralIndices(['NDWI']))
            ts = s2.getTimeSeriesByRegion(geometry = polygon,
                                bands = ['NDWI'],
                                reducer = [ee.Reducer.mean()],
                                scale = 30)
            tsPandas = geemap.ee_to_pandas(ts)
            tsPandas['date'] = pd.to_datetime(tsPandas['date'],infer_datetime_format = True)
            tsPandas = pd.melt(tsPandas,
                            id_vars = ['reducer','date'],
                            value_vars = ['NDWI'],
                            var_name = 'Index',
                            value_name = 'Value')
            tsPandas.drop( tsPandas[ tsPandas['Value'] ==-9999 ].index, inplace=True)
            context = {
                'date' : tsPandas ['date'].to_list(),
                'value' : tsPandas ['Value'].to_list(),
                'map' : figure  ,                               
            }
            return render(request , 'pages/phenology.html' , context ) 
        
def home(request):
    return render(request , 'pages/home.html' ) 

def about(request):

    return render(request , 'pages/about.html')