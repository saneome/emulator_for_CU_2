import sys
import os
import socket
import shlex
import argparse

def get_prompt(custom_prompt=None):
    if custom_prompt:
        return custom_prompt
    username = os.getlogin()
    hostname = socket.gethostname()
    current_dir = "~"  # Фикс, пока VFS нет
    return f"{username}@{hostname}:{current_dir}$ "

def handle_command(command_line):
    try:
        parts = shlex.split(command_line)
        if not parts:
            return ""
        
        cmd = parts[0]
        args = parts[1:]
        
        if cmd == "exit":
            print("Exiting emulator.")
            sys.exit(0)
        elif cmd in ["ls", "cd"]:
            return f"{cmd} {' '.join(args)}"  # Заглушка
        else:
            return f"Command not found: {cmd}"
    except ValueError as e:
        return f"Parsing error: {e}"

def execute_script(script_path):
    try:
        with open(script_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    print(f"{get_prompt()} {line}")
                    output = handle_command(line)
                    if output:
                        print(output)
                    if "error" in output.lower():
                        print(f"Script execution stopped due to error in: {line}")
                        break
    except FileNotFoundError:
        print(f"Error: Script file {script_path} not found.")
    except Exception as e:
        print(f"Error executing script: {e}")

def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Shell Emulator (Variant 6)")
    parser.add_argument("--vfs-path", help="Path to VFS directory")
    parser.add_argument("--prompt", help="Custom prompt string")
    parser.add_argument("--script", help="Path to startup script")
    args = parser.parse_args()

    # Отладочный вывод параметров
    print("Debug: Starting emulator with parameters:")
    print(f"  VFS Path: {args.vfs_path or 'Not specified'}")
    print(f"  Custom Prompt: {args.prompt or 'Not specified'}")
    print(f"  Script Path: {args.script or 'Not specified'}")

    if args.script:
        execute_script(args.script)
    else:
        print("Shell Emulator (Variant 6, Stage 2)")
        while True:
            prompt = get_prompt(args.prompt)
            command_line = input(prompt).strip()
            output = handle_command(command_line)
            if output:
                print(output)

if __name__ == "__main__":
    main()
