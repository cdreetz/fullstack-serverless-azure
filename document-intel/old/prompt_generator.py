from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SectionConfig:
    """Configuration for section-specific prompting"""
    key_points: List[str]
    format_instructions: str
    example_output: Optional[str] = None
    max_length: Optional[int] = None

class PromptGenerator:
    def __init__(self):
        # Define section-specific configurations
        self.section_configs: Dict[str, SectionConfig] = {
            "administrative": SectionConfig(
                key_points=[
                    "Administrative procedures and requirements",
                    "Deadlines and timeframes",
                    "Reporting requirements",
                    "Compliance obligations",
                    "Authorization processes"
                ],
                format_instructions="""
                Organize the summary with the following structure:
                1. Key Administrative Requirements
                2. Timeline and Deadlines
                3. Compliance Requirements
                4. Authorization Procedures
                
                Use bullet points for specific requirements.
                Keep language clear and concise.
                Preserve all numeric values and dates exactly as stated.
                """,
                example_output="""
                Key Administrative Requirements:
                • Agencies must submit reports within 60 days
                • Maximum administrative cost allowance of 5%
                
                Timeline and Deadlines:
                • Applications due: 80 days after announcement
                • Review period: 65 days from receipt
                
                Compliance Requirements:
                • Monthly performance reporting
                • Annual audit submission
                
                Authorization Procedures:
                • Written approval required for budget modifications
                • Dual-signature requirement for expenditures over $50,000
                """
            ),
            "financial": SectionConfig(
                key_points=[
                    "Budget allocations",
                    "Funding restrictions",
                    "Allowable costs",
                    "Financial reporting requirements",
                    "Payment procedures"
                ],
                format_instructions="""
                Present financial information in these categories:
                1. Budget Overview
                2. Funding Restrictions
                3. Financial Requirements
                4. Payment Details
                
                Use tables for numeric data when applicable.
                Maintain exact dollar amounts and percentages.
                Highlight any caps or thresholds.
                """,
                max_length=1000
            ),
            "operational": SectionConfig(
                key_points=[
                    "Operational procedures",
                    "Program requirements",
                    "Implementation guidelines",
                    "Performance metrics",
                    "Quality control measures"
                ],
                format_instructions="""
                Structure the operational summary as:
                1. Program Overview
                2. Implementation Requirements
                3. Performance Standards
                4. Quality Control
                
                Include specific operational metrics.
                Highlight critical procedures.
                Note any exceptions or special cases.
                """
            )
        }

    def _get_section_prompt(self, section_type: str, content: str) -> str:
        """
        Generate a specific prompt for the given section type and content.
        
        Args:
            section_type: Type of section (e.g., 'administrative', 'financial')
            content: The source content to be summarized
            
        Returns:
            Formatted prompt string for the LLM
        """
        if section_type not in self.section_configs:
            raise ValueError(f"Unknown section type: {section_type}")
            
        config = self.section_configs[section_type]
        
        # Build the prompt
        prompt = f"""You are a specialized document analyst focusing on {section_type} content.

Task: Create a comprehensive summary of the following {section_type} content, focusing on these key aspects:
{chr(10).join(f"• {point}" for point in config.key_points)}

Format Requirements:
{config.format_instructions}

Rules:
1. Maintain absolute accuracy - do not infer or add information not present in the source
2. Preserve all specific numbers, dates, and requirements exactly as stated
3. Use clear, professional language
4. Highlight any critical deadlines or requirements
5. Note any exceptions or special conditions
"""

        # Add example if available
        if config.example_output:
            prompt += f"\nExample Output Format:\n{config.example_output}\n"

        # Add length constraint if specified
        if config.max_length:
            prompt += f"\nLimit the summary to approximately {config.max_length} characters.\n"

        # Add the content to analyze
        prompt += f"\nContent to Analyze:\n{content}\n"

        # Add final instruction
        prompt += """
Please provide a well-structured summary following the above requirements.
Focus on accuracy and clarity while maintaining all specific details from the source content."""

        return prompt

    def generate_section_prompts(self, 
                               content_blocks: Dict[str, List[str]], 
                               max_tokens: Optional[int] = None) -> Dict[str, str]:
        """
        Generate prompts for multiple sections.
        
        Args:
            content_blocks: Dictionary mapping section types to their content
            max_tokens: Optional maximum tokens for response
            
        Returns:
            Dictionary of section types to their generated prompts
        """
        prompts = {}
        for section_type, content in content_blocks.items():
            # Join content blocks with appropriate spacing
            combined_content = "\n\n".join(content)
            
            # Generate basic prompt
            prompt = self._get_section_prompt(section_type, combined_content)
            
            # Add token constraint if specified
            if max_tokens:
                prompt += f"\nLimit your response to {max_tokens} tokens."
                
            prompts[section_type] = prompt
            
        return prompts

    def add_section_config(self, 
                          section_type: str, 
                          key_points: List[str],
                          format_instructions: str,
                          example_output: Optional[str] = None,
                          max_length: Optional[int] = None):
        """
        Add a new section configuration or update existing one.
        
        Args:
            section_type: Type of section to add/update
            key_points: List of key points to focus on
            format_instructions: Formatting instructions for the summary
            example_output: Optional example of desired output
            max_length: Optional maximum length constraint
        """
        self.section_configs[section_type] = SectionConfig(
            key_points=key_points,
            format_instructions=format_instructions,
            example_output=example_output,
            max_length=max_length
        )

# Initialize the prompt generator
prompt_gen = PromptGenerator()

# Generate a prompt for administrative content
admin_content = "Section 301. Funds made available under the heading..."
prompt = prompt_gen._get_section_prompt("administrative", admin_content)

# Add a new section type
prompt_gen.add_section_config(
    section_type="grants",
    key_points=[
        "Eligibility requirements",
        "Application process",
        "Funding limits",
        "Reporting requirements"
    ],
    format_instructions="List all requirements in bullet points...",
    example_output="Example grant summary..."
)

# Generate prompts for multiple sections
content_blocks = {
    "administrative": ["Section 301...", "Section 302..."],
    "financial": ["Budget allocation...", "Funding restrictions..."]
}
prompts = prompt_gen.generate_section_prompts(content_blocks, max_tokens=1000)

def print_prompts(prompts: dict):
    """Print prompts in a readable way"""
    print("\n" + "="*80 + "\n")
    
    for section_type, prompt in prompts.items():
        print(f"SECTION: {section_type.upper()}")
        print("-" * 40)
        print(prompt)
        print("\n" + "="*80 + "\n")

print_prompts(prompts)