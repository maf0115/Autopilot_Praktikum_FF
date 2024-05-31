/* 
This file draws a map of the Manching Military Airport. While connected to the simulation in this course's lab, it gets the 
aircraft's position from the simulator and then moves an airplane icon over the map based on its coordinates.  
*/
import processing.net.*;
import java.io.*; 
import java.net.DatagramSocket; 
import java.net.DatagramPacket; 
import java.net.SocketException; 
import java.net.Inetaddress; 

// Define images
public PImage manchingImage = null; 
public PImage fighterJetIcon = null;  //<>//

static final int PORT_NR = 9000; 
static final byte SEPARATOR = 17; 

byte[] buffer = new byte[22222];
DatagramPacket datagramPack =  new DatagramPacket(buffer, buffer.length); 
DatagramSocket myClientSocket; 

void setup() {
  size(650, 650);    //<>//
   
  try {
    myClientSocket = new DatagramSocket(PORT_NR); 
  } catch(SocketException e) {
    e.printStackTrace(); 
  }
    //<>//
  manchingImage = loadImage("./data/Manching.PNG"); 
  fighterJetIcon = loadImage("./data/FighterJetIcon.jpg");
   
  println("Leaving setup()");
}

float[] parseJSON(String jsonData) {
  float[] posi = new float[6];
  jsonData = jsonData.replace("{", "").replace("}", "").replace("\"", "");
  String[] pairs = jsonData.split(",");
 
  for (String pair : pairs) {
    String[] keyValue = pair.split(":");
    int index = Integer.parseInt(keyValue[0].trim()) - 1;
    float value = Float.parseFloat(keyValue[1].trim());
    posi[index] = value;
  }
  return posi;
}

void draw() {     //<>//
    //Get the data as a string
    try {
      println("Entering try-catch statement"); 
      myClientSocket.receive(datagramPack); 
      println("Received message!");
    } catch (IOException e) {
      e.printStackTrace(); 
      myClientSocket.close(); 
    }
    
    String message = new String(datagramPack.getData());
    float[] posi = parseJSON(message);
    println("Messages have been parsed");
    
    // Draw the map for every frame 
    println("Drawing manchingImage");
    image(manchingImage, 0, 0);
    
    // Draw th icon
    println("Drawing figtehrJetIcon");
    image(fighterJetIcon, posi[0], posi[1]);  


}
