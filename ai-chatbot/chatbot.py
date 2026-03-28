from openai import OpenAI
import pickle

client = OpenAI()
# client = OpenAI(api_key="<YOUR_OPENAI_API_KEY>")

MODEL = "gpt-4o"
MEMORY_FILE_LOCATION = "files/memories.bin"
CHATS_FILE_LOCATION = "files/chats.bin"

def load_memories() -> list:
    try:
        with open(MEMORY_FILE_LOCATION, "rb") as memory_file:
            memories = pickle.load(memory_file)
            return memories
    except (FileNotFoundError, EOFError):
        print("No existing memory found. Starting fresh...")
    except Exception as e:
        print(f"Memory could not be loaded: {e}\n")
    return []

def dump_memories(memories):
    try:
        with open(MEMORY_FILE_LOCATION, "wb") as memory_file:
            pickle.dump(memories, memory_file)
    except Exception as e:
        print(f"Memory could not be stored: {e}\n")

def create_memory(memories, chat_history) -> str:
    history_for_memory = memories + chat_history
    history_for_memory.append({"role":"system", "content":"Imagine you are an AI chatbot. You want to concisely save only the relevant and NEW worthwhile information about the user for future reference. Use third person for the user and use the word 'user' in your memory to refer to them. Concisely return ONLY what memory you would store. Don't repeat the memories that are already stored. If you don't have worthwhile new information, return '_'."})
    # print(history_for_memory)
    memory = client.responses.create(
        model=MODEL,
        input=history_for_memory,
    )
    return memory.output_text

def add_memory(new_memory : str):
    memories = load_memories()
    memories.append({"role":"system", "content":f"Restored memory: {new_memory}"})
    dump_memories(memories=memories)

def print_memories():
    memories = load_memories()
    i = 1
    try:
        for memory in memories:
            print(f"{i}. {memory["content"]}")
            i += 1
    except:
        i = 1
        # print("No stored memory found.")

def clear_memory():
    memories = []
    dump_memories(memories)

def remove_memory(index:int):
    memories = load_memories()
    memories.pop(index-1)
    dump_memories(memories)

def load_all_chats() -> list:
    try:
        with open(CHATS_FILE_LOCATION, "rb") as chats_file:
            all_chats = pickle.load(chats_file)
            return all_chats
    except (FileNotFoundError, EOFError):
        print("No previous conversation found.")
        # new_conversation()
    except Exception as e:
        print(f"Previous conversations could not be loaded: {e}\n")
    return []

def dump_all_chats(all_chats):
    try:
        with open(CHATS_FILE_LOCATION, "wb") as chats_file:
            pickle.dump(all_chats, chats_file)
    except Exception as e:
        print(f"Error saving conversations: {e}\n")

def display_all_chats():
    all_chats = load_all_chats()
    i = 1
    for chat in all_chats:
        print(f"{i}. {chat[0]['name']}")
        i += 1

def save_conversation(chat_history):
    decision = client.responses.create(
        model=MODEL,
        input=chat_history + [{"role":"system","content":"Is this conversation worth saving? Return 'FALSE' ONLY if it has merely casual greetings and no potentialy productive talks. Just return 'TRUE' or 'FALSE'. No extra character."}],
    )
    # print(decision.output_text)
    if decision.output_text == 'FALSE':
        return
    conversation = []
    name = client.responses.create(
        model=MODEL,
        input=chat_history + [{"role":"system","content":"Suggest a suitable and concise name for saving this conversation. Just return the name, nothing else."}],
    )
    conversation.append({"name":name.output_text})
    conversation = conversation + chat_history
    all_chats = load_all_chats()
    try:
        with open(CHATS_FILE_LOCATION, "wb") as chats_file:
            all_chats.append(conversation)
            pickle.dump(all_chats, chats_file)
    except Exception as e:
        print(f"Error saving conversation: {e}\n")

def new_conversation(chat_history = []):
    memories = load_memories()
    while True:
        input_prompt = input("You: ")
        if input_prompt.lower() == "quit":
            new_memory_str = create_memory(memories, chat_history)
            # print(f"Memory to be saved: {new_memory_str}")
            if new_memory_str != '_':
                memories.append({"role":"system", "content":f"Restored memory: {new_memory_str}"})
                dump_memories(memories)
            save_conversation(chat_history)
            break
        # if input_prompt.lower() == "memories":
        #     print_memories()
        #     continue
        # if input_prompt.lower() == "clear memories":
        #     clear_memory()
        #     print("AI: Your memory has been cleared!")
        #     continue
        # if input_prompt.lower() == "remove memory #":
        #     clear_memory()
        #     print("AI: Your memory has been cleared!")
        #     continue
        chat_history.append({"role":"user", "content":input_prompt})
        response = client.responses.create(
            model=MODEL,
            tools=[{"type": "web_search"}],
            input=memories+chat_history,
        )
        chat_history.append({"role":"assistant", "content":response.output_text})

        print(f"AI: {response.output_text}\n")

    print("AI: See you again. Have a great day!\n")

