#!/usr/bin/env python3
from knowledge_base import KnowledgeBase
import sys

def main():
    kb = KnowledgeBase()
    print("""
Vector Knowledge Base
=====================
Commands:
- Remember [text] - Store information
- Forget [text]   - Remove specific information
- Forget          - Remove previous information
- Threshold [0-1] - Set similarity threshold
- Exit            - Quit the program
""")
    
    while True:
        try:
            inp = input("Query: ").strip()
            if not inp: 
                continue
            
            # Handle basic commands
            cmd = inp.lower().split(" ", 1)
            cmd_name = cmd[0]
            arg = cmd[1] if len(cmd) > 1 else ""
            
            if cmd_name in ('exit', 'quit'): 
                print("\nGoodbye.")
                sys.exit(0)
            elif cmd_name == 'remember' and arg: 
                kb.remember(arg)
                print("System: Remembered.")
            elif cmd_name == 'forget':
                if kb.forget(arg if arg else None):
                    print("System: Forgot.")
                else:
                    print("System: Nothing to forget.")
            elif cmd_name == 'threshold' and arg:
                try: 
                    val = float(arg)
                    kb.set_similarity_threshold(val)
                    print(f"System: Threshold set to {val:.3f}")
                except:
                    print("System: Invalid threshold")
            else:
                # Treat as a query
                response = kb.respond(inp).message
                print(f"\nSystem: {response}\n")
                
        except KeyboardInterrupt:
            print("\nGoodbye.")
            sys.exit(0)
        except Exception as e:
            print(f"System: Error occurred. {str(e)}")

if __name__ == "__main__": 
    main()