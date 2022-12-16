---
title: Application & Version
sidebar_label: Application & Version
sidebar_position: 4.1
---

# Application & Version

On LinguFlow, you can build your own LLM applications, each supporting multiple versions.

## Application

Create an application and assign it a meaningful name that reflects its business purpose. Each application should correspond to a specific business function, addressing a particular business challenge.

Applications can also [invoke each other](builder/blocks#invoke-category), enabling a modular approach to problem-solving.

### Optional: Enabling Tracing

When creating an application in LinguFlow, you have the option to enable [tracing](../run/tracing) by providing specific `LANGFUSE_SECRET_KEY` and `LANGFUSE_PUBLIC_KEY` f