def continue_conversation(index):
    if index == 0:
        new_conversation()
    else:
        # memories = load_memories()
        try:
            all_chats = load_all_chats()
            current_chat = all_chats[index-1]
            chat_history = current_chat.copy()
            print(f"\n{chat_history[0]['name']}\n")
            chat_history.pop(0)
            for dialogue in chat_history:
                if dialogue['role'] == 'user':
                    print(f"You: {dialogue['content']}")
                if dialogue['role'] == 'assistant':
                    print(f"AI: {dialogue['content']}\n")
            new_conversation(chat_history=chat_history)
        except Exception as e:
            # print(f"Error opening conversation: {e}")
            raise e

def delete_conversation(index):
    try:
        all_chats = load_all_chats()
        all_chats.pop(index-1)
        dump_all_chats(all_chats=all_chats)
    except Exception as e:
        # print(f"Error removing conversation: {e}")
        raise e

def delete_all_chats():
    try:
        dump_all_chats(all_chats=[])
    except Exception as e:
        print(f"Error removing conversation: {e}")

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Start new conversation")
        print("2. All Conversations")
        print("3. Manage memories")
        print("0. Quit")
        try:
            op_id = int(input("\nEnter your choice: "))
        except Exception as e:
            print(f"\nInvalid input: {e}. Please try again.")
            continue
        if op_id == 0:
            print("See you again. Have a great day!")
            break
        elif op_id == 1:
            print("\nStarting new conversation...")
            new_conversation()
        elif op_id == 2:
            history_menu()
        elif op_id == 3:
            memories_menu()
        else:
            print("\nInvalid input. Please try again.")

def history_menu():
    while True:
        print("\nAll Conversations:")
        display_all_chats()
        print("\nOptions:")
        print("*. Start new conversation")
        print("<Conversation_#>. Continue a previous conversation")
        print("d. Delete any conversation")
        print("0. Back to Main Menu")
        op_id = input("\nEnter your choice: ")
        if op_id == '0':
            print("Returning to Main Menu...")
            break
        elif op_id == '*':
            print("\nStarting new conversation...")
            new_conversation()
        elif op_id == 'd':
            delete_conversation_menu()
        elif op_id.isdigit():
            try:
                continue_conversation(int(op_id))
            except Exception as e:
                print(f"\nInvalid input: {e}. Please try again.")
        else:
            print("\nInvalid input. Please try again.")

def delete_conversation_menu():
    while True:
        print("\nPast Conversations:")
        display_all_chats()
        print("\nOptions:")
        print("<Conversation_#>. Delete this conversation")
        print("a. Delete ALL conversations")
        print("0. Back to All Conversations")
        op_id = input("\nEnter your choice: ")
        if op_id == '0':
            break
        if op_id == 'a':
            delete_all_chats()
        elif op_id.isdigit():
            try:
                delete_conversation(int(op_id))
            except Exception as e:
                print(f"\nInvalid input: {e}. Please try again.")
        else:
            print("\nInvalid input. Please try again.")

def memories_menu():
    while True:
        print("\nSaved Memories:")
        print_memories()
        print("\nOptions:")
        print("a. Add new memory")
        print("d. Delete any memory")
        print("0. Back to Main Menu")
        op_id = input("\nEnter your choice: ")
        if op_id == '0':
            print("Returning to Main Menu...")
            break
        elif op_id == 'a':
            add_memory_menu()
        elif op_id == 'd':
            delete_memory_menu()
        else:
            print("\nInvalid input. Please try again.")

def add_memory_menu():
    new_memory = input("Enter text to add as memory: ")
    add_memory(new_memory)
    print("Memory added.")

def delete_memory_menu():
    while True:
        print("\nSaved Memories:")
        print_memories()
        print("\nOptions:")
        print("<Memory_#>. Delete this memory")
        print("a. Delete ALL memories")
        print("0. Back to Saved Memories")
        op_id = input("\nEnter your choice: ")
        if op_id == '0':
            break
        if op_id == 'a':
            clear_memory()
            break
        if op_id.isdigit():
            try:
                remove_memory(int(op_id))
            except Exception as e:
                print(f"\nInvalid input: {e}. Please try again.")
        else:
            print("\nInvalid input. Please try again.")

main_menu()