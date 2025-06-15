import asyncio
import io
import speech_recognition as sr
import edge_tts
import pygame


class RealTimeSpeechToSpeech:
    def __init__(self, 
                 voice: str = "en-US-JennyNeural",
                 listen_duration: int = 10):
        """
        Initialise the real-time Speech-to-Speech system.
        
        Param:
            :voice: TTS voice to use
            :listen_duration: How long to listen for each input
        """
        self.recogniser = sr.Recognizer()
        self.voice = voice
        self.listen_duration = listen_duration
        self.is_running = False
        
        # Initialise pygame to access audio from memory
        pygame.mixer.init()

        print("Initialising Speech-to-Speech system...")
    
    def listen_for_speech(self) -> str:
        """
        Record audio from microphone through the speech recognition library, and transcribe it
        utilsing the Google's API.
        
        Returns:
            Transcribed text or error message
        """
        with sr.Microphone() as source:
            print("Listening... (speak now)")
            
            try:
                # Calibrates background noise level to differentiate speech from silence
                self.recogniser.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for speech with longer timeout
                audio = self.recogniser.listen(source, timeout=2, phrase_time_limit=self.listen_duration)
                
                # Transcribe using Google's API
                text = self.recogniser.recognize_google(audio)
                print(f"You said: '{text}'")
                return text
                
            except sr.WaitTimeoutError:
                print("No speech detected within timeout period")
                return "TIMEOUT"
            
            except sr.UnknownValueError:
                print("Could not understand audio")
                return "UNCLEAR"
            
            except sr.RequestError as e:
                print(f"API error: {e}")
                return "ERROR"
            
            except Exception as e:
                print(f"Unexpected error: {e}")
                return "ERROR"

    def generate_response(self, user_input: str) -> str:
        """
        Generate a response based on user input.
        
        Param:
            :user_input: The transcribed user speech
            
        Returns:
            Response text to be spoken
        """
        # Simple hard-coded responses
        if "hello" in user_input.lower():
            return "Hello there! How can I help you today?"
        
        elif "how are you" in user_input.lower():
            return "I'm doing great, thank you for asking!"
        
        elif "bye" in user_input.lower() or "goodbye" in user_input.lower():
            return "Goodbye! It was nice talking with you."
        
        elif "stop" in user_input.lower() or "quit" in user_input.lower():
            return "Stopping the conversation. See you later!"
        
        else:
            return f"I heard you say: {user_input}. That's interesting!"
        
    async def play_audio_directly(self, audio_data: bytes):
        """
        Play audio data directly from memory using pygame.
        
        Param:
            audio_data: Raw audio data bytes
        """
        try:
            # Load audio from bytes into pygame mixer
            audio_io = io.BytesIO(audio_data)
            pygame.mixer.music.load(audio_io)
            pygame.mixer.music.play()
            
            # Wait for audio to finish playing with fail safe
            while pygame.mixer.music.get_busy():
                try:
                    await asyncio.sleep(0.1)
                    
                except asyncio.CancelledError:
                    # If cancelled, stop the music and raise
                    pygame.mixer.music.stop()
                    raise
                
        except asyncio.CancelledError:
            # raise CancelledError to allow for cleanup
            raise
        
        except Exception as e:
            print(f"Could not play audio: {e}")
    
    async def speak_response(self, text: str):
        """
        Convert text to speech and play it directly using pygame.
        
        Param:
            :text: Text to be converted to speech
        """
        try:
            # Utilse Microsoft Edge TTS to generate speech from text
            communicate = edge_tts.Communicate(text, self.voice)
            
            # Convert audio into bytes through chunks
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            # Play audio directly from memory
            await self.play_audio_directly(audio_data)
            
        except asyncio.CancelledError:
            # Handle cancellation
            print("\nAudio playback cancelled")
            raise
        
        except Exception as e:
            print(f"Error generating/playing speech: {e}")
            

    async def conversation_loop(self):
        """
        Main conversation loop for real-time interaction.
        """
        print("💡 Say 'stop' or 'quit' to end the conversation")
        print("=" * 50)
        
        self.is_running = True
        
        try:
            while self.is_running:
                # Listen for user input
                user_input = self.listen_for_speech()
                
                # Handle special cases
                if user_input == "TIMEOUT":
                    print("Listening again...")
                    continue
                
                elif user_input in ["UNCLEAR", "ERROR"]:
                    response = "I'm sorry, I didn't catch that. Could you please repeat?"
                    
                else:
                    # Generate response
                    response = self.generate_response(user_input)
                    
                    # Check for stop commands
                    if any(word in user_input.lower() for word in ["stop", "quit", "bye", "goodbye", "cya"]):
                        self.is_running = False
                
                # Convert response to speech and play
                print(f"Response: {response}")
                try:
                    await self.speak_response(response)
                except asyncio.CancelledError:
                    print("\nConversation interrupted")
                    break
                
                # Small delay before next iteration
                try:
                    await asyncio.sleep(0.5)
                    
                except asyncio.CancelledError:
                    print("\nConversation interrupted")
                    break
                
                if not self.is_running:
                    break
                    
        except KeyboardInterrupt:
            print("\nConversation interrupted by user")
            
        except asyncio.CancelledError:
            print("\nConversation cancelled")
            
        finally:
            # Cleanup
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        
        print("Thank you for using Speech-to-Speech!")


async def main():
    """
    Main function to run the Speech-to-Speech system
    """
    try:
        # Initialise the S2S system
        s2s = RealTimeSpeechToSpeech(
            voice = "en-US-JennyNeural",  
            listen_duration = 10 # How long to listen for each input
        )
        
        # Choose mode:
        await s2s.conversation_loop()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the system
if __name__ == "__main__":
    
    # Run the async main function
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
        
    except Exception as e:
        print(f"Fatal error: {e}")