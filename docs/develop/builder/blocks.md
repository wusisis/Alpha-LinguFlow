---
title: Blocks
sidebar_label: Blocks
sidebar_position: 4.3
toc_max_heading_level: 4
---


# Blocks

## General

A Block represents a node within the [Directed Acyclic Graph (DAG)](https://en.wikipedia.org/wiki/Directed_acyclic_graph), each embodying a specific processing logic. Typically, a Block comprises several components:
- **Block Info**:
    - **Block Name**: The name of the block.
    - **Block ID**: The unique identifier of the block.
    - **Copy Block ID**: A feature to copy the block's ID.
- **Conditional Port**: Accepts True or False outputs from upstream `condition` type blocks, determining whether to execute this block based on the upstream result.
- **Inport**: The information inputted into this block. Some blocks support multiple inports. Inports can handle `text`, `list`, `dict` data types.
    - **Add an Inport**: Adds an additional inport to the block. Manually added inports support connections of `any` data type.
- **Outport**: The information outputted from this block. Outports typically support `text`, `list`, `dict`, `boolean` data types.
- **Parameters**: Specific parameter details for the block, which vary from one block type to another.

## Block Categories

LinguFlow offers essential Block categories necessary for building LinguFlow applications, including:
- **Input & Output Category**: For receiving inputs and sending outputs.
- **D