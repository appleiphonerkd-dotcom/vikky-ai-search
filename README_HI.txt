VIKKY AI SEARCH — Android पर इंस्टॉल होने वाला वेब ऐप (PWA)

यह अभी Play Store APK/AAB नहीं है। यह मोबाइल पर ऐप की तरह इंस्टॉल होने वाला PWA प्रोजेक्ट है।
वेब सर्च और AI उत्तर चलाने के लिए सर्वर पर अपनी OpenAI और Tavily API keys जोड़ना जरूरी है।

फ्री होस्टिंग पर शुरू करने के चरण:
1. इस ZIP को कंप्यूटर पर खोलें।
2. GitHub पर नया private/public repository बनाकर सभी फाइलें अपलोड करें।
3. Render.com पर GitHub repository से नया Web Service बनाएं।
4. Render build command: pip install -r requirements.txt
5. Start command: uvicorn app:app --host 0.0.0.0 --port $PORT
6. Environment में OPENAI_API_KEY और TAVILY_API_KEY जोड़ें।
7. Deploy होने के बाद HTTPS URL खोलें।

मोबाइल पर इंस्टॉल:
Chrome में अपना HTTPS ऐप URL खोलें → ⋮ मेन्यू → Add to Home screen / Install app।

Play Store:
Play Store पर डालने के लिए बाद में इस HTTPS PWA को Trusted Web Activity (TWA) से Android App Bundle (AAB) में पैक करना,
Digital Asset Links सेट करना, Play Console account बनाना और Google की मौजूदा testing/policy requirements पूरी करना होगा।
इस ZIP में Play Store-ready AAB शामिल नहीं है।

सुरक्षा:
- API keys केवल hosting के server-side Environment Variables में रखें।
- API keys को HTML/JavaScript, GitHub या किसी public file में कभी न डालें।
- Public launch से पहले authentication, rate limiting, usage caps, privacy policy और abuse protection जोड़ें।
- Free hosting sleep/usage limits रख सकती है; API providers भी मुफ्त नहीं हो सकते।
