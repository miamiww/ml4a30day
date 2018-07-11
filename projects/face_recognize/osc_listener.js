var osc = require('osc');
var beep = require('beepbeep');
var faceWatch = true;

var udpPort = new osc.UDPPort({
	localAddress: "localhost",
	localPort: 12000 
});

udpPort.on("ready", function () {
	var ipAddresses = ["localhost"];

	console.log("Listening for OSC over UDP.");
		ipAddresses.forEach(function (address) {
			console.log(" Host:", address + ", Port:", udpPort.options.localPort);
		});
});

udpPort.on("message", function(oscMessage){
//	console.log(oscMessage);
	if(oscMessage.args[0] > 0.8 && faceWatch){
		beep();
		console.log('welcome alden');
		faceWatch = false;
	} else {
		if(oscMessage.args[0] < 0.8){
		faceWatch = true;
		}
	}
});

udpPort.on("error", function(err){
	console.log(err);
});

udpPort.open();
