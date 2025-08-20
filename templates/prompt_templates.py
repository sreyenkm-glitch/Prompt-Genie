"""
Prompt templates for different use cases
These serve as starting points for the AI agents
"""

# Basic prompt templates by department ( dont hardcode anything )
DEPARTMENT_TEMPLATES = {
    "content": {
        "blog_post": "Create a comprehensive blog post about {topic} for {audience}",
        "social_media": "Design a social media campaign for {platform} about {topic}",
        "email_newsletter": "Write an engaging email newsletter about {topic} for {subscribers}",
        "content_strategy": "Develop a content strategy for {brand} targeting {audience}"
    },
    "digital_marketing": {
        "campaign_planning": "Plan a {campaign_type} marketing campaign for {product} targeting {audience}",
        "seo_optimization": "Optimize {content_type} for SEO targeting {keywords}",
        "ppc_strategy": "Create a PPC strategy for {product} with budget {budget}",
        "lead_generation": "Develop a lead generation strategy for {business_type}"
    },
    "digital_analytics": {
        "data_analysis": "Analyze {data_type} data to provide insights about {objective}",
        "kpi_reporting": "Create a KPI dashboard for {department} focusing on {metrics}",
        "performance_optimization": "Optimize {process} performance based on {data_source}",
        "trend_analysis": "Analyze trends in {data_set} over {time_period}"
    },
    "solutions": {
        "solution_design": "Design a solution for {problem} using {technology}",
        "business_consulting": "Provide consulting advice for {business_challenge}",
        "implementation_plan": "Create an implementation plan for {solution}",
        "transformation_strategy": "Develop a digital transformation strategy for {organization}"
    },
    "digital_operations": {
        "process_optimization": "Optimize the {process_name} process to improve {metric}",
        "automation_strategy": "Design an automation strategy for {workflow}",
        "efficiency_improvement": "Improve efficiency in {department} operations",
        "workflow_design": "Design a workflow for {task} with {constraints}"
    },
    "martech": {
        "platform_integration": "Integrate {platform1} with {platform2} for {purpose}",
        "stack_optimization": "Optimize the marketing technology stack for {business}",
        "automation_setup": "Set up marketing automation for {campaign_type}",
        "tool_evaluation": "Evaluate {tool_category} tools for {use_case}"
    },
    "ai_engineering": {
        "model_development": "Develop a {model_type} model for {task}",
        "ml_pipeline": "Design an ML pipeline for {data_type} processing",
        "ai_integration": "Integrate AI capabilities into {system}",
        "optimization": "Optimize {model} performance for {metric}"
    }
}

# Generic prompt structure template
GENERIC_PROMPT_STRUCTURE = """
You are an expert {role} with deep knowledge in {domain}.

**Context:**
{context}

**Task:**
{task}

**Requirements:**
- {requirements}

**Expected Output:**
{output_format}

**Quality Criteria:**
- {quality_criteria}

**Additional Guidelines:**
{guidelines}
"""

# Department-specific expertise areas
DEPARTMENT_EXPERTISE = {
    "content": [
        "Content strategy and planning",
        "SEO and content optimization", 
        "Social media content creation",
        "Email marketing and newsletters",
        "Brand voice and messaging",
        "Content performance analytics"
    ],
    "digital_marketing": [
        "Campaign planning and execution",
        "SEO/SEM strategies",
        "Social media marketing",
        "Email marketing automation",
        "Lead generation and nurturing",
        "Marketing analytics and ROI"
    ],
    "digital_analytics": [
        "Data analysis and interpretation",
        "KPI tracking and reporting",
        "Performance optimization",
        "Business intelligence",
        "Statistical analysis",
        "Data visualization"
    ],
    "solutions": [
        "Solution architecture design",
        "Business consulting",
        "Digital transformation",
        "Project management",
        "Technology implementation",
        "Strategic planning"
    ],
    "digital_operations": [
        "Process optimization",
        "Workflow automation",
        "Operational efficiency",
        "Digital transformation",
        "Change management",
        "Performance monitoring"
    ],
    "martech": [
        "Marketing technology stack",
        "Platform integration",
        "Marketing automation",
        "Tool evaluation and selection",
        "Technology implementation",
        "System optimization"
    ],
    "ai_engineering": [
        "Machine learning model development",
        "AI/ML pipeline design",
        "Model optimization and tuning",
        "AI system integration",
        "Data preprocessing",
        "MLOps and deployment"
    ]
}
