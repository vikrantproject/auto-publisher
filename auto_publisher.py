
import subprocess
import sys
import random
import time
import os
from datetime import datetime

# ============================================================================
# PHASE 1: DEPENDENCY MANAGEMENT (SELF-CORRECTION)
# ============================================================================

def check_and_install_dependencies():
    """
    Check if required modules are installed, and install them if missing.
    Required modules: moviepy, pyttsx3, schedule, Pillow, google-api-python-client
    """
    print("=" * 60)
    print("PHASE 1: CHECKING AND INSTALLING DEPENDENCIES")
    print("=" * 60)
    
    # Special handling for moviepy - need specific version and editor module
    print("\nChecking moviepy.editor...")
    try:
        from moviepy.editor import ImageClip
        print("✓ moviepy.editor is working")
    except (ImportError, ModuleNotFoundError):
        print("✗ moviepy.editor not available. Installing moviepy 1.0.3...")
        try:
            # Uninstall any existing moviepy first
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "moviepy"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Install working version
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "moviepy==1.0.3", 
                "--break-system-packages"
            ])
            print("✓ moviepy 1.0.3 installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install moviepy: {e}")
            sys.exit(1)
    
    # Check other required modules
    required_modules = {
        'pyttsx3': 'pyttsx3',
        'schedule': 'schedule',
        'PIL': 'Pillow',
        'googleapiclient': 'google-api-python-client',
        'google_auth_oauthlib': 'google-auth-oauthlib',
        'google.auth': 'google-auth',
    }
    
    for module_name, package_name in required_modules.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} is already installed")
        except ImportError:
            print(f"✗ {package_name} is missing. Installing...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package_name, 
                    "--break-system-packages"
                ])
                print(f"✓ {package_name} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {package_name}: {e}")
                sys.exit(1)
    
    print("\n✓ All dependencies are ready!\n")


# Run dependency check at script start
check_and_install_dependencies()

# Now import all required modules
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pyttsx3
import schedule
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Configure ImageMagick for moviepy
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})


# ============================================================================
# PHASE 2: CONTENT GENERATION (LOCAL & OFFLINE)
# ============================================================================

# Comprehensive topic database with templates for dynamic generation
# Categories: Technology, Business, Finance, Cybersecurity, Health, Science, Personal Development, etc.

