import time
import random
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from db import save_conversation, save_feedback, get_db_connection

# Set the timezone to CET (Europe/Berlin)
tz = ZoneInfo("Asia/Jakarta")

# List of sample questions and answers
SAMPLE_QUESTIONS = [
    "What is a blockchain?",
    "What is blockchain software?",
    "What is a blockchain database?",
    "What is a blockchain system?",
    "How does a blockchain work?"
]

SAMPLE_ANSWERS = [
    "A blockchain is a distributed, cryptographically-secure database structure that allows network participants to establish a trusted and immutable record of transactional data without the need for intermediaries. A blockchain can execute a variety of functions beyond transaction settlement, such as smart contracts. Smart contracts are digital agreements that are embedded in code and that can have limitless formats and conditions. Blockchains have proven themselves as superior solutions for securely coordinating data, but they are capable of much more, including tokenization, incentive design, attack-resistance, and reducing counterparty risk. The very first blockchain was the Bitcoin blockchain, which itself was a culmination of over a century of advancements in cryptography and database technology.",
    "Blockchain software is like any other software. The first of its kind was Bitcoin, which was released as open source software, making it available to anyone to use or change. There are a wide variety of efforts across the blockchain ecosystem to improve upon Bitcoin’s original software. Ethereum has its own open source blockchain software. Some blockchain software is proprietary and not available to the public.",
    "Historically, databases have incorporated a centralized client-server architecture, in which a sole authority controls the central server. This design means that data security, alteration, and deletion rests with a single point of failure. The decentralized architecture of blockchain databases emerged as a solution for many of the weaknesses of centralized database architecture. A blockchain network consists of a large number of distributed nodes––voluntary participants who must reach consensus and maintain a single transactional record together.",
    "A blockchain system refers to all the aspects and features that go into a particular blockchain, everything from the consensus algorithm to the state machine to cryptographic functions. As Andreas Antonopoulus and Gavin Wood note in Mastering Ethereum, there are “a huge variety of blockchains with different properties”––qualifiers “help us understand the characteristics of the blockchain in question, such as open, public, decentralized, neutral, and censorship-resistant.”",
    "When a digital transaction occurs in a blockchain network, it is grouped together in a cryptographically-secure “block” with other transactions that have occurred in the same time frame. The block is then broadcast to the network. A blockchain network is comprised of nodes or participants who validate and relay transaction information. The block of transactions is verified by participants called miners, who use computing power to solve a cryptographic puzzle and validate the block of transactions. The first miner to solve and validate the block is rewarded. Each verified block is connected to the previously verified block, creating a chain of blocks. One important cryptographic underpinning of blockchains is the hash function. Hashing assigns a fixed value to a string that is inputted into the system. Blockchain hashing power results in a deterministic, quickly-computable, and preimage-resistant system. Explore our knowledge base to learn more about how a blockchain works."
    ]

MODELS = ["ollama/phi3", "openai/gpt-3.5-turbo", "openai/gpt-4o", "openai/gpt-4o-mini"]
RELEVANCE = ["RELEVANT", "PARTLY_RELEVANT", "NON_RELEVANT"]


def generate_synthetic_data(start_time, end_time):
    current_time = start_time
    conversation_count = 0
    print(f"Starting historical data generation from {start_time} to {end_time}")
    while current_time < end_time:
        conversation_id = str(uuid.uuid4())
        question = random.choice(SAMPLE_QUESTIONS)
        answer = random.choice(SAMPLE_ANSWERS)
        model = random.choice(MODELS)
        relevance = random.choice(RELEVANCE)

        openai_cost = 0

        if model.startswith("openai/"):
            openai_cost = random.uniform(0.001, 0.1)

        answer_data = {
            "answer": answer,
            "response_time": random.uniform(0.5, 5.0),
            "relevance": relevance,
            "relevance_explanation": f"This answer is {relevance.lower()} to the question.",
            "model_used": model,
            "prompt_tokens": random.randint(50, 200),
            "completion_tokens": random.randint(50, 300),
            "total_tokens": random.randint(100, 500),
            "eval_prompt_tokens": random.randint(50, 150),
            "eval_completion_tokens": random.randint(20, 100),
            "eval_total_tokens": random.randint(70, 250),
            "openai_cost": openai_cost,
        }

        save_conversation(conversation_id, question, answer_data, current_time)
        print(
            f"Saved conversation: ID={conversation_id}, Time={current_time}, Model={model}"
        )

        if random.random() < 0.7:
            feedback = 1 if random.random() < 0.8 else -1
            save_feedback(conversation_id, feedback, current_time)
            print(
                f"Saved feedback for conversation {conversation_id}: {'Positive' if feedback > 0 else 'Negative'}"
            )

        current_time += timedelta(minutes=random.randint(1, 15))
        conversation_count += 1
        if conversation_count % 10 == 0:
            print(f"Generated {conversation_count} conversations so far...")

    print(
        f"Historical data generation complete. Total conversations: {conversation_count}"
    )


def generate_live_data():
    conversation_count = 0
    print("Starting live data generation...")
    while True:
        current_time = datetime.now(tz)
        # current_time = None
        conversation_id = str(uuid.uuid4())
        question = random.choice(SAMPLE_QUESTIONS)
        answer = random.choice(SAMPLE_ANSWERS)
        model = random.choice(MODELS)
        relevance = random.choice(RELEVANCE)

        openai_cost = 0

        if model.startswith("openai/"):
            openai_cost = random.uniform(0.001, 0.1)

        answer_data = {
            "answer": answer,
            "response_time": random.uniform(0.5, 5.0),
            "relevance": relevance,
            "relevance_explanation": f"This answer is {relevance.lower()} to the question.",
            "model_used": model,
            "prompt_tokens": random.randint(50, 200),
            "completion_tokens": random.randint(50, 300),
            "total_tokens": random.randint(100, 500),
            "eval_prompt_tokens": random.randint(50, 150),
            "eval_completion_tokens": random.randint(20, 100),
            "eval_total_tokens": random.randint(70, 250),
            "openai_cost": openai_cost,
        }

        save_conversation(conversation_id, question, answer_data, current_time)
        print(
            f"Saved live conversation: ID={conversation_id}, Time={current_time}, Model={model}"
        )

        if random.random() < 0.7:
            feedback = 1 if random.random() < 0.8 else -1
            save_feedback(conversation_id, feedback, current_time)
            print(
                f"Saved feedback for live conversation {conversation_id}: {'Positive' if feedback > 0 else 'Negative'}"
            )

        conversation_count += 1
        if conversation_count % 10 == 0:
            print(f"Generated {conversation_count} live conversations so far...")

        time.sleep(1)


if __name__ == "__main__":
    print(f"Script started at {datetime.now(tz)}")
    end_time = datetime.now(tz)
    start_time = end_time - timedelta(hours=6)
    print(f"Generating historical data from {start_time} to {end_time}")
    generate_synthetic_data(start_time, end_time)
    print("Historical data generation complete.")

    print("Starting live data generation... Press Ctrl+C to stop.")
    try:
        generate_live_data()
    except KeyboardInterrupt:
        print(f"Live data generation stopped at {datetime.now(tz)}.")
    finally:
        print(f"Script ended at {datetime.now(tz)}")
