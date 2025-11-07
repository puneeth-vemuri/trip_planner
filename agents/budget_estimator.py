from crewai import Agent

def create_budget_estimator(llm=None):
    """Creates a budget estimation agent"""
    agent_config = {
        'role': 'Travel Budget Analyst',
        'goal': 'Provide accurate budget estimates and cost breakdowns for travel plans',
        'backstory': """You are a meticulous travel budget analyst with deep knowledge of 
        travel costs worldwide. You provide detailed breakdowns of expenses including 
        flights, accommodation, food, activities, and transportation. You're skilled at 
        finding ways to optimize budgets while maintaining quality experiences.""",
        'verbose': True,
        'allow_delegation': False
    }
    
    if llm:
        agent_config['llm'] = llm
    
    return Agent(**agent_config)
