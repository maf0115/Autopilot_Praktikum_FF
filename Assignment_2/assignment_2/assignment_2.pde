/* 
This file draws a map of the Manching Military Airport. While connected to the simulation in this course's lab, it gets the 
aircraft's position from the simulator and then moves an airplane icon over the map based on its coordinates.  
*/
import processing.net.*;

// Declare images
PImage manchingImage = null; 
PImage fighterJetIcon = null; 

// Set needed elements for the passage of data from the simulation to this program 
Client simulationDataClient; 
int PORT = 80; 

void setup() 
{
  size(650, 650);   
  
  //Open up a server to receive data from the simulator
  simulationDataClient = new Client(this, "192.0.101.1", PORT);
  
  manchingImage = loadImage("./data/Manching.PNG"); 
  fighterJetIcon = loadImage("./data/FighterJetIcon.jpg");
}

void draw() 
{ 
    // Draw the map for every frame 
  image(manchingImage, 0, 0);
   
  if (simulationDataClient.available() != 0) 
  {    
    JSONObject simulatorData = parseJSONObject(simulationDataClient.readStringUntil(byte('\n'))); 
    if (simulatorData == null)
      println("No data received"); 
      
    else
    {
      float lat = float(simulatorData.getString("lat"));  
      float lon = float(simulatorData.getString("lon"));
      println("Received data from simulation");
      // float rollAngle = float(simulatorData.getString("rollAngle")); 
      
        // Draw th icon
        image(fighterJetIcon, lat, lon); 
    }
  
  }

}
