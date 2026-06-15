import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "AIzaSyDEWS2dgfCw0nH73piStWdrDVCxySsvaZs")

# ✅ Use a currently available model from your list
model = genai.GenerativeModel("gemini-2.5-flash")

prompt = "Say hello from Gemini AI and confirm that you are working fine!"
response = model.generate_content(prompt)

print("\n------ Gemini API Test Output ------")
print(response.text)
print("------------------------------------")






