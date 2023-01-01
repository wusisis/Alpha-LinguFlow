---
title: Overview
sidebar_label: Overview
sidebar_position: 1
---

# Overview

Welcome to the LinguFlow User Guide! LinguFlow is a cutting-edge LLM (Large Language Model) application builder that facilitates the creation of LLM applications through a visual, [DAG(Directed Acyclic Graph)](https://en.wikipedia.org/wiki/Directed_acyclic_graph)-based interface.

This guide is designed to familiarize you with the capabilities of LinguFlow and navigate you through its wide array of features and functionalities.

After reading, feel free to dive into the [QuickStart](quickstart) section to get hands-on experience with LinguFlow.

## Key Features

### Development

- **LinguFlow UI**: After deployment ([locally](deployment/local) or [self-hosted](deployment/self_host)), you can manage your LLM applications within an organized framework of [Apps and Versions](develop/application_and_version).
    - **App**: Each LLM application is recognized as an `application`, which can be executed directly using its `application_id` during production.
    - **Version**: Each App can house multiple versions, with one specified as the `published version`. Each version can be independently edited.
- **Builder**: Opening a version reveals the [Builder](develop/builder/summary), w