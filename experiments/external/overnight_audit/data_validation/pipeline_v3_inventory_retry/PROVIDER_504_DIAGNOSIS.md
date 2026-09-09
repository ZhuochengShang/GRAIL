# Confirmed 504 failures and remaining uncertainty

The saved provider response is `ServerError: 504 DEADLINE_EXCEEDED` with the message
“Deadline expired before operation could complete.” These are actual recorded
provider errors, not a guess based on an idle process. Selected invocation totals
are about 599–601 seconds. They failed before usable code/native execution.

[Bound API examples and timings](PROVIDER_504_EVIDENCE.json) include tslearn A2
compute/jacobian_product and Thumbnailator A1 clear/createOutputStream/region.
Their delivered document lengths range from 87 to 12,000 characters. These are
only document lengths, not total prompt sizes; they do not establish context
length as the cause.

[Google's error guide](https://ai.google.dev/gemini-api/docs/generate-content/api-errors)
identifies 504 as failure to finish within a deadline and documents long context
as a possible cause. It distinguishes 429 resource exhaustion from 504. Our
responses do not establish a rate-limit cause.

The installed langchain-google-genai 4.2.1 recognizes the configured timeout and
retry aliases and passes a 300-second timeout and two SDK attempts to google-genai
1.67.0. The outer invocation deadline is 630 seconds. SDK attempts may contribute
to total latency, but per-attempt timing is not captured, so 600 seconds cannot
be attributed definitively to one server call or two SDK attempts.

Underlying provider processing/queue delay, prompt complexity and transport
behavior remain unresolved. Scheduling changes remove unnecessary waits and
bound local concurrency; they do not constitute proof of fixing the provider's
504 cause. No active measured prompt, model, generation setting or timeout was
changed for this diagnosis, and no extra diagnostic model call was made.
