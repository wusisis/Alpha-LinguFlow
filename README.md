
# Alpha-LinguFlow

🎉🚀🌍 **Alpha-LinguFlow** is now live for the world to see! `Hello, World!`

## What is Alpha-LinguFlow

Alpha-LinguFlow is a simplified yet efficient low-code tool crafted explicitly for LLM application development. It streamlines the building, debugging, and deployment process for developers with its [DAG (Directed Acyclic Graph)](https://en.wikipedia.org/wiki/Directed_acyclic_graph)-based message flow.

### The Need for Alpha-LinguFlow?

Applying LLM to real-world scenarios often leads to certain challenges, which can be managed using Alpha-LinguFlow. The major issues include:

- Difficulty in improving accuracy further.
- The inability to restrict the conversation to only business-relevant topics.
- Complexities in handling intricate business processes.

### Features of Alpha-LinguFlow

Alpha-LinguFlow is rich with features that facilitate the construction of applications with LLM:

- **Technical Features**: Construction based on a DAG of information flow, multi-interactions with an LLM, and overcoming the limitations of single interactions.
- **Business Advantages**: Clear understanding of problem-solving using LLM, suitable for complex logic and requiring higher accuracy.

## Get Started

### Localhost (docker)

You can run Alpha-LinguFlow on your local machine using [docker compose](https://docs.docker.com/compose/install/). This setup is perfect for testing, developing Alpha-LinguFlow applications, and diagnosing integration issues.

```sh
# Clone the Alpha-LinguFlow repository
git clone git@github.com:wusisis/Alpha-LinguFlow.git

# Navigate into the Alpha-LinguFlow directory
cd Alpha-LinguFlow

# Start the UI and API server
docker-compose -f docker-compose.dev.yaml up
```

### Self-Hosting (docker)

Alpha-LinguFlow Server, which includes the API and Web UI, is open-source and can be self-hosted using Docker.

### API Call

1. Click the Connect App button within the App.
2. Follow the instructions to use the POST API to call the asynchronous interface, obtaining the interaction id for this interaction.
3. Use the GET API to query the previously obtained interaction id, retrieving the final response from the Alpha-LinguFlow application.

## License

This repository is MIT licensed. See [LICENSE](LICENSE) for more details.