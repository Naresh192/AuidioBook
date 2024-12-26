import streamlit as st
import streamlit.components.v1 as components

# Title of the Streamlit app
st.title("Text to Speech with Voice Selection")

# Add a text input field for the user to enter text
text_input = st.text_area("Enter text here...", height=150)

# Add a button to trigger speech
if st.button("Speak"):
    if text_input:
        # Embed the HTML and JavaScript for text-to-speech with voice selection
        components.html("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Text to Speech with Voice Selection</title>
        </head>
        <body>
            <h3>Text to Speech Demo</h3>
            
            <!-- Text input field -->
            <textarea id="textInput" rows="4" cols="50" placeholder="Enter text here..." style="width:100%"></textarea><br><br>
            
            <!-- Dropdown to select voice -->
            <label for="voiceSelect">Choose a voice:</label>
            <select id="voiceSelect"></select><br><br>
            
            <!-- Button to trigger text-to-speech -->
            <button onclick="speakText()">Speak</button>
            
            <script>
                // Function to fetch available voices and populate the dropdown
                function loadVoices() {
                    const voices = window.speechSynthesis.getVoices();
                    const voiceSelect = document.getElementById('voiceSelect');
                    voiceSelect.innerHTML = ''; // Clear previous voices
                    
                    // Add each voice to the dropdown
                    voices.forEach(function(voice) {
                        const option = document.createElement('option');
                        option.textContent = voice.name + (voice.lang ? ' (' + voice.lang + ')' : '');
                        option.value = voice.name;
                        voiceSelect.appendChild(option);
                    });
                }

                // Function to convert text to speech
                function speakText() {
                    // Get the text from the input field
                    const text = document.getElementById('textInput').value;

                    // Check if text is empty
                    if (text === '') {
                        alert('Please enter some text!');
                        return;
                    }

                    // Get the selected voice
                    const selectedVoiceName = document.getElementById('voiceSelect').value;
                    const voices = window.speechSynthesis.getVoices();
                    const selectedVoice = voices.find(voice => voice.name === selectedVoiceName);

                    // Create a new SpeechSynthesisUtterance instance
                    const utterance = new SpeechSynthesisUtterance(text);

                    // Set the selected voice
                    utterance.voice = selectedVoice;

                    // Optional: Set properties like pitch, rate, or volume
                    utterance.pitch = 1;  // Range: 0 to 2 (default is 1)
                    utterance.rate = 1;   // Range: 0.1 to 10 (default is 1)
                    utterance.volume = 1; // Range: 0 to 1 (default is 1)

                    // Speak the text
                    window.speechSynthesis.speak(utterance);
                }

                // Load voices when the page is ready or when voices change
                window.speechSynthesis.onvoiceschanged = loadVoices;

                // Initialize the voice selection dropdown
                loadVoices();
            </script>
        </body>
        </html>
        """, height=600)
    else:
        st.error("Please enter some text in the textarea to use the text-to-speech feature.")
