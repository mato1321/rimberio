🐾 RIMBERIO - Pet Matching Recommendation SystemRIMBERIO is a smart adoption consultant based on the LINE Chatbot. By combining vector space algorithms with the ChromaDB vector database and utilizing a "6-Dimensional Compatibility Matching Model," it precisely recommends the most suitable pets for owners, aiming to reduce return rates after adoption.Core FeaturesFeatureDescriptionRecommendation EngineVector Space Model (VSM) + ChromaDB vector similarity calculation to accurately match owners and petsReal-time LINE InteractionNo App download required; conduct compatibility assessments directly via LINE chat6-Dimensional AnalysisActivity, Affection, Independence, Space Needs, Grooming, Noise LevelMulti-turn Conversation6 contextualized questions to progressively build the user preference vector6-Dimensional Feature Space DesignRIMBERIO defines "Owner-Pet Compatibility" within a 6-dimensional vector space, where each dimension ranges from [0.0 ~ 1.0]:Dim IDFeature NameDescriptionLow Value (0.0)High Value (1.0)0ActivityEnergy LevelHomebodyFitness Enthusiast1AffectionClinginessLonerVelcro Pet2IndependenceIndependencePlenty of timeFrequently out3SpaceSpace NeedsStudio AptLarge Yard4GroomingShedding LevelHypoallergenicHeavy Shedder5NoiseVocal LevelQuiet as a mouseLoud/VocalPet Characteristic Vector ExamplesPet NameActivityAffectionIndependenceSpaceGroomingNoiseSuitable OwnerBorder Collie1.00.60.30.90.80.7Active outdoor enthusiastBritish Shorthair0.20.30.90.20.50.1Busy office workerBeagle0.90.90.30.60.41.0Playful young personSiamese Cat0.61.00.10.20.30.9Someone wanting a companionShiba Inu0.70.40.90.51.00.6Independent, patient ownerQuestionnaire Design (6 Questions)Q1【Activity】
   The weekend is here, what is your ideal itinerary?
   ✓ Hiking/Running/Adventure    → value=0.9 (High Activity)
   ✓ Park Stroll/Shopping        → value=0.5 (Medium Activity)
   ✓ Binge-watching/Sleeping     → value=0.1 (Low Activity)

Q2【Affection】
   When you are relaxing at home, you want your pet to:
   ✓ Cuddle/Stick to you         → value=0.9 (High Affection)
   ✓ Be in same room/Interact    → value=0.5 (Medium Affection)
   ✓ Do their own thing          → value=0.2 (Low Affection)

Q3【Independence】
   How long are you away for work on average per day?
   ✓ Over 10 hours               → value=0.9 (Needs High Independence)
   ✓ About 8 hours               → value=0.5 (Needs Medium Independence)
   ✓ WFH/Lots of free time       → value=0.1 (Needs Low Independence)

Q4【Space】
   What is your current living environment?
   ✓ House/Large Yard            → value=0.9 (Large Space)
   ✓ Apartment (3 rooms)         → value=0.5 (Medium Space)
   ✓ Studio/Shared Room          → value=0.1 (Small Space)

Q5【Grooming Tolerance】
   How do you feel about pet hair in the house?
   ✓ Absolutely not/Allergic     → value=0.1 (Cannot Accept)
   ✓ Okay if I clean often       → value=0.5 (Acceptable)
   ✓ Fur is home decoration      → value=0.9 (Fully Accept)

Q6【Noise Level】
   Regarding pet sounds/barking, your situation is:
   ✓ Poor soundproofing/Hate noise → value=0.1 (Needs Quiet)
   ✓ Residential area/Occasional   → value=0.5 (Standard Residential)
   ✓ Countryside/Detached house    → value=0.9 (Accepts Noise)
