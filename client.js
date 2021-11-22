var carNames = [];
var saveButton = document.querySelector("#car-button");

//globals for new boxes. (need to change eventually)
var updateCarInputYear = document.querySelector("#new-year-box");
var updateCarInputMake = document.querySelector("#new-make-box");
var updateCarInputModel = document.querySelector("#new-model-box");
var updateCarInputType = document.querySelector("#new-type-box");
var updateCarInputRating = document.querySelector("#new-rating-box");

saveButton.onclick = function() 
{
	var newCarInputYear = document.querySelector("#year-box");
	var newCarInputMake = document.querySelector("#make-box");
	var newCarInputModel = document.querySelector("#model-box");
	var newCarInputType = document.querySelector("#type-box");
	var newCarInputRating = document.querySelector("#rating-box");
	
	createCarOnServer(newCarInputYear.value, newCarInputMake.value,
						 newCarInputModel.value, newCarInputType.value,
						  newCarInputRating.value);	
	newCarInputYear.value = "Year";
	newCarInputMake.value = "Make";
	newCarInputModel.value = "Model";
	newCarInputType.value = "Type";
	newCarInputRating.value = "Rating";
};


function createCarOnServer( carYear, carMake, carModel, carType, carRating )
{
	var data = "year=" + encodeURIComponent(carYear);
	data += "&make=" + encodeURIComponent(carMake);
	data += "&model=" + encodeURIComponent(carModel);
	data += "&type=" + encodeURIComponent(carType);
	data += "&rating=" + encodeURIComponent(carRating);

	fetch("https://car-saver.herokuapp.com/cars",
	{ 
		//request options go here: method, header(s), body.
		method: "POST",
		credentials: "include",
		body: data,
		headers: 
		{
			"Content-Type": "application/x-www-form-urlencoded"
		}
		
	}).then(function(response)
	{
		//TODO: refresh the data by calling loadCarsFromServer()
		loadCarsFromServer();
	});
}

function deleteCarOnServer(carID)
{
	fetch(`https://car-saver.herokuapp.com/cars/${carID}`,
	{
		method: "DELETE",
		credentials: "include"
	}).then(function (response)
	{
		loadCarsFromServer();
	});
}

