var app = window.app||{};
	app.view = jQuery("#view");
	app.startButton=jQuery("#startBtn");
	app.endButton=jQuery("#endBtn"); 
	app.sendButton=jQuery("#sendMessageBtn");
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
		app.log[0].scrollTop = app.log[0].scrollHeight;
	 };
	 app.warn = function(message) {
		//alert(message);
	};
	app.sendMessage = function( event ) {
		event.preventDefault();
		 time = (Date.now()/1000);

		 var msg = {
			"two_way_message_from": app.fromNumber,
			"two_way_message_to": jQuery("#messageTo").val(),
			"two_way_message_text":  jQuery("#messageBody").val(),
			"two_way_message_time": time
		};
		app.logData ( "Sending Message");
		app.logData( JSON.stringify(msg) );
		Oneline.once("send_message", msg);
	 };
			
	 jQuery( app.startButton ).click(  app.startLogging );
	 jQuery( app.endButton ).click( app.endPushing );
	 jQuery( app.sendButton ).click( app.sendMessage );

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
				} else if ( res.response.type === "send_message" ) {
					app.logData("--- RECEIVED SEND MESSAGE RESPONSE ---");
				}
			}
				
	      }).run();
	});

