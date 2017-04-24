== Problem Statement ==

Implement a simple chat client which transmits user message to a multicast address and receives messages sent from other clients on other machines sent to the same multicast address.

When implementing the chat client, as a minimum, you will need to implement the transmitter code and the listener code as separate threads so that live messages from other sources may be received and displayed while the user is also typing a new message to be sent.

The basic components of the code for communicating in Java are given in the lecture notes on the topic of multicast communication. Java threads were used in CS240 in second year, we will also look at them again after the midterm break. Put the two together.

== Notes ==

This problem requires threads (or some other form of async).