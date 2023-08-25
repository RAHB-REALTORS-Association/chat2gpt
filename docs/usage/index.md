---
title: "🧑‍💻 Usage"
layout: page
nav_order: 2
has_children: true
---

# 🧑‍💻 Usage

- **Dynamic Interactions:** Chat²GPT is deeply integrated with your chat environment. Invoke it directly in chat rooms by tagging `@botname`. For confidential interactions or specific queries, slide into its direct messages.

- **Interactive Sessions:** Chat²GPT recalls multiple interaction rounds for each user, creating a seamless dialogue illusion. It can refer back to earlier parts of the conversation, providing a more human-like chat experience.

- **Session Management:** Efficiency is key. Conversations are confined by a tunable setting, ideally between 5-10 turns. The bot also watches for inactive periods, resetting sessions automatically after a certain duration. Users wishing for a fresh start can use the `/reset` command to reinitialize their session.

- **Content Moderation:** Keeping our interactions safe, Chat²GPT screens both incoming messages and its own responses to make sure they're in line with content standards. If any content is flagged, a polite reminder is returned, ensuring all interactions uphold a high quality standard.

- **Image Generation:** Visualize thoughts effortlessly with the `/image <prompt>` command. Feed in your prompt, and watch as Chat²GPT, utilizing OpenAI's DALL·E 2 API, crafts a fitting image.

- **Text-to-Speech (TTS):** Utilize the power of Eleven Labs TTS API with the `/tts <voice> <prompt>` command. This command will return a voice response based on the given prompt in the specified voice. To see a list of available voices, use the `/voices` command.

- **Optimized Performance:** A fluid experience is paramount. The bot reviews message length by analyzing token count. If a message is overly verbose, a friendly error message nudges the user to keep it more concise. This ensures consistent, smooth interactions without overburdening the system.

- **Help On-Demand:** Have questions on how to use Chat²GPT? Just type in the `/help` command. The bot fetches content directly from the `docs/usage/help.md` file, ensuring users get accurate, up-to-date information.

Chat²GPT's versatility shines, making it apt for deployment across Google Cloud, FaaS (Function as a Service), and PaaS (Platform as a Service) platforms, cementing its place in all your Google Chat activities.
