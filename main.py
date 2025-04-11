#!/usr/bin/env python3
from chatbot import Chatbot
import sys

def main():
    bot = Chatbot()
    print("Minimalist CLI Chatbot\n=====================\nCommands:\n- Remember [text] - Store information\n- Forget [text] - Remove specific information\n- Forget - Remove previous answer\n- Threshold [0-1] - Set similarity threshold\n- Exit - Quit the program")
    
    while True:
        try:
            inp = input("\nYou: ").strip()
            if not inp: continue
            
            # Handle basic commands
            cmd = inp.lower().split(" ", 1)
            cmd_name = cmd[0]
            arg = cmd[1] if len(cmd) > 1 else ""
            
            if cmd_name in ('exit', 'quit'): 
                print("\nGoodbye."); sys.exit(0)
            elif cmd_name == 'remember' and arg: 
                bot.remember(arg); print("System: Remembered.")
            elif cmd_name == 'forget':
                if bot.forget(arg if arg else None): print("System: Forgot.")
                else: print("System: Nothing to forget.")
            elif cmd_name == 'threshold' and arg:
                try: 
                    val = float(arg)
                    bot.set_similarity_threshold(val)
                    print(f"System: Threshold: {val}")
                except: print("System: Invalid threshold")
            else:
                # Treat as a query
                print(f"System: {bot.respond(inp).message}")
                
        except KeyboardInterrupt:
            print("\nGoodbye."); sys.exit(0)
        except:
            print("System: Error occurred.")

if __name__ == "__main__": main()