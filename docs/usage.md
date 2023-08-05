---
title: "🧑‍💻 Usage"
layout: page
nav_order: 2
---

# 🧑‍💻 Usage

Your bot is all set and ready for action! It's capable of interacting in any chat room, responding when directly mentioned (@botname), or when it receives a direct message, based on the functionality you've programmed. Our bot is designed to remember several rounds of a conversation per user session, providing a coherent and continuous interaction. This means you can ask a question, receive a response, and continue the conversation by referencing the initial query or its response.

However, for performance optimization, there are a few limitations in place. First, the length of the conversation is limited by a configurable setting; we recommend setting it to 5-10 turns. Each session also tracks the time since the last received message, automatically resetting if it exceeds a specified time limit. This ensures a seamless and efficient conversation experience with the bot.

Additionally, to ensure we don't overload the system with large messages, we've implemented a mechanism to count the tokens in a message before it's sent for processing. If the message is too large, the bot will respond with an error message asking the user to try a shorter message.