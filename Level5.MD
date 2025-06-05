### Level 5: Agentic Systems

* This is where agents go from being tools to infrastructure. Agentic Systems are full APIs — systems that take in a user request, kick off an async workflow, and stream results back as they become available.

# Sounds clean in theory. In practice, it’s hard. Really hard.

* You need to persist state when the request comes in, spin up a background job, track progress, and stream output as it’s generated. Websockets can help, but they’re tricky to scale and maintain. Most teams underestimate the backend complexity here.

* This is what it takes to turn agents into real products. At this level, you’re not building a feature — you’re building a system.
