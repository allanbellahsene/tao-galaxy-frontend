context_content = """
# TAO Galaxy — Core Context for Research Agent

This document provides essential background to help the Research Agent understand the Bittensor ecosystem, the role of subnets, the dTAO mechanism, and TAO Galaxy's purpose.

---

## 🧠 What is Bittensor?

Bittensor is a decentralized network that incentivizes the development of useful artificial intelligence. It is often referred to as the "Bitcoin of Intelligence."

### Key Features:
- **Subnets**: Independent AI modules that run on the network and compete for rewards (TAO emissions).
- **Yuma Consensus**: A reputation-based consensus mechanism that ranks the performance of subnet participants.
- **TAO Token**: The native token of the network, used to incentivize useful computation.

Each subnet is effectively its own mini-network focused on solving a specific problem, such as language modeling, image classification, trading strategies, or validation.

---

## ⚙️ How Does Bittensor Work?

1. **Subnet Creation**: Anyone can create a subnet by burning TAO.
2. **Staking**: Delegators stake TAO on subnets they believe will perform well.
3. **Mining & Validation**: Participants (miners/validators) provide value (e.g., AI services) and are ranked via Yuma Consensus.
4. **Emission Distribution**: TAO emissions are distributed across subnets based on performance. Each subnet distributes TAO among its own miners, validators, and delegators.

---

## 🔁 Subnet Economics

- Every subnet has its own "alpha token," denominated in TAO.
- The **price of a subnet** = amount of TAO staked to it / circulating supply of its alpha token.
- The **price** determines how much emission the subnet receives. The higher the price, the larger its share of TAO emissions.

This mechanism creates **constant demand for TAO**:
- Subnets need staked TAO to receive emissions.
- Delegators buy TAO to stake to subnets they believe in.
- Teams burn TAO to create subnets.

---

## 🧬 What is dTAO?

dTAO is an updated protocol layer introduced in early 2024. It introduces:
- Permissionless subnet registration with TAO burn.
- Decentralized emission redistribution based on market-driven subnet performance.
- Improved flexibility for how subnets can define their logic and objectives.

Subnets operate more like startups or services with TAO emissions as their primary revenue.

---

## 🌌 What is TAO Galaxy?

TAO Galaxy is an independent platform that helps investors and researchers:
- **Discover** and understand Bittensor subnets.
- **Track** their performance, fundamentals, and updates.
- **Evaluate** them using structured, AI-generated research and scoring.

TAO Galaxy simplifies and organizes the otherwise scattered information landscape of Bittensor. This becomes increasingly important as the number of subnets grows rapidly.

---

## 🧩 Your Role as Research Agent

You will use this document as foundational context to:
- Understand how the ecosystem functions.
- Prioritize what matters when analyzing subnets (team, product, roadmap, incentives, emissions).
- Ensure factual alignment with how TAO and dTAO mechanics actually work.

Use this to cross-check any ambiguous or unclear claims when reviewing subnets.
"""