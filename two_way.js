var app = window.app||{};
	app.view = jQuery("#view");
	app.startButton=jQuery("#startBtn");
	app.endButton=jQuery("#endBtn"); 
	app.log=jQuery("#consoleLog");
      Oneline.setup({ 
            module: 'two_way', 
            host: document.location.host, 
            freq: 1000
      });
	app.startLogging = function() {
		app.logData("--- Starting Logging ---");
		app.logData("--- Sending HELLO ---");
		Oneline.once("hello", {});
	 };
	app.startPushing = function() {
		app.logData("--- Sending START_PUSH ---");
		Oneline.once("start_push", {});
			
	 };
	app.endPushing = function() {
		app.logData("--- Sending END_PUSH ---");
		Oneline.once("end_push", {});
	 };
	app.showData = function(data) {
		app.logData(JSON.stringify(data));
	 };
	app.logData = function(message) {
		var currentText = jQuery(app.log).val();
		var newText=currentText+"\r\n"+message;
		jQuery( app.log ).val( newText );
	 };
	 app.warn = function(message) {
		//alert(message);
	};
	 jQuery( app.startButton ).click(  app.startLogging );
	 jQuery( app.endButton ).click( app.endPushing );

	Oneline.ready(function() {
		jQuery(app.view).show();
	      Oneline.pipeline(function(res) {
			console.log( res );
			if ( res.good && res.response ){
				if ( res.response.type === "hello" ) {
					//start pushing
					app.warn("Pushing has started");
					app.logData("--- RECEIVED HELLO RESPONSE ---");
					app.startPushing();
				} else if ( res.response.type === "push_notification" && res.response.messages.length > 0) {
					app.logData("--- RECEIVED PUSH NOTIFICATION ---");
					app.showData( res.response.messages );
				} else if ( res.response.type === "end_push" ) {
					app.logData("--- RECEIVED END PUSH RESPONSE ---");
					app.warn("Pushing has stopped");
				}
			}
				
	      }).run();
	});