TOPIC_CATEGORIES = {
    "cybersecurity": [
        "SQL Injection attacks exploit database vulnerabilities through malicious queries. Attackers insert harmful SQL code into input fields. This can expose sensitive data or compromise systems. Prevention includes input validation and parameterized queries. Always use prepared statements to protect your databases.",
        "Phishing remains one of the most common cyber threats today. Attackers impersonate trusted entities via email or messages. They trick users into revealing passwords or financial information. Look for suspicious URLs and grammatical errors. Always verify the sender before clicking links.",
        "Zero-day exploits target unknown software vulnerabilities. Hackers discover security flaws before developers can patch them. These attacks are highly valuable and dangerous. Organizations use threat intelligence to detect anomalies. Regular updates and security monitoring are essential defenses.",
        "Two-factor authentication adds an extra security layer to accounts. It requires both password and secondary verification method. This dramatically reduces unauthorized access risk. Use authenticator apps instead of SMS when possible. Enable it on all critical accounts immediately.",
        "Ransomware encrypts victim files and demands payment for decryption. It spreads through malicious emails and compromised websites. Victims often face data loss or hefty ransom fees. Regular backups are your best defense strategy. Never pay ransoms as it encourages more attacks.",
        "Man-in-the-middle attacks intercept communication between two parties. Attackers eavesdrop or modify data in transit. Public WiFi networks are common attack vectors. Use VPNs to encrypt your internet traffic. Avoid sensitive transactions on unsecured networks.",
        "Social engineering exploits human psychology rather than technical vulnerabilities. Attackers manipulate people into breaking security protocols. This includes pretexting, baiting, and tailgating techniques. Employee training is crucial for prevention. Trust but verify all unusual requests.",
        "DDoS attacks overwhelm servers with massive traffic floods. Multiple compromised systems target a single victim. This causes service disruption and financial losses. Content delivery networks help absorb attack traffic. Have an incident response plan ready.",
        "Password cracking uses various methods to break authentication. Brute force tries every possible combination systematically. Dictionary attacks use common words and phrases. Use long, complex, and unique passwords. Password managers make this easier to maintain.",
        "Network sniffing captures data packets traveling through networks. Attackers analyze traffic to extract sensitive information. Unencrypted data is especially vulnerable to interception. HTTPS and VPNs encrypt your communications. Always check for secure connections.",
    ],
    "finance": [
        "Compound interest is the eighth wonder of the world. Your money earns returns on both principal and accumulated interest. Starting early dramatically amplifies wealth accumulation over time. Even small amounts grow significantly with patience. Time in the market beats timing the market.",
        "Diversification reduces portfolio risk by spreading investments across assets. Don't put all eggs in one basket. Mix stocks, bonds, real estate, and other asset classes. This protects against market volatility and sector-specific downturns. Rebalance periodically to maintain target allocation.",
        "Emergency funds provide financial security during unexpected events. Aim for three to six months of living expenses. Keep it in easily accessible, low-risk accounts. This prevents forced selling of investments during emergencies. Build it gradually through automatic savings.",
        "Dollar-cost averaging removes emotion from investing decisions. Invest fixed amounts regularly regardless of market conditions. You buy more shares when prices are low. This strategy reduces timing risk and builds discipline. Automation makes it effortless to maintain.",
        "Credit scores impact loan terms and interest rates significantly. Payment history is the most important factor. Keep credit utilization below thirty percent of limits. Longer credit history improves your score over time. Check reports annually for errors.",
        "Index funds offer broad market exposure at low costs. They track market indices like the S&P 500. Management fees are minimal compared to active funds. Historical data shows most active managers underperform indices. Passive investing is powerful for long-term wealth.",
        "Tax-advantaged accounts accelerate wealth building through savings. 401k and IRA contributions reduce current taxable income. Investments grow tax-deferred or tax-free over decades. Employer matching is free money you shouldn't leave. Maximize contributions to these accounts first.",
        "Inflation erodes purchasing power over time silently. Your money buys less as prices increase. Cash loses real value if returns don't beat inflation. Investing in appreciating assets is essential protection. Stocks historically outpace inflation long-term.",
        "Asset allocation determines most of portfolio performance variance. Your mix of stocks, bonds, and cash matters more than picking individual securities. Adjust allocation based on age and risk tolerance. Younger investors can handle more stock exposure. Shift to bonds as retirement approaches.",
        "Debt snowball method builds momentum by paying smallest debts first. List debts from smallest to largest balance. Make minimum payments on all except the smallest. Attack that one with extra funds aggressively. Move to next debt after each payoff.",
    ],
    "business": [
        "Customer retention is more profitable than acquisition typically. Existing customers cost less to serve and buy more. They provide valuable referrals and feedback for improvement. Focus on exceptional service and relationship building. Loyalty programs encourage repeat business effectively.",
        "Cash flow management determines business survival more than profits. You can be profitable on paper but fail without cash. Monitor accounts receivable and payable closely always. Maintain reserves for unexpected expenses or opportunities. Invoice promptly and follow up on payments.",
        "Product-market fit is essential before scaling operations aggressively. Your product must solve real problems people will pay for. Gather customer feedback continuously and iterate quickly. Don't fall in love with your idea. The market determines success ultimately.",
        "Unique value propositions differentiate you from competitors clearly. Explain why customers should choose you specifically. Focus on benefits rather than just features. Make it clear, concise, and compelling always. Test different messages to find what resonates.",
        "Strategic partnerships multiply resources and reach exponentially. Find businesses with complementary offerings and shared customers. Joint ventures can open new markets quickly. Negotiate win-win agreements that benefit all parties. Start small and build trust gradually.",
        "Data-driven decisions outperform gut feelings consistently over time. Track key metrics relevant to your business goals. Use analytics to identify trends and opportunities. Test assumptions with experiments and measure results. Let evidence guide your strategy.",
        "Employee engagement directly impacts productivity and retention rates. Engaged workers are more innovative and customer-focused. Provide clear purpose, autonomy, and growth opportunities. Regular feedback and recognition boost morale significantly. Culture starts at the top.",
        "Pricing strategy affects both revenue and brand perception simultaneously. Price too low and you leave money on the table. Price too high and you limit market size. Consider value delivered, not just costs incurred. Test different price points to optimize revenue.",
        "Marketing funnels guide prospects from awareness to purchase systematically. Each stage requires different content and touchpoints. Nurture leads with valuable information before selling hard. Measure conversion rates at each stage carefully. Optimize weak points in the funnel.",
        "Scalable systems enable growth without proportional cost increases. Automate repetitive tasks wherever possible for efficiency. Document processes so they're repeatable by anyone. Invest in technology that grows with you. Design for scale from the beginning.",
    ],
    "technology": [
        "Artificial intelligence is transforming every industry rapidly today. Machine learning enables computers to learn from data patterns. Applications range from healthcare to autonomous vehicles everywhere. Ethical considerations around AI are increasingly important. The technology will reshape the workforce profoundly.",
        "Blockchain provides decentralized and transparent record-keeping systems. Transactions are recorded in immutable distributed ledgers. This eliminates need for central authorities or intermediaries. Applications extend beyond cryptocurrency to supply chains. Trust is built through cryptographic verification.",
        "Cloud computing delivers on-demand access to computing resources. Companies avoid large upfront infrastructure investments this way. Scalability allows resources to grow with demand. Major providers include AWS, Azure, and Google Cloud. Security and compliance remain important considerations.",
        "Internet of Things connects everyday devices to the internet. Sensors collect data and enable remote monitoring and control. Smart homes, cities, and factories are becoming reality. This generates massive amounts of data for analysis. Privacy and security challenges must be addressed.",
        "Quantum computing promises exponential increases in processing power. It uses quantum bits that can exist in multiple states. Complex problems unsolvable today become feasible with this technology. Cryptography will need new approaches for quantum resistance. Commercial applications are still emerging gradually.",
        "5G networks provide faster speeds and lower latency than predecessors. This enables real-time applications like remote surgery. More devices can connect simultaneously without congestion. Edge computing brings processing closer to data sources. Infrastructure rollout continues globally at varying paces.",
        "Augmented reality overlays digital information on physical environments. Applications include gaming, education, and industrial training scenarios. Hardware improvements make experiences more immersive and practical. Businesses use AR for product visualization and assembly. The line between digital and physical blurs.",
        "Edge computing processes data near its source rather than in centralized data centers. This reduces latency and bandwidth usage significantly. Critical for applications requiring real-time responses like autonomous vehicles. Privacy is enhanced as less data travels to cloud. Distributed architecture increases resilience.",
        "DevOps practices unite development and operations teams for faster delivery. Automation streamlines testing, deployment, and monitoring processes continuously. This enables more frequent releases with fewer errors. Cultural change is as important as tools. Organizations become more agile and responsive.",
        "Containers package applications with all dependencies for consistent deployment. They're lightweight compared to traditional virtual machines. Docker popularized containerization for software development and deployment. Kubernetes orchestrates containers across multiple hosts efficiently. This simplifies scaling and management.",
    ],
    "health": [
        "Regular exercise reduces risk of chronic diseases significantly. Aim for at least 150 minutes of moderate activity weekly. Physical activity improves both physical and mental health. It boosts energy, mood, and cognitive function noticeably. Start small and build consistency over intensity.",
        "Sleep quality affects nearly every aspect of health and performance. Adults need seven to nine hours nightly for optimal function. Poor sleep increases disease risk and impairs judgment. Maintain consistent sleep schedules even on weekends. Create dark, cool, quiet environments for better rest.",
        "Hydration is essential for every bodily function and system. Water regulates temperature, transports nutrients, and removes waste. Dehydration impairs physical and cognitive performance quickly. Drink water throughout the day, not just when thirsty. Individual needs vary based on activity and climate.",
        "Processed foods contribute to obesity and chronic disease epidemics. They're typically high in sugar, salt, and unhealthy fats. Whole foods provide more nutrients and fiber naturally. Reading labels helps identify hidden unhealthy ingredients. Cook at home to control what you consume.",
        "Stress management is crucial for mental and physical wellbeing. Chronic stress damages immune function and accelerates aging. Techniques include meditation, deep breathing, and regular exercise. Social connections and hobbies provide important stress relief. Seek professional help when feeling overwhelmed.",
        "Gut health influences immune function, mood, and overall wellness. The microbiome contains trillions of beneficial bacteria we need. Fermented foods and fiber support healthy gut bacteria. Antibiotics can disrupt this delicate balance temporarily. Probiotics may help restore gut health.",
        "Vitamin D deficiency is surprisingly common despite its importance. It supports bone health, immune function, and mood. Sunlight exposure triggers natural vitamin D production. Many people need supplements, especially in winter months. Blood tests can determine your levels accurately.",
        "Mental health deserves equal attention to physical health always. Depression and anxiety affect millions worldwide every year. Therapy and medication can be highly effective treatments. Reducing stigma encourages people to seek needed help. Self-care practices support mental wellness daily.",
        "Preventive care catches health issues before they become serious. Regular checkups and screenings save lives through early detection. Vaccinations protect against dangerous infectious diseases effectively. Dental care prevents problems affecting overall health too. Insurance often covers preventive services fully.",
        "Social connections significantly impact longevity and life satisfaction. Loneliness increases mortality risk comparable to smoking cigarettes. Strong relationships provide emotional support during difficult times. Community involvement gives life meaning and purpose. Invest time in nurturing important relationships regularly.",
    ],
    "personal_development": [
        "Growth mindset believes abilities can be developed through effort. This contrasts with fixed mindset that sees talent as innate. Embracing challenges becomes opportunity rather than threat. Failure is valuable feedback for learning and improvement. Your potential is not predetermined or limited.",
        "Goal setting provides direction and motivation for achievement. Write specific, measurable, achievable, relevant, time-bound goals carefully. Break large goals into smaller actionable steps daily. Regular review keeps you on track toward objectives. Celebrate progress to maintain momentum forward.",
        "Time management skills multiply your effectiveness and productivity dramatically. Prioritize important tasks over merely urgent ones. Use time blocking to dedicate focus to specific activities. Eliminate or delegate low-value activities whenever possible. Protect your time as your most valuable resource.",
        "Continuous learning keeps skills relevant in changing world. Read widely across different subjects and perspectives regularly. Online courses make education accessible and affordable now. Apply new knowledge through practice and experimentation immediately. Curiosity is the engine of personal growth.",
        "Emotional intelligence determines success as much as IQ does. Self-awareness means understanding your emotions and triggers well. Self-regulation involves managing reactions and impulses effectively. Empathy enables understanding others' perspectives and feelings genuinely. Social skills facilitate positive relationships and influence.",
        "Habit formation is key to lasting behavior change. Tiny habits are easier to establish than big ones. Consistency matters more than intensity or perfection initially. Environment design makes desired behaviors easier to execute. Stack new habits onto existing routines for success.",
        "Public speaking skills boost career and personal opportunities significantly. Most people fear it but it's a learnable skill. Preparation and practice reduce anxiety and improve delivery. Focus on audience value rather than your nervousness. Start with small, low-stakes speaking opportunities.",
        "Networking builds relationships that create opportunities over time. Focus on giving value rather than just taking. Maintain connections through regular, genuine outreach and engagement. Diverse networks expose you to different ideas and possibilities. Quality of connections matters more than quantity.",
        "Financial literacy empowers better money decisions throughout life. Understand basic concepts like budgeting, investing, and compound interest. Start learning regardless of current financial situation today. Knowledge reduces anxiety and increases confidence with money. Financial education is rarely taught in schools.",
        "Resilience helps you bounce back from setbacks and failures. Adversity is inevitable but response determines outcomes ultimately. Reframe challenges as opportunities for growth and learning. Build support systems before you need them desperately. Self-compassion accelerates recovery from difficulties.",
    ],
    "science": [
        "CRISPR gene editing technology enables precise DNA modifications. Scientists can add, remove, or alter genetic material. Applications include treating genetic diseases and improving crops. Ethical debates surround human genome editing capabilities. This technology will transform medicine and agriculture.",
        "Climate change results from increasing greenhouse gas concentrations. Human activities, especially fossil fuel combustion, are primary causes. Global temperatures are rising with serious environmental consequences. Renewable energy and efficiency can mitigate future impacts. Action now prevents worse outcomes later.",
        "Black holes are regions where gravity is so strong nothing escapes. They form when massive stars collapse after dying. Even light cannot escape their gravitational pull completely. They warp spacetime around them in extreme ways. Studying them tests our understanding of physics.",
        "Antibiotics revolutionized medicine but overuse creates resistant bacteria. These drugs kill bacteria or prevent their reproduction. Resistance develops when bacteria survive and pass on immunity. This threatens our ability to treat common infections. Use antibiotics only when truly necessary.",
        "Stem cells can develop into many different cell types. They have potential to repair or replace damaged tissues. Research explores treatments for diseases like Parkinson's and diabetes. Ethical debates exist around embryonic stem cell sources. Adult stem cells avoid some controversial aspects.",
        "Renewable energy sources don't deplete with use unlike fossil fuels. Solar, wind, and hydroelectric power are increasingly cost-competitive. They produce electricity with minimal greenhouse gas emissions. Storage technology is improving to handle intermittent generation. Transition is essential for sustainable future.",
        "Vaccines train immune systems to fight specific diseases effectively. They contain weakened or inactive parts of pathogens. Your body learns to recognize and attack these invaders. This prevents or reduces disease severity dramatically. Vaccination protects individuals and communities through herd immunity.",
        "Neuroplasticity means brains can reorganize and form new connections. This continues throughout life, not just childhood. Learning new skills strengthens neural pathways physically. Brain health benefits from mental and physical exercise. You can literally change your brain structure.",
        "Biodiversity supports ecosystem health and human wellbeing directly. Different species play important roles in food webs. Loss of species can trigger cascading ecosystem failures. Protecting habitats preserves biodiversity for future generations. We depend on nature more than realized.",
        "Plate tectonics explains Earth's surface movements and geology. Massive plates float on semi-fluid mantle below crust. Their movements cause earthquakes, volcanoes, and mountain formation. Continents drift slowly over millions of years. This theory unified many geological observations elegantly.",
    ],
}

