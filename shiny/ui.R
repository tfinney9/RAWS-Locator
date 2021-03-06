#
#==========================================================
# RAWS Locator 2.0
# Table with small map
#==========================================================
# 
# 
# 
#

library(shiny)
library(shinyjs)
library(shinythemes)
library(leaflet)

jsCode<-'shinyjs.func = function(){ navigator.geolocation.getCurrentPosition(onSuccess, onError);
                                      function onError (err) {
                                      Shiny.onInputChange("geolocation", false);
                                      }
                                      
                                      function onSuccess (position) {
                                      setTimeout(function () {
                                      var coords = position.coords;
                                      console.log(coords.latitude + ", " + coords.longitude);
                                      Shiny.onInputChange("geolocation", true);
                                      Shiny.onInputChange("geoLat", coords.latitude);
                                      Shiny.onInputChange("geoLon", coords.longitude);
                                      }, 1100)
                                      }
                                      };'


shinyUI(fluidPage(theme=shinytheme("united"),
  useShinyjs(),
  extendShinyjs(text=jsCode,functions=c("func")),  
  titlePanel("RAWS Locator"),
  h3("Finds Weather Stations Near You"),
  # fluidRow(
    # column(12,
    # actionButton("run_app",label="Go!"))
    # ),
    br(),
    fluidRow(
      column(5,wellPanel(radioButtons("locationType",label=("Location Options"),
                                      choices=list("Enter Lat/Lon"=1,"Use Your Location"=2,
				      "Select Location"=3,"Large Fires"=4), 
                                      selected=1,inline=TRUE),uiOutput("location")
                         
                         )),
      # column(3,
      # numericInput("lat",label=("Enter Latitude"),value=46.92),
      # numericInput("lon",label=("Enter Latitude"),value=-114.1)
      
    column(7,
      sliderInput("radius", label = h3("Observations Radius: (miles)"), min = 1,
                  max = 50, value = 5)),
    column(3,
      selectInput("timeZone",label=("Select Time Zone"),choices=list("Pacific"=1,"Mountain"=2,
					"Arizona"=3,"Central"=4,"Eastern"=5,
					"Hawaii"=6,"Alaska"=7)))),
  fluidRow(
    column(3,
           actionButton("run_app",label="Go!",class="btn-primary")
    )),
  fluidRow(br()),
  
  tabsetPanel(type="tabs",
              tabPanel("Table",dataTableOutput("table")),
              tabPanel("Map",leafletOutput("l_map",height=600))),
  br()
  # fluidRow(
  # column(12,
  #   dataTableOutput("table")
  # )),
  # fluidRow(
  #   column(12,
  #          leafletOutput("l_map")
  #   ))
  
  ))
