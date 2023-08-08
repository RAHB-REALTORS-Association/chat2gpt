---
title: "🧑‍💻 Usage"
layout: page
nav_order: 2
---

# 🧑‍💻 Usage

- **Dynamic Interactions:** Chat²GPT is attentive to its surroundings. You can invoke it in chat rooms by directly mentioning it using `@botname`. Alternatively, for more private interactions or queries, you can send a direct message to the bot.

- **Interactive Sessions:** This bot remembers multiple rounds of a conversation per user, creating an illusion of continuous dialogue. It can even reference past questions or answers, mimicking a natural conversation flow.

- **Session Management:** To maintain efficient performance, each conversation is limited by a configurable setting, recommended at 5-10 turns. Moreover, the bot keeps an eye on the time since the last message, auto-resetting the session if a set time limit is surpassed. And if needed, users can manually reset their own session anytime with the `/reset` command.

- **Image Generation:** Want to visualize an idea? Use the `/image <prompt>` command. Based on the given prompt, which can range from a word to a paragraph, the bot leverages OpenAI's DALL·E 2 API to generate a relevant image.

- **Optimized Performance:** We prioritize a smooth experience. Before processing any message, the bot checks its size by counting its tokens. If found too lengthy, an error message suggests the user to condense their message. This ensures uninterrupted bot interactions without straining the system.

Remember, Chat²GPT is flexible, suitable for deployment on Google Cloud, FaaS (Function as a Service), or PaaS (Platform as a Service) environments, ensuring it's a perfect fit for all your Google Chat endeavors.