function updateCarOnServer( carYear, carMake, carModel, carType, carRating, carID)
{
	var data = "year=" + encodeURIComponent(carYear);
	data += "&make=" + encodeURIComponent(carMake);
	data += "&model=" + encodeURIComponent(carModel);
	data += "&type=" + encodeURIComponent(carType);
	data += "&rating=" + encodeURIComponent(carRating);

	fetch(`https://car-saver.herokuapp.com/cars/${carID}`,
	{
		method: "PUT",
		credentials: "include",
		body: data,
		headers:
		{
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function(response)
	{
		loadCarsFromServer();
	});
}
//////////////////////////////////////////////////////////// Authorization notes
function loadCarsFromServer()
{
	fetch("https://car-saver.herokuapp.com/cars",
	{
		credentials: "include"
	}).then(function (response)
	{
		if (response.status == 401)
		{
			//show login-box
			var loginBox = document.querySelector("#login-box");
			loginBox.style.display = "block";

			//show create-box
			var createBox = document.querySelector("#create-box");
			createBox.style.display = "block";
			
			//hide cars data
			var ogDiv = document.querySelector("#original-box");
			ogDiv.style.display = "none";

			//hide button div
			var buttonBox = document.querySelector("#button");
			buttonBox.style.display = "none";

			//hide saved-cars div
			var buttonBox = document.querySelector("#Saved-Cars");
			buttonBox.style.display = "none";

			return;
		}
		else if (response.status == 200)
		{
			//hide login-box
			var loginBox = document.querySelector("#login-box");
			loginBox.style.display = "none";
			
			//hide create-box
			var createBox = document.querySelector("#create-box");
			createBox.style.display = "none";

			//show cars data
			var ogDiv = document.querySelector("#original-box");
			ogDiv.style.display = "grid";

			//show button div
			var buttonBox = document.querySelector("#button");
			buttonBox.style.display = "grid";

			//show saved-cars div
			var buttonBox = document.querySelector("#Saved-Cars");
			buttonBox.style.display = "grid";
		}
		response.json().then(function (dataFromServer)
		{
			carNames = dataFromServer;		
			var carNameList = document.querySelector("#car-list");
			carNameList.innerHTML = "";	
			carNames.forEach(function (car) 
			{
				console.log("one time through the loop:", car );

				var carNameItem = document.createElement("li");

				var yearDiv = document.createElement("div");
				yearDiv.innerHTML = car.year;
				yearDiv.classList.add("car-year");
				carNameItem.appendChild(yearDiv);

				var makeDiv = document.createElement("div");
				makeDiv.innerHTML = car.make;
				makeDiv.classList.add("car-make");
				carNameItem.appendChild(makeDiv);

				var modelDiv = document.createElement("div");
				modelDiv.innerHTML = car.model;
				modelDiv.classList.add("car-model");
				carNameItem.appendChild(modelDiv);

				var typeDiv = document.createElement("div");
				typeDiv.innerHTML = car.type;
				typeDiv.classList.add("car-type");
				carNameItem.appendChild(typeDiv);

				var ratingDiv = document.createElement("div");
				ratingDiv.innerHTML = car.rating;
				ratingDiv.classList.add("car-rating");
				carNameItem.appendChild(ratingDiv);


				var deleteButton = document.createElement("button");
				deleteButton.innerHTML = "Remove";
				deleteButton.classList.add("delete-button");
				deleteButton.onclick = function () {
					console.log("Please delete this", car.id);
					if(confirm("Are you sure you want to remove this?")) {
					deleteCarOnServer(car.id);
					}
				};

				var editButton = document.createElement("button");
				editButton.innerHTML = "Edit";
				editButton.classList.add("edit-button");
				editButton.onclick = function () 
				{
					updateCarInputYear.value = car.year;
					updateCarInputMake.value = car.make;
					updateCarInputModel.value = car.model;
					updateCarInputType.value = car.type;
					updateCarInputRating.value = car.rating;

					var updateButton = document.createElement("button");
					updateButton.innerHTML = "Update";
					updateButton.classList.add("update-button");
					updateButton.onclick = function() 
					{
						updateCarOnServer(updateCarInputYear.value, updateCarInputMake.value,
											updateCarInputModel.value, updateCarInputType.value,
											updateCarInputRating.value, car.id);
						
						var ogDiv = document.querySelector("#original-box");
						ogDiv.style.display = "inline-block";
						saveButton.style.display = "inline-block";

						var newDiv = document.querySelector("#new-box");
						newDiv.style.display = "none";
						updateButton.style.display = "none";
					};

					var ogDiv = document.querySelector("#original-box");
					ogDiv.style.display = "none";
					saveButton.style.display = "none";

					var newDiv = document.querySelector("#new-box");
					newDiv.style.display = "inline-block";
					updateButton.style.display = "inline-block";

					var updateDiv = document.querySelector("#update-button");
					updateDiv.innerHTML = "";
					updateDiv.appendChild(updateButton);

					console.log("update: ", car.id);
				}

				carNameList.appendChild(editButton);

				carNameList.appendChild(deleteButton);

				carNameList.appendChild(carNameItem);	
			});
		});
	});
}

////// USER STUFF //////

function createUserOnServer( fname, lname, email, password )
{
	var data = "fname=" + encodeURIComponent(fname);
	data += "&lname=" + encodeURIComponent(lname);
	data += "&email=" + encodeURIComponent(email);
	data += "&password=" + encodeURIComponent(password);

	fetch("https://car-saver.herokuapp.com/users",
	{ 
		//request options go here: method, header(s), body.
		method: "POST",
		credentials: "include",
		body: data,
		headers: 
		{
			"Content-Type": "application/x-www-form-urlencoded"
		}
		
	}).then(function(response)
	{
		if ( response.status == 422 )
		{
			confirm("This email is already in use.")
			loadCarsFromServer();
		}
		else if ( response.status == 201 )
		{
			loadCarsFromServer();
		}
		loadCarsFromServer();
	});
}

var createButton = document.querySelector("#create-button");

createButton.onclick = function() 
{
	var newEmail = document.querySelector("#new-email-box");
	var newFname = document.querySelector("#new-fname-box");
	var newLname = document.querySelector("#new-lname-box");
	var newPassword = document.querySelector("#new-password-box");
	
	createUserOnServer(newFname.value, newLname.value,
				 newEmail.value, newPassword.value);	
	newEmail.value = "Email";
	newFname.value = "First Name";
	newLname.value = "Last Name";
	newPassword.value = "Password";
};

function loginUserOnServer(email, password)
{
	var data = "email=" + encodeURIComponent(email);
	data += "&password=" + encodeURIComponent(password);

	fetch("https://car-saver.herokuapp.com/sessions",
	{ 
		//request options go here: method, header(s), body.
		method: "POST",
		credentials: "include",
		body: data,
		headers: 
		{
			"Content-Type": "application/x-www-form-urlencoded"
		}
		
	}).then(function(response)
	{
		if ( response.status == 401 )
		{
			confirm("Invalid Password.")
			loadCarsFromServer();
		}
		else if ( response.status == 201 )
		{
			loadCarsFromServer();
		}
		loadCarsFromServer();
	});
}


var loginButton = document.querySelector("#login-button");

loginButton.onclick = function()
{
	var loginEmail = document.querySelector("#email-box");
	var loginPassword = document.querySelector("#password-box");

	loginUserOnServer(loginEmail.value, loginPassword.value);
	
	loginEmail.value = "Email";
	loginPassword.value = "Password";
};

//when the page loads:
loadCarsFromServer();
