## Open Queries

1. what is the upper limit for consul KV watches? (can not trigger more than ~150 watches due to open fd limitations.)
* https://discuss.hashicorp.com/t/upper-limit-for-consul-kv-watches/11803/4
2. How to know which key got updated inside keyprefix is being watched? (prefix watch doesn't return particular key change when key's value gets updated)
* https://discuss.hashicorp.com/t/how-to-know-which-key-got-updated-inside-keyprefix-is-being-watched/12066
3. higher avaialability is not possible with watches
* if watch is running on some agent & when that particular agent gets down, cluster will stop watching on those KV
* multiple watches on multiple nodes are creating multiple triggers on HTTP end point.
* https://discuss.hashicorp.com/t/is-there-a-way-to-continue-watching-key-or-key-prefix-by-other-agents-if-watching-agent-shuts-down/12175
