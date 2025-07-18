from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)


load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
        model="gemini-2.0-flash-exp",
        voice="Puck",
        temperature=0.8,
        instructions="You are a helpful assistant",)
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))



"""
Process to set up and use this project:

1. **Install Python and Create Virtual Environment**
   - Open terminal in the project directory.
   - Run:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```
       source venv/bin/activate
       ```

2. **Install Dependencies**
   - Run:
     ```
     pip install -r requirements.txt
     ```

3. **Configure Environment**
   - Create a `.env` file with required environment variables (API keys, credentials).

4. **Download Required Files**
   - Run:
     ```
     python agent.py download-files
     ```
   - This will fetch any necessary files for the project.

5. **Run the Agent in Console Mode**
   - Start the assistant:
     ```
     python agent.py console
     ```

6. **Usage**
   - The agent will connect to the specified room, greet the user, and offer assistance.
   - Customize the assistant by modifying the `Assistant` class or session parameters.

7. **Troubleshooting**
   - Check error messages and logs for issues.
   - Ensure all dependencies and environment variables are correctly set.

"""