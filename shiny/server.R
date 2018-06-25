#NuWeather
library(shiny)
library(shinyjs)
library(leaflet)


if(Sys.getenv("USER")[1]=="ubuntu") #We Are Deploying this on the server
{
  inputFile<-"/home/ubuntu/src/nuwx/shiny/data/" #General Data Path
  runPath<-"/home/ubuntu/src/nuwx/backend/meso-server.py" #Server File Locaiton
  locData<-read.csv(file="/home/ubuntu/src/nuwx/backend/loc.csv") #File Location List
  punWrath<-"/home/ubuntu/src/nuwx/backend/tz-detector.py" #Time zone detector file location
  
}
if(Sys.getenv("USER")[1]=="tanner") #Development
{
  inputFile<-"/home/tanner/src/nu-weather/RAWS-Locator/shiny/data/"
  runPath<-"/home/tanner/src/nu-weather/RAWS-Locator/backend/meso-server.py"
  locData<-read.csv(file="/home/tanner/src/nu-weather/RAWS-Locator/backend/loc.csv")
  punWrath<-"/home/tanner/src/src2/web_timeZoneFinder/tz-detector.py"
}

shinyServer(function(input, output,session) {
  useShinyjs()
  # g<-Sys.glob(inputFile)
  #runFile<-"/home/tanner/src/nu-weather/nuwx/data/nu-1523231749.csv"
  
  onclick("locate",{js$func()})
  output$location<-renderUI({
    if (is.null(input$locationType))
      return()
    
    switch(input$locationType,
           "1" = tagList(
             numericInput("lat", label = ("Enter Latitude (Decimal Degrees)"), value = 46.92,step=0.1),
             verbatimTextOutput("latVal"),
             numericInput("lon", label = ("Enter Longitude (Decimal Degrees)"), value = -114.1,step=0.1),
             verbatimTextOutput("lonVal")),
           "2" = tagList(actionButton("locate","Allow Location Access",class="btn-primary"),br(),br(),verbatimTextOutput("glat"),verbatimTextOutput("glon")),
           "3" = tagList(
             #div('NOTE: Selecting a Fire Location REPLACES the location set by a preset. Use \'Enter Lat/Lon\' if you want to use the preset location. ',style="color:blue"),
             hr(),selectInput('Location','Select Location',
                              c(Choose='',locData[1]),selectize=TRUE),br(),
             verbatimTextOutput("fLat"),br(),
             verbatimTextOutput("fLon"))





           # "3" = tagList(
           #   div('NOTE: Selecting a Fire Location REPLACES the location set by a preset. Use \'Enter Lat/Lon\' if you want to use the preset location. ',style="color:blue"),
           #   hr(),selectInput('fire_name','Select Fire Location',
           #                    c(Choose='',fireData[1]),selectize=TRUE),br(),
           #   verbatimTextOutput("fLat"),br(),
           #   verbatimTextOutput("fLon"))
           
    )
  })
  


  output$glat<-renderPrint(paste('Lat:',input$geoLat,sep=" "))
  output$glon<-renderPrint(paste('Lon:',input$geoLon,sep=" "))
  
  #
  # Automatic Time Zone Detection Stuff
  #
  observeEvent(input$locationType,{
    if(input$locationType==1)
    {
      observeEvent({input$lat
                    input$lon},{
                      targs=paste("\"",input$lat,"\" \"",input$lon,"\"",sep="")
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
      observeEvent(input$Location,{
        #print("locChanged")
        naLoc<-match(input$Location,locData[[1]])
        fiLat<-locData[[2]][naLoc]
        fiLon<-locData[[3]][naLoc]
    
        targs=paste("\"",fiLat,"\" \"",fiLon,"\"",sep="")
        #print(targs)
        tz_check<-system2(command=punWrath,args=targs,stdout = TRUE)
        #print(tz_check)
        updateSelectInput(session,"timeZone",selected=tz_check)
        
      })
    }
  })
  #
  #End Automatic Time Zone Detection stuff
  #


  observeEvent(input$Location,{
    nLoc<-match(input$Location,locData[[1]])
    output$fLat<-renderPrint(paste('Lat:',locData[[2]][nLoc],sep=""))
    output$fLon<-renderPrint(paste('Lon:',locData[[3]][nLoc],sep=""))
    #       fireLat<-renderPrint(fireData[[3]][nLoc])
    #       fireLon<-renderPrint(fireData[[2]][nLoc])
  })


  observeEvent(input$run_app,{
    xLat<-""
    xLon<-""
    if(input$locationType==1)
    {
      gArgs=paste("\"",input$lat,"\" \"",input$lon,"\" \"",input$radius,"\" \"",input$timeZone,"\"",sep="")
      xLat<-input$lat
      xLon<-input$lon
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
      naLoc<-match(input$Location,locData[[1]])
      fiLat<-locData[[2]][naLoc]
      fiLon<-locData[[3]][naLoc]
      print(fiLat)
      print(fiLon)
      xLat<-fiLat
      xLon<-fiLon
      gArgs=paste("\"",fiLat,"\" \"",fiLon,"\" \"",input$radius,"\" \"",input$timeZone,"\"",sep="")
    }
    runFile<-system2(command=runPath,args=gArgs,stdout = TRUE)
    print(runFile)
    tbl<-read.csv(runFile)
    output$table<-renderDataTable(tbl,escape=FALSE)
    
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
    
    output$l_map <- renderLeaflet({
      leaflet() %>%
        addProviderTiles(providers$Stamen.Terrain,
                         options = providerTileOptions(noWrap = TRUE)
        ) %>%
        addMarkers(lonList[[1]],latList[[1]],popup=test) %>%
        addCircleMarkers(xLon,xLat,popup="Entered Location",color="red")
    })
    
    
    
    
  })
  # observeEvent(input$run_app,{
  #   tbl<-read.csv(runFile)
  #   output$table<-renderDataTable(tbl)
  # })

  

})
