import time
import keys
import hashlib

class Block:
    def __init__(self, index, previous_hash, timestamp, nonce, current_hash, transactions=[]):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.nonce = nonce
        self.current_hash = current_hash
        self.transactions = transactions

    def __repr__(self):
        transactions_repr = ''.join([str(transaction) + '\n' for transaction in self.transactions])
        return (f"Index: {self.index}\nPrevious Hash: {self.previous_hash}\nTimestamp: {self.timestamp}"
                f"\nNonce: {self.nonce}\nCurrent Hash: {self.current_hash}\nTransactions:\n{transactions_repr}")

class Transaction:
    def __init__(self, sender_public_key, receiver_public_key, amount, signature):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.signature = signature

    def __repr__(self):
        return (f"Sender: {self.sender_public_key}, Receiver: {self.receiver_public_key}, "
                f"Amount: {self.amount}, Signature: {self.signature}")

class Blockchain:
    # Contructor to initialize the blockchain
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.balance_sheet = {}
        self.create_genesis_block()

    # Create the genesis block
    def create_genesis_block(self):
        genesis_block = Block(0, "0", int(time.time()), 0, "0", [])
        self.chain.append(genesis_block)

    # Calculate the hash of a block
    def calculate_hash(self, index, previous_hash, timestamp, nonce, transactions):
        block_string = f"{index}{previous_hash}{timestamp}{nonce}{''.join(str(tx) for tx in transactions)}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    # Mint new coins
    def mint_coins(self, public_key, amount):
        self.add_transaction(0, public_key, amount)
        print(f"Minted {amount} coins for {public_key}")

    # Get the balance of a public key
    def get_balance(self, public_key):
        return self.balance_sheet.get(public_key, 0)
    
    # Print the blockchain
    def print_blockchain(self):
        for block in self.chain:
            print(block)
    
    # Methods to code in lesson

    def add_transaction(self):

        pass

    def mine_block(self):
        
        pass



# Main loop
def main():
    blockchain = Blockchain()

    while True:
        command = input("Enter 'T' for transaction, 'Mine' for mining, 'Mint' for minting, 'P' for printing blockchain, 'GB' for get balance of public key, or 'Q' to quit: ").strip().lower()

        if command == 't':
            sender_private_key = int(input("Enter private key to send from (1-3): ")) - 1
            receiver_public_key = int(input("Enter public key to send to (1-3): ")) - 1
            amount = float(input("Enter the amount to send: "))

            # Add transaction
            transaction_added = blockchain.add_transaction(keys.key_pairs[sender_private_key]["private"], keys.key_pairs[receiver_public_key]["public"], amount)
            if transaction_added:
                print("Transaction successfully added.")
            else:
                print("Failed to add transaction.")

        elif command == 'mine':
            # Mine a new block
            mined_block = blockchain.mine_block()
            if mined_block:
                print("Successfully mined a new block.")
            else:
                print("Failed to mine a new block.")

        elif command == 'mint':
            public_key = int(input("Enter public key to mint coins for (1-3): ")) - 1
            amount = float(input("Enter the amount to mint: "))

            # Mint new coins
            blockchain.mint_coins(keys.key_pairs[public_key]["public"], amount)

        elif command == 'p':
            # Print the blockchain
            blockchain.print_blockchain()
        
        elif command == 'gb':
            public_key = int(input("Enter public key to get balance for (1-3): ")) - 1
            balance = blockchain.get_balance(keys.key_pairs[public_key]["public"])
            print(f"Balance for {public_key+1}: {balance}")

        elif command == 'q':
            print("Quitting...")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()