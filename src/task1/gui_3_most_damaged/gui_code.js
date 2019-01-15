
let jsnn = {};
let all_image_names = [];
let all_images = [];
let img_counter = 0;
let img_switched = [false, false, false];

function setup() {
  createCanvas(1280, 850);
  tmp_pic = loadImage("tmp_pic.jpg");
  img1 = loadImage("tmp_pic.jpg");  // Load the image
  img2 = loadImage("tmp_pic.jpg"); 
  img3 = loadImage("tmp_pic.jpg"); 
  background(50);
  all_image_names = jsnn["positive"];

  for(i = 0; i < all_image_names.length; i++){
    all_images.push(loadImage(all_image_names[i]));
  }
}

function preload(){
	jsnn = loadJSON('in.json');

}	

function draw() {
  
  // Displays the image at its actual size at point (0,0)
  // image(img, 0, 0, 720, img.height*720/img.width);
  // Displays the image at point (0, height/2) at half size
  //image(img, 0, height/2, img.width/2, img.height/2);

  //drawing background rectangles and text//
  fill(204, 101, 192, 127);
  stroke(0);
  background(40);

  rect(40, 100, 375, 300);
  rect(40+375+25, 100, 375, 300);
  rect(40+375+375+25+25, 100, 375, 300);

  fill(204, 204, 204, 255);
  stroke(0);

  textSize(32);
  text('#1 Most Damaged', 40, 100+300+32);

  textSize(32);
  text('#2 Most Damaged', 40+25+375, 100+300+32);

  textSize(32);
  text('#3 Most Damaged', 40+25+375+25+375, 100+300+32);

  fill(204, 204, 204, 255);
  stroke(0);

  rect(40+25+375, (800/2)+65, 375, 300);

  fill(204, 204, 204, 255);
  stroke(0);

  textSize(32);
  text('Candidate Panel', 40+25+375, (800/2)+375, 375, 300);
  //end b ackground rectangles and text//

  //drawing test images//

  drawPic(img1, 40, 100, 375, 300);
  drawPic(img2, 40+375+25, 100, 375, 300);
  drawPic(img3, 40+375+375+25+25, 100, 375, 300);

  if(all_images.length != 0){
  	drawPic(all_images[img_counter], 40+25+375, (800/2)+65, 375, 300);
  }
  else{
  	drawPic(tmp_pic, 40+25+375, (800/2)+65, 375, 300);
  }

  //testing stuff
  // console.log(all_image_names);
  //end testing stuff
}

//function for drawing pictures scaled to be within a certain rectangle
function drawPic(img, x, y, width, height){
  if(width/height > img.width/img.height){//long boi images
  	console.log("LONG BOI")
  	x += (375-(img.width*300/img.height))/2;
  	image(img, x, y, img.width*300/img.height, 300);
  }
  else{//wide boi images
  	y += (300-(img.height*375/img.width))/2;
  	image(img, x, y, 375, img.height*375/img.width);
  }
  	
}

function keyPressed() {
  if(keyCode == 49){//keycode for '1'
  	// background(0);
  	var tmp = img1;
  	img1 = all_images[img_counter];
  	// all_images.splice(img_counter);
  	if(img_switched[0]){//image has already been switched 
  		all_images.splice(img_counter, 1, tmp);

  	}
  	else{
  		all_images.splice(img_counter, 1);
  		all_image_names.splice(img_counter, 1);
  		img_switched[0] = true;
  	}
  }
  if(keyCode == 50){//keycode for '2'
  	// background(100);
  	var tmp = img2;
  	img2 = all_images[img_counter];
  	// all_images.splice(img_counter);
  	if(img_switched[1]){//image has already been switched 
  		all_images.splice(img_counter, 1, tmp);

  	}
  	else{
  		all_images.splice(img_counter, 1);
  		all_image_names.splice(img_counter, 1);
  		img_switched[1] = true;
  	}
  }
  if(keyCode == 51){//keycode for '3'
  	// background(255);
  	var tmp = img3;
  	img3 = all_images[img_counter];
  	// all_images.splice(img_counter);
  	if(img_switched[2]){//image has already been switched 
  		all_images.splice(img_counter, 1, tmp);

  	}
  	else{
  		all_images.splice(img_counter, 1);
  		all_image_names.splice(img_counter, 1);
  		img_switched[2] = true;
  	}
  }
  if(keyCode == RIGHT_ARROW){//advance an image
  	// background(255, 100,100);
  	if(img_counter < all_images.length-1){
  		img_counter++;
  	}
  }
  if(keyCode == LEFT_ARROW){
  	// background(255, 255, 100);
  	if(img_counter > 0){
  		img_counter--;
  	}
  }
}
