"""
AI Prompt Generator Agents using Google Gemini API
Intelligent agents that dynamically determine prompt requirements and generate structured prompts
"""

import requests
import json
import os
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv

load_dotenv()

class GeminiPromptGeneratorAgents:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Department detection agent
        self.department_detector = "Department Detection Specialist"
        # Interactive questioning agent
        self.question_generator = "Interactive Questioning Specialist"
        # Final prompt generator
        self.prompt_generator = "Final Prompt Generator"

    def _call_gemini_api(self, prompt: str, role: str = "AI Assistant") -> str:
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""You are an advanced {role} with deep expertise in AI, business strategy, and user experience.

SYSTEM CAPABILITIES:
- Advanced context understanding and analysis
- Sophisticated problem-solving with multiple perspectives
- Intelligent suggestion generation
- Adaptive response patterns based on user skill level
- Deep domain knowledge across all business departments

RESPONSE GUIDELINES:
- Provide highly specific, actionable insights
- Use advanced reasoning and analysis
- Offer multiple perspectives when relevant
- Include sophisticated examples and analogies
- Adapt complexity to user's apparent skill level
- Maintain professional yet approachable tone

{prompt}"""
                        }
                    ]
                }
            ]
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0].get('content', {})
                    parts = content.get('parts', [])
                    if parts and len(parts) > 0:
                        return parts[0].get('text', '')
            return f"Error: API returned status {response.status_code}"
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"

    def detect_department(self, user_request: str) -> Dict[str, Any]:
        """Intelligently detect the department based on user intent"""
        prompt = f"""
        Analyze the following user request and determine which department it belongs to.
        
        Available departments:
        1. Content - Content creation, writing, storytelling, editorial work, blog posts, articles
        2. Solutions - Problem-solving, consulting, strategy development, business solutions
        3. Digital Marketing - Marketing campaigns, user acquisition, brand promotion, social media, advertising
        4. Digital Analytics - Data analysis, insights, reporting, metrics, business intelligence, dashboards
        5. Digital Operations - Process optimization, operational efficiency, workflow automation, business processes
        6. Martech - Marketing technology, tools, automation, CRM, marketing platforms
        7. AI Engineering - Machine learning, AI development, algorithms, data engineering, model development, technical projects
        
        User Request: "{user_request}"
        
        **ENHANCED ANALYSIS GUIDELINES:**
        1. **Data Engineering** = AI Engineering (data pipelines, ETL, data infrastructure)
        2. **Portfolio Projects** = AI Engineering (technical skill demonstration)
        3. **Fresher/Entry-level** = Consider the learning aspect and career development
        4. **Technical Projects** = AI Engineering (coding, development, engineering)
        5. **Data Analysis** = Digital Analytics (business insights, reporting)
        6. **Marketing Projects** = Digital Marketing (campaigns, promotion)
        7. **Content Creation** = Content (writing, storytelling)
        8. **Business Solutions** = Solutions (strategy, consulting)
        9. **Process Improvement** = Digital Operations (efficiency, automation)
        10. **Technology Implementation** = Martech (tools, platforms)
        
        **SPECIAL CASES:**
        - "Data engineering" + "portfolio" + "fresher" = AI Engineering (technical portfolio building)
        - "Data analysis" + "insights" = Digital Analytics (business intelligence)
        - "Marketing" + "campaign" = Digital Marketing (promotional activities)
        - "Content" + "blog/article" = Content (writing and publishing)
        
        Analyze the intent, context, and keywords to determine the most appropriate department.
        Consider the primary goal, tools mentioned, and expected outcomes.
        
        Respond in JSON format:
        {{
            "department": "department_name",
            "confidence": "high/medium/low",
            "reasoning": "detailed explanation of why this department was chosen",
            "keywords_detected": ["list", "of", "relevant", "keywords"],
            "context_analysis": {{
                "primary_goal": "what the user wants to achieve",
                "skill_level": "fresher/intermediate/expert",
                "project_type": "portfolio/career/business/personal",
                "technical_focus": "yes/no"
            }}
        }}
        
        Only respond with the JSON, no additional text.
        """
        
        response = self._call_gemini_api(prompt, self.department_detector)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                # Fallback parsing
                return {
                    "department": "AI Engineering",  # Default fallback for technical projects
                    "confidence": "low",
                    "reasoning": "Could not parse department detection response",
                    "keywords_detected": [],
                    "context_analysis": {
                        "primary_goal": "unknown",
                        "skill_level": "unknown",
                        "project_type": "unknown",
                        "technical_focus": "unknown"
                    }
                }
        except json.JSONDecodeError:
            return {
                "department": "AI Engineering",  # Default fallback for technical projects
                "confidence": "low",
                "reasoning": "Failed to parse department detection response",
                "keywords_detected": [],
                "context_analysis": {
                    "primary_goal": "unknown",
                    "skill_level": "unknown",
                    "project_type": "unknown",
                    "technical_focus": "unknown"
                }
            }

    def generate_interactive_questions(self, user_request: str, department: str, user_answers: Dict[str, str] = None) -> Dict[str, Any]:
        """Generate smart, reduced questions based on department and current progress"""
        
        if user_answers is None:
            user_answers = {}
        
        # Enhanced context analysis
        request_lower = user_request.lower()
        is_portfolio_project = "portfolio" in request_lower
        is_fresher = "fresher" in request_lower or "beginner" in request_lower or "entry" in request_lower
        is_data_engineering = "data engineering" in request_lower
        is_technical_project = any(word in request_lower for word in ["project", "build", "create", "develop"])
        
        prompt = f"""
        You are a Smart Questioning Specialist for {department} department.
        
        User's original request: "{user_request}"
        Department: {department}
        Current answers collected: {json.dumps(user_answers, indent=2)}
        
        **CONTEXT ANALYSIS:**
        - Portfolio Project: {is_portfolio_project}
        - Fresher/Entry-level: {is_fresher}
        - Data Engineering: {is_data_engineering}
        - Technical Project: {is_technical_project}
        
        **SMART QUESTION REDUCTION RULES:**
        1. **Maximum 3-5 questions total** for the entire process
        2. **Skip obvious questions** - if the intent is clear from the request, don't ask
        3. **Prioritize critical information** - only ask questions that significantly impact the final prompt quality
        4. **Combine related questions** - group similar concepts into single questions
        5. **Use intelligent defaults** - suggest reasonable options when possible
        6. **Focus on department-specific essentials** - what does {department} absolutely need to know?
        
        **PORTFOLIO PROJECT ENHANCEMENTS:**
        - For portfolio projects: Focus on skills demonstration, project scope, timeline, and career impact
        - For freshers: Consider learning curve, realistic goals, and entry-level expectations
        - For data engineering: Include technical stack, data sources, and implementation approach
        - For career development: Emphasize job market relevance and skill showcase
        
        **DEPARTMENT-SPECIFIC PRIORITIES:**
        - Content: Target audience, content type, tone, distribution channels (skip if obvious)
        - Solutions: Problem scope, success metrics, constraints, stakeholders (skip if clear)
        - Digital Marketing: Target audience, campaign goals, budget, channels (skip if mentioned)
        - Digital Analytics: Data sources, KPIs, stakeholders, reporting needs (skip if obvious)
        - Digital Operations: Process scope, efficiency goals, tools, team size (skip if clear)
        - Martech: Technology needs, integration requirements, user adoption (skip if mentioned)
        - AI Engineering: Project type, technical requirements, skill level, timeline, career goals (skip if clear)
        
        **ANALYZE THE REQUEST FIRST:**
        - What information is already clear from the user's request?
        - What critical gaps remain that would significantly improve the prompt?
        - Can we infer reasonable defaults for any missing information?
        - For portfolio projects: What will make this project stand out to employers?
        - For freshers: What will make this project achievable yet impressive?
        
        **RESPOND IN JSON FORMAT:**
        {{
            "questions": [
                {{
                    "id": "q1",
                    "question": "What is your primary goal?",
                    "type": "multiple_choice",
                    "options": ["option1", "option2", "option3"],
                    "required": true,
                    "department_focus": "explanation of why this question is critical",
                    "inferred_from_request": "what we already know from the request"
                }}
            ],
            "progress_percentage": 80,
            "next_step": "description of what we're working towards",
            "is_complete": false,
            "smart_analysis": {{
                "information_already_clear": ["list", "of", "what", "we", "know"],
                "critical_gaps": ["list", "of", "what", "we", "need"],
                "inferred_defaults": ["list", "of", "reasonable", "assumptions"],
                "portfolio_focus": {is_portfolio_project},
                "fresher_focus": {is_fresher},
                "career_development": {is_portfolio_project or is_fresher}
            }}
        }}
        
        **IMPORTANT:** Only ask questions if the answer would significantly improve the final prompt. If the request is already comprehensive, consider completing the process with fewer questions.
        
        **PORTFOLIO PROJECT SPECIAL CONSIDERATIONS:**
        - Focus on skills that employers value
        - Consider project complexity vs. timeline
        - Include learning objectives and career impact
        - Emphasize real-world applicability
        
        Only respond with the JSON, no additional text.
        """
        
        response = self._call_gemini_api(prompt, self.question_generator)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                
                # Smart completion check - if we have enough info, complete the process
                if len(result.get('questions', [])) <= 2 and len(user_answers) >= 1:
                    result['is_complete'] = True
                    result['progress_percentage'] = 100
                
                return result
            else:
                # Fallback - minimal questions
                return {
                    "questions": [
                        {
                            "id": "q1",
                            "question": "What is your primary objective?",
                            "type": "text",
                            "required": True,
                            "department_focus": "Understanding the main goal",
                            "inferred_from_request": "Basic intent from request"
                        }
                    ],
                    "progress_percentage": 50,
                    "next_step": "Gathering essential requirements",
                    "is_complete": False,
                    "smart_analysis": {
                        "information_already_clear": ["Basic intent"],
                        "critical_gaps": ["Specific objectives"],
                        "inferred_defaults": ["General approach"],
                        "portfolio_focus": is_portfolio_project,
                        "fresher_focus": is_fresher,
                        "career_development": is_portfolio_project or is_fresher
                    }
                }
        except json.JSONDecodeError:
            return {
                "questions": [
                    {
                        "id": "q1",
                        "question": "What is your primary objective?",
                        "type": "text",
                        "required": True,
                        "department_focus": "Understanding the main goal",
                        "inferred_from_request": "Basic intent from request"
                    }
                ],
                "progress_percentage": 50,
                "next_step": "Gathering essential requirements",
                "is_complete": False,
                "smart_analysis": {
                    "information_already_clear": ["Basic intent"],
                    "critical_gaps": ["Specific objectives"],
                    "inferred_defaults": ["General approach"],
                    "portfolio_focus": is_portfolio_project,
                    "fresher_focus": is_fresher,
                    "career_development": is_portfolio_project or is_fresher
                }
            }

    def generate_final_prompt(self, user_request: str, department: str, all_answers: Dict[str, str]) -> str:
        """Generate the final, ready-to-use prompt based on collected information and smart analysis"""
        
        # Enhanced context analysis
        request_lower = user_request.lower()
        is_portfolio_project = "portfolio" in request_lower
        is_fresher = "fresher" in request_lower or "beginner" in request_lower or "entry" in request_lower
        is_data_engineering = "data engineering" in request_lower
        is_technical_project = any(word in request_lower for word in ["project", "build", "create", "develop"])
        
        # Analyze what we know and what we can infer
        smart_analysis = {
            "information_already_clear": [],
            "critical_gaps": [],
            "inferred_defaults": []
        }
        
        # Extract information from the original request
        if "app" in request_lower or "application" in request_lower:
            smart_analysis["information_already_clear"].append("App development project")
        if "campaign" in request_lower or "marketing" in request_lower:
            smart_analysis["information_already_clear"].append("Marketing campaign")
        if "analyze" in request_lower or "data" in request_lower:
            smart_analysis["information_already_clear"].append("Data analysis task")
        if "content" in request_lower or "blog" in request_lower or "article" in request_lower:
            smart_analysis["information_already_clear"].append("Content creation")
        if "ai" in request_lower or "machine learning" in request_lower or "model" in request_lower:
            smart_analysis["information_already_clear"].append("AI/ML development")
        if is_data_engineering:
            smart_analysis["information_already_clear"].append("Data engineering project")
        if is_portfolio_project:
            smart_analysis["information_already_clear"].append("Portfolio building for career development")
        if is_fresher:
            smart_analysis["information_already_clear"].append("Entry-level skill development")
        
        # Enhanced department-specific defaults
        if department == "AI Engineering":
            smart_analysis["inferred_defaults"].extend([
                "Technical implementation approach",
                "Industry-standard tools and technologies",
                "Best practices for code quality and documentation",
                "Performance and scalability considerations"
            ])
            if is_portfolio_project:
                smart_analysis["inferred_defaults"].extend([
                    "Portfolio presentation and documentation",
                    "GitHub repository setup and management",
                    "README file with project overview",
                    "Technical skills demonstration for employers"
                ])
            if is_fresher:
                smart_analysis["inferred_defaults"].extend([
                    "Learning objectives and skill development",
                    "Realistic timeline for entry-level developers",
                    "Common interview questions this project can help answer",
                    "Next steps for career advancement"
                ])
        elif department == "Digital Marketing":
            smart_analysis["inferred_defaults"].extend([
                "Target audience: General consumers",
                "Channels: Social media and digital platforms",
                "Goal: Brand awareness and engagement"
            ])
        elif department == "Content":
            smart_analysis["inferred_defaults"].extend([
                "Tone: Professional and engaging",
                "Format: Digital content",
                "Distribution: Online platforms"
            ])
        
        prompt = f"""
        You are a Final Prompt Generator specializing in {department} department with expertise in portfolio development and career guidance.
        
        User's original request: "{user_request}"
        Department: {department}
        Collected answers: {json.dumps(all_answers, indent=2)}
        Smart analysis: {json.dumps(smart_analysis, indent=2)}
        
        **CONTEXT ANALYSIS:**
        - Portfolio Project: {is_portfolio_project}
        - Fresher/Entry-level: {is_fresher}
        - Data Engineering: {is_data_engineering}
        - Technical Project: {is_technical_project}
        
        Create a comprehensive, ready-to-use prompt that:
        1. Incorporates all the collected information
        2. Uses intelligent defaults for missing information (based on smart analysis)
        3. Is specific to {department} domain expertise
        4. Provides clear structure and guidelines
        5. Is immediately actionable
        6. Follows best practices for prompt engineering
        7. Includes role definition, context, tasks, and expected output format
        
        **PORTFOLIO PROJECT ENHANCEMENTS:**
        - Include portfolio presentation guidelines
        - Add career development insights
        - Emphasize skills that employers value
        - Include project documentation requirements
        - Add interview preparation tips
        - Include next steps for career advancement
        
        **FRESHER/ENTRY-LEVEL CONSIDERATIONS:**
        - Focus on learning objectives
        - Include realistic timelines
        - Add common beginner mistakes to avoid
        - Include resources for further learning
        - Emphasize skill development over complexity
        
        **TECHNICAL PROJECT REQUIREMENTS:**
        - Include technical stack recommendations
        - Add implementation best practices
        - Include testing and deployment guidelines
        - Add performance optimization tips
        - Include security considerations
        
        **SMART ENHANCEMENT GUIDELINES:**
        - Use the smart analysis to fill in reasonable defaults
        - Leverage department-specific best practices
        - Include industry-standard terminology and approaches
        - Make assumptions based on common patterns in {department}
        - Ensure the prompt is comprehensive despite minimal user input
        - Focus on real-world applicability and career impact
        
        The prompt should be professional, detailed, and optimized for AI tools.
        Make it comprehensive enough that users can copy-paste and use immediately.
        
        Format the response with clear sections and professional formatting.
        Include a brief note about what information was inferred vs. provided by the user.
        
        **SPECIAL FOCUS FOR PORTFOLIO PROJECTS:**
        - Make it portfolio-ready with clear deliverables
        - Include employer-focused skill demonstration
        - Add project showcase recommendations
        - Include technical depth appropriate for the skill level
        - Emphasize real-world problem solving
        """
        
        return self._call_gemini_api(prompt, self.prompt_generator)

    def analyze_input_intent(self, user_request: str) -> Dict[str, Any]:
        """Analyze user input to determine if it's a question, suggestion request, or direct request"""
        prompt = f"""
        Analyze the following user input to determine the user's intent and provide appropriate response.
        
        User Input: "{user_request}"
        
        **INTENT ANALYSIS:**
        Determine if the user is:
        1. **Asking a Question** - Seeking information, advice, or explanation
        2. **Requesting Suggestions** - Looking for ideas, options, or recommendations
        3. **Making a Direct Request** - Wanting to create/generate something specific
        
        **QUESTION INDICATORS:**
        - Starts with "What", "How", "Why", "When", "Where", "Which"
        - Contains "best way", "how to", "what should", "can you explain"
        - Asks for advice, tips, or guidance
        - Seeks understanding or clarification
        
        **SUGGESTION REQUEST INDICATORS:**
        - Contains "ideas", "suggestions", "recommendations", "options"
        - Asks for "what can I", "what should I", "give me ideas"
        - Looking for alternatives or possibilities
        - Wants to explore different approaches
        
        **DIRECT REQUEST INDICATORS:**
        - "I want to create", "I need to build", "Help me make"
        - Specific action-oriented language
        - Clear intent to generate something
        
        **RESPONSE GUIDELINES:**
        - For Questions: Provide helpful, educational answer with actionable insights
        - For Suggestions: Offer 3-5 relevant options with brief explanations
        - For Direct Requests: Acknowledge and proceed with prompt generation
        
        Respond in JSON format:
        {{
            "intent_type": "question/suggestion_request/direct_request",
            "confidence": "high/medium/low",
            "response": "AI's helpful response to the user",
            "follow_up_question": "Next question to guide the user toward prompt generation",
            "context_enhanced": "Enhanced context for the next step",
            "department_hint": "suggested department based on the input"
        }}
        
        Only respond with the JSON, no additional text.
        """
        
        response = self._call_gemini_api(prompt, "Input Intent Analyzer")
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                # Fallback - treat as direct request
                return {
                    "intent_type": "direct_request",
                    "confidence": "low",
                    "response": "",
                    "follow_up_question": "",
                    "context_enhanced": user_request,
                    "department_hint": "general"
                }
        except json.JSONDecodeError:
            return {
                "intent_type": "direct_request",
                "confidence": "low",
                "response": "",
                "follow_up_question": "",
                "context_enhanced": user_request,
                "department_hint": "general"
            }

    def generate_smart_response(self, user_request: str, intent_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent response based on intent analysis with enhanced intelligence"""
        
        # Get conversation context and user profile
        context = self._get_conversation_context(user_request, intent_analysis)
        
        if intent_analysis["intent_type"] == "question":
            # Generate educational response with context awareness
            prompt = f"""
            You are an intelligent AI mentor with deep expertise in project development and prompt engineering.
            
            CONVERSATION CONTEXT:
            {context}
            
            USER'S QUESTION: "{user_request}"
            INTENT ANALYSIS: {intent_analysis}
            
            RESPONSE GUIDELINES:
            1. **Direct Answer**: Provide a specific, actionable answer to their question
            2. **Context Awareness**: Reference their situation and adapt to their experience level
            3. **Personalized Guidance**: Give advice tailored to their specific project and goals
            4. **Next Steps**: Provide clear, specific next steps they can take immediately
            5. **Follow-up Questions**: Ask 1-2 relevant follow-up questions to understand their needs better
            
            IMPORTANT: Be specific, avoid generic advice, and provide concrete examples relevant to their situation.
            
            Format your response as:
            - Direct answer to their question
            - Specific guidance for their situation
            - Clear next steps
            - 1-2 follow-up questions to better understand their needs
            """
            
            response = self._call_gemini_api(prompt, "AI Mentor")
            
            return {
                "type": "question_response",
                "content": response,
                "next_action": "ask_follow_up",
                "follow_up": self._generate_contextual_follow_up(user_request, intent_analysis, context),
                "context_used": context
            }
            
        elif intent_analysis["intent_type"] == "suggestion_request":
            # Generate personalized suggestions based on context
            prompt = f"""
            You are an intelligent AI mentor with deep expertise in project development and prompt engineering.
            
            CONVERSATION CONTEXT:
            {context}
            
            USER'S REQUEST: "{user_request}"
            INTENT ANALYSIS: {intent_analysis}
            
            SUGGESTION GUIDELINES:
            1. **Personalized Options**: Provide 3-5 suggestions specifically tailored to their situation
            2. **Skill Level Match**: Ensure suggestions match their experience and capabilities
            3. **Project Relevance**: Focus on suggestions that directly help their current project
            4. **Implementation Guidance**: Include brief implementation steps for each suggestion
            5. **Priority Ranking**: Rank suggestions by relevance and feasibility
            
            IMPORTANT: Be specific, avoid generic suggestions, and provide actionable options.
            
            Format your response as:
            - 3-5 specific, ranked suggestions
            - Brief implementation guidance for each
            - Ask which option interests them most and why
            """
            
            response = self._call_gemini_api(prompt, "AI Mentor")
            
            return {
                "type": "suggestions_response",
                "content": response,
                "next_action": "ask_for_choice",
                "follow_up": "Which of these options interests you most, and what specific aspects would you like to explore further?",
                "context_used": context
            }
            
        else:
            # Enhanced default response for direct requests
            return {
                "type": "direct_request",
                "content": f"I understand you want to proceed with: '{user_request}'. Let me help you create a targeted prompt for this specific project. I'll ask you a few focused questions to ensure we create exactly what you need.",
                "next_action": "proceed_to_prompt_generation",
                "follow_up": "",
                "context_used": context
            }

    def _get_conversation_context(self, user_request: str, intent_analysis: Dict[str, Any]) -> str:
        """Get conversation context for enhanced responses"""
        # Extract key information from the request
        request_lower = user_request.lower()
        
        # Detect experience level
        if any(word in request_lower for word in ['first', 'beginner', 'new', 'start', 'zero experience', 'no experience']):
            experience_level = "beginner"
        elif any(word in request_lower for word in ['intermediate', 'some experience', 'learning']):
            experience_level = "intermediate"
        elif any(word in request_lower for word in ['expert', 'advanced', 'experienced']):
            experience_level = "advanced"
        else:
            experience_level = "unknown"
        
        # Detect project type
        project_keywords = {
            'website': 'web development',
            'app': 'application development',
            'data': 'data analysis',
            'marketing': 'marketing',
            'content': 'content creation',
            'portfolio': 'portfolio project',
            'optimization': 'optimization project'
        }
        
        project_type = "general"
        for keyword, project in project_keywords.items():
            if keyword in request_lower:
                project_type = project
                break
        
        return f"""
        USER REQUEST: {user_request}
        EXPERIENCE LEVEL: {experience_level}
        PROJECT TYPE: {project_type}
        INTENT TYPE: {intent_analysis.get('intent_type', 'unknown')}
        CONFIDENCE: {intent_analysis.get('confidence', 'unknown')}
        CONTEXT: User is seeking guidance for {project_type} project as a {experience_level}
        """

    def _generate_contextual_follow_up(self, user_request: str, intent_analysis: Dict[str, Any], context: str) -> str:
        """Generate contextual follow-up questions based on conversation"""
        follow_up_prompt = f"""
        Based on the user's question: "{user_request}"
        And the conversation context: {context}
        
        Generate 1-2 specific follow-up questions that will help understand their needs better.
        Focus on their specific situation and project requirements.
        
        Return only the questions, one per line.
        """
        
        response = self._call_gemini_api(follow_up_prompt, "Follow-up Generator")
        questions = [q.strip() for q in response.split('\n') if q.strip() and '?' in q]
        return questions[0] if questions else "What specific aspect would you like to focus on?"

    def process_interactive_workflow(self, user_request: str) -> Dict[str, Any]:
        """Main workflow for interactive prompt generation with enhanced intelligence"""
        
        # Pre-process user request for better understanding
        request_lower = user_request.lower()
        
        # Handle common variations and edge cases
        if "help" in request_lower and len(request_lower.split()) < 5:
            # Only treat as help if it's a very short request with "help"
            return {
                "workflow_state": "help_needed",
                "message": "It looks like you might need help. Try describing what you want to accomplish, like 'I want to create a marketing campaign' or 'I need to analyze customer data'."
            }
        
        if len(user_request.strip()) < 10:
            # Too short, might need more information
            return {
                "workflow_state": "need_more_info",
                "message": "Please provide more details about what you want to accomplish. For example: 'I want to create a social media campaign for our new product' or 'I need to build a data analysis dashboard'."
            }
        
        # Step 1: Analyze input intent
        intent_analysis = self.analyze_input_intent(user_request)
        
        # Step 2: Generate smart response if needed
        smart_response = self.generate_smart_response(user_request, intent_analysis)
        
        # Step 3: Handle different response types
        if smart_response["type"] in ["question_response", "suggestions_response"]:
            return {
                "workflow_state": "chat_mode",
                "intent_analysis": intent_analysis,
                "smart_response": smart_response,
                "original_request": user_request
            }
        
        # Step 4: Proceed with normal prompt generation for direct requests
        # Detect department with enhanced intelligence
        department_info = self.detect_department(user_request)
        
        # Generate initial questions with context awareness
        questions_info = self.generate_interactive_questions(user_request, department_info["department"])
        
        return {
            "workflow_state": "awaiting_answers",
            "department_detected": department_info,
            "questions": questions_info,
            "original_request": user_request
        }

    def continue_from_smart_response(self, original_request: str, user_choice: str) -> Dict[str, Any]:
        """Continue workflow after smart response based on user's choice"""
        
        # Combine original request with user's choice for better context
        enhanced_request = f"{original_request} - User chose: {user_choice}"
        
        # Detect department with enhanced intelligence
        department_info = self.detect_department(enhanced_request)
        
        # Generate initial questions with context awareness
        questions_info = self.generate_interactive_questions(enhanced_request, department_info["department"])
        
        return {
            "workflow_state": "awaiting_answers",
            "department_detected": department_info,
            "questions": questions_info,
            "original_request": enhanced_request
        }

    def continue_workflow(self, user_request: str, department: str, current_answers: Dict[str, str]) -> Dict[str, Any]:
        """Continue the workflow with user answers and enhanced intelligence"""
        
        # Validate answers
        if not current_answers:
            return {
                "workflow_state": "error",
                "error": "No answers provided. Please answer the questions to continue."
            }
        
        # Check for empty or invalid answers
        empty_answers = [k for k, v in current_answers.items() if not v or v.strip() == ""]
        if empty_answers:
            return {
                "workflow_state": "error",
                "error": f"Please answer all questions. Missing answers for: {', '.join(empty_answers)}"
            }
        
        # Generate next set of questions or final prompt
        questions_info = self.generate_interactive_questions(user_request, department, current_answers)
        
        if questions_info.get("is_complete", False):
            # Generate final prompt with enhanced intelligence
            final_prompt = self.generate_final_prompt(user_request, department, current_answers)
            return {
                "workflow_state": "complete",
                "final_prompt": final_prompt,
                "department": department,
                "summary": {
                    "total_questions_answered": len(current_answers),
                    "department": department,
                    "original_request": user_request,
                    "processing_time": "3-5 minutes",
                    "quality_score": "High"
                }
            }
        else:
            return {
                "workflow_state": "awaiting_answers",
                "questions": questions_info,
                "department": department,
                "progress": questions_info.get("progress_percentage", 0)
            }
