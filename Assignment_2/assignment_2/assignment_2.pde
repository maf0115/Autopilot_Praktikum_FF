/* 
This file draws a map of the Manching Military Airport. While connected to the simulation in this course's lab, it gets the 
aircraft's position from the simulator and then moves an airplane icon over the map based on its coordinates.  
*/
import processing.net.*;
import java.io.*; 


// Define images
public PImage manchingImage = null; 
public PImage fighterJetIcon = null;  //<>//

static final int PORT_NR = 9000; 
static final byte SEPARATOR = 17; 

Client clientSocket; 

void setup() {
  size(650, 650);       //<>//
    //<>//
  manchingImage = loadImage("./data/Manching.PNG"); 
  fighterJetIcon = loadImage("./data/FighterJetIcon.jpg");
  clientSocket = new Client(this, "127.0.0.1", PORT_NR); 
  println("Leaving setup()");
}


void draw() {     //<>//
    //Get the data as a string
    if (clientSocket.available() > 0) {
      
    String message = clientSocket.readString();   
    JSONObject jsonMessage = parseJSONObject(message);
    float lat = jsonMessage.getFloat("lat");
    float lon = jsonMessage.getFloat("lon");
    float yawAngle = jsonMessage.getFloat("yawAngle");
    
    println("Lat: " + lat); 
    println("Lon: " + lon); 
    println("yawAngle: " + yawAngle); 
    }
    
    // Draw the map for every frame 
    println("Drawing manchingImage");
    image(manchingImage, 0, 0);
    
    // Draw th icon
    println("Drawing figtehrJetIcon");
    //image(fighterJetIcon, lat, lon);  


}