Quick Start1️⃣ Prerequisite EnvironmentBash# Check Python version (Requires 3.8+, Recommended 3.10+)
python --version
2️⃣ Create Virtual Environment & Install PackagesBash# Clone this project to local machine
git clone https://github.com/mato1321/rimberio.git
cd rimberio

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
3️⃣ Setup LINE Official Account (Messaging API)A. Create LINE Developers AccountGo to LINE Developers ConsoleLog in with your LINE accountClick "Create" to make a new Provider (e.g., Rimberio)B. Create Messaging API ChannelUnder the Provider you just created, click "Create a new channel"Select Messaging APIFill in the following info:Channel name:  RIMBERIO BotChannel description: Pet compatibility matching systemCategory: Personal UseSubcategory: OtherAgree to terms and complete creationC. Get Keys and Disable Auto-replyGo to your created Channel and navigate to:1. Basic Settings PageFind "Channel Secret"Click "Copy"2. Messaging API PageFind "Channel access token"Click "Generate" or "Regenerate"Click "Copy"3. Disable Auto-replyFind the "Auto-reply messages" section on the Messaging API pageClick "Edit"Set "Auto-response" to DisabledSet "Greeting message" to DisabledClick "Save"4️⃣ Setup Environment Variables (.env.example)Rename .env.example to .env and paste the Token and Secret you just copied:Bash# .env
LINE_CHANNEL_ACCESS_TOKEN=Your_Copied_Long_Channel_Access_Token
LINE_CHANNEL_SECRET=Your_Copied_Channel_Secret_Code
5️⃣ Start Local Development ServerBash# Ensure virtual environment is activated
python -m uvicorn main:app --reload
Output should look like this:INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
6️⃣ Create Public Tunnel (Ngrok)To allow LINE servers to connect to your local machine, use Ngrok to create a secure tunnel.A. Download and Install NgrokGo to Ngrok Official SiteDownload the version for your OSUnzip to a convenient location (e.g., C:\Tools\ngrok)B. Start NgrokRun in a new terminal window:Bash# Windows (Assuming ngrok is in C:\Tools\ngrok)
C:\Tools\ngrok\ngrok.exe http 8000

# macOS / Linux
./ngrok http 8000
You will see output similar to:ngrok                                                             (Ctrl-C to quit)

Session Status                online
Session Expires               1 hour, 59 minutes
Version                       3.0.0
Region                        Tokyo (jp)
Forwarding                    https://xxxx-xxxx.ngrok-free.app -> http://localhost:8000
Forwarding                    http://xxxx-xxxx.ngrok-free.app -> http://localhost:8000
Copy the HTTPS URL from the Forwarding field (Must start with https), example:https://1a2b-3c4d-5e6f.ngrok-free.app
7️⃣ Setup LINE Webhook URLReturn to the LINE Developers Console, on your Channel's Messaging API page:Find the "Webhook URL" fieldClick "Edit"Paste the Ngrok URL + /callback, example:https://1a2b-3c4d-5e6f.ngrok-free.app/callback
Click "Update"Ensure the "Use webhook" toggle is ONFind the "Verify" button and click itIf it shows "Success", your bot is successfully connected!Usage TutorialStep 1: Add Bot as FriendOn the LINE Developers Console Channel page, find the QR CodeScan the QR Code with your LINE AppClick "Add" to friend the botStep 2: Start TestType any of the following keywords in the chat:StartTestStart Test (or 開始, 測驗 in Chinese)The bot will reply:Welcome to RIMBERIO!
We will help you find the perfect pet through 6 questions.

Are you ready? Let's start!
Step 3: Answer QuestionsThe bot will ask questions one by one. Select your answer by clicking the buttons:Question 1

【Q1/6 Activity】
The weekend is here, what is your ideal itinerary?

[Hiking/Run] [Park/Shop] [Home/Sleep]
Step 4: Receive RecommendationsAfter finishing the 6 questions, the bot will immediately analyze and reply:RIMBERIO Recommendation Results!
Based on your lifestyle, your most suitable partners are:

Rank 1: British Shorthair
Match Score: 85%
A quiet and steady gentleman, suitable for busy office workers in small apartments.
--------------------

Rank 2: Siamese Cat
Match Score: 72%
The velcro of the cat world, very vocal and needs your constant company.
--------------------

Rank 3: Border Collie
Match Score: 45%
Genius level intelligence, but needs massive exercise and space. For experienced outdoor types.
--------------------

Want to test again? Please type "Start".
Technical Deep DiveCore Algorithm: Vector Space Model (VSM)The core of RIMBERIO's recommendation engine is Euclidean Distance:$$d = \sqrt{\sum_{i=0}^{5} (user_i - pet_i)^2}$$Where:user_i = User's preference value in dimension ipet_i = Pet's characteristic value in dimension id = Euclidean Distance (Smaller is more similar)Match Score Calculation:match_score = max(0, (1 - distance) × 100%)
Advantages of ChromaDBCompared to calculating all distances directly, using ChromaDB vector database offers:AdvantageDescriptionEfficient QueryingUses HNSW indexing to quickly locate nearest neighbor petsScalabilityQuery time remains logarithmic as the number of pets increasesPersistencePet data is persisted; no need to re-initialize on server restartFlexible MetadataSupports text metadata like pet names and descriptionsFastAPI Asynchronous FlowPython# Event Driven Flow
1. LINE User sends message
   └─> 2.   Ngrok forwards to /callback endpoint
        └─> 3. handler.handle() parses signature and event
            └─> 4. @handler.add() route dispatch
                ├─> MessageEvent (Start Test)
                │   └─> send_question() Send first question
                └─> PostbackEvent (Answer Question)
                    └─> Update user_sessions[user_id]['vector']
                    └─> Check if more questions exist
                        ├─> YES: send_question() Send next question
                        └─> NO:  show_recommendation() Recommend pet
