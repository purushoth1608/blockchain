import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def __repr__(self):
        return f"Block(index={self.index}, previous_hash={self.previous_hash}, timestamp={self.timestamp}, data={self.data}, hash={self.hash})"

def calculate_hash(index, previous_hash, timestamp, data):
    value = f"{index}{previous_hash}{timestamp}{data}"
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = create_new_block(previous_block, data)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def display_chain(self):
        for block in self.chain:
            print(block)

class BlockchainManager:
    def __init__(self):
        self.blockchains = {}

    def create_blockchain(self, purpose):
        self.blockchains[purpose] = Blockchain()

    def add_transaction(self, purpose, data):
        if purpose in self.blockchains:
            self.blockchains[purpose].add_block(data)
        else:
            print(f"Blockchain for {purpose} does not exist. Please create it first.")

    def display_blockchains(self):
        for purpose, blockchain in self.blockchains.items():
            print(f"Blockchain for {purpose}:")
            blockchain.display_chain()
            print("\n")

    def is_all_chains_valid(self):
        for purpose, blockchain in self.blockchains.items():
            if not blockchain.is_chain_valid():
                print(f"Blockchain for {purpose} is invalid.")
                return False
        print("All blockchains are valid.")
        return True

def main():
    manager = BlockchainManager()

    while True:
        print("\n1. Create a new blockchain for a purpose")
        print("2. Add a transaction to a blockchain")
        print("3. Display all blockchains")
        print("4. Validate all blockchains")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            purpose = input("Enter the purpose of the blockchain (e.g., household, vehicle): ")
            manager.create_blockchain(purpose)
            print(f"Blockchain for {purpose} created.")

        elif choice == '2':
            purpose = input("Enter the purpose of the blockchain to add a transaction: ")
            data = input("Enter the transaction data: ")
            manager.add_transaction(purpose, data)
            print(f"Transaction added to {purpose} blockchain.")

        elif choice == '3':
            manager.display_blockchains()

        elif choice == '4':
            manager.is_all_chains_valid()

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
