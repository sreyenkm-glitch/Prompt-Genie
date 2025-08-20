"""
AI Prompt Generator Agents using CrewAI
Intelligent agents that dynamically determine prompt requirements and generate structured prompts
"""

try:
    from crewai import Agent, Task, Crew, Process
    from langchain_community.llms import Ollama
    from langchain.tools import Tool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("Warning: CrewAI and LangChain dependencies not available. CrewAI agents will be disabled.")

from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PromptGeneratorAgents:
    """
    CrewAI agents for intelligent prompt generation
    """
    
    def __init__(self):
        """Initialize the agents with Ollama LLM"""
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI dependencies not available. Please install crewai, langchain, and langchain-community for this functionality.")
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            model=os.getenv("OLLAMA_MODEL", "llama2"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        
        # Initialize agents
        self.requirements_analyzer = self._create_requirements_analyzer()
        self.prompt_architect = self._create_prompt_architect()
        self.department_specialist = self._create_department_specialist()
        self.quality_validator = self._create_quality_validator()
    
    def _create_requirements_analyzer(self) -> Agent:
        """
        Agent that analyzes user input and determines what information is needed
        """
        return Agent(
            role="Requirements Analysis Specialist",
            goal="Analyze user input and dynamically determine what additional information is needed for optimal prompt generation",
            backstory="""You are an expert at analyzing user requirements and determining what information is missing 
            for creating effective prompts. You understand various business contexts and can identify gaps in information.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                Tool(
                    name="analyze_requirements",
                    func=self._analyze_user_requirements,
                    description="Analyze user input and determine missing information"
                )
            ]
        )
    
    def _create_prompt_architect(self) -> Agent:
        """
        Agent that designs the structure and format of prompts
        """
        return Agent(
            role="Prompt Architecture Expert",
            goal="Design structured, well-defined prompts with appropriate constraints and context",
            backstory="""You are a master at creating prompt architectures that maximize AI performance. 
            You understand how to structure prompts for clarity, specificity, and optimal results.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                Tool(
                    name="design_prompt_structure",
                    func=self._design_prompt_structure,
                    description="Design the structure and format for prompts"
                )
            ]
        )
    
    def _create_department_specialist(self) -> Agent:
        """
        Agent that provides department-specific expertise and context
        """
        return Agent(
            role="Department-Specific AI Specialist",
            goal="Provide expert knowledge and context for specific departments to enhance prompt quality",
            backstory="""You are an expert in multiple business departments including Content, Solutions, 
            Digital Marketing, Digital Analytics, Digital Operations, Martech, and AI Engineering. 
            You understand the unique needs, terminology, and best practices for each department.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                Tool(
                    name="add_department_context",
                    func=self._add_department_context,
                    description="Add department-specific context and expertise to prompts"
                )
            ]
        )
    
    def _create_quality_validator(self) -> Agent:
        """
        Agent that validates and improves prompt quality
        """
        return Agent(
            role="Prompt Quality Validator",
            goal="Validate and improve prompt quality, ensuring clarity, completeness, and effectiveness",
            backstory="""You are a quality assurance expert for AI prompts. You ensure prompts are clear, 
            complete, and optimized for the best possible AI responses. You catch potential issues and suggest improvements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                Tool(
                    name="validate_prompt_quality",
                    func=self._validate_prompt_quality,
                    description="Validate and improve prompt quality"
                )
            ]
        )
    
    def _analyze_user_requirements(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input and determine what additional information is needed
        """
        analysis_prompt = f"""
        Analyze the following user input and determine what additional information would be helpful for creating an optimal prompt:
        
        User Input: {user_input}
        
        Consider:
        1. What department/domain is this related to?
        2. What specific task or goal is the user trying to achieve?
        3. What context or constraints are missing?
        4. What output format would be most useful?
        5. What level of detail is needed?
        
        Provide a structured analysis with:
        - Identified department/domain
        - Suggested questions to ask the user
        - Recommended prompt type
        - Missing context that should be gathered
        """
        
        response = self.llm.invoke(analysis_prompt)
        return {
            "analysis": response,
            "user_input": user_input
        }
    
    def _design_prompt_structure(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design the structure and format for the prompt
        """
        structure_prompt = f"""
        Based on the following requirements analysis, design a structured prompt format:
        
        Requirements: {requirements}
        
        Create a modern, sleek prompt structure that includes:
        1. Clear role definition
        2. Specific context and constraints
        3. Expected output format
        4. Quality criteria
        5. Any necessary examples or guidelines
        
        Make it professional, clear, and optimized for AI performance.
        """
        
        response = self.llm.invoke(structure_prompt)
        return {
            "prompt_structure": response,
            "requirements": requirements
        }
    
    def _add_department_context(self, prompt_structure: Dict[str, Any], department: str) -> Dict[str, Any]:
        """
        Add department-specific context and expertise
        """
        context_prompt = f"""
        Enhance the following prompt structure with department-specific expertise for {department}:
        
        Prompt Structure: {prompt_structure}
        Department: {department}
        
        Add:
        1. Department-specific terminology and concepts
        2. Industry best practices
        3. Common challenges and solutions
        4. Relevant metrics and KPIs
        5. Professional standards and guidelines
        
        Make it highly relevant and valuable for {department} professionals.
        """
        
        response = self.llm.invoke(context_prompt)
        return {
            "enhanced_prompt": response,
            "department": department,
            "original_structure": prompt_structure
        }
    
    def _validate_prompt_quality(self, enhanced_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and improve prompt quality
        """
        validation_prompt = f"""
        Validate and improve the quality of this prompt:
        
        Enhanced Prompt: {enhanced_prompt}
        
        Check for:
        1. Clarity and specificity
        2. Completeness of information
        3. Appropriate constraints and guidelines
        4. Professional tone and formatting
        5. Potential improvements or additions
        
        Provide the final, polished prompt with any necessary improvements.
        """
        
        response = self.llm.invoke(validation_prompt)
        return {
            "final_prompt": response,
            "quality_score": "High",
            "improvements_made": "Validated and optimized"
        }
    
    def generate_prompt(self, user_input: str, department: str = None) -> Dict[str, Any]:
        """
        Generate a structured prompt using the AI agent crew
        """
        # Create tasks for the crew
        analysis_task = Task(
            description=f"""
            Analyze the user input and determine what additional information is needed:
            User Input: {user_input}
            Department: {department or 'Not specified'}
            
            Provide a comprehensive analysis of what information would be helpful for creating an optimal prompt.
            """,
            agent=self.requirements_analyzer,
            expected_output="Detailed analysis of user requirements and missing information"
        )
        
        structure_task = Task(
            description="""
            Based on the requirements analysis, design a structured prompt format that is modern, sleek, and professional.
            Focus on clarity, specificity, and optimal AI performance.
            """,
            agent=self.prompt_architect,
            expected_output="Well-structured prompt format with clear guidelines"
        )
        
        context_task = Task(
            description=f"""
            Enhance the prompt structure with department-specific expertise for {department or 'general business'}.
            Add relevant terminology, best practices, and professional standards.
            """,
            agent=self.department_specialist,
            expected_output="Department-enhanced prompt with professional context"
        )
        
        validation_task = Task(
            description="""
            Validate and improve the final prompt quality.
            Ensure it's clear, complete, and optimized for the best possible AI responses.
            """,
            agent=self.quality_validator,
            expected_output="Final, polished prompt ready for use"
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[self.requirements_analyzer, self.prompt_architect, 
                   self.department_specialist, self.quality_validator],
            tasks=[analysis_task, structure_task, context_task, validation_task],
            verbose=True,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        return {
            "generated_prompt": result,
            "user_input": user_input,
            "department": department,
            "status": "completed"
        }
