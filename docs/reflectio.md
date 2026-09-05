# Reflection

## What was the hardest part?

The hardest part was integrating the complete end-to-end flow between ServiceNow, FastAPI, Gemini, and the ServiceNow REST API.

Each part worked independently, but connecting them introduced several practical issues. One example was the ServiceNow write-back for the `respond` decision. The PATCH request reached ServiceNow, but the incident could not be resolved because the PDI required a valid Resolution code. The API returned a Data Policy error, which helped identify that the configured `close_code` value was not accepted by the instance. After checking the available Resolution code values in the PDI, I updated the service to use `Solution provided`.

Another challenge was making the Gemini decision behavior reliable. The vague email test initially returned `respond` instead of `ask`, so I refined the prompt to distinguish between a clear knowledge-base match and an incident that is too vague to confidently apply a solution. I also added validation for Gemini's JSON output and retry handling for temporary API failures.

## What would I improve with more time?

With more time, I would improve reliability and production readiness.

The current duplicate guard is stored in memory, which is acceptable for this task but resets whenever the application restarts. I would replace it with persistent storage such as a database or Redis.

I would also move background processing to a durable job queue so incidents are not lost if the application stops during Gemini processing or ServiceNow write-back.

Finally, I would add more automated tests, structured logging, monitoring, and stronger retry/error handling for external API failures. This would make the system easier to operate, debug, and scale beyond a prototype.