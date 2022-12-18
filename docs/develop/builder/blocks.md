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
- **Data Process Category**: For manipulating and processing data.
- **Condition Category**: For making decisions based on certain conditions.
- **LLM Category**: For integrating Large Language Model functionalities.
- **Invoke Category**: For calling other blocks or applications within LinguFlow.
- **Tools Category**: For utilizing third-party tools or services.

### Input & Output Category

#### Text_Input

- **Description**: Defines the input type for a LinguFlow App. It allows sending information of `text` type to the LinguFlow application during an API call.
- **Outport**: `text`
- **Example**:

```markdown
- Outport: "Who are you?"
```

#### List_Input

- **Description**: Defines the input type for a LinguFlow App. It supports sending information of `list` type to the LinguFlow application during an API call.
- **Outport**: `list`
- **Example**:

```markdown
- Outport: ["hi", "Hello, can I help you?", "Who are you?"]
```

#### Dict_Input

- **Description**: Defines the input type for a LinguFlow App. It facilitates sending information of `dict` type to the LinguFlow application during an API call.
- **Outport**: `dict`
- **Example**:

```markdown
- Outport: {"key_1": "value_1", "key_2": "value_2"}
```

#### Text_Output

- **Description**: Specifies the output type for a LinguFlow App. After the LinguFlow application has finished running, it outputs a result of `text` type.
- **Inport**: `text`
- **Example**:

```markdown
- Inport: "I'm LinguFlow."
```

### Data Processing Category

#### Dict_KeySelect_to_Text

- **Description**: Selects a specific `key`'s `value` from a `dict`.
- **Inport**: `dict`
- **Outport**: `text`
- **Parameters**:
    - **Key**: Specifies a particular `key`.
- **Example**:

```markdown
- Inport: {"key_1": "value_1", "key_2": "value_2"}
- Parameters: key="key_1"
- Outport: "value_1"
```

#### List_Join_to_Text

- **Description**: Merges a `list` into a single `text` string. The `list` typically contains multiple `text` elements.
- **Inport**: Supports multiple inports, each corresponding to a `list`.
- **Outport**: Merged `text`
- **Parameters**:
    - **Template**: Describes how to render each list element.
    - **Delimiter**: Describes how to concatenate the rendered elements.
- **Example**:

```markdown
- Inport: ["text 1", "text 2", "text 3"]
- Parameters:
    - template="