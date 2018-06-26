#
#==========================================================
# RAWS Locator 2.0
# Map Edition
#==========================================================
# 
# 
# 
#

library(shiny)
library(leaflet)
library(shinyjs)
library(shinythemes)

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

# Define UI for application that draws a histogram
shinyUI(bootstrapPage(theme=shinytheme("flatly"),
  useShinyjs(),
  tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
  leafletOutput("mymap",height="100%",width="100%"),
  absolutePanel(top=10,right=10,
                wellPanel(h4("Raws Locator"),
                  radioButtons("locationType",label=("Location Options"),
                               choices=list("Click Location"=1,"Use Your Location"=2,
                                            "Large Fires"=3), 
                               selected=1,inline=TRUE),
                  uiOutput("location"),
                  sliderInput("radius", label = ("Observations Radius: (miles)"), min = 1,
                              max = 50, value = 5),
                  selectInput("timeZone",label=("Select Time Zone"),choices=list("Pacific"=1,"Mountain"=2,
                                                                                 "Arizona"=3,"Central"=4,"Eastern"=5,
                                                                                 "Hawaii"=6,"Alaska"=7)),
                  actionButton("run_app",label="Go!",class="btn-primary")
                          )
                )
  
))