def generate_comprehensive_topic_database():
    """
    Generate a comprehensive database of 15,000+ topics by expanding base templates.
    """
    all_topics = []
    topic_id = 1
    
    # Add all base topics from categories
    for category, topics in TOPIC_CATEGORIES.items():
        for script in topics:
            # Extract topic from first sentence
            topic_name = script.split('.')[0]
            all_topics.append({
                "id": topic_id,
                "category": category,
                "topic": topic_name,
                "script": script
            })
            topic_id += 1
    
    # Generate variations and additional topics to reach 15k
    variations = [
        "Understanding", "Mastering", "Exploring", "Deep Dive into", "Introduction to",
        "Advanced", "Basics of", "Secrets of", "Guide to", "Tutorial on",
        "Everything About", "Facts About", "Truth Behind", "Science of", "Art of"
    ]
    
    additional_topics = {
        "cryptocurrency": [
            "Bitcoin uses blockchain technology for decentralized digital currency. Transactions are verified by network nodes through cryptography. It was created in 2009 by Satoshi Nakamoto. Supply is limited to 21 million coins total. Volatility remains a major characteristic of cryptocurrencies.",
            "Ethereum enables smart contracts and decentralized applications on blockchain. It introduced programmable blockchain functionality beyond simple transactions. Developers build DeFi and NFT platforms on Ethereum. The network is transitioning to proof-of-stake consensus. Gas fees can be high during network congestion.",
            "DeFi eliminates traditional financial intermediaries using blockchain technology. Users can lend, borrow, and trade without banks. Smart contracts automate and enforce agreements transparently. Returns can be higher but risks are significant. The space is innovative but largely unregulated.",
        ],
        "marketing": [
            "Content marketing attracts customers through valuable information rather than ads. It builds trust and establishes expertise in your field. Blog posts, videos, and podcasts are common formats. Consistency is more important than perfection in output. Distribution matters as much as content creation.",
            "Email marketing delivers exceptional ROI when done correctly. Build your list organically with genuine value offers. Segment audiences for more relevant messaging and higher engagement. Personalization increases open and click-through rates significantly. Test subject lines and send times systematically.",
            "Social media marketing requires platform-specific strategies for success. Each platform has different demographics and content preferences. Engagement algorithms favor consistent posting and interaction habits. Paid advertising can amplify organic content reach. Authenticity resonates more than polished corporate messaging.",
        ],
        "productivity": [
            "Pomodoro Technique uses timed intervals for focused work sessions. Work for 25 minutes then take a 5-minute break. After four pomodoros take a longer 15-30 minute break. This prevents burnout and maintains high concentration levels. Time constraints often increase focus and efficiency.",
            "Eisenhower Matrix categorizes tasks by urgency and importance. Focus on important but not urgent tasks for long-term success. Urgent and important tasks require immediate attention obviously. Delegate or eliminate unimportant tasks when possible. This framework prevents firefighting mentality.",
            "Getting Things Done system captures and organizes all commitments. Empty your mind by recording every task and idea. Process items regularly to determine next actions needed. Review weekly to maintain system integrity and perspective. Trusted system reduces mental load dramatically.",
        ],
        "psychology": [
            "Cognitive biases affect decision-making in predictable ways systematically. Confirmation bias makes us favor information supporting existing beliefs. Anchoring bias gives disproportionate weight to first information received. Awareness of biases helps make more rational decisions. No one is immune to these mental shortcuts.",
            "Dopamine drives motivation and reward-seeking behavior in brains. It's released in anticipation of rewards, not just receiving them. This explains addictive behaviors and habit formation mechanisms. Understanding dopamine helps manage motivation and focus better. Balance is important for mental health.",
            "Neuroplasticity allows brains to adapt and reorganize throughout life. New experiences create and strengthen neural pathways physically. This underlies learning, memory, and recovery from injury. You can literally rewire your brain with practice. Age doesn't prevent neuroplastic changes completely.",
        ],
        "entrepreneurship": [
            "Minimum viable product tests business ideas with minimal resources. Build only core features needed to validate assumptions. Get real customer feedback before investing heavily in development. Iterate based on what you learn from users. Perfect is the enemy of done here.",
            "Bootstrapping means building business without external funding initially. This maintains control and forces profitability focus early. Growth may be slower but more sustainable long-term. Customer revenue funds development and expansion naturally. Not every business needs venture capital.",
            "Pivot means fundamentally changing business model or product direction. Successful companies often pivot multiple times before finding product-market fit. Pay attention to signals that current approach isn't working. Be willing to abandon sunk costs quickly. Flexibility is a competitive advantage.",
        ],
        "leadership": [
            "Servant leadership prioritizes employee growth and wellbeing above all. Leaders serve their teams rather than being served. This approach builds trust, loyalty, and high performance. Empowering others multiplies impact beyond individual capacity. The leader's success is measured by team success.",
            "Situational leadership adapts style to context and team member needs. Different situations require different leadership approaches flexibly. New employees need more direction than experienced ones. Crisis demands different style than business as usual. Effective leaders read situations accurately.",
            "Transformational leadership inspires change through compelling vision and values. Leaders motivate followers to exceed expected performance levels. They challenge status quo and encourage innovation continuously. Personal example is more powerful than words alone. This creates lasting organizational culture change.",
        ],
        "investing": [
            "Value investing seeks undervalued stocks with strong fundamentals. Buy companies trading below intrinsic value estimates. This requires patience as market recognition takes time. Warren Buffett exemplifies this approach successfully long-term. Margin of safety protects against estimation errors.",
            "Growth investing targets companies with above-average growth potential. These stocks often trade at higher valuations. Revenue and earnings growth drive returns over time. Technology sector offers many growth opportunities historically. Higher risk accompanies higher potential returns.",
            "REITs provide real estate exposure without property management hassles. They must distribute 90% of income as dividends. This offers steady income and inflation protection. Different REITs focus on commercial, residential, or industrial properties. Liquidity is much higher than physical real estate.",
        ],
    }
    
    # Add additional topics
    for category, topics in additional_topics.items():
        for script in topics:
            topic_name = script.split('.')[0]
            all_topics.append({
                "id": topic_id,
                "category": category,
                "topic": topic_name,
                "script": script
            })
            topic_id += 1
    
    # Generate variations to reach 15k topics efficiently
    base_count = len(all_topics)
    print(f"Base topics created: {base_count}")
    
    # Pre-calculate how many variations needed
    target = 15000
    needed = target - base_count
    
    if needed > 0:
        # Generate efficiently using list comprehension
        for i in range(needed):
            base_topic = all_topics[i % base_count]
            variation_prefix = variations[i % len(variations)]
            
            all_topics.append({
                "id": topic_id,
                "category": base_topic["category"],
                "topic": f"{variation_prefix} {base_topic['topic']}",
                "script": base_topic["script"]
            })
            topic_id += 1
    
    print(f"Total topics generated: {len(all_topics)}")
    return all_topics