Dependency OverviewPlaintextCore Framework Layer
├── fastapi==0.124.2          (Web Framework)
├── uvicorn==0.38.0           (ASGI Server)
├── starlette==0.50.0         (FastAPI Base)
└── httptools==0.7.1          (HTTP Parsing)

LINE Integration Layer
├── line-bot-sdk==3.21.0      (LINE Official SDK)
├── aiohttp==3.13.2           (Async HTTP)
└── websockets==15.0.1        (WebSocket Support)

Vector DB Layer
├── chromadb==1.3.6           (Vector Database)
├── onnxruntime==1.23.2       (Model Inference)
├── numpy==2.3.5              (Numerical Comp)
└── pandas==2.3.3             (Data Processing)

Environment & Tools
├── python-dotenv==1.2.1      (Env Var Management)
├── pydantic==2.12.5          (Data Validation)
└── requests==2.32.5          (HTTP Client)
Full Package List: See requirements.txt (Total 104 dependencies)System Architecture┌─────────────────────────────────────────────────────┐
│                      LINE User                      │
│            (Scan QR Code to add Bot)                │
└────────────────────┬────────────────────────────────┘
                     │ LINE Messaging API
                     ▼
┌─────────────────────────────────────────────────────┐
│  Ngrok (Public HTTPS Tunnel - https://xxxx.app)     │
│       (Bridge: Local Dev Env → Public Internet)     │
└────────────────────┬────────────────────────────────┘
                     │ POST /callback
                     ▼
┌─────────────────────────────────────────────────────┐
│          FastAPI Web Server (Port 8000)             │
│                    (main.py)                        │
│  ┌──────────────────────────────────────────────┐   │
│  │  • WebhookHandler Event Routing              │   │
│  │  • MessageEvent Handler (Start Test)         │   │
│  │  • PostbackEvent Handler (Answer Questions)  │   │
│  │  • user_sessions Memory Management           │   │
│  └──────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │ Vector Query
                     ▼
┌─────────────────────────────────────────────────────┐
│       Data Model Layer (data_model.py)              │
│  ┌──────────────────────────────────────────────┐   │
│  │  DIMENSIONS:  [Activity, Affection, ...]     │   │
│  │  QUESTIONS:   6 Assessment Questions         │   │
│  │  PET_DB: 5 Pets (Vector Representation)      │   │
│  │  ChromaDB: Vector DB (Euclidean Distance)    │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                     │ Recommendation Result
                     ▼
┌─────────────────────────────────────────────────────┐
│    Recommendation (Flex Message / Text Message)     │
│  • Top 3 Pet Candidates                             │
│  • Match Score (0-100%)                             │
│  • Pet Characteristic Description                   │
└─────────────────────────────────────────────────────┘
Project Directory Structurerimberio/
├── .env.example                  # Env vars, rename this (LINE Token & Secret)
├── .gitignore                    # Git ignore settings
├── main.py                       # FastAPI Main Program
│   ├── FastAPI App Init
│   ├── LINE WebhookHandler Routing
│   ├── Text Message Handling (Start Logic)
│   ├── Postback Handling (Answer Logic)
│   ├── send_question() - Function to send Qs
│   └── show_recommendation() - Function to show results
│
├── data_model.py                 # Data Model & Vector DB 
│   ├── DIMENSIONS[] - 6 Dim Definitions
│   ├── PET_DB[] - 5 Pet Data (With Vectors)
│   ├── QUESTIONS[] - 6 Questions
│   └── ChromaDB Init & get_recommendations()
│
├── requirements.txt              # Dependency List 
ContactEmail: mato1321@example.comGitHub: @mato1321Issues: If you have any questions, feel free to open an issue at GitHub IssuesLicenseThis project is licensed under the MIT License. You are free to use, copy, and modify this project.Welcome to RIMBERIO, finding the perfect home for furry friends! ```ᙏ̥ (๑•́  ω •̀๑)∧_∧( ´・ω・)/   ⊃⊂(´・ω・`)