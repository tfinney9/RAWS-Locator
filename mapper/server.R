#
#==========================================================
# RAWS Locator 2.0
# Map Edition
# Parasitizes the Main code!
#==========================================================
# 
#

library(shiny)
library(leaflet)

if(Sys.getenv("USER")[1]=="ubuntu") #We Are Deploying this on the server
{
  inputFile<-"/home/ubuntu/src/nuwx/shiny/data/" #General Data Path
  runPath<-"/home/ubuntu/src/nuwx/backend/meso-server.py" #Server File Locaiton
  punWrath<-"/home/ubuntu/src/nuwx/backend/tz-detector.py" #Time zone detector file location
  firePath<-"/home/ubuntu/fwas_data/NIFC/incidents.csv"
  
}
if(Sys.getenv("USER")[1]=="tanner") #Development
{
  inputFile<-"/home/tanner/src/nu-weather/RAWS-Locator/shiny/data/"
  runPath<-"/home/tanner/src/nu-weather/RAWS-Locator/backend/meso-server.py"
  punWrath<-"/home/tanner/src/src2/web_timeZoneFinder/tz-detector.py"
  firePath<-"/media/tanner/vol2/NIFC/incidents.csv"
}

# Define server logic required to draw a histogram
shinyServer(function(input, output,session) {
  useShinyjs()
  onclick("locate",{js$func()})
  
  
  output$location<-renderUI({
    if (is.null(input$locationType))
      return()
    xfireData<-reactiveFileReader(1000,NULL,firePath,read.csv)
    fireData<-xfireData()
    
    
    switch(input$locationType,
           "2" = tagList(actionButton("locate","Allow Location Access",class="btn-primary"),
                         br(),br(),verbatimTextOutput("glat"),verbatimTextOutput("glon")),
           "3" = tagList(
             hr(),selectInput('fire_name','Select Fire Location',
                              c(Choose='',fireData[1]),selectize=TRUE),br(),
             verbatimTextOutput("fLat"),br(),
             verbatimTextOutput("fLon"))
    )
  })
  
  observeEvent(input$fire_name,{
    xfireData<-reactiveFileReader(1000,NULL,firePath,read.csv)
    fireData<-xfireData()
    nLoc<-match(input$fire_name,fireData[[1]])
    output$fLat<-renderPrint(paste('Lat:',fireData[[3]][nLoc],sep=""))
    output$fLon<-renderPrint(paste('Lon:',fireData[[2]][nLoc],sep=""))
    #       fireLat<-renderPrint(fireData[[3]][nLoc])
    #       fireLon<-renderPrint(fireData[[2]][nLoc])
  })
  
  output$glat<-renderPrint(paste('Lat:',input$geoLat,sep=" "))
  output$glon<-renderPrint(paste('Lon:',input$geoLon,sep=" "))
  
  output$mymap <- renderLeaflet({
    leaflet() %>%
      addProviderTiles(providers$Stamen.Terrain,
                       options = providerTileOptions(noWrap = TRUE)
      )%>%
      setView(-114,46,zoom=8)
  })
  
  # clickLat=0.0
  # clickLon=0.0
  
  
  #####################################################
  # Map Click Test!
  #####################################################
  observeEvent(input$mymap_click,
               {
                 print("test")
                 print(input$mymap_click$lat)
                 print(input$mymap_click$lng)
                 clickLat=input$mymap_click$lat
                 clickLon=input$mymap_click$lng
                 
                 #####################################################
                 # Automatic Time Zone Detection Stuff
                 #####################################################
                 observeEvent(input$locationType,{
                   if(input$locationType==1)
                   {
                     clickLat=input$mymap_click$lat
                     clickLon=input$mymap_click$lng
                     observeEvent({clickLat
                       clickLon},{
                         targs=paste("\"",clickLat,"\" \"",clickLon,"\"",sep="")
                         #print(targs)
                         tz_check<-system2(command=punWrath,args=targs,stdout = TRUE)
                         #print(tz_check)
                         updateSelectInput(session,"timeZone",selected=tz_check)
                         
                       })
                   }
                 })
                 #####################################################
                 # END Automatic Time Zone Detection Stuff
                 #####################################################
                 
                 
                # xmap<-leafletProxy("mymap")
                
                # xmap%>%setView(lng=input$mymap_click$lng,lat=input$mymap_click$lat)
                 
                 # setView(mymap,lng=input$mymap_click$lng,lat=input$mymap_click$lat,zoom=2)
                 
                 
                 
               })
  
#####################################################
# Automatic Time Zone Detection Stuff
#####################################################
  observeEvent(input$locationType,{
    if(input$locationType==1)
    {
      clickLat=input$mymap_click$lat
      clickLon=input$mymap_click$lng
      observeEvent({clickLat
        clickLon},{
          targs=paste("\"",clickLat,"\" \"",clickLon,"\"",sep="")
          #print(targs)
          tz_check<-system2(command=punWrath,args=targs,stdout = TRUE)
          #print(tz_check)
          updateSelectInput(session,"timeZone",selected=tz_check)

        })
    }
    if(input$locationType==2)
    {
      observeEvent({
        input$geoLat
        input$geoLon
      },{
        targs=paste("\"",input$geoLat,"\" \"",input$geoLon,"\"",sep="")
        #print(targs)
        tz_check<-system2(command=punWrath,args=targs,stdout = TRUE)
        #print(tz_check)
        #updateSelectInput(session,"timeZone",selected=tz_check)
      })
    }
    if(input$locationType==3)
    {
      #print("type:3")
      observeEvent(input$fire_name,{
        xfireData<-reactiveFileReader(1000,NULL,firePath,read.csv)
        fireData<-xfireData()
        nLoc<-match(input$fire_name,fireData[[1]])
        fiLat<-fireData[[3]][nLoc]
        fiLon<-fireData[[2]][nLoc]
        
        print(fiLat)
        print(fiLon)

        targs=paste("\"",fiLat,"\" \"",fiLon,"\"",sep="")
        #print(targs)
        tz_check<-system2(command=punWrath,args=targs,stdout = TRUE)
        #print(tz_check)
        updateSelectInput(session,"timeZone",selected=tz_check)

      })
    }
  })
#####################################################
# END Automatic Time Zone Detection Stuff
#####################################################
  
  
  observeEvent(input$run_app,{
    
    clickLat=input$mymap_click$lat
    clickLon=input$mymap_click$lng
    xmap<-leafletProxy("mymap")
    xmap%>%clearMarkers()
    
    if(input$locationType==1)
    {
      gArgs=paste("\"",clickLat,"\" \"",clickLon,"\" \"",input$radius,"\" \"",input$timeZone,"\"",sep="")
      xLat<-clickLat
      xLon<-clickLon
    }
    if(input$locationType==2)
    {
      gArgs=paste("\"",input$geoLat,"\" \"",input$geoLon,"\" \"",input$radius,"\" \"",input$timeZone,"\"",sep="")
      xLat<-input$geoLat
      xLon<-input$geoLon
      print(gArgs)
    }
    if(input$locationType==3)
    {
      # print(input$geoLat)
      # print(input$geoLon)
      xfireData<-reactiveFileReader(1000,NULL,firePath,read.csv)
      fireData<-xfireData()
      nLoc<-match(input$fire_name,fireData[[1]])
      fiLat<-fireData[[3]][nLoc]
      fiLon<-fireData[[2]][nLoc]
      print(fiLat)
      print(fiLon)
      xLat<-fiLat
      xLon<-fiLon
      gArgs=paste("\"",fiLat,"\" \"",fiLon,"\" \"",input$radius,"\" \"",input$timeZone,"\"",sep="")
    }
    runFile<-system2(command=runPath,args=gArgs,stdout = TRUE)
    print(runFile)
    # tbl<-read.csv(runFile)
    # output$table<-renderDataTable(tbl,escape=FALSE)
    ds<-read.csv(runFile)
    
    urlList<-ds[1]
    nameList<-ds[2]
    temp_List<-ds[3]
    spd_List<-ds[4]
    gust_List<-ds[5]
    dir_List<-ds[6]
    rh_List<-ds[7]
    dist_List<-ds[8]
    hdg_List<-ds[9]
    date_list<-ds[10]
    time_List<-ds[11]
    latList<-ds[12]
    lonList<-ds[13]
    
    i=1
    test<-paste("Name:",urlList[[i]],
                "<br/>ID:",nameList[[i]],
                "<br/>Temp(F):",temp_List[[i]],
                "<br/>Wind Speed(mph):",spd_List[[i]],
                "<br/>Wind Gust(mph):",gust_List[[i]],
                "<br/>Wind Direction:",dir_List[[i]],
                "<br/>Relative Humidity:",rh_List[[i]],
                "<br/>Distance(mi):",dist_List[[i]],
                "<br/>Heading:",hdg_List[[i]],
                "<br/>Date:",date_list[[i]],
                "<br/>Time:",time_List[[i]],
                "<br/>Latitude:",latList[[i]],
                "<br/>Longitude:",lonList[[i]])
    
    
    if(nrow(ds)>0)
    {
      xmap%>%addMarkers(lonList[[1]],latList[[1]],popup=test) %>%
        addCircleMarkers(xLon,xLat,popup="Entered Location",color="red") %>%
        setView(lng=xLon,lat=xLat,zoom=8)
    }
    
    
  })
  
  
  
  
})