# Generate comprehensive database at module load
print("Initializing topic database...")
COMPREHENSIVE_TOPICS = generate_comprehensive_topic_database()
print(f"Ready: {len(COMPREHENSIVE_TOPICS)} topics available\n")


def generate_content_metadata():
    """
    Generate content metadata by selecting a random topic from 15k+ database.
    Returns: (script_text, video_title, video_description)
    """
    print("\n" + "=" * 60)
    print("PHASE 2A: GENERATING CONTENT METADATA")
    print("=" * 60)
    
    # Select a random topic from comprehensive database
    selected_topic = random.choice(COMPREHENSIVE_TOPICS)
    
    script_text = selected_topic["script"]
    category = selected_topic["category"].replace("_", " ").title()
    video_title = f"{selected_topic['topic']} | {category}"
    video_description = f"Discover insights about {selected_topic['topic']} in this educational video. Category: {category}. {script_text[:150]}..."
    
    print(f"✓ Topic ID: {selected_topic['id']}")
    print(f"✓ Category: {category}")
    print(f"✓ Selected Topic: {selected_topic['topic']}")
    print(f"✓ Video Title: {video_title}")
    print(f"✓ Script Length: {len(script_text)} characters")
    print(f"✓ Total Topics in Database: {len(COMPREHENSIVE_TOPICS)}")
    
    return script_text, video_title, video_description


