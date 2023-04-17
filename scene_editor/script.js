$(document).ready(function() {
  var data = {
	"settings": {
	  "speakerAlign": "left",
	  "textAlign": "left",
	  "textPos.x": 0.11,
	  "textPos.y": 0.94,
	  "speakerPos.x": 0.1,
	  "speakerPos.y": 0.91,
	  "screenMult": 1,
	  "showBox": 1,
	  "fontPath": "assets/arial.ttf",
	  "fontSize": 21
	},
	"scenes": {}
  };

  $("#add-scene-btn").click(function() {
	var sceneName = $("#scene-name").val();
	var backgroundImage = $("#background-image").val();
	data["scenes"][sceneName] = {
	  "background": backgroundImage,
	  "characters": {},
	  "dialogue": []
	};
	saveData();
  });

  $("#add-character-btn").click(function() {
	var sceneName = $("#scene-name").val();
	var characterName = $("#character-name").val();
	var characterImage = $("#character-image").val();
	var characterPositionX = $("#character-position-x").val();
	var characterPositionY = $("#character-position-y").val();
	data["scenes"][sceneName]["characters"][characterName] = {
	  "image": characterImage,
	  "position": [parseFloat(characterPositionX), parseFloat(characterPositionY)]
	};
	saveData();
  });

  $("#add-dialogue-btn").click(function() {
	var sceneName = $("#scene-name").val();
	var dialogueSpeaker = $("#dialogue-speaker").val();
	var dialogueText = $("#dialogue-text").val();
	data["scenes"][sceneName]["dialogue"].push({
	  "speaker": dialogueSpeaker,
	  "text": dialogueText
	});
	saveData();
  });

  // Add event listener to the editable div
  $("#output").on("input", function() {
  var editedData = $("#output").html();
  var selectionStart = this.selectionStart;
  var selectionEnd = this.selectionEnd;
  editedData = editedData.replace(/<br>/g, '\n'); // Replace <br> tags with newlines
  editedData = editedData.replace(/&nbsp;/g, ' '); // Replace &nbsp; entities with spaces
  
  try {
	data = JSON.parse(editedData);
	// saveData();
	// Restore the cursor position after modifications are complete
	this.setSelectionRange(selectionStart, selectionEnd);
  } catch (error) {
	// JSON parse error, don't update the data
  }
});

	function renderCanvas() {
		var canvas = document.getElementById("canvas");
		var ctx = canvas.getContext("2d");
	
		// Clear the canvas
		ctx.clearRect(0, 0, canvas.width, canvas.height);
	}

  function saveData() {
	var formattedData = JSON.stringify(data, null, '\t'); // Use tabs for indentation
	formattedData = formattedData.replace(/\n/g, '<br>'); // Replace newlines with <br> tags
	formattedData = formattedData.replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;'); // Replace tabs with 4 spaces
	document.getElementById("output").innerHTML = formattedData + "<br><br>";
	
	formattedData_new = formattedData.replace(/<br>/g, '\n'); // Replace <br> tags with newlines
	formattedData_new = formattedData_new.replace(/&nbsp;/g, ' '); // Replace &nbsp; entities with spaces

	 // Create a new anchor element
	var downloadLink = document.createElement('a');
	downloadLink.setAttribute('href', 'data:text/json;charset=utf-8,' + encodeURIComponent(formattedData_new));
	downloadLink.setAttribute('download', 'output.json');
	downloadLink.innerHTML = 'Download JSON';

	// Append the anchor element to the output div
	var outputDiv = document.getElementById("output2");
	outputDiv.innerHTML = '';
	outputDiv.appendChild(downloadLink);
	outputDiv.insertAdjacentHTML('beforeend', '<br><br>');
  }
});