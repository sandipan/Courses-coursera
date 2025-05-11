const form = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const responseElem = document.getElementById("response");

form.addEventListener("submit", async (event) => {

	event.preventDefault();

	const userInputValue = userInput.value.trim();
	if (!userInputValue) {
		return;
	}

	try {
		  const resp = await fetch("/chat", {
			method: "POST",
			headers: {
			  "Content-Type": "application/json",
			},
			body: JSON.stringify({ user_input: userInputValue })
		  });
		  const responseData = await resp.json();
		  alert(responseData)
		  if (resp.ok) {
			const chatResponse = responseData.ans;
			responseElem.value = chatResponse;
		  } else {
			alert("Error when fetching response from ChatGPT API.");
		  }
	} catch (error) {
		console.log('Fetch error: ', error);
		alert(error)
	}
	
 });