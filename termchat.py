#!/usr/bin/env python3
"""
TermChat - A simple terminal AI chat application using OpenRouter
"""

import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner

# Load environment variables
load_dotenv()

class TermChat:
    def __init__(self):
        self.console = Console()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.default_model = os.getenv("DEFAULT_MODEL", "deepseek/deepseek-r1:free")
        
        if not self.api_key:
            self.console.print("[red]Error: OPENROUTER_API_KEY not found in environment variables.[/red]")
            self.console.print("Please copy env.example to .env and add your OpenRouter API key.")
            sys.exit(1)
        
        # Initialize OpenAI client with OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        self.conversation: List[Dict[str, str]] = []
        self.current_model = self.default_model
        
    def display_welcome(self):
        """Display welcome message and instructions"""
        welcome_text = Text()
        welcome_text.append("🤖 TermChat - Terminal AI Assistant\n\n", style="bold cyan")
        welcome_text.append(f"Current model: {self.current_model}\n", style="dim")
        welcome_text.append("Commands:\n", style="bold")
        welcome_text.append("  /help    - Show this help\n", style="dim")
        welcome_text.append("  /model   - Change AI model\n", style="dim")
        welcome_text.append("  /clear   - Clear conversation\n", style="dim")
        welcome_text.append("  /quit    - Exit the application\n", style="dim")
        welcome_text.append("\nType your message and press Enter to chat!", style="green")
        
        panel = Panel(welcome_text, title="Welcome", border_style="cyan")
        self.console.print(panel)
        self.console.print()

    def get_available_models(self) -> List[str]:
        """Get list of popular models available on OpenRouter"""
        return [
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "openai/o1-preview",
            "openai/o1-mini",
            "openai/gpt-3.5-turbo",
            "meta-llama/llama-3.1-8b-instruct:free",
            "microsoft/wizardlm-2-8x22b",
            "google/gemini-pro-1.5",
            "mistralai/mistral-7b-instruct:free",
            "deepseek/deepseek-r1:free",
            "google/gemma-3n-e4b-it:free",
        ]

    def change_model(self):
        """Allow user to change the AI model"""
        models = self.get_available_models()
        
        # Create the model selection display
        menu_text = Text()
        menu_text.append("\nAvailable Models:\n", style="bold")
        for i, model in enumerate(models, 1):
            marker = "→" if model == self.current_model else " "
            menu_text.append(f"{marker} {i}. {model}\n")
        menu_text.append(f"\nCurrent: {self.current_model}\n")
        
        # Display the menu
        self.console.print(menu_text)
        
        choice = Prompt.ask(
            "Enter model number (or press Enter to keep current)",
            default="",
            show_default=False
        )
        
        # Move cursor up to overwrite the menu and input
        lines_to_clear = len(models) + 5  # models + headers + current + prompt + input
        for _ in range(lines_to_clear):
            self.console.file.write("\033[1A\033[2K")  # Move up and clear entire line
        self.console.file.flush()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                old_model = self.current_model
                self.current_model = models[idx]
                self.console.print(f"[green]✓ Model changed from {old_model.split('/')[-1]} to {self.current_model.split('/')[-1]}[/green]")
            else:
                self.console.print("[red]Invalid model number[/red]")
        elif choice:
            self.console.print("[yellow]Invalid input - keeping current model[/yellow]")
        else:
            self.console.print("[dim]Keeping current model[/dim]")

    def clear_conversation(self):
        """Clear the conversation history"""
        if self.conversation and Confirm.ask("Clear conversation history?"):
            self.conversation.clear()
            self.console.print("[green]✓ Conversation cleared[/green]")

    def display_help(self):
        """Display help information"""
        help_text = Text()
        help_text.append("TermChat Commands:\n\n", style="bold cyan")
        help_text.append("/help    - Show this help message\n", style="dim")
        help_text.append("/model   - Change the AI model\n", style="dim")
        help_text.append("/clear   - Clear conversation history\n", style="dim")
        help_text.append("/quit    - Exit the application\n", style="dim")
        help_text.append("\nTips:\n", style="bold")
        help_text.append("• Press Ctrl+C to interrupt AI response\n", style="dim")
        help_text.append("• Conversation history is maintained until cleared\n", style="dim")
        help_text.append("• Use /model to switch between different AI models\n", style="dim")
        
        panel = Panel(help_text, title="Help", border_style="blue")
        self.console.print(panel)

    def get_ai_response(self, message: str) -> tuple[str, bool]:
        """Get response from OpenRouter AI"""
        try:
            # Add user message to conversation
            self.conversation.append({"role": "user", "content": message})
            
            # Create the API request
            response = self.client.chat.completions.create(
                model=self.current_model,
                messages=self.conversation,
                stream=True,
                temperature=0.7,
            )
            
            # Stream the response with live updates
            full_response = ""
            reasoning_content = ""
            current_section = "response"  # Track if we're in reasoning or response
            
            with Live(Text("AI is thinking...", style="dim"), refresh_per_second=20) as live:
                for chunk in response:
                    # Check for reasoning content (o1 models)
                    if hasattr(chunk.choices[0].delta, 'reasoning') and chunk.choices[0].delta.reasoning:
                        reasoning_content += chunk.choices[0].delta.reasoning
                        current_section = "reasoning"
                        # Show reasoning with a different style
                        thinking_display = Text()
                        thinking_display.append("🤔 AI is thinking:\n", style="bold yellow")
                        thinking_display.append(reasoning_content, style="dim italic")
                        live.update(thinking_display)
                    
                    # Regular response content
                    elif chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        current_section = "response"
                        
                        # If we had reasoning, show both sections
                        if reasoning_content:
                            combined_display = Text()
                            combined_display.append("🤔 AI was thinking:\n", style="bold yellow")
                            combined_display.append(reasoning_content + "\n\n", style="dim italic")
                            combined_display.append("💬 Response:\n", style="bold green")
                            combined_display.append(full_response)
                            live.update(Panel(
                                combined_display,
                                title="AI Response with Reasoning",
                                border_style="blue"
                            ))
                        else:
                            # Show just the response as before
                            live.update(Markdown(full_response))
            
            # Add AI response to conversation (only the actual response, not reasoning)
            self.conversation.append({"role": "assistant", "content": full_response})
            
            # Return response and whether reasoning was present
            return full_response, bool(reasoning_content)
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Response interrupted by user[/yellow]")
            # Remove the last user message since we didn't get a complete response
            if self.conversation and self.conversation[-1]["role"] == "user":
                self.conversation.pop()
            return "", False
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
            # Remove the last user message on error
            if self.conversation and self.conversation[-1]["role"] == "user":
                self.conversation.pop()
            return "", False

    def run(self):
        """Main chat loop"""
        self.display_welcome()
        
        try:
            while True:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]", default="").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    command = user_input.lower()
                    
                    if command == '/quit' or command == '/exit':
                        if Confirm.ask("Are you sure you want to quit?"):
                            break
                    elif command == '/help':
                        self.display_help()
                    elif command == '/model':
                        self.change_model()
                    elif command == '/clear':
                        self.clear_conversation()
                    else:
                        self.console.print(f"[red]Unknown command: {user_input}[/red]")
                        self.console.print("Type /help for available commands")
                    continue
                
                # Get AI response
                self.console.print(f"\n[bold green]AI ({self.current_model})[/bold green]:")
                response, had_reasoning = self.get_ai_response(user_input)
                
                # For models without reasoning, add spacing after streaming
                # For models with reasoning, everything is already displayed nicely
                if response and not had_reasoning:
                    self.console.print()  # Add a blank line for spacing
                
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Goodbye! 👋[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]Unexpected error: {str(e)}[/red]")

def main():
    """Entry point for the application"""
    chat = TermChat()
    chat.run()

if __name__ == "__main__":
    main() 