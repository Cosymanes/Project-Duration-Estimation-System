// Function to validate user input
function validateInput() {
    var location = document.getElementById("location").value;
    var projectType = document.getElementById("projectType").value;
    var squareMeters = document.getElementById("squareMeters").value;
    var numRooms = document.getElementById("numRooms").value;
    var soilType = document.getElementById("soilType").value;
    var budget = document.getElementById("budget").value;
    var periodOfMonth = document.getElementById("periodOfMonth").value;
    var numFloors = document.getElementById("numFloors").value;



    return true; // Return true if validation passes, false otherwise
}

// Function to display prediction result
function displayPrediction(result) {
    var predictionResult = document.getElementById("predictionResult");
    predictionResult.innerHTML = "Estimated time spent: " + result + " months";
    predictionResult.style.display = "block"; // Make the prediction result visible
}

// Function to make an AJAX request to the server for prediction
function predictTimeSpent() {
    if (validateInput()) {
        var xhr = new XMLHttpRequest();
        var url = "/predict"; // Endpoint URL to handle prediction
        var data = {
            location: document.getElementById("location").value,
            projectType: document.getElementById("projectType").value,
            squareMeters: document.getElementById("squareMeters").value,
            numRooms: document.getElementById("numRooms").value,
            soilType: document.getElementById("soilType").value,
            budget: document.getElementById("budget").value,
            periodOfMonth: document.getElementById("periodOfMonth").value,
            numFloors: document.getElementById("numFloors").value
        };
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var result = JSON.parse(xhr.responseText).prediction;
                displayPrediction(result);
            }
        };
        xhr.send(JSON.stringify(data));
    }
}
