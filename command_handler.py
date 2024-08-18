class CommandHandler:
    def __init__(self, config, history):
        self.config = config
        self.history = history
        self.commands = {
            "help": {
                "func": self.show_help,
                "desc": "Shows all available commands and their descriptions."
            },
            "history": {
                "func": self.show_history,
                "desc": "Displays the conversation history."
            },
            "clear": {
                "func": self.clear_history,
                "desc": "Clears the conversation history."
            },
            "system": {
                "func": self.show_system_prompt,
                "desc": "Shows the current system prompt."
            },
            "system prompt": {
                "func": self.update_system_prompt,
                "desc": "Updates the system prompt, clears history, and restarts."
            },
            "model": {
                "func": self.show_model,
                "desc": "Displays the current Claude model."
            },
            "model change": {
                "func": self.change_model,
                "desc": "Changes the Claude model."
            },
        }

    def handle_command(self, command):
        command = command.strip().lower()
        matched_cmd = None
        matched_length = 0

        for cmd in self.commands:
            if command.startswith(cmd) and len(cmd) > matched_length:
                matched_cmd = cmd
                matched_length = len(cmd)

        if matched_cmd:
            try:
                return self.commands[matched_cmd]["func"](command[matched_length:].strip())
            except Exception as e:
                print(f"Error executing command: {e}")
                return True
        return False

    def show_help(self, _):
        print("\nAvailable commands:")
        for cmd, info in self.commands.items():
            print(f"{cmd}: {info['desc']}")
        return True

    def show_history(self, _):
        print("\nConversation History:")
        for entry in self.history.messages:
            print(f"{entry['role'].capitalize()}: {entry['content']}")
        return True

    def clear_history(self, _):
        self.history.clear()
        print("Conversation history cleared.")
        return True

    def show_system_prompt(self, _):
        print(f"Current system prompt: {self.config.system_prompt}")
        return True

    def update_system_prompt(self, new_prompt):
        if not new_prompt:
            print("Error: New system prompt cannot be empty.")
            return True
        try:
            self.config.system_prompt = new_prompt
            self.history.clear()
            self.config.save_config()
            print("System prompt updated. Conversation history cleared.")
            print(f"New system prompt: {self.config.system_prompt}")
        except Exception as e:
            print(f"Error updating system prompt: {e}")
        return True

    def show_model(self, _):
        print(f"Current model: {self.config.model}")
        return True

    def change_model(self, new_model):
        if not new_model:
            print("Error: New model name cannot be empty.")
            return True
        try:
            self.config.model = new_model
            self.config.save_config()
            print(f"Model changed to: {self.config.model}")
        except Exception as e:
            print(f"Error changing model: {e}")
        return True