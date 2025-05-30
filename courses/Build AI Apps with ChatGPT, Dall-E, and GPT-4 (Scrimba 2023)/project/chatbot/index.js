import { Configuration, OpenAIApi } from 'openai'
import { process } from './env'

const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
})

const openai = new OpenAIApi(configuration)

const chatbotConversation = document.getElementById('chatbot-conversation')
 
const conversationArr = [
    {
        role: 'system',
        content: 'You are a highly knowledgeable assistant that is always happy to help.'
    }
] 
 
document.addEventListener('submit', (e) => {
    e.preventDefault()
    const userInput = document.getElementById('user-input')   
    conversationArr.push({ 
        role: 'user',
        content: userInput.value
    })
    fetchReply()
    const newSpeechBubble = document.createElement('div')
    newSpeechBubble.classList.add('speech', 'speech-human')
    chatbotConversation.appendChild(newSpeechBubble)
    newSpeechBubble.textContent = userInput.value
    userInput.value = ''
    chatbotConversation.scrollTop = chatbotConversation.scrollHeight
})

async function fetchReply(){
    const response = await openai.createChatCompletion({
        model: 'gpt-4',
        messages: conversationArr  
    })
    console.log(response)
/*
Challenge:
    1. Pass the completion to the renderTypewriterText function
       so it updates the DOM.
    2. Push an object to 'conversationArr'. This object 
       should have a similar format to the object we pushed 
       in line 21 but the 'role' should hold the string 
       'assistant' and the 'content' should hold the completion
       we get back from the API.
    3. Log out conversationArr to check it's working.
    
🔎 I am going to give you a big hint. To save yourself some 
   time and work, have a close look at the response before 
   tackling number 2.
*/
}

// {data: {id: "chatcmpl-76GLdLSofnnUt9SIiv0LBPtDB9dR8", object: "chat.completion", created: 1681727165, model: "gpt-4-0314", usage: {prompt_tokens: 31, completion_tokens: 7, total_tokens: 38}, choices: [{message: {role: "assistant", content: "The capital of Tunisia is Tunis."}, finish_reason: "stop", index: 0}]}, status: 200, statusText: "", headers: {cache-control: "no-cache, must-revalidate", content-type: "application/json"}, config: {transitional: {silentJSONParsing: true, forcedJSONParsing: true, clarifyTimeoutError: false}, adapter: xhrAdapter(e), transformRequest: [transformRequest(e,t)], transformResponse: [transformResponse(e)], timeout: 0, xsrfCookieName: "XSRF-TOKEN", xsrfHeaderName: "X-XSRF-TOKEN", maxContentLength: -1, maxBodyLength: -1, validateStatus: validateStatus(e), headers: {Accept: "application/json, text/plain, */*", Content-Type: "application/json", User-Agent: "OpenAI/NodeJS/3.2.1", Authorization: "Bearer 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"}, method: "post", data: "{"model":"gpt-4","messages":[{"role":"system","content":"You are a highly knowledgeable assistant that is always happy to help."},{"role":"user","content":"What is the capital of Tunisia?"}]}", url: "https://api.openai.com/v1/chat/completions"}, request: XMLHttpRequest {}}



function renderTypewriterText(text) {
    const newSpeechBubble = document.createElement('div')
    newSpeechBubble.classList.add('speech', 'speech-ai', 'blinking-cursor')
    chatbotConversation.appendChild(newSpeechBubble)
    let i = 0
    const interval = setInterval(() => {
        newSpeechBubble.textContent += text.slice(i-1, i)
        if (text.length === i) {
            clearInterval(interval)
            newSpeechBubble.classList.remove('blinking-cursor')
        }
        i++
        chatbotConversation.scrollTop = chatbotConversation.scrollHeight
    }, 50)
}