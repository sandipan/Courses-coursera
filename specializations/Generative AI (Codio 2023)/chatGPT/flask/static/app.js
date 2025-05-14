const form = document.getElementById("rest-form");
const user_input = document.getElementById("user-name");
const response_elem = document.getElementById("name-exists");

form.addEventListener("submit", async (event) => {

	event.preventDefault();

	const user_input_value = user_input.value.trim();
	if (!user_input_value) {
		return;
	}

	try {
		  const resp = await fetch("/get_name", {
			method: "POST",
			headers: {
			  "Content-Type": "application/json",
			},
			body: JSON.stringify({ user_name: user_input_value })
		  });
		  const response_data = await resp.json();
		  if (resp.ok) {
			const chat_response = response_data.name;
			response_elem.value = chat_response;
		  } else {
			alert("Error when fetching response");
		  }
	} catch (error) {
		console.log('Fetch error: ', error);
		alert(error)
	}
	
 });