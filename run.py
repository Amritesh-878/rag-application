import subprocess
import sys

def main():
    print("RAG Document Q&A System Launcher")
    print("=" * 40)
    print("1. Web UI (Modern Frontend)")
    print("2. Process Documents from /docs folder")
    print("3. Exit")

    while True:
        choice = input("\nSelect option (1-3): ").strip()

        if choice == "1":
            print("Starting modern web UI...")
            subprocess.run([sys.executable, "ui/web_server.py"])

        elif choice == "2":
            print("Processing documents from docs folder...")
            subprocess.run([sys.executable, "utils/ingest.py"])

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
