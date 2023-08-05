/*global window, rJS, jIO, FormData */
/*jslint indent: 2, maxerr: 3 */

(function (window, rJS) {
  "use strict";

  rJS(window)
    .ready(function (gadget) {
      console.log("~~ loading_gadget: is ready");
      return gadget;
    })

  /*
   Service listening to load gadget-events (which creates the gadget)
   */
    .declareService(function () {
      var gadget = this;


      function loadGadget(e) {
	// The URL of the gadget-to-be-loaded
	var url = e.detail.url;
	// The uid of the gadget-to-be-loaded
	var gadgetId = e.detail.gadgetId;
	console.log("~~ gadgetID=" + gadgetId);
	console.log("~~ trying to load gadget with url=" + url);


	// Find the running/post-active cell to append the
	// gadget-to-be-loaded to
	var gadgetParent = null;
	var notebookcontainer = $("#notebook-container");
	// If this gets executed quick the cell might still be "running"
	gadgetParent = document.querySelector(".running");
	// If no cell is running take the cell before the currently active
	// cell as parent
	if(gadgetParent != null) {
	  var activeIndex = -1;
	  // Find the index of the class=selected cell
	  for(var i = 0; i < notebookcontainer.children(".cell").length; i++) {
	    var iele = notebookcontainer.children(".cell")[i];
	    if((' ' + iele.className + ' ').indexOf(' selected ') > -1) {
	      activeIndex = i;
	      break;
	    }
	  }
	  // The cell before the selected cell is what we want
	  gadgetParent = notebookcontainer.children(".cell")[activeIndex - 1];
	}
	if(gadgetParent == null) {
	  console.log("~~ ERROR: gadgetParent is null");
	  return;
	}
	// If there is already a gadget associated with the cell, destroy it
	// (overwrite it)
	if (gadgetParent.querySelector(".external_gadget") != null) {
	  gadgetParent.removeChild(gadgetParent.querySelector(".external_gadget"));
	}

	// Create the gadget's div
	var gadgetDiv = document.createElement("div");
	gadgetDiv.className += "external_gadget";
	gadgetParent.appendChild(gadgetDiv);
	var options = {
	  element: gadgetDiv,
	  sandbox: "iframe",
	  scope: gadgetId
	};
	// Create the new gadget in an iframe
	return gadget.declareGadget(url, options)
	  .push(function(external_gadget) {
	    external_gadget.getElement()
	      .push(function(element) {
		element.querySelector("iframe").style.width="100%";
		element.querySelector("iframe").style.height="400px";
		//element.querySelector("iframe"). += " " + gadgetId;
		return element;
	      });
	    return external_gadget;
	  });
      }

      // Listener for "load gadget" events
      return gadget.getElement()
	.push(function(ele) {
	  return loopEventListener(ele.querySelector(".loading_gadget"),
				   'load_gadget', false, loadGadget);
	});
    })

  /*
    Service listening to destroy-events
   */
    .declareService(function () {
      var gadget = this;
      function destroyGadget(e) {
	// The uid of the gadget-to-be-destroyed
	var gadgetId = e.detail.gadgetId;
	console.log("~~ destroying gadget with id=" + gadgetId);
	// Get the dom-element of the gadget and remove it thereby destroying
	// the gadget itself
	gadget.getDeclaredGadget(gadgetId)
	  .push(function(subGadget) {
	    subGadget.getElement()
	      .push(function(ele) {
		ele.parentNode.removeChild(ele);
		console.log("~~ destroyed gadget!");
	      });
	  });
      }

      // Listener for "destroy" events
      return gadget.getElement()
	.push(function(ele) {
	  return loopEventListener(ele.querySelector(".loading_gadget"),
				   'destroy_gadget', false, destroyGadget);
	});
    })

  /*
    Service listening to callDeclMethod-events
   */
    .declareService(function() {
      var gadget = this;
      function callGadget(e) {
	// The id of the gadget-to-be-called
	var gadgetId = e.detail.gadgetId;
	var methodName = e.detail.methodName;
	// Parse the JSON which got created in the backend via python json
	var methodArgList = JSON.parse(e.detail.methodArgs);
	console.log(methodArgList);
	gadget.getDeclaredGadget(gadgetId)
	  .push(function(subGadget) {
	    // Called methodName on subGadget and use subGadget as this and
	    // methodArgList as arguments
	    subGadget[methodName].apply(subGadget, methodArgList);
	  });
      }

      // Listener for "call" events
      return gadget.getElement()
	.push(function(ele) {
	  return loopEventListener(ele.querySelector(".loading_gadget"),
				   'call_gadget', false, callGadget);
	});
    });
}(window, rJS));
