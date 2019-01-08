
let jsnn = {};

function setup() {
  createCanvas(1280, 720);
  img = loadImage("img1.jpg");  // Load the image
}

function preload(){
	jsnn = loadJSON('in.json');
}	

function draw() {
  background(0);
  // Displays the image at its actual size at point (0,0)
  image(img, 0, 0, 720, img.height*720/img.width);
  // Displays the image at point (0, height/2) at half size
  //image(img, 0, height/2, img.width/2, img.height/2);
  console.log(jsnn["positive"]);  
}