def generate_audio(script_text, output_path):
    """
    Generate audio from text using local TTS engine.
    Uses espeak directly for reliability on Linux systems.
    
    Args:
        script_text: The text to convert to speech
        output_path: Path to save the audio file (e.g., 'audio.wav')
    
    Returns:
        float: Duration of the generated audio in seconds
    """
    print("\n" + "=" * 60)
    print("PHASE 2B: GENERATING AUDIO (LOCAL TTS)")
    print("=" * 60)
    
    try:
        # Method 1: Try using espeak directly (most reliable on Linux)
        try:
            print("✓ Using espeak for audio generation...")
            
            # Escape script text for shell
            import shlex
            escaped_text = shlex.quote(script_text)
            
            # Generate audio with espeak
            # -s: speed (words per minute, default 175)
            # -a: amplitude (volume, 0-200, default 100)
            # -w: write to WAV file
            cmd = f'espeak -s 150 -a 100 {escaped_text} -w {output_path}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✓ Audio generated successfully: {output_path}")
                print(f"✓ File size: {file_size} bytes")
                
                # Calculate audio duration based on word count and speech rate
                word_count = len(script_text.split())
                duration = (word_count / 150) * 60  # Convert to seconds
                duration = duration * 1.2  # Add buffer for pauses
                
                print(f"✓ Estimated Audio Duration: {duration:.2f} seconds")
                return duration
            else:
                raise Exception(f"espeak failed: {result.stderr}")
                
        except Exception as espeak_error:
            print(f"⚠ espeak method failed: {espeak_error}")
            print("✓ Trying pyttsx3 as fallback...")
            
            # Method 2: Fallback to pyttsx3
            engine = pyttsx3.init()
            
            # Set properties with error handling
            try:
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.9)
            except:
                pass
            
            # Save to file
            engine.save_to_file(script_text, output_path)
            engine.runAndWait()
            
            if not os.path.exists(output_path):
                raise Exception("Audio file was not created by pyttsx3")
            
            print(f"✓ Audio generated successfully: {output_path}")
            
            # Calculate duration
            word_count = len(script_text.split())
            duration = (word_count / 150) * 60
            duration = duration * 1.2
            
            print(f"✓ Estimated Audio Duration: {duration:.2f} seconds")
            return duration
        
    except Exception as e:
        print(f"✗ Error generating audio: {e}")
        raise


def generate_video(script_text, audio_duration, output_path):
    """
    Generate a video with text slides synchronized to audio duration.
    
    Args:
        script_text: The full script text
        audio_duration: Duration of audio in seconds
        output_path: Path to save the video file
    """
    print("\n" + "=" * 60)
    print("PHASE 2C: GENERATING VIDEO")
    print("=" * 60)
    
    try:
        # Video settings
        WIDTH = 1920
        HEIGHT = 1080
        FPS = 24
        BACKGROUND_COLOR = (31, 41, 55)  # Dark blue (#1f2937)
        TEXT_COLOR = 'white'
        
        # Split script into sentences/phrases
        sentences = script_text.replace('. ', '.|').split('|')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calculate duration per slide
        slide_duration = audio_duration / len(sentences)
        
        print(f"✓ Video Resolution: {WIDTH}x{HEIGHT}")
        print(f"✓ Number of Slides: {len(sentences)}")
        print(f"✓ Duration per Slide: {slide_duration:.2f} seconds")
        
        clips = []
        
        for i, sentence in enumerate(sentences):
            print(f"  Creating slide {i+1}/{len(sentences)}...")
            
            # Create background image as numpy array
            img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
            img_array = np.array(img)
            
            # Create text clip with shadow effect
            txt_clip = TextClip(
                sentence,
                fontsize=60,
                color=TEXT_COLOR,
                font='DejaVu-Sans-Bold',  # Available on Ubuntu
                size=(WIDTH - 200, None),
                method='caption',
                align='center'
            )
            
            # Create background clip from numpy array
            bg_clip = ImageClip(img_array).set_duration(slide_duration)
            
            # Position text in center
            txt_clip = txt_clip.set_position('center').set_duration(slide_duration)
            
            # Add fade in/out effects
            if i == 0:
                # First slide: fade in
                txt_clip = txt_clip.fadein(0.5)
            if i == len(sentences) - 1:
                # Last slide: fade out
                txt_clip = txt_clip.fadeout(0.5)
            
            # Composite text over background
            video_clip = CompositeVideoClip([bg_clip, txt_clip])
            clips.append(video_clip)
        
        # Concatenate all clips
        print("✓ Assembling video clips...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add audio
        audio_file = output_path.replace('.mp4', '_audio.wav')
        if os.path.exists(audio_file):
            audio = AudioFileClip(audio_file)
            final_video = final_video.set_audio(audio)
        
        # Write final video
        print("✓ Rendering final video (this may take a few minutes)...")
        final_video.write_videofile(
            output_path,
            fps=FPS,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        print(f"✓ Video generated successfully: {output_path}")
        
    except Exception as e:
        print(f"✗ Error generating video: {e}")
        raise


# ============================================================================
# PHASE 3: YOUTUBE UPLOAD & SCHEDULING
# ============================================================================

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def get_authenticated_service():
    """
    Authenticate and return YouTube API service object.
    
    SETUP INSTRUCTIONS:
    1. Go to https://console.cloud.google.com/
    2. Create a new project or select existing
    3. Enable YouTube Data API v3
    4. Create OAuth 2.0 credentials (Desktop app)
    5. Download client_secrets.json
    6. Place client_secrets.json in the same directory as this script
    """
    credentials = None
    
    # Load saved credentials if they exist
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If no valid credentials, authenticate
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not os.path.exists('client_secrets.json'):
                print("\n" + "!" * 60)
                print("ERROR: client_secrets.json NOT FOUND")
                print("!" * 60)
                print("\nPlease follow these steps:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project")
                print("3. Enable YouTube Data API v3")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download as client_secrets.json")
                print("6. Place it in the same directory as this script")
                print("\n" + "!" * 60)
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            credentials = flow.run_local_server(port=8080)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    
    return build('youtube', 'v3', credentials=credentials)


def youtube_upload(video_path, title, description):
    """
    Upload video to YouTube.
    
    Args:
        video_path: Path to the video file
        title: Video title
        description: Video description
    
    Returns:
        str: Video ID if successful, None otherwise
    """
    print("\n" + "=" * 60)
    print("PHASE 3: UPLOADING TO YOUTUBE")
    print("=" * 60)
    
    try:
        # Get authenticated service
        youtube = get_authenticated_service()
        
        if youtube is None:
            print("✗ Failed to authenticate with YouTube API")
            return None
        
        print("✓ Authenticated with YouTube API")
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['educational', 'facts', 'learning', 'knowledge'],
                'categoryId': '27'  # Education category
            },
            'status': {
                'privacyStatus': 'unlisted',  # Options: public, private, unlisted
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload object
        media = MediaFileUpload(
            video_path,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True
        )
        
        # Execute upload request
        print("✓ Starting upload...")
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"  Upload progress: {progress}%")
        
        video_id = response['id']
        print(f"✓ Upload complete!")
        print(f"✓ Video ID: {video_id}")
        print(f"✓ Video URL: https://www.youtube.com/watch?v={video_id}")
        
        return video_id
        
    except Exception as e:
        print(f"✗ Error uploading to YouTube: {e}")
        return None


# ============================================================================
# MAIN TASK ORCHESTRATION
# ============================================================================

def main_task():
    """
    Main orchestration function that runs the entire pipeline.
    """
    print("\n\n")
    print("*" * 60)
    print("STARTING NEW CONTENT CREATION CYCLE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("*" * 60)
    
    try:
        # Create output directory
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate unique filename based on timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = os.path.join(output_dir, f'audio_{timestamp}.wav')
        video_path = os.path.join(output_dir, f'video_{timestamp}.mp4')
        
        # Step 1: Generate content metadata
        script_text, video_title, video_description = generate_content_metadata()
        
        # Step 2: Generate audio
        audio_duration = generate_audio(script_text, audio_path)
        
        # Step 3: Generate video
        generate_video(script_text, audio_duration, video_path)
        
        # Step 4: Upload to YouTube
        video_id = youtube_upload(video_path, video_title, video_description)
        
        if video_id:
            print("\n" + "=" * 60)
            print("CYCLE COMPLETED SUCCESSFULLY!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("CYCLE COMPLETED (Upload skipped - check API setup)")
            print("=" * 60)
        
        # Clean up files to save space (optional)
        # Uncomment the lines below to delete files after upload
        # if video_id and os.path.exists(audio_path):
        #     os.remove(audio_path)
        # if video_id and os.path.exists(video_path):
        #     os.remove(video_path)
        
    except Exception as e:
        print(f"\n✗ Error in main task: {e}")
        import traceback
        traceback.print_exc()


# ============================================================================
# SCHEDULER
# ============================================================================

def scheduler():
    """
    Schedule the main_task to run every 2 hours.
    """
    print("\n" + "=" * 60)
    print("AUTO PUBLISHER SCHEDULER STARTED")
    print("=" * 60)
    print(f"Task will run every 2 hours")
    print(f"First run: Immediately")
    print(f"Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    # Run immediately on start
    main_task()
    
    # Schedule to run every 2 hours
    schedule.every(2).hours.do(main_task)
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         AUTO PUBLISHER - CONTENT CREATION ENGINE           ║
    ║                    v1.0 - Ubuntu 22.04                     ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        scheduler()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("Scheduler stopped by user")
        print("=" * 60)
        sys.exit(0)
